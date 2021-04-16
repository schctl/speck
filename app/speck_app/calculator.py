"""
Sample Calculator.

Authors:
    Nevin Jose
"""

import tkinter as tk

__all__ = [
    'Calculator'
]

class Calculator:
    """Simple calculator app."""

    def __init__(self):
        self._math = ""
        self._first_num = 1

    def run(self):
        """Runs the calculator under a new Tk instance."""
        root = tk.Tk()
        root.title("Simple Calculator")
        root.resizable(width=False, height="false")

        e = tk.Entry(root, width=35, borderwidth=15)
        e.grid(row=0, column=0, columnspan=3, padx=30, pady=40)

        # ---- Get and set values for the entry -----------

        def entry_get_int():
            entry = e.get()
            return int(entry if entry != '' else 0)

        def button_clear():
            e.delete(0, tk.END)

        def button_click(number):
            button_clear()

            e.insert(0, str(e.get()) + str(number))

        def button_add():
            self._math = 'add'
            self._first_num = entry_get_int()

            button_clear()

        def button_sub():
            self._math = 'sub'
            self._first_num = entry_get_int()

            button_clear()

        def button_multiply():
            self._math = 'mult'
            self._first_num = entry_get_int()

            button_clear()

        def button_div():
            self._math = 'div'
            self._first_num = entry_get_int()

            button_clear()

        def button_pwr():
            self._math = 'pow'
            self._first_num = entry_get_int()

            button_clear()

        def button_root():
            self._math = 'root'
            self._first_num = entry_get_int()

            button_clear()

        def button_mod():
            self._math = 'mod'
            self._first_num = entry_get_int()

            button_clear()

        def button_quo():
            self._math = 'floord'
            self._first_num = entry_get_int()

            button_clear()

        def button_equal():
            second_num = e.get()

            button_clear()

            if self._math == 'add':
                e.insert(0, self._first_num + int(second_num))

            elif self._math == 'sub':
                e.insert(0, self._first_num - int(second_num))

            elif self._math == 'mult':
                e.insert(0, self._first_num * int(second_num))

            elif self._math == 'div':
                if second_num == 0:
                    print('not defined')
                else:
                    e.insert(0, self._first_num / int(second_num))

            elif self._math == 'pow':
                e.insert(0, self._first_num ** int(second_num))

            elif self._math == 'root':
                e.insert(0, int(second_num) ** (1 / self._first_num))

            elif self._math == 'mod':
                e.insert(0, self._first_num % int(second_num))

            elif self._math == 'floord':
                e.insert(0, self._first_num // int(second_num))

        # -------------------------------------------------

        tk.Button(root, text="1",     padx=40, pady=20, command=lambda: button_click(1)) .grid(row=4, column=0, columnspan=1)
        tk.Button(root, text="2",     padx=40, pady=20, command=lambda: button_click(2)) .grid(row=4, column=1, columnspan=1)
        tk.Button(root, text="3",     padx=40, pady=20, command=lambda: button_click(3)) .grid(row=4, column=2, columnspan=1)

        tk.Button(root, text="4",     padx=40, pady=20, command=lambda: button_click(4)) .grid(row=3, column=0, columnspan=1)
        tk.Button(root, text="5",     padx=40, pady=20, command=lambda: button_click(5)) .grid(row=3, column=1, columnspan=1)
        tk.Button(root, text="6",     padx=40, pady=20, command=lambda: button_click(6)) .grid(row=3, column=2, columnspan=1)

        tk.Button(root, text="7",     padx=40, pady=20, command=lambda: button_click(7)) .grid(row=2, column=0, columnspan=1)
        tk.Button(root, text="8",     padx=40, pady=20, command=lambda: button_click(8)) .grid(row=2, column=1, columnspan=1)
        tk.Button(root, text="9",     padx=40, pady=20, command=lambda: button_click(9)) .grid(row=2, column=2, columnspan=1)

        tk.Button(root, text="0",     padx=40, pady=20, command=lambda: button_click(0)) .grid(row=5, column=1, columnspan=1)

        tk.Button(root, text="+",     padx=40, pady=20, command=button_add)              .grid(row=5, column=3, columnspan=1)
        tk.Button(root, text="=",     padx=39, pady=20, command=button_equal)            .grid(row=5, column=2, columnspan=1)
        tk.Button(root, text="CLEAR", padx=26, pady=20, command=button_clear)            .grid(row=5, column=0, columnspan=1)

        tk.Button(root, text="-",     padx=40, pady=20, command=button_sub)              .grid(row=4, column=3, columnspan=1)
        tk.Button(root, text="x",     padx=40, pady=20, command=button_multiply)         .grid(row=3, column=3, columnspan=1)
        tk.Button(root, text="/",     padx=40, pady=20, command=button_div)              .grid(row=2, column=3, columnspan=1)

        tk.Button(root, text="x^y",   padx=33, pady=20, command=button_pwr)              .grid(row=1, column=2,columnspan=1)
        tk.Button(root, text="x√",    padx=36, pady=20, command=button_root)             .grid(row=1, column=1,columnspan=1)
        tk.Button(root, text="%",     padx=38, pady=20, command=button_mod)              .grid(row=1, column=0,columnspan=1)
        tk.Button(root, text="//",    padx=38, pady=20, command=button_quo)              .grid(row=1, column=3,columnspan=1)

        #put buttons on screen

        root.mainloop()
