import tkinter as tk


class Changeable_OptionMenu():
    # an tk.OptionMenu that has a list which can be changed
    def __init__(self, master, dropdown_title, option_list, width):
        self.master = master
        self.unremovable_option = dropdown_title
        self.options = [self.unremovable_option]
        self.options.extend(option_list)

        self.variable = tk.StringVar(self.master)
        self.variable.set(dropdown_title)
        self.dropdown = tk.OptionMenu(self.master, self.variable, *self.options)
        self.dropdown.config(width=width)

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


class Scrollable_Frame():
    def __init__(self, master):
        # create a frame that wraps everything up
        self.frm_wrapper = tk.Frame(master=master, borderwidth=5)

        # create a canvas which will be scrollable
        self.cnv_scrollbar = tk.Canvas(master=self.frm_wrapper)
        self.cnv_scrollbar.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)

        # add a scrollbar to the canvas
        self.scb_yaxis = tk.Scrollbar(master=self.frm_wrapper, orient="vertical", command=self.cnv_scrollbar.yview)
        self.scb_yaxis.pack(side="right",fill="y")

        # configure the canvas
        self.cnv_scrollbar.configure(yscrollcommand=self.scb_yaxis.set)
        self.cnv_scrollbar.bind("<Configure>", lambda e: self.cnv_scrollbar.config(scrollregion= self.cnv_scrollbar.bbox(tk.ALL))) 

        # create another frame inside the canvas which will contain all widgets and add it to the canvas
        self.frm_container = tk.Frame(master=self.cnv_scrollbar)
        self.cnv_scrollbar.create_window((0,0), window=self.frm_container, anchor="nw")  

        # bind the scrollwheel to the scrollbar
        self.frm_container.bind("<Enter>", self._bound_to_mousewheel)
        self.frm_container.bind("<Leave>", self._unbound_to_mousewheel)
        self.frm_container.bind("<Configure>", self._adjust_scrollregion)

    # pack this widget
    def pack(self):
        self.frm_wrapper.pack(fill="both",expand=1, anchor="nw")

    # access/add all widgets via this getter function
    def get_frame(self):
        return self.frm_container
        
    # methods needed for the mousewheel to work with the scrollbar when over the area
    def _bound_to_mousewheel(self, event):
        self.cnv_scrollbar.bind_all("<MouseWheel>", self._handle_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.cnv_scrollbar.unbind_all("<MouseWheel>")

    def _handle_mousewheel(self, event):
        self.cnv_scrollbar.yview_scroll(int(-1*(event.delta/120)), "units")

    # when the frame gets bigger, the scollbarregion must be adjusted
    def _adjust_scrollregion(self, event):
        self.cnv_scrollbar.configure(scrollregion=self.cnv_scrollbar.bbox("all"))



class Display_Card_Pool():
    # display a card pool
    # not fully funtional
    def __init__(self, master):
        # frame for the card pool display
        self.frame = tk.Frame(master=master, relief=tk.RIDGE, borderwidth=5, width=30)

        # title of the frame
        lbl_title = tk.Label(master=self.frame, text="Card Pool", height=1, font=("Helvetica", "11", "bold"), anchor="nw")
        
        # display all cards in the pool
        self.card_names = []
        self.lbl_card_display = tk.Label(master=self.frame, text=self.create_card_display_text(), width=50, anchor="nw", justify="left")

        # labels
        lbl_add_card = tk.Label(master=self.frame, text="Add card:", anchor="nw")
        lbl_del_card = tk.Label(master=self.frame, text="Delete card:", anchor="nw")
        self.lbl_size = tk.Label(master=self.frame, text="Minimum pool size:", anchor="nw", width=15)

        # dropdownlists
        self.drp_add_card = Changeable_OptionMenu(self.frame, "Select card.", [], 22)
        self.drp_del_card = Changeable_OptionMenu(self.frame, "Select card.", [], 22)

        # buttons
        self.btn_add_card = tk.Button(master=self.frame, text="+ CARD", command=self.handle_btn_add)
        self.btn_del_card = tk.Button(master=self.frame, text="- CARD", command=self.handle_btn_del)
        self.btn_change_type = tk.Button(master=self.frame, text="CHANGE", command=self.handle_btn_change_type)

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

    def create_card_display_text(self):
        text_list = "Card name \n\n"
        if self.card_names != []:
            for card in self.card_names:
                text_list += card + "\n"
        else:
            text_list += "No cards in pool."
        return text_list

    def add_card(self, card):
        self.card_names.append(card)
        self.lbl_card_display.config(text=self.create_card_display_text())

    def handle_btn_add(self):
        pass

    def handle_btn_del(self):
        pass

    def handle_btn_change_type(self):
        state = self.lbl_size["text"]
        if state == "Minimum pool size:":
            self.lbl_size.config(text="Exact pool size:")
        else:
            self.lbl_size.config(text="Minimum pool size:")
        
    def get_frame(self):
        return self.frame
