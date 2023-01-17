import copy


class Deck:
    # class for storing deck info (optimized for Yu-Gi-Oh!)
    def __init__(self, deck_name, main_deck, extra_deck, side_deck):
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
    def __init__ (self, name_list, main_dict, min_slot_size = 1, boolean = True):
        # card info for pool
        self.card_names = name_list                     # store all card names that are in the pool.
        self.card_count = self.addup_cards(main_dict)   # number of card copies in the pool.

        # info for calculations
        self.min_slot_size = min_slot_size              # how many cards of this pool should be at least in a successfull sample.
        self.only_equal = boolean                       # True (only == 1 is a success), False (everything >= 1 is a success)
        self.size_list = []                             # list of all possible sizes of a slot that is occupied by cards of this pool (also depends on sample size).

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

    def create_size_list(self, sample_size):
        # create list of all possible sizes of a slot that is occupied by cards of this pool.
        # The smallest size is determined by self.min_slot_size, the maximum by min(self.card_count, sample_size).
        self.size_list = []
        if self.only_equal == True:
            self.size_list = self.min_slot_size
        else:
            self.size_list =  list(range(self.min_slot_size, min(self.card_count, sample_size) + 1))

    def add_card(self, card_name, main_dict, sample_size):
        # adds a card to the pool
        self.card_names.append(card_name)
        self.card_count = self.addup_cards(main_dict)
        self.create_size_list(sample_size)

    # getter functions
    def get_card_count(self):
        return self.card_count

    def get_card_names(self):
        return self.card_names


class Deck_Manager:
    # class for managing different card pools that are in one deck.
    def __init__(self, deck):
        # these attributes should always stay the same
        self.deck = deck                                                # entire deck info (class Deck)
        self.main_dict = self.deck.get_main()                           # main deck as a dictionary, main_dict = {"card1": int(number of card1 in deck), ... , "cardX": int(number of cardX in deck)}
        self.deck_size = self.calculate_deck_size()                     # number of card copies in deck

        # can be changed
        self.defined_card_pools = []                                    # list of different card pools
        self.unassigned_cards = self.check_unassigned_cards()           # dict of cards that are in no card pool
        self.unassigned_card_count = self.calculate_unassigned_cards()  # number of card copies that are not assigned to any pool
        self.sample_size = 0                                            # number of cards that are drawn in a sample hand
    
    def calculate_deck_size(self):
        # calculate the number of card copies in deck and return it.
        deck_size = 0
        for key in self.main_dict:
            deck_size += self.main_dict[key]
        return deck_size

    def calculate_unassigned_cards(self):
        # calculate number of card copies that are not assigned to any pool and return it.
        unassigned_card_count = self.deck_size
        if self.defined_card_pools != []:
            for pool in self.defined_card_pools:
                unassigned_card_count -= pool.get_card_count()
        return unassigned_card_count

    def check_unassigned_cards(self):
        # creates/updates the list of unassigned card names
        unassigned_cards = copy.deepcopy(self.main_dict)
        if self.defined_card_pools != []:
            for pool in self.defined_card_pools:
                if pool.get_card_names() != []:
                    for card in pool.get_card_names():
                        unassigned_cards.pop(card)
        return unassigned_cards

    def create_card_pools(self, card_pools):
        # add a list of card_pools to to the Deck_Controller.
        self.defined_card_pools.extend(card_pools)
        self.unassigned_card_count = self.calculate_unassigned_cards()  # update unassinged_card_count
        self.unassigned_cards = self.check_unassigned_cards()

    def add_card_to_pool(self, pool_index, card_name):
        # adds a card_name to a card pool
        self.defined_card_pools[pool_index].add_card(card_name, self.main_dict, self.sample_size)
        self.unassigned_card_count = self.calculate_unassigned_cards() 
        self.unassigned_cards = self.check_unassigned_cards()       

    def set_sample_size(self, sample_size):
        # set number of cards (sample_size) that are drawn in a sample hand.
        self.sample_size = sample_size
        if self.defined_card_pools != []:
            for pool in self.defined_card_pools:
                pool.create_size_list(self.sample_size)   # create valid slot size list for each pool.

    # getter functions
    def get_pool_slot_sizes(self):
        # get a list with all possible slot sizes of each pool (also lists).
        slot_sizes = []
        for pool in self.defined_card_pools:
            slot_sizes.append(pool.size_list)
        return slot_sizes

    def get_main_dict(self):
        return self.main_dict

    def get_deck_size(self):
        return self.deck_size
    
    def get_card_pools(self):
        return self.defined_card_pools

    def get_unassigned_card_count(self):
        return self.unassigned_card_count