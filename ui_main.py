"""
Frontend for speck.

Authors:
    2021 Nevin Jose
         Sachin Cherian
"""

import os

from speck.speck import Speck
from speck.errors import *

import speck_ui

from tkinter import *
from tkinter import messagebox

from PIL import ImageTk

from datetime import datetime as dt
from datetime import timedelta as td

from hashlib import md5

class SpeckFrontend:
    def __init__(self):
        ##     Application Flow
        ##     ----------------
        ##
        ##      Welcome Screen
        ##  Username and Password Entry
        ##      Login Button
        ##             ↓
        ##    Location Entry Screen
        ##       Location Entry
        ##        "GET" Button
        ##             ↓
        ##      Type Entry Screen                       ---> (Doesn't change state)
        ##  Current, Forecast, Astro Buttons
        ##             ↓
        ##     Unique TopLevels

        self.main_canvas = None

        self.active_widgets = []

        self.bg = None

        self.root = None

        self.style = speck_ui.SpeckStyle.from_file("style.json")

        self.entry_cleared = False

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
        # Step 1 in application flow

        SpeckFrontend.__cleanup_widget(self.main_canvas)
        self.__cleanup_active_widgets()

        self.bg = ImageTk.PhotoImage(file='./res/exports/base_login.png')

        self.main_canvas = Canvas(
            self.root,
            width              = self.style.window.width,
            height             = self.style.window.height,
            bd                 = 0,
            highlightthickness = 0
        )
        self.main_canvas.pack(fill="both", expand=True)
        self.main_canvas.create_image(0, 0, image=self.bg, anchor="nw") # put img on canvas

        welcome_username_entry = Entry(
            self.root,
            font  = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_medium),
            width = 15,
            fg    = self.style.colors["primary"].fg,
            bd    = 0
        )
        welcome_password_entry = Entry(
            self.root,
            font  = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_medium),
            width = 15,
            fg    = self.style.colors["primary"].fg,
            bd    = 0
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

                welcome_username_entry.delete(0, END)
                welcome_password_entry.delete(0, END)
                # change pw to ***
                welcome_password_entry.config(show='*')

                self.entry_cleared = True

        # bind the entry boxes, ie when you click it, the text on input box shd vanish
        welcome_username_entry.bind("<Button-1>", entry_clear) 
        welcome_password_entry.bind("<Button-1>", entry_clear)

        # add entry boxes to canvas
        un_window = self.main_canvas.create_window(38, 325, anchor='nw', window=welcome_username_entry)
        pw_window = self.main_canvas.create_window(38, 380, anchor='nw', window=welcome_password_entry)

        welcome_login_button = Button(
            self.root,
            text    = "LOGIN",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 8,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 0,
            command = check_login
        )
        self.active_widgets.append(welcome_login_button)

        welcome_login_button_win = self.main_canvas.create_window(38, 435, anchor='nw', window=welcome_login_button)

    def location_entry(self):
        """Implementation for Location Entry Screen."""
        # Step 2 in application flow

        self.bg = ImageTk.PhotoImage(file='./res/exports/base_login.png')

        SpeckFrontend.__cleanup_widget(self.main_canvas)
        self.__cleanup_active_widgets()

        self.main_canvas = Canvas(
            self.root,
            width              = self.style.window.width,
            height             = self.style.window.height,
            bd                 = 0,
            highlightthickness = 0
        )
        self.main_canvas.pack(fill="both", expand=True)
        self.main_canvas.create_image(0, 0, image=self.bg, anchor="nw")

        location_input_entry = Entry(
            self.root,
            font  = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_medium),
            width = 15,
            fg    = self.style.colors["primary"].fg,
            bd    = 0
        )
        self.active_widgets.append(location_input_entry)

        location_input_entry.insert(0, "Search Location")

        def clear_location_entry(e):
            if location_input_entry.get().lower() == "search location":
                location_input_entry.delete(0, END)

        location_input_entry.bind("<Button-1>", clear_location_entry)

        location_entry_window = self.main_canvas.create_window(38, 355, anchor='nw', window=location_input_entry)

        location_input_button = Button(
            self.root,
            text    = "Continue",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 8,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 0,
            command = lambda: self.type_entry(location_input_entry.get())
        )
        self.active_widgets.append(location_input_button)

        location_input_button_win = self.main_canvas.create_window(38, 405, anchor='nw', window=location_input_button)

    def type_entry(self, actual_loc):
        """Implementation for Data Type Entry Screen."""
        # Step 3 in application flow
        self.bg = ImageTk.PhotoImage(file='./res/exports/secondary_logo.png')

        SpeckFrontend.__cleanup_widget(self.main_canvas)
        self.__cleanup_active_widgets()

        self.main_canvas = Canvas(
            self.root,
            width              = self.style.window.width,
            height             = self.style.window.height,
            bd                 = 0,
            highlightthickness = 0
        )
        self.main_canvas.pack(fill="both", expand=True)
        self.main_canvas.create_image(0, 0, image=self.bg, anchor="nw")

        current_search_button = Button(
            self.root,
            text    = "Current",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_medium),
            width   = 14,
            fg      = self.style.colors["primary"].fg,
            command = lambda: self.current_search(actual_loc)
        )
        forecast_search_button = Button(
            self.root,
            text    = "Forecast",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_medium),
            width   = 14,
            fg      = self.style.colors["primary"].fg,
            command = lambda: self.forecast_search(actual_loc)
        )
        astronomy_search_button = Button(
            self.root,
            text    = "Astronomy",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_medium),
            width   = 14,
            fg      = self.style.colors["primary"].fg,
            command = lambda: self.astro_search(actual_loc)
        )
        caclulator_init_button = Button(
            self.root,
            text    = "Calculator",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_medium),
            width   = 14,
            fg      = self.style.colors["primary"].fg,
            command = lambda: self.calculator_search()
        )

        self.active_widgets.append(current_search_button)
        self.active_widgets.append(forecast_search_button)
        self.active_widgets.append(astronomy_search_button)
        self.active_widgets.append(caclulator_init_button)

        curr_btn_win  = self.main_canvas.create_window(38, 220, anchor='nw', window=current_search_button)
        fore_btn_win  = self.main_canvas.create_window(38, 280, anchor='nw', window=forecast_search_button)
        astro_btn_win = self.main_canvas.create_window(38, 340, anchor='nw', window=astronomy_search_button)
        calc_btn_win  = self.main_canvas.create_window(38, 400, anchor='nw', window=caclulator_init_button)

        back_btn = Button(
            self.root,
            text    = 'Back',
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 4,
            fg      = self.style.colors["secondary"].fg,
            bg      = self.style.colors["secondary"].bg,
            bd      = 0,
            command = self.location_entry, highlightthickness=0
        )
        self.active_widgets.append(back_btn)

        back_btn = self.main_canvas.create_window(124, 46, anchor='nw', window=back_btn)

    # Step 3 - - - - - - - - - - - - - - - - - -

    def current_search(self, loc):
        """Implementation for Current Weather screen."""
        try:
            cur_data = self.speck.current(loc)
        except InvalidRequestUrl:
            rloc = self.speck.find_city(loc)[0]
            cur_data = self.speck.current(f"{rloc['lat']},{rloc['lon']}")

        font = int(min((30 - len(cur_data.location.name)), 24))
        
        top = Toplevel()
        top.title(f"Current weather in {cur_data.location.name}")
        top.geometry(f'{self.style.window.width}x{self.style.window.height}')
        top.resizable(width=False, height="false")

        loc_label = Label(
            top,
            text = f"{cur_data.location.name},\n{cur_data.location.country}",
            font = (self.style.fonts["primary"].family, font)
        )
        temp_label = Label(
            top,
            text = f"{cur_data.temp_c()}°C",
            font = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_big),
            fg   =  self.style.colors["primary"].fg
        )

        loc_label.pack()
        temp_label.pack()

        temp_unit = StringVar()
        temp_unit.set("°C")

        for i in ['°C', '°F']:
            Radiobutton(
                top,
                text     = i,
                font     = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
                variable = temp_unit,
                value    = i
            ).pack(anchor='nw')

        def clicked(val):
            if val == '°C':
                temp_label.config(text=f"{cur_data.temp_c()}°C")
            else:
                temp_label.config(text=f"{cur_data.temp_c.fahrenheit()}°F")

        update_button = Button(
            top,
            text    = "Update",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 15,
            fg      = self.style.colors["primary"].fg,
            command = lambda: clicked(temp_unit.get())
        )
        update_button.pack()

        close_button = Button(
            top,
            text    = "Close",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 15,
            fg      = self.style.colors["primary"].fg,
            command = top.destroy
        )
        close_button.pack()

    def forecast_search(self, loc):
        """Implementation for Weather Forecast screen."""
        try:
            fore_data = self.speck.forecast(loc)
        except InvalidRequestUrl:
            rloc = self.speck.find_city(loc)[0]
            fore_data = self.speck.forecast(f"{rloc['lat']},{rloc['lon']}")

        font = int(min((30 - len(fore_data[0].location.name)), 24))

        top = Toplevel()
        top.title(f"Forecast weather in {fore_data[0].location.name}")
        top.geometry(f'{self.style.window.width}x{self.style.window.height}')
        top.resizable(width=False, height="false")

        lbl = Label(
            top,
            text = f"\n{fore_data[0].location.name},\n{fore_data[0].location.country}",
            font = (self.style.fonts["primary"].family, font)
        )
        lbl.pack()

        options = []

        for n, i in enumerate(fore_data):
            ndt = dt.now() + td(days=n+1)

            options.append(f"{ndt.day}-{ndt.month}-{ndt.year}")

        main_info_lbl = Label(
            top,
            text = f"\n\nAverage temperature on {options[0]}:\n{fore_data[0].day.avgtemp_c()}°C\n\n",
            font = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            fg   = self.style.colors["primary"].fg
        )
        main_info_lbl.pack()

        day_select_menu = StringVar()
        day_select_menu.set(options[0])

        day_select_drop = OptionMenu(top, day_select_menu, *options)
        day_select_drop.pack()
        day_select_drop.config(
            font  = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width = 16,
            fg    = self.style.colors["primary"].fg
        )

        def callback():
            n = options.index(day_select_menu.get())
            main_info_lbl.config(text=f"\n\nAverage temperature on {options[n]}:\n{fore_data[n].day.avgtemp_c()}°C\n\n", fg="dark blue")

        _lbl = Label(top, text="\n\n\n\n")
        _lbl.pack()

        update_button = Button(
            top,
            text    = "Update",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            command = callback
        )
        update_button.pack()

        close_button = Button(
            top,
            text    = "Close",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 15,
            fg      = self.style.colors["primary"].fg,
            command = top.destroy
        )
        close_button.pack()

    def astro_search(self, loc):
        """Implementation for Astronomy Information screen."""
        try:
            cur_data = self.speck.astro(loc)
        except InvalidRequestUrl:
            rloc = self.speck.astro(loc)[0]
            cur_data = self.speck.astro(f"{rloc['lat']},{rloc['lon']}")

        font = int(min((30 - len(cur_data.location.name)), 24))
        
        top = Toplevel()
        top.title(f"Astronomy Information in {cur_data.location.name}")
        top.geometry(f'{self.style.window.width}x{self.style.window.height}')
        top.resizable(width=False, height="false")

        
        lbl = Label(
            top,
            text = f"\n\n{cur_data.location.name},\n{cur_data.location.country}",
            font = (self.style.fonts["primary"].family, font)
        )
        lbl2 = Label(
            top,
            text = f"\n\nMoon Phase Today:\n{cur_data.moon_phase}\n\n",
            font = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            fg   = self.style.colors["primary"].fg
        )

        lbl.pack()
        lbl2.pack()

        close_button = Button(
            top,
            text    = "Close",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 15,
            fg      = self.style.colors["primary"].fg,
            command = top.destroy
        )
        close_button.pack()

    def calculator_search(self):
        """Run the calculator."""
        speck_ui.calculator.main()

    # - - - - - - - - - - - - - - - - - - - - - -

    def run(self):
        """Run the entire application. This is blocking."""
        self.root = Tk()
        self.root.title('Speck Frontend')
        self.root.geometry(f'{self.style.window.width}x{self.style.window.height}')
        # make sure app cant be resized
        self.root.resizable(width=False, height="false")

        self.welcome()

        self.root.mainloop()

if __name__ == '__main__':
    app = SpeckFrontend() # Create an instance
    app.run()
