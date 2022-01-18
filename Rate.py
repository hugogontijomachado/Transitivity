# -*- coding: UTF-8 -*-
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import os
import numpy as np
from RateLib import reaction, Title
import matplotlib.pyplot as plt
import matplotlib

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


class Rate:
    __species = {
        'Reac1': 'Reactant 1',
        'Reac2': 'Reactant 2',
        'TS': 'Transition State',
        'Prod1': 'Product 1',
        'Prod2': 'Product 2'
    }
    __speciesListBox = {}
    __speciesEnVar = {}
    __speciesEnEntry = {}
    __speciesFilename = {}
    __labelTemp = {}
    __txtTemp = {}
    __TempVar = {}
    __T = {}
    def __init__(self,parent):
        #parent.geometry("1000x700+50+50")
        #parent.resizable(False, False)

        ### Create Variables
        self.__variables()

        ### Configure Tabs
        self.__configureTabs(parent)

        ### Create Tabs
        ctstTab = ttk.Frame(parent)
        self.__tabs.add(ctstTab, text="Conventional TST")
        self.__ctstTab(ctstTab)

        vtstTab = ttk.Frame(parent)
        self.__tabs.add(vtstTab, text="Variational TST")
        self.__vtstTab(vtstTab)

    def __configureTabs(self,parent):
        for rows in range(0,50):
            parent.rowconfigure(rows, weight=1)
            parent.columnconfigure(rows, weight=1)
            rows += 1
        self.__tabs = ttk.Notebook(parent)
        self.__tabs.pack(fill=BOTH, expand=TRUE, anchor=CENTER)

    def __ctstTab(self,parent):

        ##Title
        title = Label(parent, text="Rate Constant", font=('arial', 27, 'bold'))
        title.pack(pady=35,anchor=CENTER)


        ### Separator
        sep = Frame(parent,height=3, bd=1, relief=SUNKEN)
        sep.pack(fill=X, padx=11, pady=10,anchor=N)

        ### Frame Species
        frameSpecies = Frame(parent)
        frameSpecies.pack(anchor = N, expand=TRUE, fill = BOTH)
        self.__BuildframeSpecies(frameSpecies)

        ### Separator
        #sep = Frame(height=3, bd=1, relief=SUNKEN)
        #sep.pack(fill=X, padx=5,pady=10)

        ### Frame Buttons and Temperature
        frameBtTemp = Frame(parent)
        frameBtTemp.pack(expand=TRUE, fill=X,ipady=5)
        self.__BuildframeBtTemp(frameBtTemp)

        ### Separator
        #sep = Frame(parent,height=3, bd=3, relief=GROOVE, bg='black')
        #sep.pack(fill=X, padx=5, pady=15)

    def __vtstTab(self,parent):

        ##Title
        title = Label(parent, text="Rate Constant", font=('arial', 27, 'bold'))
        title.pack(pady=35,anchor=CENTER)

        ## Label Frame
        lbframe = LabelFrame(parent, text="Reaction Path", bd=2, relief=GROOVE)
        lbframe.pack(side=TOP, expand=TRUE, ipadx=15, ipady=15, fill=X, padx=60)

        openBt = Button(lbframe, text="Open File", command=self.__Open, width=8, height=1, bd=5)
        openBt.pack(side=TOP, anchor=CENTER)#, padx=5)

        self.__vtstFilename = ''

        self.__vtstListBox = Listbox(lbframe, height=1, font=('arial', 10))
        self.__vtstListBox.configure(justify=CENTER)
        self.__vtstListBox.pack(side=TOP, expand=TRUE, anchor=W, fill=X,padx=20)

        ## Frame Bottom
        frameB = Frame(parent)
        frameB.pack(side=BOTTOM,expand=TRUE,anchor=N)

        frameBL = Frame(frameB)
        frameBL.pack(side=LEFT,expand=TRUE,fill=BOTH)

        self.__BuildframeTemp(frameBL, 'vtst')

        ### Separator
        sep = Frame(frameB,width=0, bd=0, relief=SUNKEN)
        sep.pack(side=LEFT, fill=Y, pady=25,padx=100)

        frameBR = Frame(frameB)
        frameBR.pack(side=LEFT, expand=TRUE, fill=BOTH)

        calcBt = Button(frameBR, text="Calculate", fg='blue', command=self.__Calculate, font=('Arial', 12, 'bold'),width=14, height=1, bd=5)
        calcBt.pack(side=LEFT, anchor = CENTER )#, pady=8)

    def __BuildframeBtTemp(self,parent):
        ## Frame Left
        frameL = Frame(parent)
        frameL.pack(side=LEFT,expand=TRUE,fill=BOTH)
        self.__BuildframeTemp(frameL, 'ctst')

        ### Separator
        sep = Frame(parent,width=3, bd=1, relief=SUNKEN)
        sep.pack(side=LEFT, fill=Y)

        ## Frame Center
        frameC = Frame(parent)
        frameC.pack(side=LEFT,expand=TRUE, fill=BOTH)

        calcBt = Button(frameC, text="Calculate", fg='blue', command=self.__Calculate,font=('Arial', 12, 'bold'), width=12, height=1, bd=5)
        calcBt.pack(side=TOP,expand=TRUE)

        btQuick = Button(frameC, text= "Quick Check on\nSpecies Properties",height= 2, width=18,relief=RAISED,command=self.__quick)
        btQuick.pack(side=TOP,expand=TRUE)

        ### Separator
        sep = Frame(parent,width=3, bd=1, relief=SUNKEN)
        sep.pack(side=LEFT, fill=Y)

        ## Frame Right
        frameR = Frame(parent)
        frameR.pack(side=LEFT,expand=TRUE, fill=BOTH)

        self.__SpeciesPropBt = Button(frameR, fg='blue', text="Species Properties", height=1, width=18,relief=GROOVE, command=self.__SpeciesProperties, state=DISABLED)
        self.__SpeciesPropBt.pack(expand=TRUE)

        self.__ReacPropBt = Button(frameR, fg='blue', text="Reaction Properties", height=1, width=18,relief=GROOVE, command=self.__ReactionProperties, state=DISABLED)
        self.__ReacPropBt.pack(expand=TRUE)

        self.__SolvPropBt = Button(frameR, fg='blue', text="Solvent Effect", height=1, width=18, relief=GROOVE,command=self.__SolventProperties, state=DISABLED)
        self.__SolvPropBt.pack(expand=TRUE)

    def __BuildframeTemp(self,parent,theory):

        self.__labelTemp[theory] = Label(parent, text="Set Temperature", fg='gray')
        self.__labelTemp[theory].pack()#padx=50,anchor=W)
        self.__txtTemp[theory] = ScrolledText(parent, height=10, width=10,state=DISABLED,bg='gray95')
        self.__txtTemp[theory].pack()#padx=50)
        TempCb = Checkbutton(parent, text="Default Temperature Range", variable=self.__TempVar[theory],command=lambda theory=theory: self.__SetTemp(theory))
        TempCb.select()
        TempCb.pack()

    def __BuildframeSpecies(self,parent):
        ipadx = 5
        ipady = 0
        bd = 2

        frameR1 = LabelFrame(parent, text = "Reactant 1", bd=bd, relief=GROOVE)
        frameR1.pack(side=LEFT, expand=TRUE, anchor=CENTER, ipadx=ipadx, ipady=ipady)
        self.__BuildlbframeSpecies(frameR1,'Reac1')

        frameR2 = LabelFrame(parent,text = "Reactant 2", bd=bd, relief=GROOVE)
        frameR2.pack(side=LEFT, expand=TRUE, anchor=CENTER, ipadx=ipadx, ipady=ipady)
        self.__BuildlbframeSpecies(frameR2, 'Reac2')

        frameTS = LabelFrame(parent, text = "Transition State", bd=bd, relief=GROOVE)
        frameTS.pack(side=LEFT, expand=TRUE, anchor=CENTER, ipadx=ipadx, ipady=ipady)
        self.__BuildlbframeSpecies(frameTS, 'TS')

        frameP1 = LabelFrame(parent, text = "Product 1", bd=bd, relief=GROOVE)
        frameP1.pack(side=LEFT, expand=TRUE, anchor=CENTER, ipadx=ipadx, ipady=ipady)
        self.__BuildlbframeSpecies(frameP1, 'Prod1')

        frameP2 = LabelFrame(parent,  text = "Product 2", bd=bd, relief=GROOVE)
        frameP2.pack(side=LEFT, expand=TRUE, anchor=CENTER, ipadx=ipadx, ipady=ipady)
        self.__BuildlbframeSpecies(frameP2, 'Prod2')

    def __BuildlbframeSpecies(self,parent,species):
        species_bt = Button(parent, text ="Open File", command=lambda species = species: self.__Open(species), bd=3, relief=RAISED)
        species_bt.pack(side= TOP, pady = 5)

        self.__speciesListBox[species] = Listbox(parent, height=1, width=21, font=('arial', 10))
        self.__speciesListBox[species].configure(justify=CENTER)
        self.__speciesListBox[species].pack(side = TOP)

        self.__speciesEnEntry[species] = Entry(parent, width=25)
        self.__speciesEnEntry[species]["state"] = DISABLED
        self.__speciesEnEntry[species].pack(side = BOTTOM, padx=4, pady=5)

        speciesEnCb = Checkbutton(parent, text="Set Energy (a.u.)",variable=self.__speciesEnVar[species],command=lambda species=species: self.__SetEn(species), height=2)
        speciesEnCb.deselect()
        speciesEnCb.pack(side = BOTTOM)#, anchor=SW)

    def __variables(self):
        for species in self.__species:
            self.__speciesEnVar[species] = BooleanVar()
        self.__TempVar['ctst'] = BooleanVar()
        self.__TempVar['vtst'] = BooleanVar()

    def __SetTemp(self,theory):
        state, bg, fg = [(NORMAL, 'white', 'black'), (DISABLED, 'gray95', 'gray')][self.__TempVar[theory].get()]
        self.__txtTemp[theory]['state'] = state
        self.__txtTemp[theory]['bg'] = bg
        self.__labelTemp[theory]['fg'] = fg
        if self.__TempVar[theory].get() == 0:
            self.__txtTemp[theory].focus_force()

    def __SetEn(self,species):
        self.__speciesEnEntry[species]["state"] = (DISABLED,NORMAL)[self.__speciesEnVar[species].get()]

    def __Open(self,species):
        self.__speciesFilename[species] = filedialog.askopenfilename(title="Select file", filetypes=[("Gaussian Output files", "*.log;*.out"),("all files", "*.*")])
        self.__speciesListBox[species].delete(0, END)
        self.__speciesListBox[species].insert(1,os.path.basename(self.__speciesFilename[species]))

    def __vtstOpen(self):
        self.__vtstFilename = filedialog.askopenfilename(title="Select file", filetypes=[("Gaussian Output files", "*.log;*.out"),("all files", "*.*")])
        self.__vtstListBox[species].delete(0, END)
        self.__vtstListBox[species].insert(1,os.path.basename(self.__speciesFilename[species]))

    def __TempCheck(self,theory):
        self.__T[theory] = self.__txtTemp[theory].get(1.0, END).splitlines()
        try:
            self.__T[theory] = [float(x) for x in self.__T[theory] if x != ""]
            return True
        except:
            messagebox.showwarning(title="Temperature Warning!", message="Invalid temperature range")
            #self.tab.focus_force()
            return False

    def __Calculate(self):
        a = reaction()
        a.setDefaultTemp()
        self.__SpeciesPropBt['state'] = DISABLED
        self.__ReacPropBt['state'] = DISABLED
        self.__SolvPropBt['state'] = DISABLED

        if not os.path.isfile(self.__speciesFilename['Reac1']) and not os.path.isfile(self.__speciesFilename['Reac2']):
            messagebox.showerror(title="Error", message="Select at least one reactant")
            #self.tab.focus_force()
            return

        if not os.path.isfile(self.__speciesFilename['TS']):
            messagebox.showerror(title="Error", message="Select the Transition State file")
            #self.tab.focus_force()
            return

        if self.__TempVar['ctst'] == False:
            if self.__TempCheck('ctst'):
                a.setTemp(self.__T['ctst'])

        self.__addSpecies(a)

        a.run_reaction()
        self.__SpeciesPropBt['state'] = ACTIVE
        self.__ReacPropBt['state'] = ACTIVE
        try:
            a.Kramer()
            self.__SolvPropBt['state'] = ACTIVE
        except:
            pass
        try:
            a.Smoluchowski()
            self.__SolvPropBt['state'] = ACTIVE
        except:
            pass

        self.reaction = a
        messagebox.showinfo(title="Success!", message="Successful Calculation!")

    def __addSpecies(self,a):
        if os.path.isfile(self.__speciesFilename['Reac1']):
            a.add_reactant(self.__speciesFilename['Reac1'])
            if self.__speciesEnVar['Reac1'].get():
                try:
                    En = float(self.__speciesEnEntry['Reac1'].get())
                    a.setEnReac(En, -1)
                except:
                    messagebox.showwarning(title="Warning", message="The Reactant 1 energy was not set or is not a float.\nThe value was extracted from the file")
        if os.path.isfile(self.__speciesFilename['Reac2']):
            a.add_reactant(self.__speciesFilename['Reac2'])
            if self.__speciesEnVar['Reac2'].get():
                try:
                    En = float(self.__speciesEnEntry['Reac2'].get())
                    a.setEnReac(En, -1)
                except:
                    messagebox.showwarning(title="Warning",
                                           message="The Reactant 2 energy was not set or is not a float.\nThe value was extracted from the file")
        if os.path.isfile(self.__speciesFilename['TS']):
            a.add_ts(self.__speciesFilename['TS'])
            if self.__speciesEnVar['TS'].get():
                try:
                    En = float(self.__speciesEnEntry['TS'].get())
                    a.setEnTS(En)
                except:
                    messagebox.showwarning(title="Warning",
                                           message="The Transition State energy was not set or is not a float.\nThe value was extracted from the file")
        if os.path.isfile(self.__speciesFilename['Prod1']):
            a.add_product(self.__speciesFilename['Prod1'])
            if self.__speciesEnVar['Prod1'].get():
                try:
                    En = float(self.__speciesEnEntry['Prod1'].get())
                    a.setEnProd(En, -1)
                except:
                    messagebox.showwarning(title="Warning",
                                           message="The Product 1 energy was not set or is not a float.\nThe value was extracted from the file")
        if os.path.isfile(self.__speciesFilename['Prod2']):
            a.add_product(self.__speciesFilename['Prod2'])
            if self.__speciesEnVar['Prod2'].get():
                try:
                    En = float(self.__speciesEnEntry['Prod2'].get())
                    a.setEnProd(En, -1)
                except:
                    messagebox.showwarning(title="Warning",
                                           message="The Product 2 energy was not set or is not a float.\nThe value was extracted from the file")

    def __vtstCalculate(self):
        pass

    def __quick(self):
        if True:
            filename = filedialog.askopenfilename(title="Select file", filetypes=[("Gaussian Output files", "*.log;*.out"),("all files", "*.*")])
            a = reaction()
            a.setDefaultTemp()
            if self.__TempVar['ctst'] == False:
                if self.__TempCheck('ctst'):
                    a.setTemp(self.__T['ctst'])
            if os.path.isfile(filename):
                a.add_reactant(filename)
        #except:
        #    return

        SpeciesProperties(a, True)

    def __ReactionProperties(self):
        ReactionProperties(self.reaction)

    def __SpeciesProperties(self):
        SpeciesProperties(self.reaction,False)

    def __SolventProperties(self):
        SolventProperties(self.reaction)

class SpeciesProperties:
    dict1 = {
        'basefilename': ("Filename", "Filename: ", '1'),
        'zpe': ("Zero Point Energy (kcal/mol)", "ZPE (kcal/mol) (298.15K): ", '1'),
        'En': ("Energy+ZPE (kcal/mol)", "Energy (kcal/mol) (298.15K):", '1'),
        'Ent': ("Enthalpy+ZPE (kcal/mol)", 'Enthalpy (kcal/mol) (298.15K):', '1'),
        'EnG': ("Gibbs Energy+ZPE (kcal/mol)", 'Gibbs Energy (kcal/mol) (298.15K):', '1'),
        'mass': ("Molecular Mass (u.a)", 'Molecular Mass (a.u.): ', '1'),
        'DoF': ("Degree of Freedom", 'Degree of Freedom: ', '3'),
        'NSym': ("Symetry number", 'Symmetry Number: ', '3'),
        'freqi': ("Imaginary frequency of the Transition State", 'Imaginary Frequency (cm^-1): ', '3'),
        'Qe': ("(Qe) Electronic Partition Coefficient", 'Electronic Partition Coefficient: ', '2')
    }
    dict2 = {
        'Qt': ("(Qt) Translational Partition Funcion", "Qt: ", '2', 'Q Transational'),
        'Qr': ("(Qr) Rotational Partition Function", "Qr: ", '2', 'Q Rotational'),
        'Qv': ("(Qv) Vibrational Partition Function", "Qv: ", '2', 'Q Vibrational'),
        'QTot': ("(QTot) Total Partition Function", "Q Total: ", '2', 'Q Total')
    }
    dict3 = {
        'Trot': ("Rotational Temperatures", "Trot: ", '3'),
        'Tvib': ("Vibrational Temperatures", "Tvib: ", '3'),
    }
    def __init__(self,reaction,quick):
        parent = Toplevel()
        parent.focus_force()
        parent.title('Species Properties')
        #parent.geometry("1000x800+50+50")
        parent.geometry("700x550+50+50")
        parent.resizable(False, False)
        try:parent.wm_iconbitmap('transitivity.ico')
        except:pass

        self.reaction = reaction
        self.quick = quick
        if not quick:
            self.dict0 = {'Reactant 1': self.reaction.reac[0],
                    'Reactant 2': self.reaction.reac[1],
                    'Transition State': self.reaction.ts,
                    'Product 1': self.reaction.prod[0],
                    'Product 2': self.reaction.prod[1]}
        else:
            self.dict0 = {'Reactant 1': self.reaction.reac[0],
                          'Reactant 2': self.reaction.reac[0],
                          'Transition State': self.reaction.reac[0],
                          'Product 1': self.reaction.reac[0],
                          'Product 2': self.reaction.reac[0]}
        self.__variables()

        title = Label(parent, text="Species Properties", font=('arial', 27, 'bold'))
        title.pack(pady=35,anchor=CENTER)

        ### Separator
        #sep = Frame(parent,height=3, bd=1, relief=SUNKEN)
        #sep.pack(fill=X, padx=11, pady=10,anchor=N)

        self.__buildMenu(parent)

        frame1 = Frame(parent)
        frame1.pack(expand=True, fill=BOTH,side=TOP)

        frameRight = Frame(frame1)  # ,text='Thermodynamic Properties',font = ('Arial',12))
        frameRight.pack(expand=False, fill=BOTH, side=RIGHT, padx=10, pady=10)
        self.__buildFrameRight(frameRight)

        frameLeft = Frame(frame1)
        frameLeft.pack(expand=True, fill=BOTH, side=LEFT)
        self.__buildFrameLeft(frameLeft)


    def __buildFrameLeft(self,parent):
        padx = 25
        pady = 15
        rb = {}
        for key,value in self.dict0.items():
            if not self.quick:
                rb[key] = ttk.Radiobutton(parent, text=key + '\n' + "({})".format(os.path.basename(value['filename'])), variable=self.SpecieVar, value=key, command=self.__display);
            else:
                if key == 'Reactant 1':
                    rb[key] = ttk.Radiobutton(parent, text=key + '\n' + "({})".format(os.path.basename(value['filename'])), variable=self.SpecieVar, value=key, command=self.__display);
                else:
                    rb[key] = ttk.Radiobutton(parent, text=key + '\n', variable=self.SpecieVar, value=key, command=self.__display);
                    rb[key].configure(state=DISABLED)
            rb[key].pack(side=TOP,   padx=padx, pady=pady)
        rb['Reactant 1'].invoke()

        frame0 = Frame(parent)
        frame0.pack(side=TOP,expand=True)#,fill=BOTH)

        bt_clear = Button(frame0, text='Clear', command=self.__clear, fg='red', bd=3, width=10, font=('Arial', 10))
        bt_clear.pack(pady=6, expand=True, side=LEFT,padx=padx)  #

        bt_save = Button(frame0, text='Save *txt file', command=self.__save, fg='blue', bd=3, width=10, font=('Arial', 10))
        bt_save.pack(pady=6, expand=True, side=LEFT,padx=padx)  #

    def __save(self):
        try:
            save_filename = filedialog.asksaveasfilename(title="Save File", defaultextension='txt', filetypes=(
            ("txt files", "*.txt"), ("dat files", "*.dat"), ("all files", "*.*")))
            self.save_file = open(save_filename, 'w', encoding="utf-8")
        except:
            return

        for value in self.Var.values():
            value.set(True)
        if self.SpecieVar.get() != 'Transition State':
            self.Var['freqi'].set(False)

        specie = self.dict0[self.SpecieVar.get()]

        self.save_file.writelines(Title())
        self.save_file.writelines('Properties of Specie: '+ specie['basefilename']+'\n\n')

        for dict in self.dict1, self.dict3:
            for key,value in dict.items():
                if self.Var[key].get() is True:
                    self.save_file.writelines(value[1] +'\t'+ str(specie[key]) + '\n')
        self.save_file.writelines("\n\n")

        self.save_file.writelines('{:^10s}\t'.format('T'))
        for key, value in self.dict2.items():
            self.save_file.writelines("{:^24s}\t".format(value[1]))
        self.save_file.writelines('\n\n')
        for i, T in enumerate(self.reaction.T):
            self.save_file.writelines('{:^10s}'.format("%.1f"%T))
            for key, value in self.dict2.items():
                self.save_file.writelines("{:^24s}\t".format(str(specie[key][i])))
            self.save_file.writelines('\n')
        self.save_file.close()

    def __clear(self):
        for value in self.Var.values():
            value.set(False)
        self.__display()

    def __buildFrameRight(self, parent):
        self.listbox = Listbox(parent,width=40, height=25,font=('arial', 10) ,justify=CENTER,selectmode=EXTENDED)
        self.listbox.pack(side=LEFT)
        scrollbar = Scrollbar(parent)
        scrollbar.pack(side=LEFT,fill=Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.__display()

    def __variables(self):
        self.Var = {}
        for item in self.dict1:
            self.Var[item] = BooleanVar()
            self.Var[item].set(True)
        for item in self.dict2:
            self.Var[item] = BooleanVar()
        for item in self.dict3:
            self.Var[item] = BooleanVar()

        self.SpecieVar = StringVar()
        self.SpecieVar.set('Reactant 1')

    def __buildMenu(self,parent):
        menubar = Menu(parent)

        thermoProperties_menu = Menu(menubar)
        for dict in self.dict1, self.dict2, self.dict3:
            for key,value in dict.items():
                thermoProperties_menu.add_checkbutton(label=value[0], onvalue=1, offvalue=0, variable=self.Var[key],command=self.__display)

        menubar.add_cascade(label='Thermodynamic Properties', menu=thermoProperties_menu)

        parent.config(menu=menubar)

    def __display(self):
        self.listbox.delete(0, END)
        if not self.quick:
            specie = self.dict0[self.SpecieVar.get()]
        else:
            specie = self.reaction.reac[0]

        for key,value in self.dict1.items():
            if self.Var[key].get() is True:
                self.listbox.insert(END, value[1], specie[key], '\n', )

        for key,value in self.dict2.items():
            if self.Var[key].get() is True:
                self.listbox.insert(END,"{:6s}".format('T (K)') +  "{:^20s}".format(value[1]))
                for T, k in zip(self.reaction.T, specie[key]):
                    self.listbox.insert(END, "{:^6s}".format( str("%.1f" % T) )+ "{:^20s}".format( str("%1.6E" % k)))
                self.listbox.insert(END, '\n')

        for key, value in self.dict3.items():
            if self.Var[key].get() is True:
                self.listbox.insert(END, "{:^20s}".format(value[1]))
                for k in specie[key]:
                    self.listbox.insert(END,  "{:^20s}".format(str("%1.6E" % k)))
                self.listbox.insert(END, '\n')

class ReactionProperties:
    AdictTheory = {
        'TST': ('Transition State (TST)', 'ktst', "Lnktst", "Logktst", 'k (TST)', 'Lnk (TST)', 'Log10k (TST)', '1'),
        'd-TST': (
        'Aquilanti-Mundim (d-TST)', 'kdtst', "Lnkdtst", "Logkdtst", 'k (d-TST)', 'Lnk (d-TST)', 'Log10k (d-TST)', '1'),
        'Eckart': (
        'Eckart', 'keckart', "Lnkeckart", "Logkeckart", 'k (eckart)', 'Lnk (eckart)', 'Log10k (eckart)', '1'),
        'ST': ('Skodje and Truhlar (ST)', 'kST', "LnkST", "LogkST", 'k (ST)', 'Lnk (ST)', 'Log10k (ST)', '2'),
        'Bell35': (
        'Bell 35', 'kbell35', "Lnkbell35", "Logkbell35", 'k (Bell35)', 'Lnk (Bell35)', 'Log10k (Bell35)', '2'),
        'Bell58': (
        'Bell 58', 'kbell58', "Lnkbell58", "Logkbell58", 'k (Bell58)', 'Lnk (Bell58)', 'Log10k (Bell58)', '3'),
        'Bell2T': (
        'Bell 582T', 'kbell2T', "Lnkbell2T", "Logkbell2T", 'k (Bell582t)', 'Lnk (Bell582t)', 'Log10k (Bell582t)', '3'),
    }
    dictTheory = {
        'TST': ('Transition State (TST)', 'ktst', 'k (TST)'),
        'd-TST': ('Aquilanti-Mundim (d-TST)', 'kdtst', 'k (d-TST)'),
        'Eckart': ('Eckart', 'keckart','k (eckart)'),
        'ST': ('Skodje and Truhlar (ST)', 'kST',  'k (ST)'),
        'Bell35': ('Bell 35', 'kbell35', 'k (Bell35)'),
        'Bell58': ('Bell 58', 'kbell58', 'k (Bell58)'),
        'Bell2T': ('Bell 582T','kbell2T', 'k (Bell582t)')}
    dictProperties = {
        'Ef': ('Barrier Heigth (Eo)', '2', "%.5f", ' kcal/mol'),
        'de': ('Reaction Energy (ΔE)', '1', "%.5f", ' kcal/mol'),
        'dh': ('Reaction Enthalpy (ΔH)', '1', "%.5f", ' kcal/mol'),
        'dg': ('Reaction Gibbs Energy (ΔG)', '1', "%.5f", ' kcal/mol'),
        'd': ("'d' Parameter", '2', "%.5f", ""),
        'freqi': ('Imaginary Frequency', '2', "%.5f", " cm^-1"),
        'Tc': ('Tc', '3', "%.5f", " (K)"),
        'alpha': ('Alpha', '3', "%1.8E", "")

    }
    dictTempFormat = {'1000/T':"1000/T (K)",
                "T":"T (K)",
                "1/T":"1/T (K)",
                "LnT":"LnT (K)",
                "Log10T":"Log10T (K)"}
    dictRateFormat = {'k':'k',
                      'ln':'Ln(k)',
                      'log10':'Log10(k)'}

    def __init__(self,reaction):
        parent = Toplevel()
        parent.focus_force()
        parent.title('Reaction Properties')
        #parent.geometry("1000x800+50+50")
        parent.geometry("700x800+50+50")
        parent.resizable(False, False)
        try:parent.wm_iconbitmap('transitivity.ico')
        except:pass

        self.reaction = reaction
        self.dictRateUnit = ({'uni':'1/s'},
                             {'mol':'cm³/mol.s','molecule':'cm³/molecule.s'})[len(self.reaction.reac)-1]

        self.__variables()

        title = Label(parent, text="Reaction Properties", font=('arial', 27, 'bold'))
        title.pack(pady=35,anchor=CENTER)

        ### Separator
        #sep = Frame(parent,height=3, bd=1, relief=SUNKEN)
        #sep.pack(fill=X, padx=11, pady=10,anchor=N)

        self.__buildMenu(parent)

        pady = 15
        padx = 20
        frame1 = Frame(parent)
        frame1.pack(expand=True, fill=BOTH,side=TOP)

        frameLeft = LabelFrame(frame1,text='Arrhenius Plot', font=('Arial',12,'bold'))
        frameLeft.pack( fill = Y, side=LEFT, pady=pady,padx=padx)
        self.__BuildframeLeft(frameLeft)

        frameRight = Frame(frame1)#,text='Arrhenius Plot')
        frameRight.pack(expand=TRUE, fill=BOTH, side=LEFT, pady=pady,padx=padx,anchor=N)

        frameRightTop = LabelFrame(frameRight,text='Thermodynamic Properties', font=('Arial',10,'bold'))
        frameRightTop.pack(expand=TRUE, fill=BOTH, side=TOP, pady=pady)
        self.__BuildframeRight(frameRightTop)


        frameRightBottom = Frame(frameRight)
        frameRightBottom.pack( side=TOP, pady=pady)

        self.__BuildframeButtons(frameRightBottom)

    def __BuildframeButtons(self,parent):
        bt_list = [
            ('PES', self.__PES, 'black'),
            ('Clear', self.__Clear, 'red'),
            ('Save *txt file', self.__SaveAll, 'blue'),
        ]

        for bt, cmd, color in bt_list:
            event_bt = Button(parent, text=bt, command=cmd, fg=color, bd=3, width=10,font=('Arial',10))
            event_bt.pack(pady=6,expand=True, fill=X,side = TOP)  #

    def __PES(self):
        E = np.array([self.reaction.sum_reac('En'), self.reaction.ts['En'],self.reaction.sum_prod('En')])
        E = E - min(E)
        dif = max(E) - min(E)
        label = ['R', 'TS', 'P']
        color_plot = 'black'
        color_marker = 'black'
        x_label = 'Reaction Coordinate'
        y_label = 'Energy (kcal/mol)'
        ipadx = 0.3
        ipady = 0.1 * dif
        marker_size = 600
        marker_space = 0.1
        font_type = 'arial'
        font_color = 'black'
        font_weight = 'normal'
        font_size = 12

        fig = plt.figure()
        ax = fig.add_subplot(111)

        for i in range(1, len(E)):
            plt.plot([i + marker_space, i + 1 - marker_space], [E[i - 1], E[i]], linestyle=':', color=color_plot)
        plt.scatter(range(1, len(E) + 1), E, s=marker_size, c=color_marker, marker='_')
        for i in range(len(label)):
            plt.text(i + 1, E[i] + (0.03 * dif), label[i], horizontalalignment='center', verticalalignment='center',
                     fontdict={'family': font_type, 'color': font_color, 'weight': font_weight, 'size': font_size})
        # ax.set_title(title, fontsize='x-large')
        ax.set_xlabel(x_label, fontsize='x-large', labelpad=12)
        ax.set_ylabel(y_label, fontsize='x-large', labelpad=10)
        plt.xticks([])
        plt.axis([1 - ipadx, 3 + ipadx, min(E) - ipady, max(E) + ipady])
        plt.show()
        plt.close()

    def __Clear(self):
        self.rateUnitVar.set(('uni', 'mol')[len(self.reaction.reac) - 1])
        self.rateFormatVar.set(1)
        self.tempFormatVar.set('1000/T')

        for item in self.dictTheory:
            self.dictTheoryVar[self.dictTheory[item][1]].set(False)

        self.dictTheoryVar['ktst'].set(True)

        self.expPointsVar.set(False)

        self.__plot()

    def __SaveAll(self):
        try:
            save_filename = filedialog.asksaveasfilename(title="Save File", defaultextension='txt', filetypes=(
            ("txt files", "*.txt"), ("dat files", "*.dat"), ("all files", "*.*")))
            self.save_file = open(save_filename, 'w', encoding="utf-8")
        except:
            return

        self.save_file.writelines(Title())

        if len(self.reaction.reac) == 1:
            self.save_file.writelines("# REACTION:  " + os.path.basename(self.reaction.reac[0]['filename']).split('.')[0] + "  --->  " +
                         os.path.basename(self.reaction.prod[0]['filename']).split('.')[0] + "\n\n" )
        else:
            self.save_file.writelines("# REACTION:  " + os.path.basename(self.reaction.reac[0]['filename']).split('.')[0] + ' + ' + os.path.basename(self.reaction.reac[1]['filename']).split('.')[0] + "  --->  " +
                                      os.path.basename(self.reaction.prod[0]['filename']).split('.')[0] + ' + ' +os.path.basename(self.reaction.prod[1]['filename']).split('.')[0] + "\n\n" )
               
        self.save_file.writelines('Reactional properties in kcal/mol \n')



        rate_unity = {'uni':('1/s', 'Uni'), 'mol':('cm³/mol s', 'Bi'), 'molecule':('cm³/molecule s', 'Bi')}[ self.rateUnitVar.get()]
        self.save_file.writelines(
            'Kinetic properties in ' + rate_unity[0] + ' : ' + rate_unity[1] + 'molecular Reaction \n\n')

        for key,value in self.dictProperties.items():
            self.save_file.writelines(value[0] + '= ' + "{:.5}".format(self.reaction.reaction[key]) + ' ' + str(value[3]) + '\n')
        self.save_file.writelines("\n\n")

        self.save_file.writelines('{:^10}'.format(self.dictTempFormat[self.tempFormatVar.get()])+'\t')


        for key,value in self.dictTheory.items():
            if self.rateFormatVar.get() == 'k':
                self.save_file.writelines("{:^24}\t".format(value[2]))
            else:
                self.save_file.writelines("{:>5}{:<19}\t".format(self.rateFormatVar.get(),value[2]))

        self.save_file.writelines("{:^24}\t".format('Beta'))
        self.save_file.writelines("\n\n")
        T = {'1000/T': self.reaction.Tinv1000,
             'T': self.reaction.T,
             '1/T': self.reaction.Tinv,
             'LnT': self.reaction.LnT,
             'Log10T': self.reaction.LogT}[self.tempFormatVar.get()]

        if self.rateFormatVar.get() == 'k':
            fmt = "%.4f"
        else:
            fmt = "%.17f"
        if self.rateUnitVar.get() == 'molecule':
            fmt = "%.4e"

        k = {}
        for key, value in self.dictTheory.items():
            k[key] = self.reaction.reaction[value[1]]
            print(type(k[key]))
            if self.rateUnitVar.get() == 'molecule':
                print(1)
                k[key] = k[key] / 6.0221409E23
            if self.rateFormatVar.get() == 'ln':
                print(2)
                k[key] = np.log(k[key])
            if self.rateFormatVar.get() == 'log10':
                print(3)
                k[key] = np.log10(k[key])

        for i,j in enumerate(T):
            self.save_file.writelines('{:^10}\t\t'.format(str("%.4f" % j)))
            for key,value in self.dictTheory.items():
                self.save_file.writelines("{:<24s}\t".format(str(fmt % k[key][i])))
            self.save_file.writelines("{:<24s}\t".format(str("%.1f" %self.reaction.reaction['beta'][i])))
            self.save_file.writelines("\n")



        self.save_file.close()

    def __BuildframeRight(self,parent):

        #Label(parent,text='Thermodynamic Properties',font=('Arial',14)).pack(pady=15)

        listbox = Listbox(parent, font=('arial', 10), justify=CENTER,selectmode=EXTENDED, relief='flat',width=40)#, height=19)
        listbox.pack(side=LEFT,expand= True, fill= BOTH)
        scrollbar = Scrollbar(parent)
        scrollbar.pack(side=RIGHT, fill=Y)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        for key, value in self.dictProperties.items():
            #print(item)
            listbox.insert(END, value[0],value[2] % self.reaction.reaction[key] + value[3], "\n\n")

    def __buildMenu(self,parent):
        menubar = Menu(parent)

        rateTheory_menu = Menu(menubar)
        for item in self.dictTheory:
            rateTheory_menu.add_checkbutton(label=item, onvalue=1, offvalue=0, variable=self.dictTheoryVar[self.dictTheory[item][1]],command=self.__plot)
        rateTheory_menu.add_checkbutton(label='Experimental', onvalue=1, offvalue=0, variable=self.expPointsVar, command=self.__ExpPoints)
        menubar.add_cascade(label='rateTheory', menu=rateTheory_menu)

        rateTheory_menu.add_separator()
        rateUnit_menu = Menu(rateTheory_menu)
        for item in self.dictRateUnit:
            rateUnit_menu.add_radiobutton(label=self.dictRateUnit[item], variable=self.rateUnitVar,value=item,command=self.__plot)
        rateTheory_menu.add_cascade(label='rateUnit', menu=rateUnit_menu)

        rateFormat_menu = Menu(rateTheory_menu)
        for key,value in self.dictRateFormat.items():
            rateFormat_menu.add_radiobutton(label=value, variable=self.rateFormatVar,value=key,command=self.__plot)
        rateTheory_menu.add_cascade(label='rateFormat', menu=rateFormat_menu)

        tempFormat_menu = Menu(menubar)
        for key,value in self.dictTempFormat.items():
            tempFormat_menu.add_radiobutton(label=value, variable=self.tempFormatVar, value=key,command=self.__plot)
        menubar.add_cascade(label='tempFormat', menu=tempFormat_menu)

        parent.config(menu=menubar)

    def __ExpPoints(self):
        if  self.expPointsVar.get() is True:
            self.exp = reactionExpPoints(self.ax,self.canvas,self.tempFormatVar,self.rateFormatVar,self.rateUnitVar)
            self.__plot()
        else:
            self.exp = ''
            self.__plot()

    def __plot(self):
        self.ax.clear()
        #self.ax.set_title('Arrhenius Plot')

        T = {'1000/T': self.reaction.Tinv1000,
             'T': self.reaction.T,
             '1/T': self.reaction.Tinv,
             'LnT': self.reaction.LnT,
             'Log10T': self.reaction.LogT}[self.tempFormatVar.get()]            ## tempFormat

        marker = ['.', 'v', 's', 'D', '*', 'x', '1']
        for  i, (key,value) in enumerate(self.dictTheory.items()):
            if self.dictTheoryVar[value[1]].get() == True:
                theory = self.dictTheory[key][1]
                k = self.reaction.reaction[theory]
                if self.rateUnitVar.get() == 'molecule':
                    k = np.array([x/6.0221409E23 for x in k])
                if self.rateFormatVar.get() == 'ln':
                    k = np.log(k)
                if self.rateFormatVar.get() == 'log10':
                    k = np.log10(k)
                self.ax.plot(T, k, label=theory,marker=marker[i])

        if self.expPointsVar.get() is True:
            try:
                Texp = self.exp.Xexp
                if self.tempFormatVar.get() == '1000/T':
                    Texp = 1000/Texp
                elif self.tempFormatVar.get() == '1/T':
                    Texp = 1 / Texp
                elif self.tempFormatVar.get() == 'LnT':
                    Texp = np.log(Texp)
                elif self.tempFormatVar.get() == 'Log10T':
                    Texp = np.log10(Texp)

                kexp = self.exp.Yexp
                if self.rateUnitVar.get() == 'molecule':
                    kexp = np.array([x/6.0221409E23 for x in kexp])
                if self.rateFormatVar.get() == 'k':
                    kexp = np.exp(kexp)
                if self.rateFormatVar.get() == 'log10':
                    kexp = np.exp(kexp)
                    kexp = np.log10(kexp)
                self.ax.plot(Texp, kexp, label='Experimental', marker="8")
            except: pass
        
        self.ax.legend(loc = 'best')
        xlabel = self.dictTempFormat[self.tempFormatVar.get()]
        self.ax.set_xlabel(xlabel)
        ylabel = "{} {}".format(self.dictRateFormat[self.rateFormatVar.get()],self.dictRateUnit[self.rateUnitVar.get()])
        self.ax.set_ylabel(ylabel)

        try:self.canvas.draw()
        except:pass

    def __variables(self):

        self.rateUnitVar = StringVar()
        self.rateUnitVar.set(('uni','mol')[len(self.reaction.reac)-1])

        self.rateFormatVar = StringVar()
        self.rateFormatVar.set('k')

        self.tempFormatVar = StringVar()
        self.tempFormatVar.set('1000/T')

        self.dictTheoryVar = {}
        for value in self.dictTheory.values():
            self.dictTheoryVar[value[1]] = BooleanVar()

        self.expPointsVar = BooleanVar()

        self.dictTheoryVar['ktst'].set(True)

    def __BuildframeLeft(self,parent):

        self.fig = Figure(figsize=(4, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.__plot()

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=X, expand=0)

        self.toolbar = NavigationToolbar2Tk(self.canvas, parent)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, self.canvas, toolbar)

        self.canvas.mpl_connect("key_press_event", on_key_press)


        """
        frame1 = Frame(parent)
        frame1.pack(expand=True, fill=X, side= TOP)
        pady = 25
        width = 25

        frame2 = Frame(parent)
        frame2.pack(expand=True, fill=X, side= TOP)

        frame3 = Frame(parent)
        frame3.pack(expand=True, fill=X, side= TOP)
        """

class reactionExpPoints:

    def __init__(self,ax,canvas,tempFormatVar,rateFormatVar,rateUnitVar):
        self.root = Toplevel()
        self.root.focus_force()

        self.ax = ax
        self.canvas = canvas
        self.tempFormatVar = tempFormatVar
        self.rateFormatVar = rateFormatVar
        self.rateUnitVar = rateUnitVar
        parent1 = ttk.Frame(self.root);        parent1.pack()
        parent2 = ttk.Frame(self.root);        parent2.pack()
        parent3 = ttk.Frame(self.root);        parent3.pack()
        parent4 = ttk.Frame(self.root);        parent4.pack()

        frame01 = ttk.Frame(parent1);        frame01.pack(side=LEFT)
        frame02 = ttk.Frame(parent1);        frame02.pack(side=LEFT)

        ttk.Label(frame01, text='Temperature', font=('arial', 10)).pack(padx=35)
        ttk.Label(frame02, text='Rate Constant', font=('arial', 10)).pack(padx=35)

        frame1 = ttk.Frame(parent2);        frame1.pack(side=LEFT)
        frame2 = ttk.Frame(parent2);        frame2.pack(side=LEFT, )

        height = 22
        width = 19

        ### Temperature
        # ttk.Label(frame1, text='Temperature', font=('arial', 10)).pack(padx=15, expand=True)
        self.txt_l = Text(frame1, height=height, width=width, relief=FLAT)
        self.txt_l.pack(fill=BOTH, expand=True, padx=3)

        ### Rate Constante
        # ttk.Label(frame2, text='Rate Constant', font=('arial', 10)).pack(padx=15, expand=True)
        self.txt_r = Text(frame2, height=height, width=width, relief=FLAT)
        self.txt_r.pack(fill=BOTH, expand=True, padx=3)
        self.scrollbar = ttk.Scrollbar(parent2)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Changing the settings to make the scrolling work
        self.scrollbar['command'] = self.on_scrollbar
        self.txt_l['yscrollcommand'] = self.on_textscroll
        self.txt_r['yscrollcommand'] = self.on_textscroll

        # Unit Radio Buttons
        frame001 = ttk.Frame(parent3);
        frame001.pack(side=LEFT)
        frame002 = ttk.Frame(parent3);
        frame002.pack(side=LEFT)
        padx = 50
        pady = 0
        self.expTVar = StringVar()
        T = ttk.Radiobutton(frame001, text='T    ', variable=self.expTVar, value='T');
        T.pack(side=TOP, anchor=W, padx=padx, pady=pady)
        T.invoke()
        Tinv = ttk.Radiobutton(frame001, text='1/T  ', variable=self.expTVar, value='Tinv');
        Tinv.pack(side=TOP, anchor=W, padx=padx, pady=pady)
        RTinv = ttk.Radiobutton(frame001, text='1000/T ', variable=self.expTVar, value='1000Tinv');
        RTinv.pack(side=TOP, anchor=W, padx=padx, pady=pady)
        self.expkVar = StringVar()
        lnk = ttk.Radiobutton(frame002, text='ln(k)', variable=self.expkVar, value='lnk');
        lnk.pack(side=TOP, anchor=W, padx=padx, pady=pady)
        lnk.invoke()
        k = ttk.Radiobutton(frame002, text='k   ', variable=self.expkVar, value='k');
        k.pack(side=TOP, anchor=W, padx=padx, pady=pady)
        log10k = ttk.Radiobutton(frame002, text='log10k', variable=self.expkVar, value='log10(k)');
        log10k.pack(side=TOP, anchor=W, padx=padx, pady=pady)

        # buttons

        self.bt_open = Button(parent4, text='Open File', command=self.__OpenExpPoints, width=8, font=('Arial', 10))
        self.bt_open.pack(side=LEFT, expand=True, pady=14, padx=7, anchor=E)
        self.bt_save = Button(parent4, text='Save points', command=self.__SaveExpPoints, width=8,
                              font=('Arial', 10))
        self.bt_save.pack(side=LEFT, expand=True, pady=14, padx=7, anchor=E)

    def on_scrollbar(self, *args):
        self.txt_l.yview(*args)
        self.txt_r.yview(*args)

    def on_textscroll(self, *args):
        self.scrollbar.set(*args)
        self.on_scrollbar('moveto', args[0])

    def RateUnitChange(self):
        """ Default = ln(k)
        k e log10(k0 se selecionados serão convertidos para k """
        if self.expkVar.get() == 'k':
            self.Yexp = np.log(self.Yexp)
        if self.expkVar.get() == 'log10k':
            self.Yexp = 10 ** self.Yexp
            self.Yexp = np.log(self.Yexp)

    def TUnitChange(self):
        """Default = T (K)
        1/T e 1/RT se selecionados serão convertidos para T"""
        if self.expTVar.get() == 'Tinv':
            self.Xexp = 1/self.Xexp

        if self.expTVar.get() == '1000Tinv':
            self.Xexp = 1000/self.Xexp

    def __OpenExpPoints(self):
            self.filename = filedialog.askopenfilename(title="Select file",
                                                       filetypes=[(".txt files", "*.txt;*.dat;*.csv"),
                                                                  ("all files", "*.*")])
            if not os.path.isfile(self.filename):
                return
            self.txt_l.delete(0.0, END)
            self.txt_r.delete(0.0, END)
            for delimiter in ['\t', ',', ';']:
                try:
                    dados = np.loadtxt(self.filename, delimiter=delimiter)
                except:
                    try:
                        dados = np.loadtxt(self.filename, delimiter=delimiter, skiprows=1)
                    except:
                        pass
            try:
                X, Y = dados[:, 0], dados[:, 1]
            except:
                messagebox.showerror(title='Error', message='Select file in csv format')
                return
            for i in range(len(X)):
                self.txt_l.insert(float(i + 1), str(X[i]) + '\n')
                self.txt_r.insert(float(i + 1), str(Y[i]) + '\n')

    def __SaveExpPoints(self):
        ###########################################
        ### X
        X = self.txt_l.get(0.0, END)
        X = X.split('\n')
        X_corr = [float(x) for x in X if len(x) > 0 and not x.isspace()]

        ### Y
        Y = self.txt_r.get(0.0, END)
        Y = Y.split('\n')
        Y_corr = [float(y) for y in Y if len(y) > 0 and not y.isspace()]

        if len(X_corr) != len(Y_corr):
            messagebox.showerror(title='Error', message='Difference in the number of points between X and Y ')
            return
        if len(X_corr) == 0 or len(Y_corr) == 0:
            messagebox.showerror(title='Error', message='Enter the values of X and Y ')
            return
        self.Xexp = np.array(X_corr)
        self.Yexp = np.array(Y_corr)

        self.RateUnitChange()
        self.TUnitChange()

        messagebox.showinfo(title='Success', message='The experimental points have been saved')

        self.__plot()
        self.root.destroy()

    def __plot(self):
        Texp = self.Xexp
        if self.tempFormatVar.get() == '1000/T':
            Texp = 1000/Texp
        elif self.tempFormatVar.get() == '1/T':
            Texp = 1 / Texp
        elif self.tempFormatVar.get() == 'LnT':
            Texp = np.log(Texp)
        elif self.tempFormatVar.get() == 'Log10T':
            Texp = np.log10(Texp)
        kexp = self.Yexp
        if self.rateUnitVar.get() == 'molecule':
            kexp = np.array([x / 6.0221409E23 for x in kexp])
        if self.rateFormatVar.get() == 'k':
            kexp = np.exp(kexp)
        if self.rateFormatVar.get() == 'log10':
            kexp = np.exp(kexp)
            kexp = np.log10(kexp)
        self.ax.plot(Texp, kexp, label='Experimental', marker="8")


        self.ax.legend(loc = 'best')
        #xlabel = self.dictTempFormat[self.tempFormatVar.get()]
        #self.ax.set_xlabel(xlabel)
        #ylabel = "{} {}".format(list(self.dictRateFormat.values())[int(self.rateFormatVar.get())], self.dictRateUnit[self.rateUnitVar.get()])
        #self.ax.set_ylabel(ylabel)

        self.canvas.draw()

class SolventProperties:
    dictK = {
        'Fric':  'Fric (s^-1)',
        'Kr':  'Kramers Transmission'}
    AdictK = {
        'Fric':  'Fric (s^-1)',
        'LnFric':   'ln(Fric) (s^-1)',
        'LogFric':   'log10(Fric) (s^-1)',
        'Kr':  'Kramers Transmission',
        'LnKr':   'ln(Kramers Transmission)',
        'LogKr':  'log10(Kramers Transmission'}
    dictS = {
        'Dif1':  "Dif - Reactant1",
        'Dif2': "Dif - Reactant2",
        'kD': "kD"}
    AdictS = {
        'Dif1': "Dif - Reactant1",
        'LnDif1': "ln(Dif - Reactant1)",
        'LogDif1': "log10(Dif - Reactant1)",
        'Dif2': "Dif - Reactant2",
        'LnDif2': "ln(Dif - Reactant2)",
        'LogDif2': "log10(Dif - Reactant2)",
        'kD': "kD",
        'LnkD': "ln(kD)",
        'LogkD': "log10(kD)"}
    dictR = {
        'kobs': ('k-obs'),
        'Lnkobs': ('Lnk-obs'),
        'Logkobs': ('Logk-obs')
    }
    dictRT = {
        'TST': ('ktst_obs', 'k-TST obs'),
        'd-TST': ('kdtst_obs', 'k-dTST obs'),
        'ST': ('kST_obs', 'k-ST obs'),
        'Bell 35': ('kbell35_obs', 'k-bell35 obs'),
        'Bell 58': ('kbell58_obs', 'k-bell58 obs'),
        'Bell 582t': ('kbell2T_obs', 'k-bell582T obs')}
    dictTemp = {'1000/T':"1000/T (K)",
                "T":"T (K)",
                "1/T":"1/T (K)",
                "LnT":"LnT (K)",
                "Log10T":"Log10T (K)"}
    dictRateFormat = {'k':'k',
                      'ln':'ln(k)',
                      'log10':'log10(k)'}

    def __init__(self, reaction):
        parent = Toplevel()
        parent.focus_force()
        parent.title('Solvent Properties')
        # parent.geometry("1000x800+50+50")
        parent.geometry("800x800+50+50")
        parent.resizable(False, False)
        try:
            parent.wm_iconbitmap('transitivity.ico')
        except:
            pass

        self.reaction = reaction
        self.__variables()

        title = Label(parent, text="Solvent Properties", font=('arial', 27, 'bold'))
        title.pack(pady=35, anchor=CENTER)

        self.dictTheory = {'k': (self.dictK,'Kramers Solvent'),
                      's': (self.dictS,'Collins-Kimball Solvent')}

        self.__buildMenu(parent)
        if len(self.reaction.reac) == 1:
            self.solventTheory_menu.entryconfig(3, state='disabled')
            self.solventTheory_menu.entryconfig(4, state='disabled')

        self.__skEnable()

        pady = 15
        padx = 15
        frame1 = Frame(parent)
        frame1.pack(expand=True, fill=BOTH, side=TOP)

        frameLeft = LabelFrame(frame1, text='Arrhenius Plot', font=('Arial', 12, 'bold'))
        frameLeft.pack(fill=Y, side=LEFT, pady=pady, padx=padx)
        self.__BuildframeLeft(frameLeft)

        frameRight = Frame(frame1)  # ,text='Arrhenius Plot')
        frameRight.pack(expand=TRUE, fill=BOTH, side=LEFT, pady=pady, padx=padx, anchor=N)

        frameRightTop = LabelFrame(frameRight, text='Thermodynamic Properties', font=('Arial', 10, 'bold'))
        frameRightTop.pack(expand=TRUE, fill=BOTH, side=TOP, pady=pady)
        self.__BuildframeRight(frameRightTop)

        frameRightBottom = Frame(frameRight)
        frameRightBottom.pack(side=TOP, pady=pady)

        self.__BuildframeButtons(frameRightBottom)
        self.__plot()

    def __plot(self):
        self.ax.clear()
        self.listbox.delete(0, END)
        # self.ax.set_title('Arrhenius Plot')

        T = {'1000/T': self.reaction.Tinv1000,
             'T': self.reaction.T,
             '1/T': self.reaction.Tinv,
             'LnT': self.reaction.LnT,
             'Log10T': self.reaction.LogT}[self.tempVar.get()]  ## tempFormat

        solvTheory = {'k': self.reaction.Kram,'s': self.reaction.Smol}[self.skVar.get()]

        # kobs rate Theories
        marker = ['.', 'v', 's', 'D', '*', 'x', '1']
        for i, (key,value) in enumerate(self.dictRT.items()):
            if self.rtVar[key].get() is True:
                k = solvTheory[value[0]]
                if self.rateFormatVar.get() == 'ln':
                    k = np.log(k)
                if self.rateFormatVar.get() == 'log10':
                    k = np.log10(k)

                self.ax.plot(T, k, label=value[1], marker=marker[i])
                self.listbox.insert(END, "{:^12s}\t{:^20s}".format(self.dictTemp[self.tempVar.get()],value[1]))
                self.listbox.insert(END, "\n\n")
                for item,j in zip(k,T):
                    self.listbox.insert(END,  "{:^12s}\t{:^20s}".format(str("%1.4f" % j),str("%1.4E" % item)))
                self.listbox.insert(END, "\n\n")

        # Kram Properties
        #if self.skVar.get() == 'k':
        for var,dict in (self.formatKvar,self.dictK.items()),(self.formatSvar,self.dictS.items()):
            for key, value in dict:
                if self.propVar[key].get() is True:
                    if key == 'Dif1':
                        prop = self.reaction.reac[0]['Dif']
                    elif key == 'Dif2':
                        prop = self.reaction.reac[1]['Dif']
                    else:
                        prop = solvTheory[key]
                    if var.get() == 'ln':
                        prop = np.log(prop)
                    if var.get() == 'log10':
                        prop = np.log10(prop)
                    self.ax.plot(T, prop, label=value)
                    self.listbox.insert(END, "{:^12s}\t{:^20s}".format(self.dictTemp[self.tempVar.get()],value))
                    self.listbox.insert(END, "\n\n")
                    for item,j in zip(prop,T):
                        self.listbox.insert(END,  "{:^12s}\t{:^20s}".format(str("%1.4f" % j),str("%1.4E" % item)))
                    self.listbox.insert(END, "\n\n")

        # Viscosity
        if  self.viscVar.get() is True:
            prop =  solvTheory['eta']
            if self.viscFormat.get() == 'ln':
                prop = np.log(prop)
            if self.viscFormat.get() == 'log10':
                prop = np.log10(prop)

            self.ax.plot(T, prop, label='Viscosity (η)')
            self.listbox.insert(END, "{:^12s}\t{:^20s}".format(self.dictTemp[self.tempVar.get()], 'Viscosity (η)'))
            self.listbox.insert(END, "\n\n")
            for item, j in zip(prop, T):
                self.listbox.insert(END, "{:^12s}\t{:^20s}".format(str("%1.4f" % j), str("%1.4E" % item)))
            self.listbox.insert(END, "\n\n")

        self.ax.legend(loc='best')
        xlabel = self.dictTemp[self.tempVar.get()]
        self.ax.set_xlabel(xlabel)
        if self.rateFormatVar.get() == 'k':
            ylabel = "k obs"
        else:
            ylabel = "{}(k) obs".format(self.rateFormatVar.get())

        self.ax.set_ylabel(ylabel)

        #matplotlib.rcParams.update({'font.size':12})
        plt.rc('ytick',labelsize=8)

        try:
            self.canvas.draw()
        except:
            pass

    def TEST(self):
        pass

    def __BuildframeButtons(self, parent):
        bt_list = [
            #('TEST', self.TEST, 'black'),
            ('Clear', self.__Clear, 'red'),
            ('Save *txt file', self.__SaveAll, 'blue'),
        ]

        for bt, cmd, color in bt_list:
            event_bt = Button(parent, text=bt, command=cmd, fg=color, bd=3, width=10, font=('Arial', 10))
            event_bt.pack(pady=6, expand=True, fill=X, side=TOP)  #

    def __Clear(self):
        for var in self.propVar.values():
            var.set(False)
        self.viscVar.set(False)

        for item in self.dictRT:
            self.rtVar[item].set(False)
        self.rtVar['TST'].set(True)

        self.tempVar.set('1000/T')
        self.rateFormatVar.set('ln')
        self.formatKvar.set('ln')
        self.formatSvar.set('ln')
        self.viscFormat.set('ln')

        self.__plot()

    def __SaveAll(self):
        try:
            save_filename = filedialog.asksaveasfilename(title="Save File", defaultextension='txt', filetypes=(
                ("txt files", "*.txt"), ("dat files", "*.dat"), ("all files", "*.*")))
            self.save_file = open(save_filename, 'w', encoding="utf-8")
        except:
            return

        self.save_file.writelines(Title())
        self.save_file.writelines(str(self.reaction))

        if len(self.reaction.reac) == 1:
            self.save_file.writelines(
                "# REACTION:  " + os.path.basename(self.reaction.reac[0]['filename']).split('.')[0] + "  --->  " +
                os.path.basename(self.reaction.prod[0]['filename']).split('.')[0] + "\n\n")
        else:
            self.save_file.writelines(
                "# REACTION:  " + os.path.basename(self.reaction.reac[0]['filename']).split('.')[0] + ' + ' +
                os.path.basename(self.reaction.reac[1]['filename']).split('.')[0] + "  --->  " +
                os.path.basename(self.reaction.prod[0]['filename']).split('.')[0] + ' + ' +
                os.path.basename(self.reaction.prod[1]['filename']).split('.')[0] + "\n\n")

        self.save_file.writelines('Reactional properties in kcal/mol \n\n')


        ######
        T = {'1000/T': self.reaction.Tinv1000,
             'T': self.reaction.T,
             '1/T': self.reaction.Tinv,
             'LnT': self.reaction.LnT,
             'Log10T': self.reaction.LogT}[self.tempVar.get()]

        if self.rateFormatVar.get() == 'k':
            fmt = "%.4f"
        else:
            fmt = "%.17f"

        def title_rates():
            self.save_file.writelines('{:^10}'.format(self.dictTemp[self.tempVar.get()])+'\t')

            for key,value in self.dictRT.items():
                if self.rateFormatVar.get() == 'k':
                    self.save_file.writelines("{:^24}\t".format(value[1]))
                else:
                    self.save_file.writelines("{:>5}{:<19}\t".format(self.rateFormatVar.get(),value[1]))
            self.save_file.writelines('\n')

        def rates_txt(solvTheory):
            k = {}
            for key, value in self.dictRT.items():
                k[key] = solvTheory[value[0]]
                if self.rateFormatVar.get() == 'ln':
                    k[key] = np.log(k[key])
                if self.rateFormatVar.get() == 'log10':
                    k[key] = np.log10(k[key])
            for i, j in enumerate(T):
                self.save_file.writelines('{:^10}\t\t'.format(str("%.4f" % j)))
                for key, value in self.dictRT.items():
                    self.save_file.writelines("{:<24s}\t".format(str(fmt % k[key][i])))
                self.save_file.writelines("\n")

        def title_prop(dict,var):
            for key, value in dict:
                if self.rateFormatVar.get() == 'k':
                    self.save_file.writelines("{:^24}\t".format(value))
                else:
                    self.save_file.writelines("{:>5}{:<19}\t".format(var, value))
            self.save_file.writelines('\n')

        def prop_txt(dict,solvTheory,var):
            prop = {}
            for key, value in dict:
                if key == 'Dif1':
                    prop[key] = self.reaction.reac[0]['Dif']
                elif key == 'Dif2':
                    prop[key] = self.reaction.reac[1]['Dif']
                else:
                    prop[key] = solvTheory[key]
                if var == 'ln':
                    prop[key] = np.log(prop[key])
                if var == 'log10':
                    prop[key] = np.log10(prop[key])
            for i, j in enumerate(T):
                self.save_file.writelines('{:^10}\t\t'.format(str("%.4f" % j)))
                for key, value in dict:
                    self.save_file.writelines("{:<24s}\t".format(str(fmt % prop[key][i])))
                self.save_file.writelines("\n")

        ### Viscosity
        self.save_file.writelines('\n\nViscosity (η)\n\n')
        visc = self.reaction.Kram['eta']

        if self.viscFormat.get() == 'k':
            self.save_file.writelines('{:^10}\t{}\n'.format(self.dictTemp[self.tempVar.get()], 'Viscosity (η)'))
        if self.viscFormat.get() == 'ln':
            visc = np.log(visc)
            self.save_file.writelines('{:^10}\t{}\n'.format(self.dictTemp[self.tempVar.get()], 'ln(Viscosity)'))
        if self.viscFormat.get() == 'log10':
            visc = np.log10(visc)
            self.save_file.writelines('{:^10}\t{}\n'.format(self.dictTemp[self.tempVar.get()], 'log10(Viscosity)'))

        for j, v in zip(T, visc):
            self.save_file.writelines('{:^10}\t{}\n'.format(str("%.4f" % j), str("%.6f" % v)))
        self.save_file.writelines('\n\n\n')


        ## Kram/Smol Rates
        self.save_file.writelines('KRAMMER Solvent Rates \n\n')
        title_rates()
        rates_txt(self.reaction.Kram)
        if len(self.reaction.reac) > 1:
            self.save_file.writelines('\n\n COLLINS-KIMBALL Solvent RAtes\n\n')
            title_rates()
            rates_txt(self.reaction.Smol)

        ## Kram/Smol properties
        self.save_file.writelines('\n\nKRAMMER Properties \n\n')
        self.save_file.writelines('{:^10}'.format(self.dictTemp[self.tempVar.get()]) + '\t')
        title_prop(self.dictK.items(),self.formatKvar.get())
        prop_txt(self.dictK.items(),self.reaction.Kram,self.formatKvar.get())
        if len(self.reaction.reac) > 1:
            self.save_file.writelines('\n\nCOLLIN-KIMBALLS Properties \n\n')
            self.save_file.writelines('{:^10}'.format(self.dictTemp[self.tempVar.get()]) + '\t')
            title_prop(self.dictS.items(), self.formatSvar.get())
            prop_txt(self.dictS.items(), self.reaction.Smol, self.formatSvar.get())

        self.save_file.close()

    def __BuildframeLeft(self, parent):

        self.fig = Figure(figsize=(4, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)

        #self.__plot()

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=X, expand=1)

        toolbar = NavigationToolbar2Tk(self.canvas, parent)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, self.canvas, toolbar)
        self.canvas.mpl_connect("key_press_event", on_key_press)

        """
        frame1 = Frame(parent)
        frame1.pack(expand=True, fill=X, side= TOP)
        pady = 25
        width = 25

        frame2 = Frame(parent)
        frame2.pack(expand=True, fill=X, side= TOP)

        frame3 = Frame(parent)
        frame3.pack(expand=True, fill=X, side= TOP)
        """

    def __BuildframeRight(self, parent):

        # Label(parent,text='Thermodynamic Properties',font=('Arial',14)).pack(pady=15)

        self.listbox = Listbox(parent, font=('arial', 10), justify=CENTER, selectmode=EXTENDED, relief='flat',
                          width=40, height=25)
        self.listbox.pack(side=LEFT, expand=True, fill=BOTH)
        scrollbar = Scrollbar(parent)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

    def __buildMenu(self, parent):
        menubar = Menu(parent)

        ## Solvent Theories
        self.solventTheory_menu = Menu(menubar)
        self.kMenu = Menu(self.solventTheory_menu)
        self.sMenu = Menu(self.solventTheory_menu)

        for key,value in self.dictK.items():
            self.kMenu.add_checkbutton(label=value, onvalue=1, offvalue=0,variable=self.propVar[key],command=self.__plot)
        self.kMenu.add_separator()
        formatKmenu = Menu(self.kMenu)
        for item in self.dictRateFormat:
            formatKmenu.add_radiobutton(label=item, variable=self.formatKvar, value=item,command=self.__plot)
        self.kMenu.add_cascade(label='format', menu=formatKmenu)

        for key,value in self.dictS.items():
            self.sMenu.add_checkbutton(label=value, onvalue=1, offvalue=0,variable=self.propVar[key],command=self.__plot)
        self.sMenu.add_separator()
        formatSmenu = Menu(self.sMenu)
        for item in self.dictRateFormat:
            formatSmenu.add_radiobutton(label=item, variable=self.formatSvar, value=item,command=self.__plot)
        self.sMenu.add_cascade(label='format', menu=formatSmenu)

        menubar.add_cascade(label='solventTheory', menu=self.solventTheory_menu)

        self.solventTheory_menu.add_radiobutton(label='Kramers Solvent', variable=self.skVar, value='k', command=self.__skEnable)
        self.solventTheory_menu.add_cascade(label='Kramers Solvent',menu = self.kMenu)
        self.solventTheory_menu.add_radiobutton(label='Collins-Kimball Solvent', variable=self.skVar, value='s',command=self.__skEnable)
        self.solventTheory_menu.add_cascade(label='Collins-Kimball Solvent', menu=self.sMenu)

        # Rate Theories
        rateTheory_menu = Menu(menubar)
        for key, value in self.dictRT.items():
            rateTheory_menu.add_checkbutton(label=value[1], variable=self.rtVar[key], onvalue=1,offvalue=0,command=self.__plot)
        menubar.add_cascade(label='rateTheories', menu=rateTheory_menu)

        rateTheory_menu.add_separator()
        # Rate Format
        rateFormat_menu = Menu(rateTheory_menu)
        for key, value in self.dictRateFormat.items():
            rateFormat_menu.add_radiobutton(label=value, variable=self.rateFormatVar, value=key,command=self.__plot)
        rateTheory_menu.add_cascade(label='rateFormat', menu=rateFormat_menu)

        # Temperature format
        temperatureFormat_menu = Menu(menubar)
        for key, value in self.dictTemp.items():
            temperatureFormat_menu.add_radiobutton(label=value, variable=self.tempVar, value=key,command=self.__plot)
        menubar.add_cascade(label='temperatureFormat', menu=temperatureFormat_menu)

        # Viscosity
        visc_menu = Menu(menubar)
        viscFormat_menu = Menu(visc_menu)
        visc_menu.add_checkbutton(label='Viscosity (η)',variable=self.viscVar,onvalue=1,offvalue=0,command=self.__plot)
        visc_menu.add_separator()

        visc_menu.add_cascade(label='Format',menu=viscFormat_menu)

        for key,value in self.dictRateFormat.items():
            viscFormat_menu.add_radiobutton(label=value, variable=self.viscFormat,value=key,command=self.__plot)

        menubar.add_cascade(label='Viscosity', menu=visc_menu)


        # Solvent Type
        solventType_menu = Menu(menubar)
        solventType_menu.add_radiobutton(label='Water', variable=self.solvTypeVar, value='water',command=self.__typeSolv)
        solventType_menu.add_radiobutton(label='Other', variable=self.solvTypeVar, value='other',command=self.__typeSolv)
        menubar.add_cascade(label='Solvent type', menu=solventType_menu)


        parent.config(menu=menubar)

    def __typeSolvCheck(self,toplevel,eps,d,eta0):
        try:
            eps = float(eps)
            d = float(d)
            eta0 = float(eta0)
        except:
            messagebox.showerror(title="Error", message="Invalid values")
            toplevel.destroy()
            return

        self.solvTypeVar.set('other')
        self.reaction.set_solvent((eps,d,eta0),water=False)
        self.reaction.Kramer()
        if len(self.reaction.reac) > 1:
            self.reaction.Smoluchowski()
        messagebox.showinfo(title='Success', message='Solvent type changed!')
        self.__plot()
        toplevel.destroy()

    def __typeSolv(self):
        if self.solvTypeVar.get() == 'water':
            self.reaction.set_solvent(None,water=True)
            self.reaction.Kramer()
            if len(self.reaction.reac) > 1:
                self.reaction.Smoluchowski()
            self.__plot()
        else:
            s = Toplevel()
            s.geometry("200x150")
            s.resizable(False, False)
            Label(s,text='Set the solvent properties').pack()
            f0 = Frame(s) ; f0.pack()
            f1 = Frame(f0) ; f1.pack(side=LEFT,expand=True)
            f2 = Frame(f0) ; f2.pack(side=RIGHT,expand=True)
            Label(f1,text='ε(J/mol):').pack() ; Label(f1,text='d:').pack() ; Label(f1,text='η0(Poise):').pack()
            eps = Entry(f2) ; eps.pack()
            d = Entry(f2) ; d.pack()
            eta0 = Entry(f2) ; eta0.pack()
            Label(s,text='η=η0*(1-dε/RT)^(1/d)').pack(pady=3)
            b= Button(s,text='OK',command= lambda:self.__typeSolvCheck(s,eps.get(),d.get(),eta0.get()));b.pack(pady=3)
            self.solvTypeVar.set('water')

    def __skEnable(self):
        stateK,stateS = {'k':('normal','disabled'),
                         's':('disabled','normal')}[self.skVar.get()]

        for prop in {'k': self.dictK,'s': self.dictS}[self.skVar.get()]:
            self.propVar[prop].set(False)

        self.solventTheory_menu.entryconfig(2, state=stateK)
        self.solventTheory_menu.entryconfig(4, state=stateS)
        try:
            self.__plot()
        except:
            pass

    def __variables(self):
        self.propVar = {}
        for dict in self.dictK, self.dictS:
            for item in dict:
                self.propVar[item] = BooleanVar()

        self.skVar = StringVar()
        self.skVar.set('k')

        self.viscVar = BooleanVar()
        self.viscVar.set(False)

        self.rtVar = {}
        for item in self.dictRT:
            self.rtVar[item] = BooleanVar()
        self.rtVar['TST'].set(True)
        self.solvTypeVar = StringVar()
        self.solvTypeVar.set('water')

        self.tempVar = StringVar()
        self.tempVar.set('1000/T')

        self.rateFormatVar = StringVar()
        self.rateFormatVar.set('ln')

        self.formatKvar = StringVar()
        self.formatKvar.set('ln')

        self.formatSvar = StringVar()
        self.formatSvar.set('ln')

        self.viscFormat = StringVar()
        self.viscFormat.set('ln')

if __name__ == '__main__':
    root = Tk()
    #main = Rate(root)

    path = r"E:\GitHub\Transitivity\example\RateConstant\Bimolecular_Solvent"
    a = reaction()
    a.add_reactant(os.path.join(path, 'nh3_m062x.out'))
    a.add_reactant(os.path.join(path, 'oh_m062x.out'))
    a.add_ts(os.path.join(path, 'nh3oh_ts_m062x.out'))
    a.add_product(os.path.join(path, 'nh2_m062x.out'))
    a.add_product(os.path.join(path, 'h2o_m062x.out'))
    a.run_reaction()
    a.Kramer()
    a.Smoluchowski()

    ReactionProperties(a)
    SpeciesProperties(a,False)
    SolventProperties(a)
    root.mainloop()