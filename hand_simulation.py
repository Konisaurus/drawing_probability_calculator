import random
from deck_controller import *
import copy

def convert_dict_to_list(old_dict):
    # create a list with all keys from a dictionary
    # Each key is added to the list as many times as its associated value.
    new_list = []
    for key in old_dict:
        copies = old_dict[key]
        for i in range(copies):
            new_list.append(key)
    return new_list


def create_counting_list(deck):
    # for every pool in the deck, one counting variable (zero) gets added to a counting list
    card_pools = deck.get_card_pools()
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

    # get all values from the Deck_Controller
    card_pools = deck.get_card_pools()
    base_counting_list = create_counting_list(deck)
    card_list = convert_dict_to_list(deck.get_main_dict())

    # loop for the iterations
    for i in range(iterations):
        # every loop needs a new counting list and sample
        counting_list = copy.copy(base_counting_list)
        card_sample = random.sample(card_list, sample_size)

        # check if the cards from the sample are in a pool
        for card in card_sample: 
            for pool in card_pools:
                index = card_pools.index(pool)
                if card in pool.get_card_names():
                    counting_list[index] += 1

        # check if success
        if 0 not in counting_list:
            success += 1

    return [success, iterations, "{}%".format(success / iterations * 100)]

# this is only for testing
main = {'Kashtira Fenrir': 3, 'Mudan the Rikka Fairy': 1, 'Traptrix Myrmeleo': 3, 'Traptrix Mantis': 2, 'Traptrix Dionaea': 1, \
        'Traptrix Vesiculo': 1, 'Traptrix Arachnocampa': 1, 'Traptrix Pudica': 1, 'Primula the Rikka Fairy': 1, 'Rikka Princess': 3, \
        'Rikka Glamour': 3, 'Rikka Konkon': 2, 'Traptrix Orchard': 1, 'Called by the Grave': 1, 'Time-Space Trap Hole': 1, \
        'Delusion Trap Hole': 1, 'Bottomless Trap Hole': 1, 'Infinite Impermanence': 3, "Ice Dragon's Prison": 2, \
        'Rikka Sheet': 2, 'Traptrix Holetaea': 3, 'The Phantom Knights of Shade Brigandine': 3}

deck = Deck_Controller(main)
deck.create_card_pools([Card_Pool(['Kashtira Fenrir'], deck.get_main_dict(), 1, False), Card_Pool(['Traptrix Myrmeleo', 'Traptrix Mantis'], deck.get_main_dict(), 1, False)])

print(sample_simulation(deck, 1000, 0))
