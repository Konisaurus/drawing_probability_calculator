import tkinter as tk
from widgets_for_gui import *
from observer_subject import Observer


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
    def __init__(self, master):
        # frame for the card pool display
        self.frame = tk.Frame(master=master, relief=tk.RIDGE, borderwidth=5, width=30)

        # title of the frame
        lbl_title = tk.Label(master=self.frame, text="Card Pool", height=1, font=("Helvetica", "11", "bold"), anchor="nw")
        
        # display all cards in the pool
        self.card_names = []
        self.lbl_card_display = tk.Label(master=self.frame, text=self.update_card_display_text(), width=50, anchor="nw", justify="left")

        # labels
        lbl_add_card = tk.Label(master=self.frame, text="Add card:", anchor="nw")
        lbl_del_card = tk.Label(master=self.frame, text="Delete card:", anchor="nw")
        self.lbl_size = tk.Label(master=self.frame, text="Minimum pool size:", anchor="nw", width=15)

        # dropdownlists
        self.drp_add_card = Changeable_OptionMenu(self.frame, "Select card.", [], 22)
        self.drp_del_card = Changeable_OptionMenu(self.frame, "Select card.", [], 22)

        # buttons
        self.btn_add_card = tk.Button(master=self.frame, text="+ CARD", command=self.on_add_card)
        self.btn_del_card = tk.Button(master=self.frame, text="- CARD", command=self.on_del_card)
        self.btn_change_type = tk.Button(master=self.frame, text="CHANGE", command=self.on_change_type)

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

    def update_card_display_text(self):
        text_list = "Card name \n\n"
        if self.card_names != []:
            for card in self.card_names:
                text_list += card + "\n"
        else:
            text_list += "No cards in pool."
        return text_list



    # must be implemented, but not here!!!!!!!!!!!!!!!!!!!!!



    def on_add_card(self):
        pass

    def on_del_card(self):
        pass

    def on_change_typel(self):
        pass
        
    def get_frame(self):
        return self.frame


class View(tk.Tk, Observer):
    # class that manages all visual aspects of the program
    def __init__(self, model, controller):
        
        # interaction with the model and the controller
        self._model = model
        self._model.attach(self)
        self._controller = controller

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
        self.btn_import = tk.Button(master=self.frm_deck_selection, text="IMPORT", command=self.on_deck_import)
        self.btn_delete = tk.Button(master=self.frm_deck_selection, text="DELETE", command=self.on_deck_delete)

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
        self.btn_add_pool = tk.Button(master=self.frm_calculation, text="+ POOL", command=self.on_add_pool)
        self.btn_calculate = tk.Button(master=self.frm_calculation, text="CALCULATE", command=self.on_calculate)

        # arrange everything
        lbl_initialize_calculation.grid(row=0, column=0, padx=1, pady=10, sticky="w")
        lbl_sample_size.grid(row=1, column=0, padx=1, pady=4, sticky="w")

        self.ent_sample_size.grid(row=1, column=1, padx=1, pady=4)

        self.btn_add_pool.grid(row=2, column=0, padx=4, pady=4, sticky="w")
        self.btn_calculate.grid(row=2, column=1, padx=10, pady=4, sticky="e")
        
        ###################################################################################################################################################

        # let the window run
        self.update()
        self.mainloop()

    # update display after a something happend
    def update(self, update_event):
    # has to be implemented yet
        pass


    
    # must be implemented, but not here!!!!!!!!!!!!!!!!!!!!!

    # adds a deck to the dropdown menu
    def on_deck_import(self):
        pass

    # deletes a deck
    def on_deck_delete(self):
        pass

    # creates a new pool section
    def on_add_pool(self):
        pass

    # deletes the selected deck from the dropdown menu        
    def on_calculate(self):
        pass
