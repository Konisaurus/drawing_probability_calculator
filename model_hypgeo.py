from itertools import product
from methods_for_model import *
from classes_for_model import *
from observer_subject import Subject


class Model_Hypgeo(Subject):
    def __init__(self):
        Subject.__init__(self)
        self.deck = None
        self.sample_size = 0
        self.slot_sizes = []

    def calculate(self):
        # find all possible configurations of the sample hand.
        # Requirements for one successfull configuration:
        # - Every slot must be in the configuration (a size of a slot can be 0).
        # - All slot sizes added up must not exceed the sample_size.
        # The binomial_coefficient of each slot is stored in one configuration.
        # All configurations are stored in the configuration_table.
        configuration_table = []
        for element in product(*self.slot_sizes):
            int_sum = 0
            combination = list(element)
            for count in combination:
                int_sum += count
            if int_sum <= self.sample_size:
                index = 0
                binomial_list = []
                for count in combination:
                    binomial_list.append(binomial_coefficient(self.deck.get_card_pools()[index].get_card_count(), count))
                    index += 1
                size_rest = self.sample_size - int_sum
                binomial_list.append(binomial_coefficient(self.deck.get_unassigned_card_count(), size_rest))
                configuration_table.append(binomial_list)

        # all possible samples (successes and failures)
        divisor = binomial_coefficient(self.deck.get_deck_size(), self.sample_size)

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

    def set_deck(self, deck):
        self.deck = deck

    def set_slot_sizes(self):
        self.slot_sizes = self.deck.get_pool_slot_sizes()

    # needs more methods to funciton properly, methods must be made compatible with MVC pattern