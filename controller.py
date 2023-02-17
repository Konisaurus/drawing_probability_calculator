'''
This module defines the Controll class.
'''

# Imports.
import copy
import json
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

    # Event handlers for "Deck Selection".
    def on_deck_import(self, path):
        '''
        Adds a deck to the storage for calculations.
        '''
        try:                                                                 # Only runs when the path of the deck exists.
            with open(path, "r") as read_deck:                               # Load the deck dictionary.
                deck = json.load(read_deck)                                 

            try:                                                             # When there are already some decks in the storage.
                with open("deck_storage.json", "r") as read_storage:         # Open the deck storage.
                    deck_storage = json.load(read_storage)
            except:                                                          # No deck is in the storage.
                deck_storage = {}

            if type(deck) == dict and list(deck.keys())[0] not in deck_storage.keys():      # Only runs when there is no name conflict and the loaded deck is a dict.
                deck_storage = deck_storage | deck                                          # Add the deck to the storage dict.
                with open("deck_storage.json", "w") as write_storage:                       # Save the new storage.
                    json.dump(deck_storage, write_storage, indent=4, separators=(",",":"))
                return True                                                                 # Something has changed, so view must display something new.
            else:
                return "file not valid"
        except:
            return "file not found"

    def on_deck_delete(self, key):
        '''
        Deletes a deck from the "Deck Selection" dropdown menu.
        '''
        if key == "Select deck.":
            return False
        else:
            with open("deck_storage.json", "r") as read_storage:                            # Open the deck storage.
                deck_storage = json.load(read_storage)
            
            deck_storage.pop(key)                                                           # Delete the deck.

            with open("deck_storage.json", "w") as write_storage:                           # Update the storage
                json.dump(deck_storage, write_storage, indent=4, separators=(",",":"))
            return True                                                                     # Something has changed, so view must display something new.
    
    def on_drp_deck_changed(self, key):
        '''
        Set the new deck as the deck manager of the model.
        '''
        if key == "Select deck.":
            pass
        else:
            self.model.set_deck_manager(key)

    # Event handlers for "Initialize Calculation".
    def on_add_pool(self):
        '''
        Create a pool in the models self.deck_manager
        '''
        if self.validate_deck():
            self.model.get_deck_manager().add_pool()
               
    def on_del_pool(self):
        '''
        Deletes a pool in the models self.deck_manager

        NOT YET IMPLEMENTED
        '''
        if self.validate_deck():
            self.model.get_deck_manager().del_pool()

    def on_clear(self):
        '''
        Resets everthing to the initial state.

        NOT YET IMPLEMENTED
        '''
        self.model = copy.deepcopy(Model_Hypgeo())  # Create a new model.
        self.view = View(self.model, self)          # Create a new view.

    def on_calculate(self):
        '''
        Calculate the probability of drawing the hand the user set up.
        '''
        if self.validate_deck():
            self.model.calculate()

    # Event handlers for "Card Pool".
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

    # Other event handlers.
    def on_set_deck_manager(self, key):
        '''
        Sets the for the calculations.
        '''
        with open("deck_storage.json", "r") as read_file:   # Load the storage.
            deck = json.load(read_file)[key]                # Get the right deck.
            self.model.set_deck_manager(deck)               # Set this deck for further calculations.

    # Other funcitons.
    def validate_deck(self):
        '''
        Checks if a deck is selected.
        '''
        if self.model.get_deck_manager() == None:
            return False
        else:
            return True
