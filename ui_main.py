"""
Frontend for speck.

Authors:
    Nevin Jose
    Sachin Cherian
"""

import os

import speck_wa
import speck_ui
import speck_graph

from speck_wa.speck import Speck

import tkinter as tk
from tkinter import messagebox

from PIL import ImageTk

from datetime import datetime as dt
from datetime import timedelta as td

from hashlib import md5

class SpeckFrontend:
    def __init__(self):
        self.main_canvas = None

        self.active_widgets = []

        self.bg = None

        self.root = None

        self.style = speck_ui.style.SpeckStyle.from_file("style.json")

        self.entry_cleared = False

        self.tracker = speck_graph.Tracker()

        with open("token.txt", "r") as f:
            self.speck = Speck(f.read().rstrip())

    @staticmethod
    def __cleanup_widget(widget):
        if widget:
            widget.destroy()

    @staticmethod
    def __verify_credentials(uname, pwd):
        # Kind of scuffed
        return md5(bytes(uname, 'utf-8')).hexdigest() == '0816da75e13696127a3ca692ccc9d06b' and \
               md5(bytes(pwd, 'utf-8')).hexdigest()   == 'e7604248bb637b6d0d7ba9b5bc07cc6f'

    def __cleanup_active_widgets(self):
        for i in self.active_widgets:
            SpeckFrontend.__cleanup_widget(i)

    # Flow --------------------------------------

    def welcome(self):
        """Implementation for Welcome screen."""
        
        # Step 1

        SpeckFrontend.__cleanup_widget(self.main_canvas)
        self.__cleanup_active_widgets()

        self.bg = ImageTk.PhotoImage(file='./res/exports/base_logo.png')

        self.main_canvas = tk.Canvas(
            self.root,
            width              = self.style.window.width,
            height             = self.style.window.height,
            bd                 = 0,
            highlightthickness = 0
        )
        self.main_canvas.pack(fill="both", expand=True)
        self.main_canvas.create_image(0, 0, image=self.bg, anchor="nw") # put img on canvas

        welcome_username_entry = tk.Entry(
            self.root,
            font  = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_big),
            width = 15,
            fg    = self.style.colors["primary"].fg,
            bd    = 1
        )
        welcome_password_entry = tk.Entry(
            self.root,
            font  = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_big),
            width = 15,
            fg    = self.style.colors["primary"].fg,
            bd    = 1
        )
        self.active_widgets.append(welcome_username_entry)
        self.active_widgets.append(welcome_password_entry)

        welcome_username_entry.insert(0, "Username")
        welcome_password_entry.insert(0, "Password")

        def check_login():
            if 'SPECK_DEV' in os.environ:
                pass

            elif not self.entry_cleared:
                return messagebox.showwarning("ERROR","ENTER USERNAME AND PASSWORD")

            elif not SpeckFrontend.__verify_credentials(welcome_username_entry.get(), welcome_password_entry.get()):
                return messagebox.showwarning("ERROR","ENTER CORRECT USERNAME AND PASSWORD")

            self.location_entry() # Move onto step 2

        def entry_clear(e):
            if not self.entry_cleared:

                welcome_username_entry.delete(0, tk.END)
                welcome_password_entry.delete(0, tk.END)
                # change pw to ***
                welcome_password_entry.config(show='*')

                self.entry_cleared = True

        # bind the entry boxes, ie when you click it, the text on input box shd vanish
        welcome_username_entry.bind("<Button-1>", entry_clear) 
        welcome_password_entry.bind("<Button-1>", entry_clear)

        # add entry boxes to canvas
        self.main_canvas.create_window(38, 325, anchor='nw', window=welcome_username_entry)
        self.main_canvas.create_window(38, 380, anchor='nw', window=welcome_password_entry)

        welcome_login_button = tk.Button(
            self.root,
            text    = "LOGIN",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_medium),
            width   = 8,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 1,
            command = check_login
        )
        self.active_widgets.append(welcome_login_button)

        self.main_canvas.create_window(38, 435, anchor='nw', window=welcome_login_button)

    def location_entry(self):
        """Implementation for Location Entry Screen."""

        # Step 2

        self.bg = ImageTk.PhotoImage(file='./res/exports/base_logo.png')

        SpeckFrontend.__cleanup_widget(self.main_canvas)
        self.__cleanup_active_widgets()

        self.main_canvas = tk.Canvas(
            self.root,
            width              = self.style.window.width,
            height             = self.style.window.height,
            bd                 = 1,
            highlightthickness = 0
        )
        self.main_canvas.pack(fill="both", expand=True)
        self.main_canvas.create_image(0, 0, image=self.bg, anchor="nw")

        location_input_entry = tk.Entry(
            self.root,
            font  = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_big),
            width = 15,
            fg    = self.style.colors["primary"].fg,
            bd    = 1
        )
        self.active_widgets.append(location_input_entry)

        location_input_entry.insert(0, "Search Location")

        def clear_location_entry(e):
            if location_input_entry.get().lower() == "search location":
                location_input_entry.delete(0, tk.END)

        location_input_entry.bind("<Button-1>", clear_location_entry)

        self.main_canvas.create_window(38, 355, anchor='nw', window=location_input_entry)

        location_input_button = tk.Button(
            self.root,
            text    = "Continue",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_medium),
            width   = 8,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 1,
            command = lambda: self.info_screen(location_input_entry.get())
        )
        self.active_widgets.append(location_input_button)

        self.main_canvas.create_window(38, 405, anchor='nw', window=location_input_button)

    def info_screen(self, loc):
        """Display information for a location."""

        # Step 3

        self.bg = ImageTk.PhotoImage(file='./res/exports/secondary.png')

        SpeckFrontend.__cleanup_widget(self.main_canvas)
        self.__cleanup_active_widgets()

        self.main_canvas = tk.Canvas(
            self.root,
            width              = self.style.window.width,
            height             = self.style.window.height,
            bd                 = 0,
            highlightthickness = 0
        )
        self.main_canvas.pack(fill="both", expand=True)
        self.main_canvas.create_image(0, 0, image=self.bg, anchor="nw")

        # Get info ----------------

        try:
            curr_i = self.speck.current(loc)
        except speck.errors.InvalidLocation:
            rloc = self.speck.find_city(loc)[0]
            curr_i = self.speck.current(f"{rloc['lat']},{rloc['lon']}")

        try:
            fore_i = self.speck.forecast(loc)
        except speck.errors.InvalidLocation:
            rloc = self.speck.find_city(loc)[0]
            fore_i = self.speck.forecast(f"{rloc['lat']},{rloc['lon']}")

        try:
            astro_i = self.speck.astro(loc)
        except speck.errors.InvalidLocation:
            rloc = self.speck.find_city(loc)[0]
            astro_i = self.speck.astro(f"{rloc['lat']},{rloc['lon']}")

        self.tracker.dump(curr_i.location.name, curr_i)

        # Display ----------------

        loc_lbl = tk.Label(
            self.root,
            text = f"{curr_i.location.name}",
            font = (self.style.fonts ["primary"]  .family, self.style.fonts["primary"].size_medium),
            fg   =  self.style.colors["secondary"].fg,
            bg   =  self.style.colors["secondary"].bg
        )

        lt_lbl = tk.Label(
            self.root,
            text = f"{str(curr_i.location.localtime)[:-3]}\nTZ: {curr_i.location.tz_id}",
            font = (self.style.fonts ["primary"]  .family, self.style.fonts["primary"].size_small),
            fg   =  self.style.colors["secondary"].fg,
            bg   =  self.style.colors["secondary"].bg
        )

        curr_lbl = tk.Label(
            self.root,
            text = f"Current Temp: {curr_i.temp_c}°C",
            font = (self.style.fonts ["primary"]  .family, self.style.fonts["primary"].size_small),
            fg   =  self.style.colors["secondary"].fg,
            bg   =  self.style.colors["secondary"].bg
        )
        fore_lbl_1 = tk.Label(
            self.root,
            text = f"Maximum Temp tomorrow: {fore_i[0].day.maxtemp_c}°C",
            font = (self.style.fonts ["primary"]  .family, self.style.fonts["primary"].size_small),
            fg   =  self.style.colors["secondary"].fg,
            bg   =  self.style.colors["secondary"].bg
        )
        fore_lbl_2 = tk.Label(
            self.root,
            text = f"Minimum Temp tomorrow: {fore_i[0].day.mintemp_c}°C",
            font = (self.style.fonts ["primary"]  .family, self.style.fonts["primary"].size_small),
            fg   =  self.style.colors["secondary"].fg,
            bg   =  self.style.colors["secondary"].bg
        )
        astro_lbl = tk.Label(
            self.root,
            text = f"{astro_i.moon_phase}",
            font = (self.style.fonts ["primary"]  .family, self.style.fonts["primary"].size_small),
            fg   =  self.style.colors["secondary"].fg,
            bg   =  self.style.colors["secondary"].bg
        )

        back_btn = tk.Button(
            self.root,
            text    = "Back",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 8,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 0,
            command = self.location_entry
        )
        plot_btn = tk.Button(
            self.root,
            text    = "Plot",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 8,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 0,
            command = lambda: speck_graph.plot(self.tracker, curr_i.location.name)
        )

        self.active_widgets.extend([loc_lbl, lt_lbl, curr_lbl, fore_lbl_1, fore_lbl_2, astro_lbl, back_btn, plot_btn])

        self.main_canvas.create_window(42,  40,  anchor='nw', window=loc_lbl  )
        self.main_canvas.create_window(42,  90,  anchor='nw', window=lt_lbl   )
        self.main_canvas.create_window(42,  150, anchor='nw', window=curr_lbl )
        self.main_canvas.create_window(42,  180, anchor='nw', window=fore_lbl_1)
        self.main_canvas.create_window(42,  210, anchor='nw', window=fore_lbl_2)
        self.main_canvas.create_window(42,  240, anchor='nw', window=astro_lbl)
        self.main_canvas.create_window(28,  523, anchor='nw', window=back_btn )
        self.main_canvas.create_window(210, 523, anchor='nw', window=plot_btn )

    def run(self):
        """Run the application."""
        self.root = tk.Tk()
        self.root.title('Speck Frontend')
        self.root.geometry(f'{self.style.window.width}x{self.style.window.height}')
        self.root.resizable(width=False, height=False)

        self.welcome()

        self.root.mainloop()

if __name__ == '__main__':
    app = SpeckFrontend() # Create an instance
    app.run()
