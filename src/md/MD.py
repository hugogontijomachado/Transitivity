# -*- coding: UTF-8 -*-
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from . import MD_module as MDM
from . import MD_multiple as MDmult
import os
from collections import Counter


class MD:
    def __init__(self,root):
#        root.resizable(False, False)

        tab = self.configure_tabs(root)

        #tab_analysis = ttk.Frame(tab)
        #tab.add(tab_analysis,text="Analysis")
        #self.run_analysys_tab(tab_analysis)

        tab_single = ttk.Frame(tab)
        tab.add(tab_single,text="Single Input")
        self.run_single_tab(tab_single)

        tab_multiple = ttk.Frame(tab)
        tab.add(tab_multiple,text="Multiple Inputs")
        self.run_multiple_tab(tab_multiple)

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

    def run_single_tab(self,parent):
# Frames
        pady=6
        framef = Frame(parent)
        framef.pack(pady=pady, expand=TRUE, anchor=CENTER)
        title = Label(framef, text="Molecular Dynamics", font=('arial', 30, 'bold'))
        title.pack(pady=10)

        frame1 = LabelFrame(framef,text="Open file ('.xyz','.gjf','.out','.log')",bd=5,relief=GROOVE)
        frame1.pack(pady=pady,fill=X,ipady=8)
        frame2 = LabelFrame(framef,text='Dynamic',bd=5)
        frame2.pack(pady=pady,fill=X)
        frame3 = LabelFrame(framef,text='Options',bd=5)
        frame3.pack(pady=pady,fill=X)
        frame4 = LabelFrame(framef,text='Lattices',bd=5)
        frame4.pack(pady=pady,fill=X)
        frame5 = Frame(framef,bd=5)
        frame5.pack(pady=pady, fill=X)

        frame2_1 = Frame(frame2)
        frame2_1.pack()
        frame2_2 = Frame(frame2)
        frame2_2.pack()

        padx = 6
        frame3_1 = Frame(frame3)
        frame3_1.pack(side=LEFT,padx=padx)
        frame3_2 = Frame(frame3)
        frame3_2.pack(side=LEFT,padx=padx)
        frame3_3 = Frame(frame3)
        frame3_3.pack(side=LEFT,padx=padx)

        frame4_1 = Frame(frame4)
        frame4_1.pack(side=LEFT, padx=padx)
        frame4_2 = Frame(frame4)
        frame4_2.pack(side=LEFT, padx=padx)
        frame4_3 = Frame(frame4)
        frame4_3.pack(side=LEFT, padx=padx)

# Open Button
        self.bt_filename = Button(frame1, text="...", command=self.Open, width=2, height=1)
        self.bt_filename.pack(side=LEFT)
        self.listb_open = Listbox(frame1,height=1, width=78, justify=CENTER)
        self.listb_open.pack(side=LEFT,fill=X)
        self.inputfilename = ""

# Type Calc Radio Buttons
        self.types = [
            ('Car Parrinello (CPMD)', 'CPMD',frame2_1),
            ('Path Integral (PIMD)', 'PIMD',frame2_1),
            ('Surface Hopping (TSH)', 'SHMD',frame2_1),
            ('Meta Dynamics (MTD)', 'MTD',frame2_2),
            ('Born Oppenheimer (BOMD)', 'BOMD',frame2_2)
        ]

        self.typecalc = StringVar()
        self.rb = {}
        for text, val, frame in self.types:
            self.rb[val] = Radiobutton(frame, text=text, variable=self.typecalc, value=val)
            self.rb[val].pack(side=LEFT, padx=5, pady=5)
        self.rb['CPMD'].select()

#Options
        self.opt = [
            ('func','Functional',frame3_1,'PBE'),
            ('temp','Temperature (K)',frame3_1,300.0),
            ('maxstep','Max Step',frame3_3,50000),
            ('timestep','Time Step',frame3_3,5.0),
            ('pseudopot','Pseudo',frame3_2,'MT')
                    ]

        self.ed = {}
        for opt,txt,frame,default in self.opt:
            Label(frame,text=txt).pack()
            self.ed[opt] = Entry(frame,width=25)
            self.ed[opt].pack(pady=5)
            self.ed[opt].insert(1,default)

#Charge
        Label(frame3_2,text="Charge").pack(anchor=W,padx=15)
        self.sb_charge = Spinbox(frame3_2,width=10,from_=0,to=1000)
        self.sb_charge.pack(side=LEFT,padx = 5,pady=5)
        self.sb_charge['from_']=-1000

#LSD
        self.lsdVar = IntVar()
        self.cb_LSD = Checkbutton(frame3_2,text='LSD',variable=self.lsdVar)
        self.cb_LSD.pack(side=RIGHT,padx=5)
        self.cb_LSD.select()

# Lattices

        self.lattice = [("a",'latta',frame4_1,10.0),
                        ("b",'lattb',frame4_2,10.0),
                        ("c",'lattc',frame4_3,10.0),
                        ("cos(a)", 'coslatta',frame4_1,0.0),
                        ("cos(b)", 'coslattb',frame4_2,0.0),
                        ("cos(c)", 'coslattc',frame4_3,0.0)]


        for txt,latt,frame,default in self.lattice:
            Label(frame,text=txt).pack()
            self.ed[latt] = Entry(frame,width=25)
            self.ed[latt].pack(pady=5)
            self.ed[latt].insert(1,default)

#Button Generate
        self.bt_gen = Button(frame5,text="Generate Input",fg='blue',command=self.Generate,width=12,height=1,bd=5,font=('Arial',12,'bold'))
        self.bt_gen.pack()

    def run_analysys_tab(self,parent):
        frame0 = Frame(parent,width=10)
        frame0.pack(pady=6, fill=BOTH, anchor=N)

        Label(frame0,text='Bond, Angle and Adiabaticity\n  Trajectory Plots', font=('arial', 30, 'bold')).pack(pady=10)

        frame1 = LabelFrame(frame0,text="Select Trajectory Directory",bd=5,relief=GROOVE)
        frame1.pack(pady=6,ipady=8,anchor=N)

        bt_path = Button(frame1, text="...", command=self.open_analysis, width=2, height=1)
        bt_path.pack(side=LEFT)

        self.listb_plot = Listbox(frame1,height=1, width=78, justify=CENTER)
        self.listb_plot.pack(side=LEFT,fill=X)

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

    def tab_bond(self,parent):
        lbf = LabelFrame(parent,text='Atoms')
        lbf.pack(side=LEFT,fill=BOTH,anchor=CENTER)

        self.listbox_bond = Listbox(lbf,width=12, height=10,font=('arial', 10) ,justify=CENTER,selectmode=EXTENDED,relief='flat')
        self.listbox_bond.pack(side=LEFT)

        self.scrollbar_bond = Scrollbar(lbf)
        self.scrollbar_bond.pack(side=RIGHT, fill=Y)

        self.listbox_bond.config(yscrollcommand=self.scrollbar_bond.set)
        self.scrollbar_bond.config(command=self.listbox_bond.yview)

        self.scrollbar_bond['command'] = self.on_scrollbar
        self.listbox_bond['yscrollcommand'] = self.on_textscroll

    def open_analysis(self):
        self.path_analysis = filedialog.askdirectory(title="Select Directory",initialdir='E:\\GitHub\\conf_35')

        self.listbox_bond.delete(0, END)
        arq = open(os.path.join(self.path_analysis,'TRAJEC.xyz'),'r')

        nat = int(arq.readline().split()[0])
        txt = arq.readline()
        atm = []
        for n in range(nat):
            a = arq.readline().split()[0]
            atm.append(a)

        arq.close()
        for item, qtd in Counter(atm).items():
            if qtd > 1:
                ind = 0
                for n in range(len(atm)):
                    if atm[n] == item:
                        atm[n] = "{}_{}".format(atm[n],ind)
                        ind+=1
        print(atm)

        for n in range(len(atm)):
            self.listbox_bond.insert(n,atm[n])

    def on_scrollbar(self, *args):
        self.listbox_bond.yview(*args)

    def on_textscroll(self, *args):
        self.scrollbar_bond.set(*args)
        self.on_scrollbar('moveto', args[0])

    def tab_angle(self,parent):
        pass

    def tab_adiabaticity(self,parent):
        pass

    def TEST(self):
        pass

    def configure_tabs(self,parent):
        for rows in range(0,50):
            parent.rowconfigure(rows, weight=1)
            parent.columnconfigure(rows, weight=1)
            rows += 1
        tab = ttk.Notebook(parent)
        tab.pack(fill=BOTH, expand=TRUE, anchor=CENTER)
        return tab

    def Open(self):
        self.inputfilename = filedialog.askopenfilename(title="Select file", filetypes=[("Guassian File", "*.gjf;*.xyz;*.out;*.log"),("all files", "*.*")])
        self.listb_open.delete(0, END)
        self.listb_open.insert(1,str(self.inputfilename))

    def Open_1(self):
        self.inputfilename_1 = filedialog.askopenfilename(title="Select file", filetypes=[("Guassian File", "*.gjf"),("all files", "*.*")])
        self.listb_open_1.delete(0, END)
        self.listb_open_1.insert(1,str(self.inputfilename_1))

    def Open_2(self):
        self.inputfilename_2 = filedialog.askopenfilename(title="Select file", filetypes=[("Guassian File", "*.gjf"),("all files", "*.*")])
        self.listb_open_2.delete(0, END)
        self.listb_open_2.insert(1,str(self.inputfilename_2))

    def number_inputs(self):
        stb = float(self.stepsb.get())
        sta = float(self.stepsa.get())
        std = float(self.stepsd.get())
        stT = float(self.stepsT.get())
        try:
            self.lb_nbinp['text'] = str(int(stb*sta*std*stT))
        except:
            messagebox.showerror(title="Error", message="Invalid Values")

    def Generate(self):
        try:
            MDM.Molecular_Dynamic(
                self.inputfilename,
                self.typecalc.get(),
                self.sb_charge.get(),
                self.ed['func'].get(),
                self.ed['temp'].get(),
                self.ed['pseudopot'].get(),
                self.lsdVar.get(),
                self.ed['maxstep'].get(),
                self.ed['timestep'].get(),
                self.ed['latta'].get(),
                self.ed['lattb'].get(),
                self.ed['lattc'].get(),
                self.ed['coslatta'].get(),
                self.ed['coslattb'].get(),
                self.ed['coslattc'].get(),
                False,
                'none'
            )
            messagebox.showinfo(title='Success',message='The input was successfully created')
        except:
            messagebox.showerror(title="Error", message="Invalid File")

    def Generate_multiple(self):
        self.number_inputs()
        if True:
            MD_sist = MDmult.system_generator(self.inputfilename_1,self.inputfilename_2)
            MD_sist.run(
                self.typecalc.get(),
                self.sb_charge.get(),
                self.ed['func'].get(),
                self.ed['pseudopot'].get(),
                self.lsdVar.get(),
                self.ed['maxstep'].get(),
                self.ed['timestep'].get(),
                self.ed['latta'].get(),
                self.ed['lattb'].get(),
                self.ed['lattc'].get(),
                self.ed['coslatta'].get(),
                self.ed['coslattb'].get(),
                self.ed['coslattc'].get(),
                float(self.bi.get()),
                float(self.bf.get()),
                float(self.stepsb.get()),
                (float(self.ai.get())+0.1),
                (float(self.af.get())+0.1),
                float(self.stepsa.get()),
                (float(self.di.get())+0.1),
                (float(self.df.get())+0.1),
                float(self.stepsd.get()),
                float(self.Ti.get()),
                float(self.Tf.get()),
                float(self.stepsT.get()),
                self.Chiral_Var.get()
                )
            messagebox.showinfo(title='Success', message='The inputs were successfully created')
        #except:
        #    messagebox.showerror(title="Error", message="Invalid File or invalid values")

class JanelaRolavel(Frame):
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # cria um canvas e uma barra de rolagem para rolá-lo:
        rolagem = Scrollbar(self, orient=VERTICAL)
        rolagem.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=rolagem.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        rolagem.config(command=self.canvas.yview)

        # reseta a visão:
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # cria um frame dentro do canvas
        # para que seja rolado junto com ele:
        self.conteudo =  Frame(self.canvas)
        self.id_conteudo = self.canvas.create_window(
            0, 0, window=self.conteudo, anchor=NW)

        # cria eventos para detectar mudanças no canvas
        # e sincronizar com a barra de rolagem:
        self.conteudo.bind('<Configure>', self._configurar_conteudo)
        self.canvas.bind('<Configure>', self._configurar_canvas)

    def _configurar_conteudo(self, evento):
            # atualiza a barra de rolagem para o tamanho do frame de conteudo:
            tamanho = (
                self.conteudo.winfo_reqwidth(),
                self.conteudo.winfo_reqheight()
            )
            self.canvas.config(scrollregion="0 0 %s %s" % tamanho)
            if self.conteudo.winfo_reqwidth() != self.canvas.winfo_width():
                # atualizar tambem a largura do canvas para caber o conteudo:
                self.canvas.config(width=self.conteudo.winfo_reqwidth())

    def _configurar_canvas(self, evento):
        if self.conteudo.winfo_reqwidth() != self.canvas.winfo_width():
            # atualizar tambem a largura do conteudo para preencher o canvas:
            self.canvas.itemconfigure(
                self.id_conteudo, width=self.canvas.winfo_width())

if __name__ == '__main__':
    root = Tk()
    MD(root)
    root.mainloop()