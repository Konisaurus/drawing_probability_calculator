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
        try:
            with open(path, "r") as read_deck:             # Only runs when the path of the deck exists.

                if path[-5:] == ".json":                   # Handle .json files.
                    deck = json.load(read_deck)            # Load the deck dictionary.
                    if type(deck) == dict:                 # Only runs when the loaded deck is a dictionary.
                        self.store_deck(deck)              # Store the deck.
                        return [True, deck.keys()]
                    else:                                  # File is not valid.
                        return "file not valid"
                    
                if path[-4:] == ".ydk":                    # Handle .ydk files
                    ydk = read_deck.read()                 # Read the ydk file.
                    try:
                        deck = self.convert_ydk(ydk, path) # Only a valid .ydk file can be converted
                        self.store_deck(deck)              # Store the deck.
                        return [True, deck.keys()]
                    except:                                # File is not valid.
                        return "file not valid"

                else:                                            # Invalid file type.
                    return "file not valid"
        except:                                                  # File does not exist.
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
    
    def on_deck_info(self):
        '''
        Opens an extra window that shows the entire deck with
        neccessary information about each card.
        '''
        if self.validate_deck():
            self.model.get_deck_manager().notify_deck_info()

    def on_clear(self):
        '''
        Resets everthing to the initial state.
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
    def on_del_pool(self, index):
        '''
        Deletes a pool in the models self.deck_manager
        '''
        if self.validate_deck():
            self.model.get_deck_manager().del_pool(index)

    def on_add_card(self, index, card_name):
        '''
        Assigns a card to a pool.
        '''
        if card_name == "Select card to add.": # Nothing is selected, do nothing.
            pass
        else:                                  # Assign the selected card.
            self.model.get_deck_manager().add_card_to_pool(index, card_name)

    def on_del_card(self, index, card_name):
        '''
        Unassigns a card from a pool.
        '''
        if card_name == "Select card to add.": # Nothing is selected, do nothing.
            pass
        else:                                  # Assign the selected card.
            self.model.get_deck_manager().del_card_in_pool(index, card_name)

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
        
    def store_deck(self, deck):
        '''
        Stores a deck in deck_storage.json.
        '''
        try:  
            with open("deck_storage.json", "r") as read_storage:         # When there are already some decks in the storage.
                deck_storage = json.load(read_storage)                   # Open the deck storage.
        except:
            deck_storage = {}                                            # No deck in storage.
        
        deck_storage = deck_storage | deck                                          # Add the deck to the storage dict.
        with open("deck_storage.json", "w") as write_storage:
            json.dump(deck_storage, write_storage, indent=4, separators=(",",":"))  # Save the new storage.
        
    def convert_ydk(self, ydk, path):
        '''
        Converts a .ydk file to a valid deck.
        '''
        deck_list = list(ydk.split("#extra"))               # Split the main deck from the rest.

        # Convert the main deck into a separate list only containing cards indexes.
        main_list = list(deck_list[0].split("\n"))
        main_list.pop(0)
        main_list.pop(0)
        main_list.pop(-1)

        temp_main_dict = {}                                 # Create a dict = {"id": "number of copies", ...}
        for element in main_list:
            try:
                temp_main_dict[element] += 1
            except:
                temp_main_dict[element] = 1

        with open("ydk_card_database.json", "r") as read_database:
            database = json.load(read_database)

        main_dict = {}                                      # Create a dict = {"name": "number of copies", ...}
        for key in temp_main_dict:
            name = database[key]
            main_dict[name] = temp_main_dict[key]

        name = str(path.split("\\")[-1][:-4])               # Use .ydk file name as deck name.
        deck = {}
        deck[name] = main_dict

        return deck
    