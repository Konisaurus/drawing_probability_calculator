# Imports
import tkinter as tk

# Classes        
class Changeable_OptionMenu():
    '''
    A tk.OptionMenu that has a list which can be changed.
    Access the tk.OptionMenu class through self.get_OptionMenu_class()
    '''
    def __init__(self, master, dropdown_title, option_list, width):
        self.unremovable_option = dropdown_title    # The first element of the dropdown list is the title, it can't be removed.
        self.options = [self.unremovable_option]    # All the options.
        self.options.extend(option_list)            # Add the options to the list

        self.variable = tk.StringVar(master)                                 # Variable which the OptionMenu becomes (strings).
        self.variable.set(dropdown_title)
        self.option_menu = tk.OptionMenu(master, self.variable, *self.options)  # OptionMenu.
        self.option_menu.config(width=width)                                    # Set a default width, so that it does NOT change depending on the item selected.

    def update_options(self):
        '''
        After a change to self.option_list, the tk.OptionMenu must be updated.
        '''
        self.option_menu["menu"].delete(0, "end")
        for item in self.options:
            self.option_menu["menu"].add_command(label=item, command=lambda value=item: self.variable.set(value))
        self.variable.set(self.unremovable_option)

    # Manage self.option_list
    def append_item(self, item):
        '''
        Appends an item to self.option_list
        '''
        self.options.append(str(item))
        self.update_options()              # Update OptionMenu

    def remove_item(self, item):
        '''
        Removes the selected item from self.option_list.
        '''
        if item in self.options and not item == self.unremovable_option:    # We don't want self.option_list to be empty.
            self.options.remove(item)               
            self.update_options()                                           # Update OptionMenu.         

    # Getter functions.
    def get_OptionMenu_class(self):
        return self.option_menu
    
    def get_variable(self):
        return self.variable.get()


class Scrollable_Frame():
    '''
    Frame with a scrollbar for the y-axis.
    Access this frame with self.get_frame()
    '''
    def __init__(self, master):
        # Create a frame that wraps everything up.
        self.frm_wrapper = tk.Frame(master=master, borderwidth=5)

        # Create a canvas which will be scrollable.
        self.cnv_scrollbar = tk.Canvas(master=self.frm_wrapper)
        self.cnv_scrollbar.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)

        # Add a scrollbar to the canvas.
        self.scb_yaxis = tk.Scrollbar(master=self.frm_wrapper, orient="vertical", command=self.cnv_scrollbar.yview)
        self.scb_yaxis.pack(side="right",fill="y")

        # Configure the canvas.
        self.cnv_scrollbar.configure(yscrollcommand=self.scb_yaxis.set)
        self.cnv_scrollbar.bind("<Configure>", lambda e: self.cnv_scrollbar.config(scrollregion= self.cnv_scrollbar.bbox(tk.ALL))) 

        # Create another frame inside the canvas which will contain all widgets and add it to the canvas.
        self.frm_container = tk.Frame(master=self.cnv_scrollbar)
        self.cnv_scrollbar.create_window((0,0), window=self.frm_container, anchor="nw")  

        # Bind the scrollwheel to the scrollbar,
        self.frm_container.bind("<Enter>", self.bind_mousewheel)
        self.frm_container.bind("<Leave>", self.unbind_mousewheel)
        self.frm_container.bind("<Configure>", self.adjust_scrollregion)

    def pack(self):
        '''
        Packs this widget.
        '''
        self.frm_wrapper.pack(fill="both",expand=1, anchor="nw")

    
    def get_frame(self):
        '''
        # Access/add all widgets in this frame.
        '''
        return self.frm_container
        
    def bind_mousewheel(self, event):
        '''
        Binds mousewheel when inside of the frame.
        '''
        self.cnv_scrollbar.bind_all("<MouseWheel>", self.handle_mousewheel)

    def unbind_mousewheel(self, event):
        '''
        Unbinds mousewheel when outside of the frame.
        '''
        self.cnv_scrollbar.unbind_all("<MouseWheel>")

    def handle_mousewheel(self, event):
        '''
        Configures the mousewheel with the scorllbar.
        '''
        self.cnv_scrollbar.yview_scroll(int(-1*(event.delta/120)), "units")

    def adjust_scrollregion(self, event):
        '''
        Adjusts the scrollbarregion when the frame gets bigger
        '''
        self.cnv_scrollbar.configure(scrollregion=self.cnv_scrollbar.bbox("all"))
