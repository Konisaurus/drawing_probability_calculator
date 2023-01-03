from itertools import product
from deck_controller import *
# import PYQT5

def faculty(n):
    # calculate faculty of n
    n_fak = 1
    if n != 0:
        for i in range(2,n+1):
            n_fak *= i
    return n_fak


def binomial_coefficient(n, k):
    # calculates the binomial coefficient
    # n = set
    # k = draws
    if 0 <= k <= n:
        dividend = 1
        divisor = 1
        for i in range(1, min(n - k, k) + 1):
            dividend *= n
            divisor *= i
            n -= 1
        return int(dividend / divisor)


def advanced_hypgeo_cdf(deck, sample_size = 0):
    # calculate probability of drawing a certain sample of cards from a deck
    # probability P(A ==/>= a, B ==/>= b, C ==/>= c, D ==/>= d, E ==/>= e, F ==/>= f)
    
    # pass the sample_size to the Deck_Controller
    deck.set_sample_size(sample_size)
    # get a list with all possible slot sizes of each pool (also lists)
    slot_sizes = deck.get_pool_slot_sizes()
    
    # find all possible configurations of the sample hand.
    # Requirements for one successfull configuration:
    # - every slot must be in the configuration (a size of a slot can be 0)
    # - all slot sizes added up must not exceed the sample_size
    # The binomial_coefficient of each slot is stored in one configuration.
    # All configurations are stored in the configuration_table.
    configuration_table = []
    for element in product(*slot_sizes):
        int_sum = 0
        combination = list(element)
        for count in combination:
            int_sum += count
        if int_sum <= sample_size:
            index = 0
            binomial_list = []
            for count in combination:
                binomial_list.append(binomial_coefficient(deck.get_card_pools()[index].get_card_count(), count))
                index += 1
            size_rest = sample_size - int_sum
            binomial_list.append(binomial_coefficient(deck.get_unassigned_card_count(), size_rest))
            configuration_table.append(binomial_list)
    
    # all possible samples (successes and failures)
    divisor = binomial_coefficient(deck.get_deck_size(), sample_size)

    # calculate the hypergeometric probability distribution function for each configuration
    # The hypgeo pdf of all configurations added up equals the hypgeo cumulative distribution function
    dividend = 0
    for configuration in configuration_table:
        temp_factor = 1
        for value in configuration:
            temp_factor *= value
        dividend += temp_factor
    hypgeo_cdf = dividend / divisor

    return hypgeo_cdf


def format_float(percentage, decimals, value):
    # formating method for floats
    # percentage: True = multiply float by 100, False = do nothing
    # decimals: number of decimals after the comma
    # value: float you want to format
    if percentage == True:
        value *= 100
    return float("%.{}f".format(decimals) % value)

main = {'Kashtira Fenrir': 3, 'Mudan the Rikka Fairy': 1, 'Traptrix Myrmeleo': 3, 'Traptrix Mantis': 2, 'Traptrix Dionaea': 1, 'Traptrix Vesiculo': 1, 'Traptrix Arachnocampa': 1, 'Traptrix Pudica': 1, 'Primula the Rikka Fairy': 1, 'Rikka Princess': 3, 'Rikka Glamour': 3, 'Rikka Konkon': 2, 'Traptrix Orchard': 1, 'Called by the Grave': 1, 'Time-Space Trap Hole': 1, 'Delusion Trap Hole': 1, 'Bottomless Trap Hole': 1, 'Infinite Impermanence': 3, "Ice Dragon's Prison": 2, 'Rikka Sheet': 2, 'Traptrix Holetaea': 3, 'The Phantom Knights of Shade Brigandine': 3}

deck = Deck_Controller(main)
deck.add_card_pools([Card_Pool(['Kashtira Fenrir'], deck.get_main_dict(), 1, False), Card_Pool(['Traptrix Myrmeleo', 'Traptrix Mantis'], deck.get_main_dict(), 1, False)])

print(format_float(True, 3, advanced_hypgeo_cdf(deck)))
