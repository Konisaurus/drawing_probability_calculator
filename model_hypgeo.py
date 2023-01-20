from itertools import product
from methods_for_model import *
from classes_for_model import *
from observer_subject import Subject


class Model_Hypgeo(Subject):
    def __init__(self):
        Subject.__init__(self)
        self.deck_manager = None

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
        # find all possible configurations of the sample hand.
        # Requirements for one successfull configuration:
        # - Every slot must be in the configuration (a size of a slot can be 0).
        # - All slot sizes added up must not exceed the sample_size.
        # The binomial_coefficient of each slot is stored in one configuration.
        # All configurations are stored in the configuration_table.
        self.notify("start calculate")
        if self.deck_manager != None:
            slot_sizes = self.deck_manager.get_pool_slot_sizes()
            configuration_table = []
            for element in product(*slot_sizes):
                size_sum = 0
                combination = list(element)
                for size in combination:
                    size_sum += size
                if size_sum <= self.deck_manager.get_sample_size():
                    index = 0
                    binomial_list = []
                    for count in combination:
                        binomial_list.append(binomial_coefficient(self.deck_manager.get_card_pools()[index].get_card_count(), count))
                        index += 1
                    size_rest = self.deck_manager.get_sample_size() - size_sum
                    binomial_list.append(binomial_coefficient(self.deck_manager.get_unassigned_card_count(), size_rest))
                    configuration_table.append(binomial_list)

            # all possible samples (successes and failures)
            divisor = binomial_coefficient(self.deck_manager.get_deck_size(), self.deck_manager.get_sample_size())

            # calculate the hypergeometric probability distribution function for each configuration.
            # The hypgeo pdf of all configurations added up equals the hypgeo cumulative distribution function.
            dividend = 0
            for configuration in configuration_table:
                temp_factor = 1
                for value in configuration:
                    temp_factor *= value
                dividend += temp_factor

            # calculate the result
            hypgeo_cdf = dividend / divisor

            return hypgeo_cdf

    def set_deck_manager(self, deck):
        self.deck_manager = Deck_Manager(self, deck)

    # getter functions
    def get_deck_manager(self):
        return self.deck_manager


# for testing the model class
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

    hypgeo.get_deck_manager().add_card_pool()
    hypgeo.get_deck_manager().add_card_to_pool(0, 'Kashtira Fenrir')
    hypgeo.get_deck_manager().set_pool_slot_size(0, 1)
    hypgeo.get_deck_manager().set_pool_only_equal(0, False)

    hypgeo.get_deck_manager().add_card_pool()
    hypgeo.get_deck_manager().set_pool_slot_size(1, 0)

    print(hypgeo.calculate())
