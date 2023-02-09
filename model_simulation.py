'''
NOT YET FULLY IMPLEMENTED
'''

# Import.
import random
import copy
from classes_for_model import *

# Mehtods.
def convert_dict_to_list(old_dict):
    # create a list with all keys from a dictionary and return it.
    # Each key is added to the list as many times as its associated value.
    new_list = []
    for key in old_dict:
        copies = old_dict[key]
        for i in range(copies):
            new_list.append(key)
    return new_list


def create_counting_list(deck):
    # for every pool in the deck, one counting variable (zero) gets added to a counting list.
    card_pools = deck.get_pools()
    counting_list = []
    for i in range(len(card_pools)):
        counting_list.append(0)
    return counting_list


def sample_simulation(deck, iterations, sample_size):
    # deck: Dech_Controller class
    # iterations: times a sample is drawn
    # sample_size: size of the sample
    # a sample is a success, when at least one card from each pool (Deck_Controller) is drawn.
    success = 0

    # get all values from the Deck_Controller.
    card_pools = deck.get_pools()
    base_counting_list = create_counting_list(deck)
    card_list = convert_dict_to_list(deck.get_main_dict())

    # loop for the iterations
    for i in range(iterations):
        # every loop needs a new counting list and sample.
        counting_list = copy.copy(base_counting_list)
        card_sample = random.sample(card_list, sample_size)

        # check if the cards from the sample are in a pool.
        for card in card_sample: 
            for pool in card_pools:
                index = card_pools.index(pool)
                if card in pool.get_card_names():
                    counting_list[index] += 1

        # check if success
        if 0 not in counting_list:
            success += 1

    return [success, iterations, "{}%".format(success / iterations * 100)]
