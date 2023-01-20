import tkinter as tk
from widgets_for_gui import *
from observer_subject import Observer
from model_hypgeo import *


# name convetions:
#
# Label 	                lbl 
# Button 	                btn 
# Entry 	                ent 
# Text 	                    txt 
# Frame 	                frm 
# Canvas                    cnv
# Scrollbar                 scb
# Changeable_OptionMenu     drp


class Card_Pool_Section:
    # display a card pool
    def __init__(self, view, index = 0):
        
        # master window
        self.view = view
        self.index = index

        # frame for the card pool display
        self.frame = tk.Frame(master=self.view.get_frm_bottom(), relief=tk.RIDGE, borderwidth=5, width=30)

        # title of the frame
        lbl_title = tk.Label(master=self.frame, text="Card Pool", height=1, font=("Helvetica", "11", "bold"), anchor="nw")
        
        # display all cards in the pool
        self.card_names = []
        self.lbl_card_display = tk.Label(master=self.frame, text="text", width=50, anchor="nw", justify="left")
        self.update_card_display_text()

        # labels
        lbl_add_card = tk.Label(master=self.frame, text="Add card:", anchor="nw")
        lbl_del_card = tk.Label(master=self.frame, text="Delete card:", anchor="nw")
        self.lbl_size = tk.Label(master=self.frame, text="Minimum pool size:", anchor="nw", width=15)

        # dropdownlists
        self.drp_add_card = Changeable_OptionMenu(self.frame, "Select card.", self.view.get_model().get_deck_manager().get_unassigned_cards(), 22)
        self.drp_del_card = Changeable_OptionMenu(self.frame, "Select card.", [], 22)

        # buttons
        self.btn_add_card = tk.Button(master=self.frame, text="+ CARD", command= lambda: self.view.get_controller().on_add_card(self.index, self.drp_add_card.get_variable()))
        self.btn_del_card = tk.Button(master=self.frame, text="- CARD", command= lambda: self.view.get_controller().on_del_card(self.index, self.drp_del_card.get_variable()))
        self.btn_change_type = tk.Button(master=self.frame, text="CHANGE", command= lambda: self.view.get_controller().on_change_type(self.index))

        # entries
        self.ent_min_size = tk.Entry(master=self.frame, width=29)

        # arrange everything
        lbl_title.grid(row=0, column=0, padx=1, pady=10, sticky="w")

        self.lbl_card_display.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nw")

        lbl_add_card.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        lbl_del_card.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.lbl_size.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.drp_add_card.get_OptionMenu_class().grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.drp_del_card.get_OptionMenu_class().grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.btn_add_card.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.btn_del_card.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.btn_change_type.grid(row=4, column=2, padx=5, pady=5, sticky="w")

        self.ent_min_size.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    def set_index(self):
        self.index = self.view.get_pool_list().index(self)

    def change_pool_type(self):
        state = self.lbl_size["text"]
        if state == "Minimum pool size:":
            self.lbl_size.config(text="Exact pool size:")
        else:
            self.lbl_size.config(text="Minimum pool size:")

    def add_card(self, card_name):
        self.card_names.append(card_name)
        self.update_card_display_text()

    def remove_card(self, card_name):
        self.card_names.remove(card_name)
        self.update_card_display_text()

    def update_card_display_text(self):
        text_list = "Card name \n\n"
        if self.card_names != []:
            for card in self.card_names:
                text_list += "- " + card + "\n"
        else:
            text_list += "No cards in pool."

        self.lbl_card_display.config(text=text_list)
    
    def get_frame(self):
        return self.frame
    
    def get_min_size(self):
        return self.ent_min_size.get()

    def get_drp_add_card(self):
        return self.drp_add_card
    
    def get_drp_del_card(self):
        return self.drp_del_card

class View(tk.Tk, Observer):
    # class that manages all visual aspects of the program
    def __init__(self, model, controller):
        
        # interaction with the model and the controller
        self.model = model
        self.model.attach(self)
        self.controller = controller

        self.pool_list = []

        ###################################################################################################################################################
        
        # setup a window
        tk.Tk.__init__(self)
        self.geometry("830x500")
        self.resizable(False, True)
        self.title("YGO Hand Master")

        # create two sections for the window
        self.frm_top = tk.Frame(master=self, borderwidth=5)
        self.frm_top.pack(anchor="nw")

        self.scb_frm_bottom = Scrollable_Frame(master=self)
        self.scb_frm_bottom.pack()
        
        ###################################################################################################################################################

        # deck controll section
        
        self.frm_deck_selection = tk.Frame(master=self.frm_top, relief=tk.RIDGE, borderwidth=5)
        self.frm_deck_selection.grid(row=0, column=0, padx=5, pady=5)
        
        # labels
        lbl_deck_selection = tk.Label(master=self.frm_deck_selection, text="Deck Selection", height=1, font=("Helvetica", "11", "bold"))
        lbl_deck_import = tk.Label(master=self.frm_deck_selection, text="Deck path:", height=1, width=15, anchor="w")
        lbl_stored_deck = tk.Label(master=self.frm_deck_selection, text="Stored decks:", height=1, width=15, anchor="w")

        # entries
        self.ent_deck_import = tk.Entry(master=self.frm_deck_selection, width=50)

        # decklist dropdown menu
        self.drp_stored_deck = Changeable_OptionMenu(self.frm_deck_selection, "Select deck.", [], 42)

        # buttons
        self.btn_import = tk.Button(master=self.frm_deck_selection, text="IMPORT", command=self.controller.on_deck_import)
        self.btn_delete = tk.Button(master=self.frm_deck_selection, text="DELETE", command=self.controller.on_deck_delete)

        # arrange everything
        lbl_deck_selection.grid(row=0, column=0, padx=1, pady=10, sticky="w")
        lbl_deck_import.grid(row=1, column=0, padx=1, pady=1, sticky="w")
        lbl_stored_deck.grid(row=2, column=0, padx=1, pady=1, sticky="w")

        self.ent_deck_import.grid(row=1, column=1, padx=1, pady=1, sticky="w")

        self.drp_stored_deck.get_OptionMenu_class().grid(row=2, column=1, padx=1, pady=1, sticky="w")

        self.btn_import.grid(row=1, column=2, padx=20, pady=1)
        self.btn_delete.grid(row=2, column=2, padx=1, pady=1)
        
        ###################################################################################################################################################

        # calculation section
        self.frm_calculation = tk.Frame(master=self.frm_top, relief=tk.RIDGE, borderwidth=5)
        self.frm_calculation.grid(row=0, column=1, padx=5, pady=5)

        # labels
        lbl_initialize_calculation = tk.Label(master=self.frm_calculation, text="Initialize Calculation", height=1, font=("Helvetica", "11", "bold"))
        lbl_sample_size = tk.Label(master=self.frm_calculation, text="Sample size:", height=1, width=15, anchor="w")

        # entries
        self.ent_sample_size = tk.Entry(master=self.frm_calculation, width=12)

        # buttons
        self.btn_add_pool = tk.Button(master=self.frm_calculation, text="+ POOL", command=self.controller.on_add_pool)
        self.btn_calculate = tk.Button(master=self.frm_calculation, text="CALCULATE", command=self.controller.on_calculate)

        # arrange everything
        lbl_initialize_calculation.grid(row=0, column=0, padx=1, pady=10, sticky="w")
        lbl_sample_size.grid(row=1, column=0, padx=1, pady=4, sticky="w")

        self.ent_sample_size.grid(row=1, column=1, padx=1, pady=4)

        self.btn_add_pool.grid(row=2, column=0, padx=4, pady=4, sticky="w")
        self.btn_calculate.grid(row=2, column=1, padx=10, pady=4, sticky="e")
        
        ###################################################################################################################################################

        # let the window run
        self.mainloop()

    def update(self, update_event, index = None, card_name = None):
    # update display after a something happend
        # create a new pool and add it to the pool list
        if update_event == "add pool":
            self.update_pool_list()

        # card was added to a pool
        elif update_event == "add card to pool":
            # update list for add (cards that are not in any pool)
            # must be done in every card pool!
            for pool in self.pool_list: 
               pool.get_drp_add_card().delete_item(card_name)
            # update list for delete (cards that are in the pool)
            self.pool_list[index].get_drp_del_card().append_item(card_name)
            # update pool display
            self.pool_list[index].add_card(card_name)

        # remove a card from the pool
        elif update_event == "removed card from pool":
            # update list for add (cards that are not in any pool)
            # must be done in every card pool!
            for pool in self.pool_list:
                pool.get_drp_add_card().append_item(card_name)
            # update list for delete (cards that are in the pool)
            self.pool_list[index].get_drp_del_card().delete_item(card_name)
            # update pool display
            self.pool_list[index].remove_card(card_name)

        # start the calculation
        elif update_event == "start calculate":
            # set the correct sample size
            sample_size = self.ent_sample_size.get()
            try:
                sample_size = int(sample_size)
            except:
                self.ent_sample_size.delete(0, tk.END) 
                self.ent_sample_size.insert(0, 0)
                sample_size = 0
            self.model.get_deck_manager().set_sample_size(int(sample_size))
            
            # set the correct slot size of every pool
            for index in range(len(self.pool_list)):
                try:
                    self.model.get_deck_manager().get_card_pools()[index].set_slot_size(int(self.pool_list[index].get_min_size()), sample_size)
                except:
                    self.model.get_deck_manager().get_card_pools()[index].set_slot_size(0, sample_size)

        # change only equal of a pool
        elif update_event == "changed only equal":
            self.pool_list[index].change_pool_type()
            

            
    def update_pool_list(self):
        pool_count = len(self.pool_list)
        pool_view = Card_Pool_Section(self)
        self.pool_list.append(pool_view)
        pool_view.set_index()
        if (pool_count % 2) == 0:
            pool_view.get_frame().grid(row=(pool_count // 2), column=0, padx=5, pady=5, sticky="nw")
        else:
            pool_view.get_frame().grid(row=(pool_count // 2), column=1, padx=5, pady=5, sticky="nw")

    # getter functions
    def get_model(self):
        return self.model
   
    def get_controller(self):
        return self.controller
    
    def get_pool_list(self):
        return self.pool_list
    
    def get_frm_bottom(self):
        return self.scb_frm_bottom.get_frame()
