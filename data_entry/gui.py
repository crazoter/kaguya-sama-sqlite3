#!/usr/bin/env python3

"""
gui.py: Basic GUI component for the data entry tool.
"""

__author__      = "crazoter"
__copyright__   = "Copyright 2020"
__license__     = "GPL"
__version__     = "1.0.0"
__status__      = "Development"

from schema import ColumnEntry, SCHEMA
import tkinter as tk
from tkinter import Tk, ttk, Menu, messagebox

class Gui:
    # Init Main Components
    def __init__(self, schema):
        # Components
        self.root = None
        self.tabs = None
        self.menu = None
        self.schema = schema
        # Data
        self.dirty_tables = [] # Used for updating components
        # Components in tabs
        self.foreign_key_components = {}
        for tablename in self.schema:
            self.foreign_key_components[tablename] = []

    def init_root(self):
        self.root = tk.Tk()

    def init_tabs(self):
        """
        Initialize tabs based on schema
        Use of mnemonics:
        Control-Tab selects the tab following the currently selected one.
        Control-Shift-Tab selects the tab preceding the currently selected one.
        Alt-K, where K is the mnemonic (underlined) character of any tab, will select that tab.
        Documentation: https://wiki.tcl-lang.org/page/tkinter.Notebook
        """
        # Store the shortcut set here
        mnemonic_set = set()
        self.tabs = ttk.Notebook(self.root)
        for tablename in self.schema:
            mnemonic_index = 0
            tab = ttk.Frame(self.tabs)
            # Can't have repeat shortcuts / mnemonics
            while (tablename[mnemonic_index] in mnemonic_set):
                mnemonic_index += 1
            mnemonic_set.add(tablename[mnemonic_index])
            # Create tab
            self.tabs.add(tab, text=tablename, underline=mnemonic_index)
            self.init_tab_body(tablename, tab)
        # Create tab list
        self.tabs.pack(expand=1, fill='both')
        # Enable mnemonics
        self.tabs.enable_traversal()
    
    def init_tab_body(self, tablename, tab):
        """
        Helper function to populate tab with items
        """
        # Add entity list display
        # Add delete field + button
        # Add fields
        for column in self.schema[tablename]:
            # Create fields based on column
            if column[ColumnEntry.foreign_key_id]:
                # Select from dropdown
            elif column[ColumnEntry._type] == str:
                # Text field
            elif column[ColumnEntry._type] == int:
                # Integer number
            elif column[ColumnEntry._type] == float:
                # Real number
            else:
                raise ValueError(column + " from  " + tablename + " type is not supported")
        # Add "Add" button

    def init_menu(self):
        self.menu = Menu(self.root)
        # Add menu buttons
        helpmenu = Menu(self.menu) 
        self.menu.add_cascade(label='Help', menu=helpmenu, command=self.show_help) 
        self.root.config(menu=self.menu)

    def start(self):
        """
        Initialize tkinter
        """
        # Initialize components
        self.init_root()
        # self.init_menu()
        self.init_tabs()
        # Run
        self.root.mainloop()

    # Event handlers
    def show_help(self):
        messagebox.showinfo("Help", "Placeholder")

if __name__ == '__main__':
    gui = Gui(SCHEMA)
    # gui.init_tabs()
    gui.start()
