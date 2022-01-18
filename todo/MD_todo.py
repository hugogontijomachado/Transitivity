# -*- coding: UTF-8 -*-
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os


class MD:
    def __init__(self,root):
#        root.resizable(False, False)
        #root.geometry("1000x700+50+50")
        tab = self.configure_tabs(root)

        tab_single = ttk.Frame(tab)
        tab.add(tab_single,text="Single Input")
        self.run_single_tab(tab_single)

        tab_multiple = ttk.Frame(tab)
        tab.add(tab_multiple,text="Multiple Inputs")
        #self.run_multiple_tab(tab_multiple)


        tab_analysis = ttk.Frame(tab)
        tab.add(tab_analysis, text="Analysis")
        #self.run_analysys_tab(tab_analysis)

    def run_multiple_tab(self,parent):
        # Frames
        pady = 6
        framem = Frame(parent)
        framem.pack(pady=pady, expand=TRUE, anchor=CENTER)
        title = Label(framem, text="Molecular Dynamics",font=('arial', 30, 'bold') )
        title.pack(pady=10)


        framem1 = LabelFrame(framem, text="Open files ('.gjf')", bd=5, relief=GROOVE)
        framem1.pack(pady=pady+10, fill=X, ipady=8)

        framem1_1 = Frame(framem1)
        framem1_1.pack(anchor=CENTER,expand=True,fill=BOTH)
        framem1_2 = Frame(framem1)
        framem1_2.pack(anchor=CENTER,expand=True,fill=BOTH)

        framemf = Frame(framem, bd=5, relief=GROOVE)
        framemf.pack(pady=pady+10,expand=True,anchor=CENTER)


        padx = 6

        framemf1 = Frame(framemf, bd=5)
        framemf1.pack(padx=padx, fill=X,pady=6)
        framemf2 = Frame(framemf, bd=5)
        framemf2.pack(padx=padx, fill=X,pady=3)
        framemf3 = Frame(framemf, bd=5)
        framemf3.pack(padx=padx, fill=X,pady=3)
        framemf4 = Frame(framemf, bd=5)
        framemf4.pack(padx=padx, fill=X,pady=3)
        framemf5 = Frame(framemf, bd=5)
        framemf5.pack(padx=padx, fill=X,pady=3)


        padx = 6
        Label(framemf1,text="Temperature").pack(side=RIGHT,fill=BOTH,padx=padx+32)
        Label(framemf1,text="Dihedral\nAngle").pack(side=RIGHT,fill=BOTH,padx=padx+35)
        Label(framemf1,text="Bond\nAngle").pack(side=RIGHT,fill=BOTH,padx=padx+36)
        Label(framemf1,text="Bond\nLenght").pack(side=RIGHT,fill=BOTH,padx=padx+37)


        Label(framemf2,text="Minimum").pack(side=LEFT,fill=BOTH,padx=padx+9)
        self.bi = Entry(framemf2)
        self.bi.pack(side=LEFT,fill=BOTH,padx=padx)
        self.bi.insert(END,'5.0')
        self.ai = Entry(framemf2)
        self.ai.pack(side=LEFT,fill=BOTH,padx=padx)
        self.ai.insert(END,'0.0')
        self.di = Entry(framemf2)
        self.di.pack(side=LEFT,fill=BOTH,padx=padx)
        self.di.insert(END,'0.0')
        self.Ti = Entry(framemf2)
        self.Ti.pack(side=LEFT,fill=BOTH,padx=padx)
        self.Ti.insert(END,'300.0')


        Label(framemf3,text="Maximum").pack(side=LEFT,fill=BOTH,padx=padx+8)
        self.bf = Entry(framemf3)
        self.bf.pack(side=LEFT,fill=BOTH,padx=padx)
        self.bf.insert(END,'5.0')
        self.af = Entry(framemf3)
        self.af.pack(side=LEFT,fill=BOTH,padx=padx)
        self.af.insert(END,'360.0')
        self.df = Entry(framemf3)
        self.df.pack(side=LEFT,fill=BOTH,padx=padx)
        self.df.insert(END,'360.0')
        self.Tf = Entry(framemf3)
        self.Tf.pack(side=LEFT,fill=BOTH,padx=padx)
        self.Tf.insert(END,'300.0')

        Label(framemf4,text="Number\nof steps").pack(side=LEFT,fill=BOTH,padx=padx+13)
        self.stepsb = Entry(framemf4)
        self.stepsb.pack(side=LEFT,fill=X,padx=padx)
        self.stepsb.insert(END,'1')
        self.stepsa = Entry(framemf4)
        self.stepsa.pack(side=LEFT,fill=X,padx=padx)
        self.stepsa.insert(END,'1')
        self.stepsd = Entry(framemf4)
        self.stepsd.pack(side=LEFT,fill=X,padx=padx)
        self.stepsd.insert(END,'1')
        self.stepsT = Entry(framemf4)
        self.stepsT.pack(side=LEFT,fill=X,padx=padx)
        self.stepsT.insert(END,'1')

        #Button Number of Inputs
        self.bt_nbinp = Button(framemf5,text = "Number of inputs = ", command=self.number_inputs)
        self.bt_nbinp.pack(side=LEFT,anchor = CENTER)
        self.lb_nbinp =  Label(framemf5, text="")
        self.lb_nbinp.pack(side=LEFT, anchor=CENTER)
        self.number_inputs()

        #CheckButton Add Chiral
        self.Chiral_Var = BooleanVar()
        self.cb_chiral = Checkbutton(framemf5,text = "Add Chiral", variable = self.Chiral_Var)
        self.cb_chiral.pack(side=RIGHT,anchor = CENTER)

        # Open Button
        self.filename_1 = Button(framem1_1, text="File 1", command=self.Open_1, width=4, height=1)
        self.filename_1.pack(side=LEFT)
        self.listb_open_1 = Listbox(framem1_1, height=1, width=98, justify=CENTER)
        self.listb_open_1.pack(side=LEFT, fill=X)
        self.inputfilename_1 = ""

        self.filename_2 = Button(framem1_2, text="File 2", command=self.Open_2, width=4, height=1)
        self.filename_2.pack(side=LEFT)
        self.listb_open_2 = Listbox(framem1_2, height=1, width=98, justify=CENTER)
        self.listb_open_2.pack(side=LEFT, fill=X)
        self.inputfilename_2 = ""


        # Button Generate
        self.btm_gen = Button(framem, text="Generate\nMultiple Inputs", fg='blue', command=self.Generate_multiple, width=12, height=2,
                             bd=5, font=('Arial', 12, 'bold'))
        self.btm_gen.pack(pady=pady+10)

    def run_analysys_tab(self,parent):
        frame0 = Frame(parent,width=10)
        frame0.pack(pady=6, fill=BOTH, anchor=N)

        Label(frame0,text='Bond, Angle and Adiabaticity\n  Trajectory Plots', font=('arial', 30, 'bold')).pack(pady=10)

        frame1 = LabelFrame(frame0,text="Select Trajectory Directory",bd=5,relief=GROOVE)
        frame1.pack(pady=6,ipady=8,anchor=N)

        bt_path = Button(frame1, text="...", width=2, height=1)#,command=self.open_analysis)
        bt_path.pack(side=LEFT)

        self.listb_plot = Listbox(frame1,height=1, width=78, justify=CENTER)
        self.listb_plot.pack(side=LEFT,fill=X)
        """
        frame_tab = Frame(frame0,bd=5) ; frame_tab.pack(expand=True,fill=X,padx=80)

        tab = self.configure_tabs(frame_tab)

        tab_bond = ttk.Frame(tab)
        tab.add(tab_bond,text="Bonds")
        self.tab_bond(tab_bond)

        tab_angle = ttk.Frame(tab)
        tab.add(tab_angle, text="Angles")
        self.tab_angle(tab_angle)

        tab_adiabaticity = ttk.Frame(tab)
        tab.add(tab_adiabaticity, text="Adiabaticity")
        self.tab_adiabaticity(tab_adiabaticity)
        """

    def run_single_tab(self, parent):
        title = Label(parent, text="Molecular Dynamics", font=('arial', 30, 'bold'))
        title.pack(pady=10)
        # Frames
        pady = 6

        frame1 = LabelFrame(parent, text="Open file ('.xyz','.gjf','.out','.log')", bd=5, relief=GROOVE)
        frame1.pack(pady=pady, expand=True, ipady=8)#, fill=X)
        frame2 = LabelFrame(parent, text='Dynamic', bd=5)
        frame2.pack(pady=pady,expand=True)#, fill=X)

        frame5 = Frame(parent, bd=5)
        frame5.pack(pady=pady, fill=X)
        frame2_1 = Frame(frame2)
        frame2_1.pack()
        frame2_2 = Frame(frame2)
        frame2_2.pack()

        # Open Button
        self.bt_filename = Button(frame1, text="...", width=2, height=1, command=self.Open)
        self.bt_filename.pack(side=LEFT)
        self.listb_open = Listbox(frame1, height=1, width=78, justify=CENTER)
        self.listb_open.pack(side=LEFT, fill=X)
        self.inputfilename = ""
        # Type Calc Radio Buttons
        self.types = [
            ('Car Parrinello (CPMD)', 'CPMD', frame2_1),
            ('Path Integral (PIMD)', 'PIMD', frame2_1),
            ('Surface Hopping (TSH)', 'SHMD', frame2_1),
            ('Meta Dynamics (MTD)', 'MTD', frame2_2),
            ('Born Oppenheimer (BOMD)', 'BOMD', frame2_2)
        ]
        self.typecalc = StringVar()
        self.rb = {}
        for text, val, frame in self.types:
            self.rb[val] = Radiobutton(frame, text=text, variable=self.typecalc, value=val)
            self.rb[val].pack(side=LEFT, padx=5, pady=5)
        self.rb['CPMD'].select()

        # Button Generate
        self.bt_gen = Button(frame5, text="Generate Input", fg='blue', command=self.Generate, width=12, height=1,
                             bd=5, font=('Arial', 12, 'bold'))
        self.bt_gen.pack()

    def configure_tabs(self,parent):
        for rows in range(0,50):
            parent.rowconfigure(rows, weight=1)
            parent.columnconfigure(rows, weight=1)
            rows += 1
        tab = ttk.Notebook(parent)
        tab.pack(fill=BOTH, expand=TRUE, anchor=CENTER)
        return tab

    def Open(self):
        pass

    def Generate(self):
        pass

if __name__ == '__main__':
    root = Tk()
    MD(root)
    root.mainloop()