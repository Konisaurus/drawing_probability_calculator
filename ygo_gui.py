# Important Note:
#
# this gui has currently no functionality with the other modules whatsoever. You could call it an "empty shell".

import tkinter as tk
from gui_classes import *

##############################################################################################################################

# name convetions:
#
# Label 	                lbl 
# Button 	                btn 
# Entry 	                ent 
# Text 	                    txt 
# Frame 	                frm 
# Changeable_OptionMenu     drp

##############################################################################################################################

# create main window
window = tk.Tk()

window.resizable(False, False)
window.title("YGO Hand Master")

##############################################################################################################################

# create a top, middle and bottom frame 
# top frame:    managing deck, initialize calculation
# middle frame: managing pools
# bottom frame: display calculation results
frm_top = tk.Frame(master=window, borderwidth=5)
frm_middle = tk.Frame(master=window, borderwidth=5)
frm_bottom = tk.Frame(master=window, borderwidth=5)

frm_top.pack()
frm_middle.pack()
frm_bottom.pack()

##############################################################################################################################

# deck selection frame

# add deck selection frame for dealing with decks
frm_deck_selection = tk.Frame(master=frm_top, relief=tk.RIDGE, borderwidth=5)
frm_deck_selection.grid(row=0, column=0, padx=5, pady=5)

# labels
lbl_deck_selection = tk.Label(master=frm_deck_selection, text="Deck Selection", height=1, font=("Helvetica", "9", "bold"))
lbl_deck_import = tk.Label(master=frm_deck_selection, text="Deck path:", height=1, width=15, anchor="w")
lbl_stored_deck = tk.Label(master=frm_deck_selection, text="Stored decks:", height=1, width=15, anchor="w")

# entries
ent_deck_import = tk.Entry(master=frm_deck_selection, width=50)

# create the decklist dropdown menu
drp_stored_deck = Changeable_OptionMenu(frm_deck_selection, "test deck", [], "Select Deck")

# adds a deck to the dropdown menu
def handle_deck_import():
    # will work differently in the end version
    try:
        drp_stored_deck.append_item(ent_deck_import.get())
        ent_deck_import.delete(0, tk.END)
    except:
        pass

# deletes the selected deck from the dropdown menu        
def handle_deck_delete():
    drp_stored_deck.delete_item()
    
# buttons
btn_import = tk.Button(master=frm_deck_selection, text="IMPORT", command=handle_deck_import)
btn_delete = tk.Button(master=frm_deck_selection, text="DELETE", command=handle_deck_delete)

# arrange everything
lbl_deck_selection.grid(row=0, column=0, padx=1, pady=10, sticky="w")
lbl_deck_import.grid(row=1, column=0, padx=1, pady=1, sticky="w")
lbl_stored_deck.grid(row=2, column=0, padx=1, pady=1, sticky="w")

ent_deck_import.grid(row=1, column=1, padx=1, pady=1, sticky="w")

drp_stored_deck.get_OptionMenu_class().grid(row=2, column=1, padx=1, pady=1, sticky="w")

btn_import.grid(row=1, column=2, padx=20, pady=1)
btn_delete.grid(row=2, column=2, padx=1, pady=1)

##############################################################################################################################

# calculation frame

# add calculation frame for initializing calculation
frm_calculation = tk.Frame(master=frm_top, relief=tk.RIDGE, borderwidth=5)
frm_calculation.grid(row=0, column=1, padx=5, pady=5)

# labels
lbl_initialize_calculation = tk.Label(master=frm_calculation, text="Initialize Calculation", height=1, font=("Helvetica", "9", "bold"))
lbl_sample_size = tk.Label(master=frm_calculation, text="Sample size:", height=1, width=15, anchor="w")

# entries
ent_sample_size = tk.Entry(master=frm_calculation, width=5)

# start calculation
def start_calculation():
    # will work differently in the end version
    try:    
        sample_size = int(ent_sample_size.get())
        print(sample_size)
    except:
        pass
    
# add pool
def add_pool():
    pass

# buttons
btn_add_pool = tk.Button(master=frm_calculation, text="+ POOL", command=add_pool)
btn_calculate = tk.Button(master=frm_calculation, text="CALCULATE", command=start_calculation)

# arrange everything
lbl_initialize_calculation.grid(row=0, column=0, padx=1, pady=10, sticky="w")
lbl_sample_size.grid(row=1, column=0, padx=1, pady=4, sticky="w")

ent_sample_size.grid(row=1, column=1, padx=1, pady=4)

btn_add_pool.grid(row=2, column=0, padx=4, pady=4, sticky="w")
btn_calculate.grid(row=2, column=1, padx=10, pady=4, sticky="e")

##############################################################################################################################

# pool management

# only for testing
pool1 = Display_Card_Pool(frm_middle)
pool1.frame.grid(row=1, column=0, padx=5, pady=5, sticky="w")

pool2 = Display_Card_Pool(frm_middle)
pool2.frame.grid(row=1, column=1, padx=5, pady=5, sticky="w")

##############################################################################################################################

# let the window run
window.mainloop()
