"""
Frontend for speck.

Authors:
    Nevin Jose
    Sachin Cherian
"""

import os

import waw
import ui
import tracker

from ui.widget import Widget
from waw.client import Client

import tkinter as tk
from tkinter import messagebox

from PIL import ImageTk

from datetime import datetime as dt
from datetime import timedelta as td

from hashlib import md5

class SpeckFrontend:
    def __init__(self):
        self.bg = None
        self.root = None
        self.main_canvas = Widget(None, (0, 0))
        self.entry_cleared = False
        
        self.widget_manager = ui.widget.WidgetManager()
        self.style = ui.style.SpeckStyle.from_file("style.json")
        self.tracker = tracker.Tracker()

        with open("token.txt", "r") as f:
            self.speck = Client(f.read().rstrip(), use_cache=True)

    @staticmethod
    def __generic_label(root, style, text):
        return tk.Label(
            root,
            text = text,
            font = (style.fonts ["primary"]  .family, style.fonts["primary"].size_small),
            fg   =  style.colors["secondary"].fg,
            bg   =  style.colors["secondary"].bg
        )

    @staticmethod
    def __verify_credentials(uname, pwd):
        # Kind of scuffed
        return md5(bytes(uname, 'utf-8')) .hexdigest() == '0816da75e13696127a3ca692ccc9d06b' and \
               md5(bytes(pwd, 'utf-8'))   .hexdigest() == 'e7604248bb637b6d0d7ba9b5bc07cc6f'

    # Flow --------------------------------------

    def welcome(self):
        """Implementation for Welcome screen."""
        
        # Step 1

        self.main_canvas.destroy()        
        self.widget_manager.clear()

        self.bg = ImageTk.PhotoImage(file='./etc/exports/base_logo.png')

        self.main_canvas = Widget(tk.Canvas(
            self.root,
            width              = self.style.window.width,
            height             = self.style.window.height,
            bd                 = 0,
            highlightthickness = 0
            ), (0, 0)
        )

        self.main_canvas.internal.pack(fill="both", expand=True)
        self.main_canvas.internal.create_image(0, 0, image=self.bg, anchor="nw") # put img on canvas

        welcome_username_entry = Widget(tk.Entry(
            self.root,
            font  = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_big),
            width = 15,
            fg    = self.style.colors["primary"].fg,
            bd    = 1
            ),
            (38, 325)
        )
        welcome_password_entry = Widget(tk.Entry(
            self.root,
            font  = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_big),
            width = 15,
            fg    = self.style.colors["primary"].fg,
            bd    = 1
            ),
            (38, 380)
        )

        welcome_username_entry.internal.insert(0, "Username")
        welcome_password_entry.internal.insert(0, "Password")

        def check_login():
            if 'SPECK_DEV' in os.environ:
                pass

            elif not self.entry_cleared:
                return messagebox.showwarning("ERROR","ENTER USERNAME AND PASSWORD")

            elif not SpeckFrontend.__verify_credentials(welcome_username_entry.internal.get(), welcome_password_entry.internal.get()):
                return messagebox.showwarning("ERROR","ENTER CORRECT USERNAME AND PASSWORD")

            self.location_entry() # Move onto step 2

        def entry_clear(e):
            if not self.entry_cleared:
                welcome_username_entry.internal.delete(0, tk.END)
                welcome_password_entry.internal.delete(0, tk.END)
                # change pw to ***
                welcome_password_entry.internal.config(show='*')

                self.entry_cleared = True

        # bind the entry boxes, ie when you click it, the text on input box shd vanish
        welcome_username_entry.internal.bind("<Button-1>", entry_clear) 
        welcome_password_entry.internal.bind("<Button-1>", entry_clear)

        welcome_login_button = Widget(tk.Button(
            self.root,
            text    = "LOGIN",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_medium),
            width   = 8,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 1,
            command = check_login
            ),
            (38, 435)
        )

        self.widget_manager.extend([
            welcome_username_entry,
            welcome_password_entry,
            welcome_login_button
        ])

        self.widget_manager.render_all(self.main_canvas.internal)

    def location_entry(self):
        """Implementation for Location Entry Screen."""

        # Step 2

        self.bg = ImageTk.PhotoImage(file='./etc/exports/base_logo.png')

        self.main_canvas.destroy()
        self.widget_manager.clear()

        self.main_canvas = Widget(tk.Canvas(
            self.root,
            width              = self.style.window.width,
            height             = self.style.window.height,
            bd                 = 1,
            highlightthickness = 0
            ), (0, 0)
        )

        self.main_canvas.internal.pack(fill="both", expand=True)
        self.main_canvas.internal.create_image(0, 0, image=self.bg, anchor="nw")

        location_input_entry = Widget(tk.Entry(
            self.root,
            font  = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_big),
            width = 15,
            fg    = self.style.colors["primary"].fg,
            bd    = 1
            ), (38, 355)
        )

        location_input_entry.internal.insert(0, "Search Location")            
        location_input_entry.internal.bind("<Button-1>", lambda _: location_input_entry.internal.delete(0, tk.END))

        location_input_button = Widget(tk.Button(
            self.root,
            text    = "Continue",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_medium),
            width   = 8,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 1,
            command = lambda: self.info_screen(location_input_entry.internal.get())
            ),
            (38, 405)
        )

        self.widget_manager.push(location_input_entry)
        self.widget_manager.push(location_input_button)

        self.widget_manager.render_all(self.main_canvas.internal)

    def info_screen(self, loc):
        """Display information for a location."""

        # Step 3

        self.bg = ImageTk.PhotoImage(file='./etc/exports/secondary.png')

        self.main_canvas.destroy()        
        self.widget_manager.clear()

        self.main_canvas = Widget(tk.Canvas(
            self.root,
            width              = self.style.window.width,
            height             = self.style.window.height,
            bd                 = 0,
            highlightthickness = 0
            ),(0, 0)
        )

        self.main_canvas.internal.pack(fill="both", expand=True)
        self.main_canvas.internal.create_image(0, 0, image=self.bg, anchor="nw")

        # Get info ----------------

        try:
            curr_i = self.speck.current(loc) # if this fails, there's no valid location

        except waw.errors.InvalidLocation:
            loc = self.speck.find_city(loc)

            if len(loc) == 0:
                self.location_entry() # if this fails as well, we go back to the location screen
                                      # TODO: add an `is_prev_fail` check

            loc = f"{rloc['lat']},{rloc['lon']}"

            curr_i = self.speck.current(loc)
        
        astro_i = self.speck.astro(loc)
        fore_i  = self.speck.forecast(loc)

        self.tracker.dump(curr_i.location.name, curr_i)

        # Display ----------------

        loc_lbl = Widget(tk.Label(
            self.root,
            text = curr_i.location.name,
            font = (self.style.fonts ["primary"]  .family, self.style.fonts["primary"].size_medium),
            fg   =  self.style.colors["secondary"].fg,
            bg   =  self.style.colors["secondary"].bg
            ), (42, 40)
        )

        #                                                 # Root     # Style     # Text                                                                 # Pos
        lt_lbl     = Widget(SpeckFrontend.__generic_label(self.root, self.style, f"{str(curr_i.location.localtime)[:-3][5:]} {curr_i.location.tz_id}"), ("+0",  "+50"))
        curr_lbl   = Widget(SpeckFrontend.__generic_label(self.root, self.style, f"Current Temp: {curr_i.temp_c}°"),                                    ("+0",  "+30"))
        fore_lbl_1 = Widget(SpeckFrontend.__generic_label(self.root, self.style, f"Maximum Temp tomorrow: {fore_i[0].day.maxtemp_c}°C"),                ("+0",  "+30"))
        fore_lbl_2 = Widget(SpeckFrontend.__generic_label(self.root, self.style, f"Minimum Temp tomorrow: {fore_i[0].day.mintemp_c}°C"),                ("+0",  "+30"))
        astro_lbl  = Widget(SpeckFrontend.__generic_label(self.root, self.style, f"{astro_i.moon_phase}"),                                              ("+0",  "+30"))

        back_btn = Widget(tk.Button(
            self.root,
            text    = "Back",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 8,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 0,
            command = self.location_entry
            ),
            (26,  523) # pos
        )
        plot_btn = Widget(tk.Button(
            self.root,
            text    = "Plot",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 8,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 0,
            command = lambda: tracker.plot(self.tracker, curr_i.location.name)
            ),
            (196, 523) # pos
        )

        self.widget_manager.extend([
            loc_lbl,
            lt_lbl,
            curr_lbl,
            fore_lbl_1,
            fore_lbl_2,
            astro_lbl,
            back_btn,
            plot_btn
        ])

        self.widget_manager.render_all(self.main_canvas.internal)

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
