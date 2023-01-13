import tkinter as tk
from gui_classes import *

# create main window
window = tk.Tk()
window.resizable(False, False)
window.title("YGO Hand Master")

# add top frame for handling decks
frm_top = tk.Frame(relief=tk.RIDGE, borderwidth=5)
frm_top.grid(row=0, column=0, padx=5, pady=5)

# labels for the top frame
lbl_top = tk.Label(master=frm_top, text="Deck Selection", height=1)
lbl_deck_import = tk.Label(master=frm_top, text="Deck path:", height=1)
lbl_stored_deck = tk.Label(master=frm_top, text="Stored decks:", height=1)

# entry for the top frame
ent_deck_import = tk.Entry(master=frm_top)

# create the decklist dropdown menu
drp_stored_deck = Changeable_OptionMenu(frm_top, "test deck", [], "Select Deck")

# adds a deck to the dropdown menu
def handle_deck_import():
    drp_stored_deck.append_item(ent_deck_import.get())
    ent_deck_import.delete(0, tk.END)

# deletes the selected deck from the dropdown menu        
def handle_deck_delete():
    drp_stored_deck.delete_item()
    
# buttons for the top frame
btn_import = tk.Button(master=frm_top, text="IMPORT", command=handle_deck_import)
btn_delete = tk.Button(master=frm_top, text="DELETE", command=handle_deck_delete)


# place everything in the top frame
lbl_top.grid(row=0, column=0, padx=1, pady=5, sticky="w")
lbl_deck_import.grid(row=1, column=0, padx=1, pady=1, sticky="w")
lbl_stored_deck.grid(row=2, column=0, padx=1, pady=1, sticky="w")

ent_deck_import.grid(row=1, column=1, padx=1, pady=1, sticky="w")

btn_import.grid(row=1, column=2, padx=20, pady=1)
btn_delete.grid(row=2, column=2, padx=1, pady=1)

drp_stored_deck.get_OptionMenu_class().grid(row=2, column=1, padx=1, pady=1, sticky="w")

# let the window run
window.mainloop()


















#frm_middle = tk.Frame(relief=tk.RIDGE, borderwidth=5)
#frm_bottom = tk.Frame(relief=tk.RIDGE, borderwidth=5)

#frm_middle.grid(row=1, column=0, padx=5, pady=5)
#frm_bottom.grid(row=2, column=0, padx=5, pady=5)

#lbl_middle = tk.Label(master=frm_middle, text=f"Slots", height=1)
#lbl_bottom = tk.Label(master=frm_bottom, text=f"Calculations",height=1)

#lbl_middle.pack(padx=5, pady=5)
#lbl_bottom.pack(padx=5, pady=5)