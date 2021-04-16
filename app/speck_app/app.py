"""
Sample tkinter frontend for speck.

Authors:
    Nevin Jose
    Sachin Cherian
"""

import os
from hashlib import md5

import speck

import tkinter as tk
from PIL import ImageTk

from .style import SpeckStyle
from .tracker import Tracker, plot
from .calculator import Calculator
from .widget import Widget, WidgetManager

__all__ = [
    'SpeckApp'
]

# -- Utils --
def _rootd(path):
    """Return absolute path of `path` relative to this file."""
    return os.path.join(os.path.dirname(__file__), path)

def _readf(fname):
    """Utility function to read a file."""
    with open(fname, 'r') as f:
        return f.read()

def _utf8_to_md5_hex(string):
    """Convert a UTF-8 encoded string to its md5 in hex format."""
    return md5(bytes(string, 'utf-8')).hexdigest()
# -----------

class SpeckApp:
    """Implementation for a sample frontend."""

    def __init__(self, token, auth_file=_rootd('etc/auth.txt')):
        self.bg = None # Background image
        self.root = None
        self.main_canvas = Widget(None, (0, 0)) # Main canvas - everything gets drawn on here.

        self.entry_cleared = False # Check if uname and pwd entries have been cleared of defaults.
        self.loc_e_cleared = False

        self.widget_manager = WidgetManager()

        self.style = SpeckStyle.from_file(_rootd('etc/style.json'))
        self.tracker = Tracker(_rootd('.tracker'))

        self.speck = speck.Client(
            token,
            use_cache=True,
            cache_path=f"{_rootd('.cache')}"
        )

        with open(auth_file, 'r') as f:
            self.__auth = f.read().split()

    @staticmethod
    def __gen_label(root, style, text):
        """Make a generic label so we don't have to do it ourselves."""
        return tk.Label(
            root,
            text = text,
            font = (style.fonts ["primary"]  .family, style.fonts["primary"].size_small),
            fg   =  style.colors["secondary"].fg,
            bg   =  style.colors["secondary"].bg
        )

    @staticmethod
    def __verify_creds(auth, uname, pwd):
        """This is just a dummy."""
        # We'll store our credentials in a file - not the best idea
        return _utf8_to_md5_hex(uname) == auth[0] and \
               _utf8_to_md5_hex(pwd)   == auth[1]

    def __warn(self, msg='Warning'):
        """Display a warning in message box."""
        tk.messagebox.showwarning('WARNING', msg)

    def __err(self, msg='Error'):
        """Display an error in message box."""
        tk.messagebox.showerror('ERROR', msg)

    def __get_loc_meta(self, loc):
        """Get all metadata for a location."""

        try:
            (curr_i, fore_i) = self.speck.forecast(loc)
            # if this fails, there's no valid location
            # recognized by weatherAPI

        except speck.errors.InvalidLocation as e:
            loc = self.speck.find_city(loc) # try to find our own

            if len(loc) == 0:
                raise speck.errors.InvalidLocation('Unknown location.', e.internal_code)

            loc = f"{loc[0]['lat']},{loc[0]['lon']}"

            (curr_i, fore_i) = self.speck.forecast(loc)

        except Exception as e: # let caller handle any other error
            raise e

        astro_i = self.speck.astro(loc)

        return curr_i, astro_i, fore_i

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
                self.__err("ENTER USERNAME AND PASSWORD")
                return

            elif not SpeckApp.__verify_creds(
                self.__auth,
                welcome_username_entry.internal.get(),
                welcome_password_entry.internal.get()
                ):
                self.__err("ENTER CORRECT USERNAME AND PASSWORD")
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

        def clear_location_entry(e):
            if not self.loc_e_cleared:
                location_input_entry.internal.delete(0, tk.END)
                self.loc_e_cleared = True

        self.loc_e_cleared = False

        location_input_entry.internal.insert(0, "Search Location")
        location_input_entry.internal.bind(
            "<Button-1>",
            clear_location_entry
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

        curr_i = None
        astro_i = None
        fore_i = None

        try:
            curr_i, astro_i, fore_i = self.__get_loc_meta(loc)
        except speck.errors.InvalidLocation:
            self.__err('Unknown location.')
            self.location_entry()
            return
        except speck.errors.InternalError as e:
            self.__err(f'Internal Error: {e}')
            self.location_entry()
            return
        except speck.errors.InvalidApiKey:
            self.__err('Invalid API key. Get the API key from https://weatherapi.com/my')
            self.location_entry()
            return
        except Exception as e:
            self.__err(f'Query failed: {e}')
            self.location_entry()
            return

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

        #                                        # Root     # Style     # Text                                                                 # Pos
        lt_lbl     = \
            Widget(SpeckApp.__gen_label(self.root, self.style, f"{str(curr_i.location.localtime)[:-3][5:]} {curr_i.location.tz_id}"), ("+0", "+50"))
        curr_lbl   = \
            Widget(SpeckApp.__gen_label(self.root, self.style, f"Current Temp: {curr_i.temp_c}°"),                                    ("+0", "+30"))
        fore_lbl_1 = \
            Widget(SpeckApp.__gen_label(self.root, self.style, f"Maximum Temp tomorrow: {fore_i[0].day.maxtemp_c}°C"),                ("+0", "+30"))
        fore_lbl_2 = \
            Widget(SpeckApp.__gen_label(self.root, self.style, f"Minimum Temp tomorrow: {fore_i[0].day.mintemp_c}°C"),                ("+0", "+30"))
        astro_lbl  = \
            Widget(SpeckApp.__gen_label(self.root, self.style, f"{astro_i.moon_phase}"),                                              ("+0", "+30"))

        back_btn = Widget(tk.Button(
            self.root,
            text    = "Back",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 4,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 0,
            command = self.location_entry
            ),
            (26,  523) # pos
        )
        calc_btn = Widget(tk.Button(
            self.root,
            text    = "Calculator",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 6,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 0,
            command = lambda: Calculator().run()
            ),
            (110, 523) # pos
        )
        plot_btn = Widget(tk.Button(
            self.root,
            text    = "Plot",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 4,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 0,
            command = lambda: plot(self.tracker, curr_i.location.name)
            ),
            (206, 523) # pos
        )

        self.widget_manager.extend([
            loc_lbl,
            lt_lbl,
            curr_lbl,
            fore_lbl_1,
            fore_lbl_2,
            astro_lbl,
            back_btn,
            calc_btn,
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
