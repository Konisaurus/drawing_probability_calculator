class Card_Pool:
    # class for different cards that can be treated as one unit (each card is the "same")
    def __init__ (self, name_list, main_dict, min_slot_size = 1, boolean = True):
        self.card_names = name_list                     # store all card names that are in the pool
        self.card_count = self.addup_cards(main_dict)   # number of card copies in the pool
        self.min_slot_size = min_slot_size              # how many cards of this pool should be at least in a successfull sample
        self.only_equal = boolean                       # True (only == 1 is a success), False (everything >= 1 is a success)
        self.size_list = []                             # list of all possible sizes of a slot that is occupied by cards of this pool (also depends on sample size)

    def addup_cards(self, main_dict):
        # calculate the number of card copies in the pool
        if self.card_names == []:
            return 0
        count = 0
        for key in self.card_names:
            count += main_dict[key]
        return count

    def create_size_list(self, sample_size):
        # create list of all possible sizes of a slot that is occupied by cards of this pool.
        # the smallest size is determined by self.min_slot_size, the maximum by min(self.card_count, sample_size)
        if self.only_equal == True:
            self.size_list = self.min_slot_size
        else:
            self.size_list =  list(range(self.min_slot_size, min(self.card_count, sample_size) + 1))

    def get_card_count(self):
        return self.card_count

class Deck_Controller:
    # class for managing different card pools that are in one deck
    def __init__(self, main_dict):
        self.main_dict = main_dict                                      # main deck as a dictionary, main_dict = {"card1": int(number of card1 in deck), ... , "cardX": int(number of cardX in deck)}
        self.deck_size = self.calculate_deck_size()                     # number of card copies in deck
        self.defined_card_pools = []                                    # list of different card pools
        self.unassigned_card_count = self.calculate_unassigned_cards()  # number of card copies that are not assigned to any pool
        self.sample_size = 0                                            # number of cards that are drawn in a sample hand
    
    def calculate_deck_size(self):
        # calculate number of card copies in deck
        deck_size = 0
        for key in self.main_dict:
            deck_size += self.main_dict[key]
        return deck_size

    def calculate_unassigned_cards(self):
        # number of card copies that are not assigned to any pool
        unassigned_card_count = self.deck_size
        if self.defined_card_pools != []:
            for pool in self.defined_card_pools:
                unassigned_card_count -= pool.get_card_count()
        return unassigned_card_count

    def add_card_pools(self, card_pools):
        # add a list of pools to to the Deck_Controller
        self.defined_card_pools.extend(card_pools)
        self.unassigned_card_count = self.calculate_unassigned_cards()  # update unassinged_card_count

    def set_sample_size(self, sample_size):
        # set number of cards that are drawn in a sample hand
        self.sample_size = sample_size
        if self.defined_card_pools != []:
            for pool in self.defined_card_pools:
                pool.create_size_list(self.sample_size)   # create valid slot size list for each pool

    # getter functions
    def get_pool_slot_sizes(self):
        # get a list with all possible slot sizes of each pool (also lists)
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
