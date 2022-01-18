# -*- coding: UTF-8 -*-
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import Fit_A
import Fit_T


class Fit:
    def __init__(self,tab):

        self.tab=tab

        self.configure_tabs()
        self.Tab_Fit_A()
        self.Tab_Fit_T()
        Fit_A.Fit(self.tab_fit_a)
        Fit_T.Fit(self.tab_fit_t)

    def configure_tabs(self):
        for rows in range(0,50):
            self.tab.rowconfigure(rows, weight=1)
            self.tab.columnconfigure(rows, weight=1)
            rows += 1
        self.tabs = ttk.Notebook(self.tab)
        self.tabs.pack(fill=BOTH, expand=TRUE, anchor=CENTER)

    def Tab_Fit_A(self):
        self.tab_fit_a = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_fit_a, text="Arrhenius Plot")

    def Tab_Fit_T(self):
        self.tab_fit_t = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_fit_t, text="Transitivity Plot")
    