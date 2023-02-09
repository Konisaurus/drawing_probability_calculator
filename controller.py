'''
This module defines the Controll class.
'''

# Imports.
import copy
from model_hypgeo import Model_Hypgeo
from view import View

# Classes.
class Controller:
    '''
    Controlls the interaction from the user with the View and Model class.
    '''
    def __init__(self):
        self.model = copy.deepcopy(Model_Hypgeo())  # Model of the system, contains logic aspects.
        self.view = View(self.model, self)          # View of the system, contians visual aspects.

    # Event handlers.
    def on_deck_import(self):
        '''
        Adds a deck to the "Deck Selection" dropdown menu.

        NOT YET IMPLEMENTED
        '''
        pass

    def on_deck_delete(self):
        '''
        Deletes a deck from the "Deck Selection" dropdown menu.

        NOT YET IMPLEMENTED
        '''
        pass

    def on_add_pool(self):
        '''
        Create a pool in the models self.deck_manager
        '''
        self.model.get_deck_manager().add_pool()
               
    def on_del_pool(self):
        '''
        Deletes a pool in the models self.deck_manager

        NOT YET IMPLEMENTED
        '''
        self.model.get_deck_manager().del_pool()

    def on_clear(self):
        '''
        Resets everthing to the initial state.

        NOT YET IMPLEMENTED
        '''
        self.model = copy.deepcopy(Model_Hypgeo())      # Create a new model.
        self.view = View(self.model, self)              # Create a new view.

    def on_calculate(self):
        '''
        Calculate the probability of drawing the hand the user set up.
        '''
        self.model.calculate()

    def on_add_card(self, index, card_name):
        '''
        Assigns a card to a pool.
        '''
        if card_name == "Select card.":     # Nothing is selected, do nothing.
            pass
        else:                               # Assign the selected card.
            self.model.get_deck_manager().add_card_to_pool(index, card_name)

    def on_del_card(self, index, card_name):
        '''
        Unassigns a card from a pool.
        '''
        if card_name == "Select card.":     # Nothing is selected, do nothing.
            pass
        else:                               # Assign the selected card.
            self.model.get_deck_manager().del_card_in_pool(index, card_name)

    def on_change_type(self, index):
        '''
        Changes the type of a pool. 
        There are only two states, so it always switches to the other.
        The two states are X == x or X <= x.
        '''
        if self.model.get_deck_manager().get_pools()[index].get_only_equal() == True:
            self.model.get_deck_manager().set_pool_only_equal(index, False)
        else:
            self.model.get_deck_manager().set_pool_only_equal(index, True)
