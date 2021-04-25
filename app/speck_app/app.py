"""
Sample tkinter frontend for speck.
"""

import os

import tkinter as tk

import speck

from . import utils
from .style import SpeckStyle
from .tracker import Tracker, plot
from .calculator import Calculator
from .widget import Widget, WidgetManager

__all__ = ['SpeckApp']

class SpeckApp:
    """Implementation for a speck frontend app."""

    def __init__(self, token, auth_file=utils.rootd('etc/auth.txt')):
        self.bg = None # Background image
        self.root = None
        self.main_canvas = Widget(None, (0, 0)) # Main canvas - everything gets drawn on here.

        self.entry_cleared = False # Check if uname and pwd entries have been cleared of defaults.
        self.loc_e_cleared = False

        self.widget_manager = WidgetManager()

        self.style = SpeckStyle.from_file(utils.rootd('etc/style.json'))
        self.tracker = Tracker(utils.rootd('.tracker'))

        self.speck = speck.Client(
            token,
            use_cache=True,
            cache_file=True,
            cache_path=utils.rootd('.cache')
        )

        print("Using cache of type:", type(self.speck.cache))

        with open(auth_file, 'r') as f:
            self.__auth = f.read().split()

    # Utils ------------------------------

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
        return utils.utf8_to_md5_hex(uname) == auth[0] and \
               utils.utf8_to_md5_hex(pwd)   == auth[1]

    def __get_loc_meta(self, loc):
        """Get all metadata for a location."""

        try:
            (curr_i, fore_i) = self.speck.forecast(loc)

        except speck.errors.InvalidLocation as e:
            loc = self.speck.find_city(loc) # try to find our own

            if len(loc) == 0:
                raise speck.errors.InvalidLocation('Unknown location.', e.internal_code)

            loc = f"{loc[0]['lat']},{loc[0]['lon']}"

            (curr_i, fore_i) = self.speck.forecast(loc)

        astro_i = self.speck.astro(loc)

        return curr_i, astro_i, fore_i

    def __clear_with_bg(self, bg_path):
        """Clear the main canvas and set a background image."""

        self.main_canvas.destroy()
        self.widget_manager.clear()

        self.bg = tk.PhotoImage(file=utils.rootd(bg_path))

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

    @staticmethod
    def __warn(msg):
        """Display a warning in message box."""
        tk.messagebox.showwarning('WARNING', msg)

    @staticmethod
    def __err(msg):
        """Display an error in message box."""
        tk.messagebox.showerror('ERROR', msg)

    # Flow --------------------------------------

    def welcome(self):
        """Implementation for Welcome screen."""

        # Step 1

        self.__clear_with_bg('etc/exports/base_login_old.png')

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
                SpeckApp.__err("ENTER USERNAME AND PASSWORD")
                return

            elif not SpeckApp.__verify_creds(
                self.__auth,
                welcome_username_entry.internal.get(),
                welcome_password_entry.internal.get()
                ):
                SpeckApp.__err("ENTER CORRECT USERNAME AND PASSWORD")
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

        self.__clear_with_bg('etc/exports/base_login_old.png')

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

    def info_screen(self, loc, info=None):
        """Display information for a location."""

        # Step 3

        self.__clear_with_bg('etc/exports/secondary.png')

        print("Cache:", self.speck.cache.debug_size(), "bytes") # Debug cache size in mem

        # Get info ----------------

        if not info:
            try:
                info = self.__get_loc_meta(loc)
            except speck.errors.InvalidLocation:
                SpeckApp.__err('Unknown location.')
                self.location_entry()
                return
            except speck.errors.InternalError as e:
                SpeckApp.__err(f'Internal Error: {e}')
                self.location_entry()
                return
            except speck.errors.InvalidApiKey:
                SpeckApp.__err('Invalid API key. Get the API key from https://weatherapi.com/my')
                self.location_entry()
                return
            except speck.WeatherApiError as e:
                SpeckApp.__err(f'Query failed: {e.message}')
                self.location_entry()
                return

        self.tracker.dump(info[0].location.name, info[0])

        # Display ----------------

        curr_i = info[0]

        loc_lbl = Widget(tk.Label(
            self.root,
            text = curr_i.location.name,
            font = (self.style.fonts ["primary"]  .family, self.style.fonts["primary"].size_medium),
            fg   =  self.style.colors["secondary"].fg,
            bg   =  self.style.colors["secondary"].bg
            ),
            (42, 40)
        )
        lt_lbl = \
            Widget(SpeckApp.__gen_label(self.root,
                self.style,f"{str(curr_i.location.localtime)[:-3][5:]} {curr_i.location.tz_id}"),
                ("+0", "+35")
            )

        cond_lbl = \
            Widget(SpeckApp.__gen_label(self.root,
                self.style,
                curr_i.condition['text']),
                ("+0", "+40")
            )
        curr_lbl = \
            Widget(SpeckApp.__gen_label(self.root,
                self.style,
                f"Current Temp: {curr_i.temp_c}°C"),
                ("+0", "+30")
            )
        feelslike_lbl = \
            Widget(SpeckApp.__gen_label(self.root,
                self.style,
                f"Feels like: {curr_i.feelslike_c}°C"),
                ("+0", "+30")
            )
        precip_lbl = \
            Widget(SpeckApp.__gen_label(self.root,
                self.style,
                f"Rain: {curr_i.precip_mm} mm"),
                ("+0", "+30")
            )
        humidity_lbl = \
            Widget(SpeckApp.__gen_label(self.root,
                self.style,
                f"Humidity: {curr_i.humidity}"),
                ("+0", "+30")
            )
        uv_lbl = \
            Widget(SpeckApp.__gen_label(self.root,
                self.style,
                f"UV: {curr_i.uv}"),
                ("+0", "+30")
            )

        forecast_btn = Widget(tk.Button(
            self.root,
            text    = "Forecast",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 8,
            fg      = self.style.colors["secondary"].fg,
            bg      = self.style.colors["secondary"].bg,
            bd      = 0,
            command = lambda: self.forecast_screen(info)
            ),
            ("+0", "+75") # pos
        )

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
            (28,  523) # pos
        )
        calc_btn = Widget(tk.Button(
            self.root,
            text    = "Calc",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 4,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 0,
            command = lambda: Calculator().run()
            ),
            ("+70", 523) # pos
        )
        plot_btn = Widget(tk.Button(
            self.root,
            text    = "Plot",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 4,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 0,
            command = lambda: plot(info[2], self.tracker, curr_i.location.name)
            ),
            ("+70", 523) # pos
        )
        docs_btn = Widget(tk.Button(
            self.root,
            text    = "?",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 4,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 0,
            command = lambda: self.docs(self.info_screen, None, info)
            ),
            ("+70", 523) # pos
        )

        self.widget_manager.extend([
            loc_lbl,

            lt_lbl,
            cond_lbl,
            curr_lbl,
            feelslike_lbl,
            precip_lbl,
            humidity_lbl,
            uv_lbl,
            forecast_btn,

            back_btn,
            calc_btn,
            plot_btn,
            docs_btn,
        ])
        self.widget_manager.render_all(self.main_canvas.internal)


    def forecast_screen(self, info):
        """Show all forecast information."""

        self.__clear_with_bg('etc/exports/secondary.png')

        # -------------------------

        fore_i = info[2]

        loc_lbl = Widget(tk.Label(
            self.root,
            text = fore_i[0].location.name,
            font = (self.style.fonts ["primary"]  .family, self.style.fonts["primary"].size_medium),
            fg   =  self.style.colors["secondary"].fg,
            bg   =  self.style.colors["secondary"].bg
            ),
            (42, 40)
        )

        fore_lbl_1 = \
            Widget(SpeckApp.__gen_label(self.root,
                self.style,
                f"Maximum Temp tomorrow: {fore_i[0].day.maxtemp_c}°C"),
                ("+0", "+40")
            )
        fore_lbl_2 = \
            Widget(SpeckApp.__gen_label(self.root,
                self.style,
                f"Minimum Temp tomorrow: {fore_i[0].day.mintemp_c}°C"),
                ("+0", "+30")
            )

        astro_btn = Widget(tk.Button(
            self.root,
            text    = "Astronomy",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 8,
            fg      = self.style.colors["secondary"].fg,
            bg      = self.style.colors["secondary"].bg,
            bd      = 0,
            command = lambda: self.astro_screen(info)
            ),
            ("+0", "+75") # pos
        )

        back_btn = Widget(tk.Button(
            self.root,
            text    = "Back",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 4,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 0,
            command = lambda: self.info_screen(None, info)
            ),
            (28,  523) # pos
        )
        calc_btn = Widget(tk.Button(
            self.root,
            text    = "Calc",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 4,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 0,
            command = lambda: Calculator().run()
            ),
            ("+70", 523) # pos
        )
        docs_btn = Widget(tk.Button(
            self.root,
            text    = "?",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 4,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 0,
            command = lambda: self.docs(self.forecast_screen, info)
            ),
            ("+70", 523) # pos
        )

        self.widget_manager.extend([
            loc_lbl,

            fore_lbl_1,
            fore_lbl_2,
            astro_btn,

            back_btn,
            calc_btn,
            docs_btn,
        ])
        self.widget_manager.render_all(self.main_canvas.internal)

    def astro_screen(self, info):
        """Show all astronomy details."""
        self.__clear_with_bg('etc/exports/secondary.png')

        # -------------------------

        astro_i = info[1]

        loc_lbl = Widget(tk.Label(
            self.root,
            text = astro_i.location.name,
            font = (self.style.fonts ["primary"]  .family, self.style.fonts["primary"].size_medium),
            fg   =  self.style.colors["secondary"].fg,
            bg   =  self.style.colors["secondary"].bg
            ),
            (42, 40)
        )

        moon_lbl  = \
            Widget(SpeckApp.__gen_label(self.root, self.style, f"Moon: {astro_i.moon_phase}"), ("+0", "+40"))
        sunrise_lbl  = \
            Widget(SpeckApp.__gen_label(self.root, self.style, f"Sunrise: {astro_i.sunrise}"), ("+0", "+30"))
        sunset_lbl  = \
            Widget(SpeckApp.__gen_label(self.root, self.style, f"Sunset: {astro_i.sunset}"), ("+0", "+30"))
        moonrise_lbl  = \
            Widget(SpeckApp.__gen_label(self.root, self.style, f"Moonrise: {astro_i.moonrise}"), ("+0", "+30"))
        moonset_lbl  = \
            Widget(SpeckApp.__gen_label(self.root, self.style, f"Moonset: {astro_i.moonset}"), ("+0", "+30"))

        back_btn = Widget(tk.Button(
            self.root,
            text    = "Back",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 4,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 0,
            command = lambda: self.forecast_screen(info)
            ),
            (28,  523) # pos
        )
        calc_btn = Widget(tk.Button(
            self.root,
            text    = "Calc",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 4,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 0,
            command = lambda: Calculator().run()
            ),
            ("+70", 523) # pos
        )
        docs_btn = Widget(tk.Button(
            self.root,
            text    = "?",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 4,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 0,
            command = lambda: self.docs(self.astro_screen, info)
            ),
            ("+70", 523) # pos
        )

        self.widget_manager.extend([
            loc_lbl,

            moon_lbl,
            sunrise_lbl,
            moonrise_lbl,
            moonset_lbl,
            sunset_lbl,

            back_btn,
            calc_btn,
            docs_btn
        ])
        self.widget_manager.render_all(self.main_canvas.internal)

    def docs(self, parent, *args, **kwargs):
        """Link to the documentation."""

        self.__clear_with_bg('etc/exports/rick.png')

        docs_label = Widget(tk.Label(
            self.root,
            text = "speck.rtfd.io",
            font = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_big),
            fg   =  self.style.colors["secondary"].fg,
            bg   =  self.style.colors["secondary"].bg
            ),
            (84, 140)
        )

        back_btn = Widget(tk.Button(
            self.root,
            text    = "Back",
            font    = (self.style.fonts["primary"].family, self.style.fonts["primary"].size_small),
            width   = 4,
            fg      = self.style.colors["primary"].fg,
            bg      = self.style.colors["primary"].bg,
            bd      = 0,
            command = lambda: parent(*args, **kwargs)
            ),
            (28,  523) # pos
        )

        self.widget_manager.extend([docs_label, back_btn])
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
