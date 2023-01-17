import tkinter as tk


class Changeable_OptionMenu():
    # an tk.OptionMenu that has a list which can be changed
    def __init__(self, master, dropdown_title, option_list, width):
        self.unremovable_option = dropdown_title
        self.options = [self.unremovable_option]
        self.options.extend(option_list)

        self.variable = tk.StringVar(master)
        self.variable.set(dropdown_title)
        self.dropdown = tk.OptionMenu(master, self.variable, *self.options)
        self.dropdown.config(width=width)

    def _update_options(self):
        # after a change to the options list, the tk.OptionMenu must be updated
        self.dropdown["menu"].delete(0, "end")
        for item in self.options:
            self.dropdown["menu"].add_command(label=item, command=lambda value=item: self.variable.set(value))

    def append_item(self, item):
        # append an item to the option list
        self.options.append(str(item))
        self._update_options()

    def delete_item(self):
        # deletes the selected item from the option list
        item = self.variable.get()
        if item in self.options and not item == self.unremovable_option:
            self.options.remove(item)
            self._update_options()
            self.variable.set(self.unremovable_option)

    def get_OptionMenu_class(self):
        # get the OptionMenu, which is the core of this class
        return self.dropdown


class Scrollable_Frame():
    # a frmae with a scrollbar for the y-axis.
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
