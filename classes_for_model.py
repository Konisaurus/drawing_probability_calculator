import copy


class Deck:
    # class for storing deck info (optimized for Yu-Gi-Oh!)
    def __init__(self, deck_name, main_deck):
        # dictionaries of all deck parts
        self.name = deck_name
        self.main = main_deck

    # getter functions
    def get_name(self):
        return self.name
    
    def get_main(self):
        return self.main


class Card_Pool_Manager:
    # class for different cards that can be treated as one unit (each card is the "same").
    def __init__ (self, deck_manager, card_names = [], min_slot_size = 0, boolean=False):

        # card info for pool
        self.card_names = card_names                                            # store all card names that are in the pool.
        self.card_count = self.addup_cards(deck_manager.get_main_dict())        # number of card copies in the pool.

        # info for calculations
        self.only_equal = boolean                                               # True (only == 1 is a success), False (everything >= 1 is a success)
        self.min_slot_size = min_slot_size                                      # how many cards of this pool should be at least in a successfull sample.
        self.size_list = self.set_size_list(deck_manager.get_sample_size())     # list of all possible sizes of a slot that is occupied by cards of this pool (also depends on sample size).


    def addup_cards(self, main_dict):
        # calculate the number of card copies in the pool.
        # needs the main_dict of the deck, so it can check how many copies of each card are in the deck.
        # returns the number of cards in this pool.
        if self.card_names == []:
            return 0
        count = 0
        for key in self.card_names:
            count += main_dict[key]
        return count

    def set_size_list(self, sample_size):
        # create list of all possible sizes of a slot that is occupied by cards of this pool.
        # The smallest size is determined by self.min_slot_size, the maximum by min(self.card_count, sample_size).
        self.size_list = []
        if self.only_equal == True:
            self.size_list = [self.min_slot_size]
            
        else:
            self.size_list =  list(range(self.min_slot_size, min(self.card_count, sample_size) + 1))

    def add_card(self, card_name, main_dict, sample_size):
        # adds a card to the pool
        self.card_names.append(card_name)
        self.card_count = self.addup_cards(main_dict)
        self.set_size_list(sample_size)

    def remove_card(self, card_name, main_dict, sample_size):
        # removes card from the pool
        self.card_names.remove(card_name)
        self.card_count = self.addup_cards(main_dict)
        self.set_size_list(sample_size)

    def set_slot_size(self, min_slot_size, sample_size):
        # changes the value of self.min_slot_size
        self.min_slot_size = min_slot_size
        self.set_size_list(sample_size)

    def set_only_equal(self, boolean, sample_size):
        # changes the value of self.only_equal
        self.only_equal = boolean
        self.set_size_list(sample_size)

    # getter functions
    def get_card_names(self):
        return self.card_names
    
    def get_only_equal(self):
        return self.only_equal
    
    def get_card_count(self):
        return self.card_count
    
    def get_size_list(self):
        return self.size_list


class Deck_Manager:
    # class for managing different card pools that are in one deck.
    def __init__(self, model, deck, sample_size = 0, defined_card_pools = []):

        # reference to the model
        self.model = model

        # these attributes should always stay the same for one particular deck.
        self.deck_name = deck.get_name()                                # entire deck info (class Deck)
        self.main_dict = deck.get_main()                                # main deck as a dictionary, main_dict = {"card1": int(number of card1 in deck), ... , "cardX": int(number of cardX in deck)}
        self.deck_size = self.calculate_deck_size()                     # number of card copies in deck

        # can be changed
        self.sample_size = sample_size                                  # number of cards that are drawn in a sample hand
        self.defined_card_pools = defined_card_pools                    # list of different card pools
        self.unassigned_cards = self.check_unassigned_cards()           # dict of cards that are in no card pool
        self.unassigned_card_count = self.calculate_unassigned_cards()  # number of card copies that are not assigned to any pool
    
    def calculate_deck_size(self):
        # calculate the number of card copies in deck and return it.
        deck_size = 0
        for key in self.main_dict:
            deck_size += self.main_dict[key]
        return deck_size

    def check_unassigned_cards(self):
        # creates/updates the list of unassigned card names
        unassigned_cards = copy.deepcopy(self.main_dict)
        if self.defined_card_pools != []:
            for pool in self.defined_card_pools:
                if pool.get_card_names() != []:
                    for card in pool.get_card_names():
                        unassigned_cards.pop(card)
        return unassigned_cards
    
    def calculate_unassigned_cards(self):
        # calculate number of card copies that are not assigned to any pool and return it.
        unassigned_card_count = self.deck_size
        if self.defined_card_pools != []:
            for pool in self.defined_card_pools:
                unassigned_card_count -= pool.get_card_count()
        return unassigned_card_count

    def add_card_pool(self):
        # creates an "empty" card pool object
        self.defined_card_pools.append(copy.deepcopy(Card_Pool_Manager(self)))

        self.model.notify("add pool")

    def add_card_to_pool(self, index, card_name):
        # adds a card_name to a card pool
        self.defined_card_pools[index].add_card(card_name, self.main_dict, self.sample_size)

        # update everything that keeps track of unassigened cards
        self.unassigned_card_count = self.calculate_unassigned_cards() 
        self.unassigned_cards = self.check_unassigned_cards()   

        self.model.notify("add card to pool", index, card_name)

    def remove_card_from_pool(self, index, card_name):
        # removes a card_name from a card pool
        self.defined_card_pools[index].remove_card(card_name, self.main_dict, self.sample_size)

        # update everything that keeps track of unassigened cards
        self.unassigned_card_count = self.calculate_unassigned_cards()
        self.unassigned_cards = self.check_unassigned_cards()

        self.model.notify("removed card from pool", index, card_name)

    def set_sample_size(self, sample_size):
        # set self.sample_size
        self.sample_size = sample_size

        # update everything is dependend on the sample size
        if self.defined_card_pools != []:
            for pool in self.defined_card_pools:
                pool.set_size_list(self.sample_size)

    def set_pool_slot_size(self, index, min_slot_size):
        # set the slot size of one defined pool
        self.defined_card_pools[index].set_slot_size(min_slot_size, self.sample_size)

    def set_pool_only_equal(self, index, boolean):
        # set the only_equal variabl
        self.defined_card_pools[index].set_only_equal(boolean, self.sample_size)

        self.model.notify("changed only equal", index)

    # getter functions
    def get_model(self):
        return self.model
    
    def get_pool_slot_sizes(self):
        # get a list with all possible slot sizes of each pool (also lists).
        slot_sizes = []
        for pool in self.defined_card_pools:
            slot_sizes.append(pool.get_size_list())
        return slot_sizes

    def get_deck_name(self):
        return self.deck_name

    def get_main_dict(self):
        return self.main_dict

    def get_deck_size(self):
        return self.deck_size
    
    def get_sample_size(self):
        return self.sample_size
    
    def get_card_pools(self):
        return self.defined_card_pools
    
    def get_unassigned_cards(self):
        return self.unassigned_cards    

    def get_unassigned_card_count(self):
        return self.unassigned_card_count
    