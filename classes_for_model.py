'''
This module is about storing information of a deck, so the model can calculate with it.

It contains the following classes:
- Deck
- Pool_Manager
- Deck_Manager
'''

# Imports.
import copy

# Classes.
class Deck:
    '''
    Class for storing deck information.
    '''
    def __init__(self, deck_name, main_deck):
        self.name = deck_name       # Name of the deck.
        self.main = main_deck       # The actual deck as a dict.

    # Getter functions.
    def get_name(self):
        return self.name
    
    def get_main(self):
        return self.main


class Pool_Manager:
    '''
    Class for managing a pool of cards. In a calculation, all cards in one pool are treated the same; they are one unit.
    '''
    def __init__ (self, deck_manager, card_names = [], min_slot_size = 0, boolean=False):

        # Card info for pool.
        self.card_names = card_names                          # All card names that are in the pool.
        self.card_count = None                                # Number of card copies in the pool.
        self.set_card_count(deck_manager.get_main_dict())     # Set self.card_count.

        # Info for calculations.
        self.min_slot_size = min_slot_size                    # How many cards of this pool should be at least in a successfull sample.
        self.only_equal = boolean                             # True (only == self.min_slot_size is a success), False (everything >= self.min_slot_size is a success).
        self.size_list = None                                 # list of all possible sizes of a slot that is occupied by cards of this pool (also depends on sample size).
        self.set_size_list(deck_manager.get_sample_size())    # Set self.size_list.

    # Setter functions.
    def set_card_count(self, main_dict):
        '''
        Calculates the number of card copies in the pool and sets self.card_count.
        Needs the main_dict of the deck to check how many copies of each card are in the deck.
        '''
        if self.card_names == []:           # If the list is empty, 0 cards are in the pool.
            self.card_count = 0
        
        else:                               # Otherwise, the number of cards is the sum of all copies of each card_name.
            count = 0
            for key in self.card_names:     
                count += main_dict[key]
            self.card_count = count
        
    def set_slot_size(self, min_slot_size, sample_size):
        '''
        Sets the value of self.min_slot_size.
        '''
        self.min_slot_size = min_slot_size
        self.set_size_list(sample_size)     # Update self.size_list, because it depends on self.min_slot_size.

    def set_only_equal(self, boolean, sample_size):
        '''
        Sets the value of self.only_equal.
        '''
        self.only_equal = boolean
        self.set_size_list(sample_size)     # Update self.size_list, because it depends on self.only_equal.

    def set_size_list(self, sample_size):
        '''
        Sets self.size_list.
        Needs the sample size to create the size list. A size list contains all accepted slot sizes of its pool.
        Only when the amount of cards of this pool in sample hand corresponds with one element of the size list, the sample hand is treated as an success.
        '''
        self.size_list = []
        if self.only_equal == True:                 # When only one slot size is accepted, then the size_list only contains this one size.
            self.size_list = [self.min_slot_size]
            
        else:                                       # Other wise, the smallest size is determined by self.min_slot_size, the maximum by min(self.card_count, sample_size).
            self.size_list =  list(range(self.min_slot_size, min(self.card_count, sample_size) + 1))

    # Managing cards.
    def add_card(self, card_name, main_dict, sample_size):
        '''
        Add a card_name to the pool. 
        Need a main_dict and sample_size for updating other parts of the class.
        '''
        self.card_names.append(card_name)     # Add the card to the list.
        self.set_card_count(main_dict)        # Update the number of cards.
        self.set_size_list(sample_size)       # Update the size_list.

    def del_card(self, card_name, main_dict, sample_size):
        '''
        Remove a card_name in the pool. 
        Need a main_dict and sample_size for updating other parts of the class.
        '''
        self.card_names.remove(card_name)     # Remove the card from the list.
        self.set_card_count(main_dict)        # Update the number of cards.
        self.set_size_list(sample_size)       # Update the size_list.

    # Getter functions.
    def get_card_names(self):
        return self.card_names
    
    def get_only_equal(self):
        return self.only_equal
    
    def get_card_count(self):
        return self.card_count
    
    def get_size_list(self):
        return self.size_list


class Deck_Manager:
    '''
    Class for managing a deck with all it's defined card pools for a calculation.
    '''
    def __init__(self, model, deck, sample_size = 0, defined_pools = []):

        # Reference to the model.
        self.model = model

        # These attributes should always stay the same for one particular deck.
        self.deck_name = deck.get_name()                   # Deck name.
        self.main_dict = deck.get_main()                   # Main deck as a dictionary, main_dict = {"card1": int(number of card1 in deck), ... , "cardX": int(number of cardX in deck)}.
        self.deck_size = self.calculate_deck_size()        # Number of card copies in deck.

        # can be changed
        self.sample_size = sample_size                     # Number of cards that are drawn in a sample hand.
        self.defined_pools = defined_pools                 # List of different card pools.
        self.unassigned_cards = None                       # Dict of cards that are in no card pool.
        self.set_unassigned_cards()                        # Set self.unassigned_cards.         
        self.unassigned_card_count = None                  # Number of card copies that are not assigned to any pool.
        self.set_unassigned_card_count()                   # Set self.unassigned_card_count.
    
    def calculate_deck_size(self):
        '''
        Calculates the size of the deck and returns it.
        '''
        deck_size = 0
        for key in self.main_dict:                         # The deck size is the sum of all copies of each card_name.
            deck_size += self.main_dict[key]
        return deck_size

    # Setter funcitions.
    def set_sample_size(self, sample_size):
        '''
        Sets self.sample_size.
        '''
        self.sample_size = sample_size

        # Update everything is dependend on the sample size.
        if self.defined_pools != []:
            for pool in self.defined_pools:
                pool.set_size_list(self.sample_size)

    def set_unassigned_cards(self):
        '''
        Sets self.unassigned_cards.
        '''
        unassigned_cards = copy.deepcopy(self.main_dict)    # Make a deep copy of the self.main_dict, because we need a new modfied version.
        if self.defined_pools != []:                        # If there are no defined card pools, we don't need to remove any cards.
            for pool in self.defined_pools:                 # Go through all pools, remove the all cards that are in a pool from unassigned_cards.
                if pool.get_card_names() != []:
                    for card in pool.get_card_names():
                        unassigned_cards.pop(card)
        self.unassigned_cards = unassigned_cards
    
    def set_unassigned_card_count(self):
        '''
        Sets self.unassigned_card_count.
        '''
        unassigned_card_count = self.deck_size                  # Get the number of cards in a deck.
        if self.defined_pools != []:                            # Reduce it by the size of each pool.
            for pool in self.defined_pools:
                unassigned_card_count -= pool.get_card_count()
        self.unassigned_card_count = unassigned_card_count

    # Access setter functions of a pool.
    def set_pool_slot_size(self, index, min_slot_size):
        '''
        Sets self.min_slot_size of the pool in self.defined_pool_list with index.
        '''
        self.defined_pools[index].set_slot_size(min_slot_size, self.sample_size)

    def set_pool_only_equal(self, index, boolean):
        '''
        sets self.only_equal of the pool in self.defined_pool_list with index.
        '''
        self.defined_pools[index].set_only_equal(boolean, self.sample_size)
        self.model.notify("changed only equal", index)                       # Use notify() method of model, because this change is noticable in the View class.

    # Managing cards and pools.
    def add_pool(self):
        '''
        Creates an "empty" card pool object and adds it to self.defined_pools.
        '''
        self.defined_pools.append(copy.deepcopy(Pool_Manager(self)))
        self.model.notify("add pool")                                        # Use notify() method of model, because this change is noticable in the View class.

    def add_card_to_pool(self, index, card_name):
        '''
        Adds a card_name to a pool in self.defined_pools with index.
        '''
        self.defined_pools[index].add_card(card_name, self.main_dict, self.sample_size)

        self.set_unassigned_cards()                                          # Update self.unassigned_cards, because we assigned a card.
        self.set_unassigned_card_count()                                     # Update self.unassigned_card_count, because we assigned a card.

        self.model.notify("add card to pool", index, card_name)              # Use notify() method of model, because this change is noticable in the View class.

    def del_card_in_pool(self, index, card_name):
        '''
        Removes a card_name from a pool in self.defined_pools with index.
        '''
        self.defined_pools[index].del_card(card_name, self.main_dict, self.sample_size)

        self.set_unassigned_cards()                                         # Update self.unassigned_cards, because we unassigned a card.
        self.set_unassigned_card_count()                                    # Update self.unassigned_card_count, because we unassigned a card.

        self.model.notify("removed card from pool", index, card_name)       # Use notify() method of model, because this change is noticable in the View class.

    # Getter functions.
    def get_model(self):
        return self.model
    
    def get_pool_slot_sizes(self):
        '''
        Get a list with all possible slot sizes of each pool (also lists) and return it.
        '''
        slot_sizes = []
        for pool in self.defined_pools:                  # Get a list with all possible slot sizes of each pool.
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
    
    def get_pools(self):
        return self.defined_pools
    
    def get_unassigned_cards(self):
        return self.unassigned_cards    

    def get_unassigned_card_count(self):
        return self.unassigned_card_count
