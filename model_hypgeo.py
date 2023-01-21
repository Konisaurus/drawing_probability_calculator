'''
This module contains a model that calculates the probability of drawing 
a sample hand from a deck with the hypergeometric cumulative distribution function.
'''

# Imports
from itertools import product
from methods_for_model import *
from classes_for_model import *
from observer_subject import Subject

# Classes.
class Model_Hypgeo(Subject):
    '''
    Model which calculates the probability of drawing a sample hand 
    from a deck with the hypergeometric cumulative distribution function.
    '''
    def __init__(self):
        Subject.__init__(self)      # inheritance of Observer pattern
        self.deck_manager = None    # deck which is used for calculations.

        # marked section is only for testing
        # will be deleted after everything is done correctly
        ###########################################################################################################################################
        deck = Deck("Traptrix-Rikka", 
            {'Kashtira Fenrir': 3, 'Mudan the Rikka Fairy': 1, 'Traptrix Myrmeleo': 3, 'Traptrix Mantis': 2, 'Traptrix Dionaea': 1, \
            'Traptrix Vesiculo': 1, 'Traptrix Arachnocampa': 1, 'Traptrix Pudica': 1, 'Primula the Rikka Fairy': 1, 'Rikka Princess': 3, \
            'Rikka Glamour': 3, 'Rikka Konkon': 2, 'Traptrix Orchard': 1, 'Called by the Grave': 1, 'Time-Space Trap Hole': 1, \
            'Delusion Trap Hole': 1, 'Bottomless Trap Hole': 1, 'Infinite Impermanence': 3, "Ice Dragon's Prison": 2, \
            'Rikka Sheet': 2, 'Traptrix Holetaea': 3, 'The Phantom Knights of Shade Brigandine': 3})
        self.set_deck_manager(deck)
        ###########################################################################################################################################

    def calculate(self):
        '''
        Calculate the probability of drawing the configured hand in the deck_manager() and return it.
        '''
        self.notify("start calculate")                                  # notifiy the Observers that the calculation will start, so the last parameters can be set before calculation.
        if self.deck_manager != None:                                   # only calculates when a deck is defined
            slot_size_list = self.deck_manager.get_pool_slot_sizes()    # get all possible slot_sizes of each pool
            combination_table = []                                      # the combination_table stores the binomial_coefficient of all possible combinations of slot_sizes.
            for element in product(*slot_size_list):                    # product(*slot_sizes_list) is a list with sublists. Every sublist is one combinations of a slot_size from each pool. product() contains all possible combinations.
                size_sum = 0                                            # Requirements for one valid combination:
                combination = list(element)                             # - Every slot must be in the combination (a size of a slot can be 0), which is ensured by product().
                for size in combination:                            
                    size_sum += size                                
                if size_sum <= self.deck_manager.get_sample_size():     # - All slot sizes added up must not exceed the sample_size. If a combinations is valid, it passes this if-statement.
                    index = 0                                           # index count variable which we need for accessing certain elements in pool_lists.
                    binomial_list = []                                  # Store the binomial coefficient of each slot_size in one combination.
                    for slot_size in combination:                       # The slot_size = we select this many cards from this pool. The binomial coeffiecent is calcualted with n = (total cards in the pool) and k = slot_size.
                        binomial_list.append(binomial_coefficient(self.deck_manager.get_pools()[index].get_card_count(), slot_size))
                        index += 1                                          
                    size_rest = self.deck_manager.get_sample_size() - size_sum                                              # Maybe not all slots of the sample hand must be occupied by a pool. Here, the size of the rest slot is calculated and stored in size_rest.
                    binomial_list.append(binomial_coefficient(self.deck_manager.get_unassigned_card_count(), size_rest))    # We calculated the binomial coefficient of the rest, n = number of unassigned cards (are in no pool), k = size_rest.
                    combination_table.append(binomial_list)                                                                 # Add the rest binomial coefficient to the list. Now, all slots of the sample hand are occupied by something.
    
            divisor = binomial_coefficient(self.deck_manager.get_deck_size(), self.deck_manager.get_sample_size())          # All possible samples that a deck can produce which includes successes and failures. It is the divisor of the probability.   

            dividend = 0                            # All successfull, possible samples that this deck can produce. It is the dividend of the probability.
            for combination in combination_table:                                                                         
                temp_factor = 1
                for value in combination:           # If we multiply all binomial coefficients of one combination, we get the number of successful samples that one combination adds to the overall probability (the dividend of the hypergeometric probability distribution function of this exact combination).
                    temp_factor *= value                
                dividend += temp_factor             # We add all dividends of the hypgeo. pdfs together and get the number of all possible successfull samples(the dividend of the hypergeometric cumulative distribution function). 

            hypgeo_cdf = dividend / divisor         # We get the hypgeo. cdf by dividing (successful samples) / (possible samples).

            return hypgeo_cdf

    # Setter functions.
    def set_deck_manager(self, deck):
        self.deck_manager = Deck_Manager(self, deck)

    # Getter functions.
    def get_deck_manager(self):
        return self.deck_manager


# Testing this model class.
if __name__ == "__main__":
    deck = Deck("Traptrix-Rikka", 
            {'Kashtira Fenrir': 3, 'Mudan the Rikka Fairy': 1, 'Traptrix Myrmeleo': 3, 'Traptrix Mantis': 2, 'Traptrix Dionaea': 1, \
            'Traptrix Vesiculo': 1, 'Traptrix Arachnocampa': 1, 'Traptrix Pudica': 1, 'Primula the Rikka Fairy': 1, 'Rikka Princess': 3, \
            'Rikka Glamour': 3, 'Rikka Konkon': 2, 'Traptrix Orchard': 1, 'Called by the Grave': 1, 'Time-Space Trap Hole': 1, \
            'Delusion Trap Hole': 1, 'Bottomless Trap Hole': 1, 'Infinite Impermanence': 3, "Ice Dragon's Prison": 2, \
            'Rikka Sheet': 2, 'Traptrix Holetaea': 3, 'The Phantom Knights of Shade Brigandine': 3})
        
    hypgeo = Model_Hypgeo()
    
    hypgeo.set_deck_manager(deck)
    hypgeo.get_deck_manager().set_sample_size(5)

    hypgeo.get_deck_manager().add_pool()
    hypgeo.get_deck_manager().add_card_to_pool(0, 'Kashtira Fenrir')
    hypgeo.get_deck_manager().set_pool_slot_size(0, 1)
    hypgeo.get_deck_manager().set_pool_only_equal(0, False)

    hypgeo.get_deck_manager().add_pool()
    hypgeo.get_deck_manager().set_pool_slot_size(1, 0)

    print(hypgeo.calculate())
