"""Simple calculator app."""

from tkinter import *

def run_calc():
    root = Tk()
    root.title('Simple Calculator')
    root.resizable(width=False, height="false")

    e = Entry(root, width=35, borderwidth=15)
    e.grid(row=0, column=0, columnspan=3, padx=30, pady=40)

    def button_click(number):
        current = e.get()
        e.delete(0, END)
        e.insert(0, str(current) + str(number))

    def button_clear():
        e.delete(0, END)

    def button_add():
        first_num = e.get()
        global f_num
        global math
        math = 'addition'
        f_num = int(first_num)
        e.delete(0, END)

    def button_equal():
        second_num = e.get()
        e.delete(0, END)

        if math == "addition":
            e.insert(0, f_num + int(second_num))

        elif math == "subtraction":
            e.insert(0, f_num - int(second_num))

        elif math == "multiplication":
            e.insert(0, f_num * int(second_num))

        elif math == "division":
            if second_num == 0:
                print('not defined')
            else:
                e.insert(0, f_num / int(second_num))

        elif math == "power":
            e.insert(0, f_num ** int(second_num))

        elif math == "root":
            e.insert(0, int(second_num)**(1/f_num))

        elif math == "remainder":
            e.insert(0, f_num % int(second_num))

        elif math == "double divide":
            e.insert(0, f_num // int(second_num))

    def button_sub():
        first_num = e.get()
        global f_num
        global math
        math = 'subtraction'
        f_num = int(first_num)
        e.delete(0, END)

    def button_multiply():
        first_num = e.get()
        global f_num
        global math
        math = 'multiplication'
        f_num = int(first_num)
        e.delete(0, END)

    def button_div():
        first_num = e.get()
        global f_num
        global math
        math = 'division'
        f_num = int(first_num)
        e.delete(0, END)

    def button_pwr():
        first_num = e.get()
        global f_num
        global math
        math = 'power'
        f_num = int(first_num)
        e.delete(0, END)

    def button_root():
        first_num = e.get()
        global f_num
        global math
        math = 'root'
        f_num = int(first_num)
        e.delete(0, END)

    def button_mod():
        first_num = e.get()
        global f_num
        global math
        math = 'remainder'
        f_num = int(first_num)
        e.delete(0, END)

    def button_quo():
        first_num = e.get()
        global f_num
        global math
        math = 'double divide'
        f_num = int(first_num)
        e.delete(0, END)

    button_1 = Button(root, text="1", padx=40, pady=20, command=lambda: button_click(1)).grid(row=4, column=0, columnspan=1)
    button_2 = Button(root, text="2", padx=40, pady=20, command=lambda: button_click(2)).grid(row=4, column=1, columnspan=1)
    button_3 = Button(root, text="3", padx=40, pady=20, command=lambda: button_click(3)).grid(row=4, column=2, columnspan=1)

    button_4 = Button(root, text="4", padx=40, pady=20, command=lambda: button_click(4)).grid(row=3, column=0, columnspan=1)
    button_5 = Button(root, text="5", padx=40, pady=20, command=lambda: button_click(5)).grid(row=3, column=1, columnspan=1)
    button_6 = Button(root, text="6", padx=40, pady=20, command=lambda: button_click(6)).grid(row=3, column=2, columnspan=1)

    button_7 = Button(root, text="7", padx=40, pady=20, command=lambda: button_click(7)).grid(row=2, column=0, columnspan=1)
    button_8 = Button(root, text="8", padx=40, pady=20, command=lambda: button_click(8)).grid(row=2, column=1, columnspan=1)
    button_9 = Button(root, text="9", padx=40, pady=20, command=lambda: button_click(9)).grid(row=2, column=2, columnspan=1)

    button_0 = Button(root, text="0", padx=40, pady=20, command=lambda: button_click(0)).grid(row=5, column=1, columnspan=1)

    button_add   = Button(root, text="+",     padx=40, pady=20, command=button_add)  .grid(row=5, column=3, columnspan=1)
    button_equal = Button(root, text="=",     padx=39, pady=20, command=button_equal).grid(row=5, column=2, columnspan=1)
    button_clear = Button(root, text="CLEAR", padx=26, pady=20, command=button_clear).grid(row=5, column=0, columnspan=1)

    button_sub      = Button(root, text="-", padx=40, pady=20, command=button_sub)     .grid(row=4, column=3, columnspan=1)
    button_multiply = Button(root, text="x", padx=40, pady=20, command=button_multiply).grid(row=3, column=3, columnspan=1)
    button_div      = Button(root, text="/", padx=40, pady=20, command=button_div)     .grid(row=2, column=3, columnspan=1)

    button_pwr      = Button(root, text="x^y", padx=33, pady=20, command=button_pwr) .grid(row=1, column=2, columnspan=1)
    button_root     = Button(root, text="x√",  padx=36, pady=20, command=button_root).grid(row=1, column=1, columnspan=1)
    button_mod      = Button(root, text="%",   padx=38, pady=20, command=button_mod) .grid(row=1, column=0, columnspan=1)
    button_quotient = Button(root, text="//",  padx=38, pady=20, command=button_quo) .grid(row=1, column=3, columnspan=1)

    # put buttons on screen

    root.mainloop()
