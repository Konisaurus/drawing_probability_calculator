'''
This module contains the View class which contains all the visual aspects of the system.
'''

# Imports
import tkinter as tk
from widgets_for_gui import *
from observer_subject import Observer
from model_hypgeo import *

# Name convetions for all tkinter widgets:
#
# Label 	                lbl 
# Button 	                btn 
# Entry 	                ent 
# Text 	                    txt 
# Frame 	                frm 
# Canvas                    cnv
# Scrollbar                 scb
# Changeable_OptionMenu     drp (short for dropdown)

# Classes.
class Pool_Section:
    '''
    Class for displaying one pool.
    '''
    def __init__(self, view, index = 0):
        
        # Associated place.
        self.view = view        # Master window.
        self.index = index      # Index where this pool in the pool_list of the master window is stored.

        # Frame for the card pool display.
        self.frame = tk.Frame(master=self.view.get_frm_bottom(), relief=tk.RIDGE, borderwidth=5, width=30)

        # Display all cards in the pool.
        self.card_names = []
        self.lbl_card_display = tk.Label(master=self.frame, text="text", width=50, anchor="nw", justify="left")
        self.set_card_display_text()

        # Labels.
        lbl_title = tk.Label(master=self.frame, text="Card Pool", height=1, font=("Helvetica", "11", "bold"), anchor="nw")
        lbl_add_card = tk.Label(master=self.frame, text="Add card:", anchor="nw")
        lbl_del_card = tk.Label(master=self.frame, text="Delete card:", anchor="nw")
        self.lbl_size = tk.Label(master=self.frame, text="Minimum pool size:", anchor="nw", width=15)

        # Dropdownlists.
        self.drp_add_card = Changeable_OptionMenu(self.frame, "Select card.", self.view.get_model().get_deck_manager().get_unassigned_cards(), 22)
        self.drp_del_card = Changeable_OptionMenu(self.frame, "Select card.", [], 22)

        # Buttons.
        self.btn_add_card = tk.Button(master=self.frame, text="+ CARD", command= lambda: self.view.get_controller().on_add_card(self.index, self.drp_add_card.get_variable()))
        self.btn_del_card = tk.Button(master=self.frame, text="- CARD", command= lambda: self.view.get_controller().on_del_card(self.index, self.drp_del_card.get_variable()))
        self.btn_change_type = tk.Button(master=self.frame, text="CHANGE", command= lambda: self.view.get_controller().on_change_type(self.index))

        # Entries.
        self.ent_min_size = tk.Entry(master=self.frame, width=29)

        # Arrange everything.
        self.lbl_card_display.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nw")

        lbl_title.grid(row=0, column=0, padx=1, pady=10, sticky="w")
        lbl_add_card.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        lbl_del_card.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.lbl_size.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.drp_add_card.get_OptionMenu_class().grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.drp_del_card.get_OptionMenu_class().grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.btn_add_card.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.btn_del_card.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.btn_change_type.grid(row=4, column=2, padx=5, pady=5, sticky="w")

        self.ent_min_size.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    # Setter functions.
    def set_index(self):
        '''
        Sets the index. Can only be used when the "Pool_Section" is appended to a list.
        '''
        self.index = self.view.get_pool_list().index(self)

    def set_pool_type(self):
        '''
        Sets the type of the "Pool Section". 
        There are only two types, so it always changes to the other type.
        '''
        state = self.lbl_size["text"]
        if state == "Minimum pool size:":
            self.lbl_size.config(text="Exact pool size:")
        else:
            self.lbl_size.config(text="Minimum pool size:")

    def set_card_display_text(self):
        '''
        Sets the card display of the "Pool Section"
        '''
        text_list = "Card name \n\n"
        if self.card_names != []:                   
            for card in self.card_names:            # Every card should be listed on a new line.
                text_list += "- " + card + "\n"
        else:                                       # If there are no cards in this pool, state this.
            text_list += "No cards in pool."

        self.lbl_card_display.config(text=text_list)

    # Managing cards.
    def add_card(self, card_name):
        '''
        Assigns a card to this pool display.
        '''
        self.card_names.append(card_name)
        self.set_card_display_text()                # Update the card display

    def del_card(self, card_name):
        '''
        Unassigns a card from this pool display.
        '''
        self.card_names.remove(card_name)
        self.set_card_display_text()                # Update the card display

    # Getter functions.
    def get_frame(self):
        return self.frame
    
    def get_min_size(self):
        return self.ent_min_size.get()

    def get_drp_add_card(self):
        return self.drp_add_card
    
    def get_drp_del_card(self):
        return self.drp_del_card

class View(tk.Tk, Observer):
    '''
    Class that manages all visual aspects of the program.
    '''
    def __init__(self, model, controller):
        
        # Interaction with the model and the controller.

        self.model = model              # Which model should be observed.
        self.model.attach(self)         # Attach to this model.
        self.controller = controller    # Controller contains all event handlers.

        ###################################################################################################################################################
        
        # Setup a window.

        tk.Tk.__init__(self)
        self.geometry("830x500")
        self.resizable(False, True)
        self.title("YGO Hand Master")

        # Create two sections for the window and pack them.
        self.frm_top = tk.Frame(master=self, borderwidth=5)
        self.frm_top.pack(anchor="nw")

        self.scb_frm_bottom = Scrollable_Frame(master=self)
        self.scb_frm_bottom.pack()
        
        ###################################################################################################################################################

        # Deck controll section.
        
        self.frm_deck_selection = tk.Frame(master=self.frm_top, relief=tk.RIDGE, borderwidth=5)
        self.frm_deck_selection.grid(row=0, column=0, padx=5, pady=5)
        
        # Labels.
        lbl_deck_selection = tk.Label(master=self.frm_deck_selection, text="Deck Selection", height=1, font=("Helvetica", "11", "bold"))
        lbl_deck_import = tk.Label(master=self.frm_deck_selection, text="Deck path:", height=1, width=15, anchor="w")
        lbl_stored_deck = tk.Label(master=self.frm_deck_selection, text="Stored decks:", height=1, width=15, anchor="w")

        # Entries.
        self.ent_deck_import = tk.Entry(master=self.frm_deck_selection, width=50)

        # Dropdownlists.
        self.drp_stored_deck = Changeable_OptionMenu(self.frm_deck_selection, "Select deck.", [], 42)

        # Buttons.
        self.btn_import = tk.Button(master=self.frm_deck_selection, text="IMPORT", command=self.controller.on_deck_import)
        self.btn_delete = tk.Button(master=self.frm_deck_selection, text="DELETE", command=self.controller.on_deck_delete)

        # Arrange everything.
        lbl_deck_selection.grid(row=0, column=0, padx=1, pady=10, sticky="w")
        lbl_deck_import.grid(row=1, column=0, padx=1, pady=1, sticky="w")
        lbl_stored_deck.grid(row=2, column=0, padx=1, pady=1, sticky="w")

        self.ent_deck_import.grid(row=1, column=1, padx=1, pady=1, sticky="w")

        self.drp_stored_deck.get_OptionMenu_class().grid(row=2, column=1, padx=1, pady=1, sticky="w")

        self.btn_import.grid(row=1, column=2, padx=20, pady=1)
        self.btn_delete.grid(row=2, column=2, padx=1, pady=1)
        
        ###################################################################################################################################################

        # Calculation section.

        self.frm_calculation = tk.Frame(master=self.frm_top, relief=tk.RIDGE, borderwidth=5)
        self.frm_calculation.grid(row=0, column=1, padx=5, pady=5)

        # Labels.
        lbl_initialize_calculation = tk.Label(master=self.frm_calculation, text="Initialize Calculation", height=1, font=("Helvetica", "11", "bold"))
        lbl_sample_size = tk.Label(master=self.frm_calculation, text="Sample size:", height=1, width=15, anchor="w")

        # Entries.
        self.ent_sample_size = tk.Entry(master=self.frm_calculation, width=12)

        # Buttons.
        self.btn_add_pool = tk.Button(master=self.frm_calculation, text="+ POOL", command=self.controller.on_add_pool)
        self.btn_calculate = tk.Button(master=self.frm_calculation, text="CALCULATE", command=self.controller.on_calculate)

        # Arrange everything.
        lbl_initialize_calculation.grid(row=0, column=0, padx=1, pady=10, sticky="w")
        lbl_sample_size.grid(row=1, column=0, padx=1, pady=4, sticky="w")

        self.ent_sample_size.grid(row=1, column=1, padx=1, pady=4)

        self.btn_add_pool.grid(row=2, column=0, padx=4, pady=4, sticky="w")
        self.btn_calculate.grid(row=2, column=1, padx=10, pady=4, sticky="e")
        
        ###################################################################################################################################################

        # Pool section.
        
        self.pool_list = []     # Store all pools that were created.
        
        ###################################################################################################################################################

        # Let the window run.

        self.mainloop()

    # Update functions.
    def update(self, update_event, index = None, card_name = None):
        '''
        Updates the View class when something happend.
        update_event specifies which part of the display shoul be updated.
        index, card_name are optional and only need for certain update_events.
        '''
    
        if update_event == "add pool":                        # Create a new pool and add it to the pool list

            self.add_pool_display()

        
        elif update_event == "add card to pool":              # Card was added to a pool

            for pool in self.pool_list:                                         # Update list for add (cards that are not in any pool).
               pool.get_drp_add_card().remove_item(card_name)                   # Must be done for every card pool!
            self.pool_list[index].get_drp_del_card().append_item(card_name)     # Update list for delete (cards that are in the pool).
            self.pool_list[index].add_card(card_name)                           # Update the pool display.

        elif update_event == "removed card from pool":        # Remove a card from the pool

            for pool in self.pool_list:                                         # Update list for add (cards that are not in any pool).
                pool.get_drp_add_card().append_item(card_name)                  # Must be done for every card pool!
            self.pool_list[index].get_drp_del_card().remove_item(card_name)     # Update list for delete (cards that are in the pool).
            self.pool_list[index].del_card(card_name)                           # Update the pool display.

        elif update_event == "start calculate":               # The calculation will start, read all data.

            sample_size = self.ent_sample_size.get()                            # Get the correct sample_size
            try:                                                                # The user input is an integer.
                sample_size = int(sample_size)                                  
            except:                                                             # The user entered something else.
                self.ent_sample_size.delete(0, tk.END) 
                self.ent_sample_size.insert(0, 0)
                sample_size = 0                                                 # Write the sample_size to 0.
            self.model.get_deck_manager().set_sample_size(int(sample_size))     # Set the sample_size.
            
            for index in range(len(self.pool_list)):                            # Because the sample_size changed, all slot_sizes of the pools must be updated.
                try:                                                            
                    self.model.get_deck_manager().get_pools()[index].set_slot_size(int(self.pool_list[index].get_min_size()), sample_size)
                except:                                                         # When the user inputs are invalid, set to 0
                    self.model.get_deck_manager().get_pools()[index].set_slot_size(0, sample_size)

        elif update_event == "changed only equal":           # Change the pool type display.
            self.pool_list[index].set_pool_type()

    # Managing pools            
    def add_pool_display(self):
        '''
        Creates a new Pool_Display and adds it to the pool_list.
        '''
        pool_count = len(self.pool_list)
        pool_view = Pool_Section(self)          # Create the Pool_Section.
        self.pool_list.append(pool_view)        # Append it to self.pool_list.
        pool_view.set_index()                   # Update the index of the pool.
        if (pool_count % 2) == 0:               # Place the pool in the frame depending on the length of self.pool_list
            pool_view.get_frame().grid(row=(pool_count // 2), column=0, padx=5, pady=5, sticky="nw")
        else:
            pool_view.get_frame().grid(row=(pool_count // 2), column=1, padx=5, pady=5, sticky="nw")

    # Getter functions.
    def get_model(self):
        return self.model
   
    def get_controller(self):
        return self.controller
    
    def get_pool_list(self):
        return self.pool_list
    
    def get_frm_bottom(self):
        return self.scb_frm_bottom.get_frame()
