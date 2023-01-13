import tkinter as tk


class Changeable_OptionMenu():
    # an tk.OptionMenu that has a list which can be changed
    def __init__(self, parent, unremovable_option, option_list, dropdown_title):
        self.parent = parent
        self.unremovable_option = unremovable_option
        self.options = [self.unremovable_option]
        self.options.extend(option_list)

        self.variable = tk.StringVar(self.parent)
        self.variable.set(dropdown_title)
        self.dropdown = tk.OptionMenu(self.parent, self.variable, *self.options)

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
        if item in self.options and not item ==  self.unremovable_option:
            self.options.remove(item)
            self.update_options()
        if self.options != []:
            self.variable.set(self.unremovable_option)

    def get_OptionMenu_class(self):
        # get the OptionMenu, which is the core of this class
        return self.dropdown


class Display_Card_Pool():
    # display a card pool
    # still needs to be implemented
    def __init__(self, name_list):
        self.card_names = name_list
