'''
This module contains the View class which contains all the visual aspects of the system.
'''

# Imports.
import tkinter as tk
import json
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
        self.frame = tk.Frame(master=self.view.get_frm_bottom(), relief=tk.RIDGE, borderwidth=5)

        # Display all cards in the pool.
        self.card_names = {}
        self.del_buttons = {}
        self.frm_card_display = tk.Frame(master=self.frame, relief=tk.FLAT, borderwidth=0)
        lbl_title_display = tk.Label(master=self.frm_card_display, text="Cards in pool:", font=("Helvetica", "9", "bold"), anchor="nw", justify="left")
        self.set_pool_display()

        # Labels.
        self.lbl_title = tk.Label(master=self.frame, text=("Card Pool " + str(self.index + 1)), height=1, width=42, font=("Helvetica", "11", "bold"), anchor="nw")
        lbl_place_holder = tk.Label(master=self.frame, text=" ")
        lbl_in_sample = tk.Label(master=self.frame, text="Cards from pool in successfull sample:", anchor="nw", width=29)
        lbl_min = tk.Label(master=self.frame, text="min.", anchor="nw", width=3)
        lbl_bewtween = tk.Label(master=self.frame, text="-", anchor="nw")
        lbl_max = tk.Label(master=self.frame, text="max.", anchor="nw", width=4)

        # Dropdownlists.
        self.drp_add_card = Changeable_OptionMenu(self.frame, "Select card to add.", self.view.get_model().get_deck_manager().get_unassigned_cards(), 40)

        # Buttons.
        self.btn_add_card = tk.Button(master=self.frame, text="+ CARD", width=10, command=lambda: self.view.get_controller().on_add_card(self.index, self.drp_add_card.get_variable_value()))
        self.btn_del_pool = tk.Button(master=self.frame, text="x", width=2, font=("Helvetica", "9", "bold"), command=lambda: self.view.get_controller().on_del_pool(self.index))

        # Entries.
        self.ent_min_in_sample = tk.Entry(master=self.frame, width=3, validate="key", justify="right")
        self.ent_min_in_sample.configure(validatecommand=(self.ent_min_in_sample.register(self.view.validate),'%d', '%P'))
        self.ent_max_in_sample = tk.Entry(master=self.frame, width=3, validate="key", justify="right")
        self.ent_max_in_sample.configure(validatecommand=(self.ent_min_in_sample.register(self.view.validate),'%d', '%P'))

        # Arrange everything.
        self.frm_card_display.grid(row=1, column=0, columnspan=6, padx=0, pady=0, sticky="nw")
        lbl_title_display.grid(row=0, column=0, columnspan=6, padx=4, pady=4, sticky="nw")

        self.lbl_title.grid(row=0, column=0, columnspan=6, padx=4, pady=10, sticky="w")
        lbl_place_holder.grid(row=2, column=0, columnspan=6)
        lbl_in_sample.grid(row=4, column=0, padx=4, pady=4, sticky="w")
        lbl_min.grid(row=4, column=1, pady=4, sticky="w")
        lbl_bewtween.grid(row=4, column=3, pady=4, sticky="e")
        lbl_max.grid(row=4, column=4, pady=4, sticky="e")

        self.drp_add_card.get_OptionMenu_class().grid(row=3, column=0, columnspan=3, padx=4, pady=4, sticky="w")

        self.btn_add_card.grid(row=3, column=3, columnspan=3, padx=4, pady=4)
        self.btn_del_pool.grid(row=0, column=5, pady=4, sticky="w")

        self.ent_min_in_sample.grid(row=4, column=2, pady=4, sticky="w")
        self.ent_max_in_sample.grid(row=4, column=5, pady=4, sticky="w")
        
    # Setter functions.
    def set_index(self):
        '''
        Sets the index. Can only be used when the "Pool_Section" is appended to a list.
        '''
        self.index = self.view.get_pool_list().index(self)
        title = "Card Pool " + str(self.index + 1)
        self.lbl_title.config(text=title)

    def set_pool_display(self):
        '''
        Sets the card display of the "Pool Section".
        '''
        self.frm_card_display.grid_forget()
        row = 1
        for key in self.card_names:
            self.card_names[key].grid(row=row, column=1, padx=4, pady=4, sticky="w")
            self.del_buttons[key].grid(row=row, column=0, padx=4, pady=4, sticky="w")
            row += 1
        self.frm_card_display.grid(row=1, column=0, columnspan=7, padx=0, pady=0, sticky="nw")

    def set_min_in_sample(self, min_in_sample):
        '''
        Inserts min_in_sample into self.ent_min_in_sample.
        '''
        self.ent_min_in_sample.delete(0, tk.END) 
        self.ent_min_in_sample.insert(0, min_in_sample)

    def set_max_in_sample(self, max_in_sample):
        '''
        Inserts max_in_sample into self.ent_max_in_sample.
        '''
        self.ent_max_in_sample.delete(0, tk.END) 
        self.ent_max_in_sample.insert(0, max_in_sample)
        
    # Managing cards.
    def add_card(self, card_count, card_name):
        '''
        Assigns a card to this pool display.
        '''
        self.card_names[card_name] = tk.Label(master=self.frm_card_display, text=str(card_count) + "x " + card_name, width=44, anchor="nw", justify="left")
        self.del_buttons[card_name] = tk.Button(master=self.frm_card_display, text="x", width=2, font=("Helvetica", "9", "bold"), command=lambda: self.view.get_controller().on_del_card(self.index, card_name))
        self.set_pool_display()                    # Update the card display.

    def del_card(self, card_name):
        '''
        Unassigns a card from this pool display.
        '''
        self.card_names[card_name].destroy()       # Destroy its display.
        self.card_names.pop(card_name)             # Remove it in the card_name dictionary.
        self.del_buttons[card_name].destroy()      # Destroy its remove button.
        self.del_buttons.pop(card_name)            # Remove the button from the dictionary.
        self.set_pool_display()                    # Reajust the card display.

    # Getter functions.
    def get_index(self):
        return self.index
    
    def get_frame(self):
        return self.frame
    
    def get_min_in_sample(self):
        return self.ent_min_in_sample.get()
    
    def get_max_in_sample(self):
        return self.ent_max_in_sample.get()

    def get_drp_add_card(self):
        return self.drp_add_card
    

class Deck_Info(tk.Toplevel):
    '''
    Class that shows general information about the deck.
    '''
    def __init__(self, view, info):

        tk.Toplevel.__init__(self)
        self.view = view
        self.set_position()
        self.frm_scb = Scrollable_Frame(self)
        self.frm_design = tk.Frame(master=self.frm_scb.get_frm_container(), relief=tk.RIDGE, borderwidth=5)
        self.info = info

        # Labels.
        self.lbl_title = tk.Label(master=self.frm_design, text="Deck Info", height=1, width=38, font=("Helvetica", "11", "bold"), anchor="w")
        self.lbl_deck = tk.Label(master=self.frm_design, text=" ", width=38, anchor="w", justify="left")
        self.set_lbl_deck()

        # Arrange everything.
        self.frm_scb.pack()
        self.frm_design.pack()
        self.lbl_title.grid(row=0, column=0,padx=4, pady=4)
        self.lbl_deck.grid(row=1, column=0, padx=4, pady=4, sticky="w")

        # Run the window.
        self.protocol("WM_DELETE_WINDOW", lambda : self.view.get_btn_deck_info().configure(state='normal') or self.destroy())   # Enable button when closed.
        self.mainloop()

    def set_position(self):
        self.geometry("405x500")
        self.resizable(False, True)                                     # Lock size.
        position_y = self.view.winfo_y()                                # Window y coordinate.
        position_x = self.view.winfo_x() + self.view.winfo_width() + 20 # Window x coordinate
        if position_x + 405>= self.winfo_screenwidth():  # Check if the window is outside of the screen.
            position_x = self.view.winfo_x()

        self.geometry("+%d+%d" %(position_x, position_y))               # Place window.
    
    def set_lbl_deck(self):
        deck = self.info[0]
        text = "\n"
        for key in deck.keys():
            text += str(deck[key]) + "x " + key + "\n"
        self.lbl_deck.config(text = text)


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
        self.geometry("860x500")
        self.resizable(False, True)
        self.title("Drawing Probability Master")

        # Create two sections for the window and pack them.
        self.frm_top = tk.Frame(master=self, borderwidth=5)
        self.frm_top.pack(anchor="nw")

        self.scb_frm_bottom = Scrollable_Frame(master=self)
        self.scb_frm_bottom.pack()
        
        ###################################################################################################################################################

        # Deck controll section.
        
        self.frm_deck_selection = tk.Frame(master=self.frm_top, relief=tk.RIDGE, borderwidth=5)
        self.frm_deck_selection.grid(row=0, column=0, padx=4, pady=4)
        
        # Labels.
        lbl_deck_selection = tk.Label(master=self.frm_deck_selection, text="Deck Selection", height=1, width=57, font=("Helvetica", "11", "bold"), anchor="w")
        lbl_deck_import = tk.Label(master=self.frm_deck_selection, text="Deck path:", height=1, width=10, anchor="w")
        lbl_stored_deck = tk.Label(master=self.frm_deck_selection, text="Stored decks:", height=1, width=10, anchor="w")

        # Entries.
        self.ent_deck_import = tk.Entry(master=self.frm_deck_selection, width=55)

        # Dropdownlists.
        try:                                                            # Get all deck keys for displaying the decks in the selection.
            with open("deck_storage.json", "r") as read_storage:
                deck_keys = list(json.load(read_storage).keys())
        except:                                                         # When the storage is empty, set an empty list.
            deck_keys = []
        self.drp_stored_decks = Changeable_OptionMenu(self.frm_deck_selection, "Select deck.",  deck_keys, 48)
        self.drp_stored_decks.get_variable().trace("w", self.deck_changed_callback)        # Set callback function.

        # Buttons.
        self.btn_import = tk.Button(master=self.frm_deck_selection, text="IMPORT", width=10, command=self.on_deck_import)
        self.btn_delete = tk.Button(master=self.frm_deck_selection, text="DELETE", width=10, command=self.on_deck_delete)

        # Arrange everything.
        lbl_deck_selection.grid(row=0, column=0, columnspan=3, padx=4, pady=10, sticky="w")
        lbl_deck_import.grid(row=1, column=0, padx=4, pady=4, sticky="w")
        lbl_stored_deck.grid(row=2, column=0, padx=4, pady=4, sticky="w")

        self.ent_deck_import.grid(row=1, column=1, padx=4, pady=4, sticky="w")

        self.drp_stored_decks.get_OptionMenu_class().grid(row=2, column=1, padx=4, pady=4, sticky="w")

        self.btn_import.grid(row=1, column=2, padx=4, pady=4)
        self.btn_delete.grid(row=2, column=2, padx=1, pady=4)
        
        ###################################################################################################################################################

        # Initialize calculation section.

        self.frm_calculation = tk.Frame(master=self.frm_top, relief=tk.RIDGE, borderwidth=5)
        self.frm_calculation.grid(row=0, column=1, padx=4, pady=4)

        # Labels.
        lbl_initialize_calculation = tk.Label(master=self.frm_calculation, text="Initialize Calculation", width=26, height=1, anchor="w", font=("Helvetica", "11", "bold"))
        lbl_sample_size = tk.Label(master=self.frm_calculation, text="Sample size:", height=1, width=10, anchor="w")

        # Entries.
        self.ent_sample_size = tk.Entry(master=self.frm_calculation, width=3, validate="key", justify="right")
        self.ent_sample_size.configure(validatecommand=(self.ent_sample_size.register(self.validate),'%d', '%P'))

        # Buttons.
        self.btn_calculate = tk.Button(master=self.frm_calculation, text="CALCULATE", width=10, command=self.controller.on_calculate)
        self.btn_add_pool = tk.Button(master=self.frm_calculation, text="+ POOL", width=10, command=self.controller.on_add_pool)
        self.btn_deck_info = tk.Button(master=self.frm_calculation, text="DECK INFO", width=10, command=self.controller.on_deck_info)
        self.btn_clear = tk.Button(master=self.frm_calculation, text="CLEAR", width=10, command=self.on_clear)

        # Arrange everything.
        lbl_initialize_calculation.grid(row=0, column=0, columnspan = 3, padx=4, pady=10, sticky="w")
        lbl_sample_size.grid(row=2, column=0, padx=4, pady=4, sticky="w")

        self.ent_sample_size.grid(row=2, column=1, padx=4, pady=4)

        self.btn_calculate.grid(row=2, column=2, padx=4, pady=5, sticky="e")
        self.btn_add_pool.grid(row=1, column=0, padx=4, pady=5, sticky="w")
        self.btn_deck_info.grid(row=1, column=1, padx=4, pady=5, sticky="w")
        self.btn_clear.grid(row=1, column=2, padx=4, pady=5, sticky="w")
        
        
        
        ###################################################################################################################################################

        # Storing other displayes inside of View.
        
        self.pool_list = []                 # Store all pools that were created.
        self.deck_info_toplevel = None      # Store the deck_info window.
        
        ###################################################################################################################################################

        # Let the window run.

        self.eval('tk::PlaceWindow . center')
        self.mainloop()
        
    # Update functions.
    def update(self, update_event, **kwargs):
        '''
        Updates the View class when something happend.
        update_event specifies which part of the display shoul be updated.
        index, card_name are optional and only need for certain update_events.
        '''

        if update_event == "add pool":                        # Create a new pool and add it to the pool list.

            self.add_pool_display()

        elif update_event == "del pool":                      # Deletes the last pool in the pool list.
            index = kwargs["index"]

            if self.pool_list != []:
                self.pool_list[index].get_frame().destroy()                                # Deletes the display of the card pool.
                self.pool_list.pop(index)                                                  # Deletes the card pool entirely.

                unassigned_cards = self.model.get_deck_manager().get_unassigned_cards()    # Correct existing pools.
                for pool in self.pool_list:                      
                    pool.set_index()
                    pool.get_frame().grid_forget()
                    pool.get_drp_add_card().set_options(unassigned_cards)

                for pool in self.pool_list:
                    index = pool.get_index()
                    if (index % 2) == 0:                   # Place the pool in the frame depending on the length of self.pool_list.
                        pool.get_frame().grid(row=(index // 2), column=0, padx=5, pady=5, sticky="nw")
                    else:
                        pool.get_frame().grid(row=(index // 2), column=1, padx=5, pady=5, sticky="nw")

        elif update_event == "add card to pool":           # Card was added to a pool.
            index = kwargs["index"]
            card_count = kwargs["card_count"]
            card_name = kwargs["card_name"]

            for pool in self.pool_list:                                         # Update list for add (cards that are not in any pool).
               pool.get_drp_add_card().set_options(self.model.get_deck_manager().get_unassigned_cards())
            self.pool_list[index].add_card(card_count, card_name)               # Update the pool display.

        elif update_event == "removed card from pool":     # Remove a card from the pool.
            index = kwargs["index"]
            card_name = kwargs["card_name"]

            for pool in self.pool_list:                                         # Update list for add (cards that are not in any pool).
                pool.get_drp_add_card().set_options(self.model.get_deck_manager().get_unassigned_cards())                  
            self.pool_list[index].del_card(card_name)                           # Update the pool display.

        elif update_event == "start calculate":            # The calculation will start, read all data.
            sample_size = self.ent_sample_size.get()                            # Get the correct sample_size.
            deck_size= self.model.get_deck_manager().get_deck_size()            # Get the correct deck_size for checking if sample_size is valid.

            if sample_size == '':                                               # If the user did not enter anything, set to 0.
                self.ent_sample_size.delete(0, tk.END) 
                self.ent_sample_size.insert(0, 0)
                sample_size = 0

            elif int(sample_size) > deck_size:                                  # If the user input sample_size is to big, change it to the deck_size.
                self.ent_sample_size.delete(0, tk.END) 
                self.ent_sample_size.insert(0, deck_size)
                sample_size = deck_size 

            self.model.get_deck_manager().set_sample_size(int(sample_size))     # Set the sample_size in the model.
            
            for index in range(len(self.pool_list)):                            # Because the sample_size changed, all slot_sizes of the pools must be updated.
                min_in_sample = self.pool_list[index].get_min_in_sample()    

                if min_in_sample == '':                                         # If the user did not enter anything, set to 0.
                    self.pool_list[index].set_min_in_sample(0)
                    min_in_sample = 0

                elif int(min_in_sample) > int(sample_size):                          # If the user input too big, change it to the sample_size.
                    self.pool_list[index].set_min_in_sample(int(sample_size))
                    min_in_sample = sample_size

                max_in_sample = self.pool_list[index].get_max_in_sample()

                if max_in_sample == '' or int(max_in_sample) > int(sample_size):# If the user did not enter anything or too big, set to sample_size.
                    self.pool_list[index].set_max_in_sample(sample_size)
                    max_in_sample = sample_size

                elif int(max_in_sample) < int(min_in_sample):                   # If max_in_sample is smaller than min_in_sample, set max_in_sample to min_in_sample.
                    self.pool_list[index].set_max_in_sample(min_in_sample)
                    max_in_sample = min_in_sample

                self.model.get_deck_manager().get_pools()[index].set_in_sample(int(sample_size), int(min_in_sample), int(max_in_sample))

        elif update_event == "end calculte":               # Share the result with the user.

            popup_result = tk.Toplevel()                                        # Create a popup window.
            popup_result.geometry("390x70")                                     # Set size.
            popup_result.resizable(False, False)                                # Lock size.
            x = self.winfo_x()
            y = self.winfo_y()
            popup_result.geometry("+%d+%d" %(x+225,y+200))                      # Center the popup in front of the main window.
            popup_result.grab_set()                                             # "Freezes" the main window until the popup is closed.

            # Labels
            lbl_result_text = tk.Label(master=popup_result, text="The probability p of drawing this configuration is:", height=1, font=("Helvetica", "11"), anchor="nw")
            result = "p = " + str(self.model.get_result())
            lbl_result = tk.Label(master=popup_result, text=result, height=1, font=("Helvetica", "11", "bold"), anchor="nw")
            
            # Arrange everything
            lbl_result_text.pack(padx=5, pady=5)
            lbl_result.pack(padx=5, pady=5)

            popup_result.mainloop()

        elif update_event == "show deck info":             # Open a new window that shows the relevant information of the deck.
            info = kwargs["deck_info"]
            
            self.btn_deck_info.configure(state='disabled') # Disable the button, so only one deck_info window can be oppend.
            self.deck_info_toplevel = Deck_Info(self, info)

    # Managing pools.
    def add_pool_display(self):
        '''
        Creates a new Pool_Display and adds it to the pool_list.
        '''
        pool_count = len(self.pool_list)
        pool_view = Pool_Section(self)          # Create the Pool_Section.
        self.pool_list.append(pool_view)        # Append it to self.pool_list.
        pool_view.set_index()                   # Update the index of the pool.
        if (pool_count % 2) == 0:               # Place the pool in the frame depending on the length of self.pool_list.
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
        return self.scb_frm_bottom.get_frm_container()
    
    def get_btn_deck_info(self):
        return self.btn_deck_info

    # Other functions.
    def on_clear(self):
        '''
        Special event handler that is partially defined outside of the Controller.
        Closes the window.
        '''
        self.destroy()                          # Close this window.
        self.controller.on_clear()              # Open the on_clear() function of the controller.

    def on_deck_import(self):
        '''
        Special event handler that is partially defined outside of the Controller.
        Depending on the actions of the deck controller, append a new deck name 
        (which is the key of the deck in deck_storage.json) to the deck dropdown.
        '''
        check = self.controller.on_deck_import(self.ent_deck_import.get())      # Give the value of the entry to the controller.
        if check[0] == True:                                                    # Controller added a new deck, so add to the display.
                self.drp_stored_decks.append_item(check[1])                     # check[1] is the key for the newly added deck.

        elif check == "file not valid":
            self.error_popup("ERROR: file is not a valid deck.")

        elif check == "file not found":
            self.error_popup("ERROR: file not found.")

    def on_deck_delete(self):
        '''
        Special event handler that is partially defined outside of the Controller.
        Depending on the actions of the deck controller, delete a deck name 
        (which is the key of the deck in deck_storage.json) from the deck dropdown.
        '''
        key = self.drp_stored_decks.get_variable_value()
        check = self.controller.on_deck_delete(key)

        if check == True:
            self.drp_stored_decks.remove_item(key)

    def validate(self, type_of_action, entry_value):
        '''
        Validate function that only allows integers as inserts in entries.
        '''
        if type_of_action == '1':           # '1' is insert
            if not entry_value.isdigit():
                return False
            else:
                return True
        else:
            return True

    def deck_changed_callback(self, *args):
        '''
        Callback function which sets the deck whenever the stored deck dropdown menu is changed.
        '''
        key = self.drp_stored_decks.get_variable_value()
        if key == "Select deck.":
            self.on_clear()
        else:
            for index in range(len(self.pool_list)-1, -1, -1):  # Remove all displays from the old deck.
                self.controller.on_del_pool(index)
            self.controller.on_set_deck_manager(key)            # Set new deck.

    def deck_info_closed_callback(self):
        '''
        Enables "DECK INFO" button
        '''
        self.btn_deck_info.configure(state='normal')

    def error_popup(self, text):
            popup_error = tk.Toplevel()                                         # Create a popup window.
            popup_error.geometry("390x50")                                      # Set size.
            popup_error.resizable(False, False)                                 # Lock size.
            x = self.winfo_x()
            y = self.winfo_y()
            popup_error.geometry("+%d+%d" %(x+225,y+200))                       # Center the popup in front of the main window.
            popup_error.grab_set()                                              # "Freezes" the main window until the popup is closed.

            # Label.
            lbl_error = tk.Label(master=popup_error, text=text, height=1, font=("Helvetica", "11", "bold"), anchor="center")

            # Arrange everything.
            lbl_error.pack(padx=15, pady=15)

            popup_error.mainloop()
