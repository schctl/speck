"""Prewritten GUI frontend for speck."""

import os
from hashlib import md5

import tkinter as tk
from PIL import ImageTk

from waw.client import Client

from ext import track

from .calculator import Calculator

from .style import SpeckStyle
from .widget import Widget, WidgetManager

# -- Utils --
def _rootd(path):
    """Return absolute path of `path` relative to this file."""
    return os.path.join(os.path.dirname(__file__), f"../../{path}")

def _readf(fname):
    """Utility function to read a file."""
    with open(fname, 'r') as f:
        return f.read()

def _utf8_to_md5_hex(string):
    """Convert a UTF-8 encoded string to its md5 in hex format."""
    return md5(bytes(string, 'utf-8')).hexdigest()
# -----------

class SampleFrontend:
    """GUI class."""
    def __init__(self):
        self.bg = None # Background image
        self.root = None
        self.main_canvas = Widget(None, (0, 0)) # Main canvas - everything gets drawn on here.

        self.entry_cleared = False # Check if uname and pwd entries have been cleared of defaults.
        self.last_loc_fail = False

        self.widget_manager = WidgetManager()

        self.style = SpeckStyle.from_file(_rootd('etc/style.json'))
        self.tracker = track.Tracker(_rootd('.tracker'))

        self.speck = Client(
            _readf(_rootd('token.txt')).rstrip(),
            use_cache=True,
            cache_path=f"{_rootd('.cache')}"
        )

    @staticmethod
    def __generic_label(root, style, text):
        """Make a generic label so we don't have to do it ourselves."""
        return tk.Label(
            root,
            text = text,
            font = (style.fonts ["primary"]  .family, style.fonts["primary"].size_small),
            fg   =  style.colors["secondary"].fg,
            bg   =  style.colors["secondary"].bg
        )

    @staticmethod
    def __verify_credentials(uname, pwd):
        """This is just a dummy."""
        # We'll store our credentials in a file - not the best idea
        auth = _readf(_rootd('etc/auth.txt')).split()
        return _utf8_to_md5_hex(uname) == auth[0] and \
               _utf8_to_md5_hex(pwd)   == auth[1]

    # Flow --------------------------------------

    def welcome(self):
        """Implementation for Welcome screen."""

        # Step 1

        self.main_canvas.destroy()
        self.widget_manager.clear()

        self.bg = ImageTk.PhotoImage(file=_rootd('etc/exports/base_logo.png'))

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

        welcome_username_entry.internal.insert(0, "Username") # Default values
        welcome_password_entry.internal.insert(0, "Password")

        def check_login():
            if 'SPECK_DEV' in os.environ:
                pass

            elif not self.entry_cleared:
                tk.messagebox.showwarning("ERROR", "ENTER USERNAME AND PASSWORD")
                return

            elif not SampleFrontend.__verify_credentials(
                welcome_username_entry.internal.get(),
                welcome_password_entry.internal.get()
                ):
                tk.messagebox.showwarning("ERROR", "ENTER CORRECT USERNAME AND PASSWORD")
                return

            self.location_entry() # Move onto step 2

        def entry_clear(_):
            if not self.entry_cleared: # Make sure we're not deleting any input
                welcome_username_entry.internal.delete(0, tk.END) # Clear defaults
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

        self.bg = ImageTk.PhotoImage(file=_rootd('etc/exports/base_logo.png'))

        self.main_canvas.destroy() # Clear the main canvas
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
        location_input_entry.internal.bind(
            "<Button-1>",
            lambda _: location_input_entry.internal.delete(0, tk.END)
        )

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

        if self.last_loc_fail:
            fail_loc = Widget(
                SampleFrontend.__generic_label(
                    self.root,
                    self.style,
                    "Unknown Location"
                ),
                ("-16", "+120")
            )
            self.widget_manager.push(fail_loc)

        self.widget_manager.render_all(self.main_canvas.internal)

    def info_screen(self, loc):
        """Display information for a location."""

        # Step 3

        self.bg = ImageTk.PhotoImage(file=_rootd('etc/exports/secondary.png'))

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
                self.last_loc_fail = True
                self.location_entry() # if this fails as well, we go back to the location screen
                return

            loc = f"{loc[0]['lat']},{loc[0]['lon']}"

            curr_i = self.speck.current(loc)

        astro_i = self.speck.astro(loc)
        fore_i  = self.speck.forecast(loc)

        self.tracker.dump(curr_i.location.name, curr_i)

        self.last_loc_fail = False

        # Display ----------------

        loc_lbl = Widget(tk.Label(
            self.root,
            text = curr_i.location.name,
            font = (self.style.fonts ["primary"]  .family, self.style.fonts["primary"].size_medium),
            fg   =  self.style.colors["secondary"].fg,
            bg   =  self.style.colors["secondary"].bg
            ), (42, 40)
        )

        #                                        # Root     # Style     # Text                                                                 # Pos
        lt_lbl     = \
            Widget(SampleFrontend.__generic_label(self.root, self.style, f"{str(curr_i.location.localtime)[:-3][5:]} {curr_i.location.tz_id}"), ("+0", "+50"))
        curr_lbl   = \
            Widget(SampleFrontend.__generic_label(self.root, self.style, f"Current Temp: {curr_i.temp_c}°"),                                    ("+0", "+30"))
        fore_lbl_1 = \
            Widget(SampleFrontend.__generic_label(self.root, self.style, f"Maximum Temp tomorrow: {fore_i[0].day.maxtemp_c}°C"),                ("+0", "+30"))
        fore_lbl_2 = \
            Widget(SampleFrontend.__generic_label(self.root, self.style, f"Minimum Temp tomorrow: {fore_i[0].day.mintemp_c}°C"),                ("+0", "+30"))
        astro_lbl  = \
            Widget(SampleFrontend.__generic_label(self.root, self.style, f"{astro_i.moon_phase}"),                                              ("+0", "+30"))

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
            command = lambda: track.plot(self.tracker, curr_i.location.name)
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

    # -------------------------------------------

    def run(self):
        """Run the application."""
        self.root = tk.Tk()
        self.root.title('Speck Frontend')
        self.root.geometry(f'{self.style.window.width}x{self.style.window.height}')
        self.root.resizable(width=False, height=False)

        self.welcome()

        self.root.mainloop()
