import copy
from model_hypgeo import Model_Hypgeo
from view import View

class Controller:
    def __init__(self):
        self.model = Model_Hypgeo()
        self.view = View(self.model, self)

    # event handlers
    def on_deck_import(self):
        # adds a deck to the dropdown menu
        pass

    def on_deck_delete(self):
        # deletes a deck
        pass

    def on_add_pool(self):
        # create pool in model
        self.model.get_deck_manager().add_card_pool()
               
    def on_calculate(self):
        # deletes the selected deck from the dropdown menu 
        print(self.model.calculate())

    def on_add_card(self, index, card_name):
        # add a card to a card pool
        if card_name == "Select card.":
            pass
        else:
            self.model.get_deck_manager().add_card_to_pool(index, card_name)

    def on_del_card(self, index, card_name):
        # deletes a card from a card pool 
        if card_name == "Select card.":
            pass
        else:
            self.model.get_deck_manager().remove_card_from_pool(index, card_name)

    def on_change_type(self, index):
        # changes the type of a card pool (X == x or X <= x)
        if self.model.get_deck_manager().get_card_pools()[index].get_only_equal() == True:
            self.model.get_deck_manager().set_pool_only_equal(index, False)
        else:
            self.model.get_deck_manager().set_pool_only_equal(index, True)
