import tkinter as tk


class Changeable_OptionMenu():
    # an tk.OptionMenu that has a list which can be changed
    def __init__(self, master, unremovable_option, option_list, dropdown_title):
        self.master = master
        self.unremovable_option = unremovable_option
        self.options = [self.unremovable_option]
        self.options.extend(option_list)

        self.variable = tk.StringVar(self.master)
        self.variable.set(dropdown_title)
        self.dropdown = tk.OptionMenu(self.master, self.variable, *self.options)

    def update_options(self):
        # after a change to the options list, the tk.OptionMenu must be updated
        self.dropdown["menu"].delete(0, "end")
        for item in self.options:
            self.dropdown["menu"].add_command(label=item, command=lambda value=item: self.variable.set(value))

    def append_item(self, item):
        # append an item to the option list
        self.options.append(str(item))
        self.update_options()

    def delete_item(self):
        # deletes the selected item from the option list
        item = self.variable.get()
        if item in self.options and not item == self.unremovable_option:
            self.options.remove(item)
            self.update_options()
            self.variable.set(self.unremovable_option)

    def get_OptionMenu_class(self):
        # get the OptionMenu, which is the core of this class
        return self.dropdown


class Display_Card_Pool():
    # display a card pool
    # not fully funtional
    def __init__(self, master):
        # frame for the card pool display
        self.frame = tk.Frame(master=master, relief=tk.RIDGE, borderwidth=5, width=30)

        # title of the frame
        lbl_title = tk.Label(master=self.frame, text="Card Pool", height=1, font=("Helvetica", "11", "bold"), anchor="nw")
        
        # display all cards in the pool
        self.card_names = ["card 1", "card 2", "card 3"]
        self.lbl_card_display = tk.Label(master=self.frame, text=self.create_card_display_text(), width=50, anchor="nw", justify="left")

        # labels
        lbl_add_card = tk.Label(master=self.frame, text="Add card:", anchor="nw")
        lbl_del_card = tk.Label(master=self.frame, text="Delete card:", anchor="nw")
        lbl_min_size = tk.Label(master=self.frame, text="Minimum Pool Size:", anchor="nw")

        # dropdownlists
        self.drp_add_card = Changeable_OptionMenu(self.frame, "Select card.", self.card_names, "Select card.")
        self.drp_del_card = Changeable_OptionMenu(self.frame, "Select card.", self.card_names, "Select card.")

        # buttons
        self.btn_add_card = tk.Button(master=self.frame, text="+ CARD", command=self.handle_btn_add)
        self.btn_del_card = tk.Button(master=self.frame, text="- CARD", command=self.handle_btn_del)

        # entries
        self.ent_min_size = tk.Entry(master=self.frame, width=17)

        # arrange everything
        lbl_title.grid(row=0, column=0, padx=1, pady=10, sticky="w")

        self.lbl_card_display.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nw")

        lbl_add_card.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        lbl_del_card.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        lbl_min_size.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.drp_add_card.get_OptionMenu_class().grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.drp_del_card.get_OptionMenu_class().grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.btn_add_card.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.btn_del_card.grid(row=3, column=2, padx=5, pady=5, sticky="w")

        self.ent_min_size.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    def create_card_display_text(self):
        text_list = "Card name \n\n"
        if self.card_names != []:
            for card in self.card_names:
                text_list += card + "\n"
        return text_list

    def add_card(self, card):
        self.card_names.append(card)
        self.lbl_card_display.config(text=self.create_card_display_text())

    def handle_btn_add(self):
        pass

    def handle_btn_del(self):
        pass
    def get_frame(self):
        return self.frame


