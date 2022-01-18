# -*- coding: UTF-8 -*-
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import Rate
import Fit
import MD


class Main(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Transitivity')
        self.geometry("1000x700+50+50")
        self.resizable(False, False)
        try:self.wm_iconbitmap('transitivity.ico')
        except:pass

        menu = Menu(self)
        self.config(menu=menu)
        subMenu = Menu(menu)

        menu.add_cascade(label='Help', menu=subMenu)
        subMenu.add_command(label='About', command=self.About)
        subMenu.add_command(label='Manual', command=self.Manual)
        subMenu.add_separator()
        subMenu.add_command(label='Exit', command=self.Exit)


        self.configure_tabs()
        self.Tab_Rate()
        self.Tab_MD()
        self.Tab_Fit()
        Rate.Rate(self.tab_rate)
        MD.MD(self.tab_md)
        Fit.Fit(self.tab_fit)

    def configure_tabs(self):
        for rows in range(0,50):
            self.rowconfigure(rows, weight=1)
            self.columnconfigure(rows, weight=1)
            rows += 1
        self.tabs = ttk.Notebook(self)
        self.tabs.grid(row=1, column=0,columnspan=50,rowspan=49,sticky='NESW')

    def Tab_Rate(self):
        self.tab_rate = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_rate,text="Rate Constant")

    def Tab_MD(self):
        self.tab_md = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_md,text="Molecular Dynamic")

    def Tab_Fit(self):
        self.tab_fit = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_fit, text="Fitting")

    def About(self):
        t = Toplevel(root)
        t.geometry("600x200")
        t.resizable(False, False)
        try:root.wm_iconbitmap('transitivity.ico')
        except:pass
        Label(t, text="\nTransitivity - Code").pack()
        Label(t, text="\nProgram developed by:\n\nHugo Gontijo Machado, Flávio Olimpio Sanches Neto,\nNayara Dantas Coutinho, Kleber Carlos Mundim,\nVincenzo Aquilanti and Valter Henrique Carvalho Silva.\n").pack()
        Label(t,text="For more information, please access: https://fatioleg.wixsite.com/vhcs/transitivity").pack()

    def Manual(self):
        try:
            os.startfile("manual_Transitivity.pdf")
        except:
            messagebox.showwarning(title='Warning',message='Please Download the manual at the address:\n\nhttps://fatioleg.wixsite.com/vhcs/transitivity')

    def Exit(self):
        root.destroy()

if __name__ == '__main__':
    root = Main()
    root.mainloop()