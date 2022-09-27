# -*- coding: UTF-8 -*-
from tkinter import *
from tkinter import filedialog
import os
from . import gsa_TransitivityPlot as gsa_T
import math as mt
from tkinter import messagebox
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import time


class Fit:
    def __init__(self,tab):
        self.tab = tab
        self.font1 = ('arial', 14, 'bold')
        self.font3 = ('arial', 10)

# Frames

        self.right = Frame(tab)
        self.right.pack(side=RIGHT,padx=50)
        self.lb1 = Label(self.right, text="GSA Fitting", font=('arial', 30, 'bold'))
        self.lb1.pack()
        self.frame0 = Frame(self.right)
        self.frame0.pack()
        self.frame1 = Frame(self.right)
        self.frame1.pack()
        self.left = Frame(tab)
        self.left.pack(side=LEFT,padx=50)
        self.frame2_0 = LabelFrame(self.left, bd=5)
        self.frame2_0.pack(pady=10)
        self.plotsg = Frame(self.frame2_0)
        self.plotsg.pack(side=BOTTOM, anchor=CENTER)
        self.frame2 = Frame(self.left)
        self.frame2.pack(side=LEFT)
        self.frame3 = Frame(self.left)
        self.frame3.pack(side=LEFT)


        self.frame11 = LabelFrame(self.frame1,text='GSA Parameters',bd=5)
        self.frame11.pack(side=TOP,pady=7,fill=X)
        self.frame12 = LabelFrame(self.frame1,text='Initial Parameters',bd=5)
        self.frame12.pack(side=TOP,pady=7,fill=X)
        self.frame13 = Frame(self.frame1)
        self.frame13.pack(side=TOP, pady=7, fill=X)

        pady= 10
        padx=15
        self.frame111 = Frame(self.frame11)
        self.frame111.pack(side=TOP,padx=padx,pady=pady,anchor=W)
        self.frame112 = Frame(self.frame11)
        self.frame112.pack(side=TOP,padx=padx,pady=pady,anchor=W)
        self.frame113 = Frame(self.frame11)
        self.frame113.pack(side=TOP,padx=padx,pady=pady,anchor=W)
        self.frame114 = Frame(self.frame11)
        self.frame114.pack(side=TOP,padx=padx,pady=pady,anchor=W)
        self.frame115 = Frame(self.frame11)
        self.frame115.pack(side=TOP,padx=padx,pady=pady,anchor=W)
        self.frame116 = Frame(self.frame11)
        self.frame116.pack(side=TOP,padx=padx,pady=pady,anchor=W)

        self.frame121 = Frame(self.frame12)
        self.frame121.pack(side=TOP,padx=padx,pady=5,anchor=W,expand=True)
        self.frame122 = Frame(self.frame12)
        self.frame122.pack(side=TOP,padx=padx,pady=5,anchor=W,expand=True)
        self.frame1anim = Frame(self.frame12)
        self.frame1anim.pack(side=TOP, padx=padx,pady=5,anchor=W,expand=True)


# Buttons
        padx = 30; pady = 0
        self.open_bt = Button(self.frame13,text='Open file',command=self.ImportFile,font = ('Arial', 12, 'bold'), width = 8, height = 1, bd = 5)
        self.open_bt.pack(side=LEFT,pady=pady,padx=padx,anchor=CENTER)

        self.calc_bt = Button(self.frame13, text='Fitting', command=self.Calc,font = ('Arial', 12, 'bold'), width = 8, height = 1, bd = 5,fg='blue')
        self.calc_bt.pack(side=RIGHT,pady=pady, padx=padx, anchor=CENTER)

        self.save_bt = Button(self.frame13, text='Save', command=self.Write,font = ('Arial', 12, 'bold'), width = 8, height = 1, bd = 5,fg='blue')
        self.save_bt.pack(side=RIGHT,pady=pady, padx=padx, anchor=CENTER)

        self.SGVar = IntVar()
        self.SG_ch = Checkbutton(self.frame2_0, text="Apply SG",variable=self.SGVar,onvalue=1, offvalue=0, font = ('Arial', 10, 'bold'))
        self.SG_ch.pack(side=LEFT)
        self.ed1 = Entry(self.frame2_0)
        self.ed1.pack(side=LEFT,padx=10)
        self.ed1.insert(1, '2')
        self.order_lb = Label(self.frame2_0,text='Polynomial \nOrder')
        self.order_lb.pack(side=LEFT)
        
        self.PlotSG_ch = Button(self.plotsg, text="Plot SG", command=self.PlotSG, font = ('Arial', 10, 'bold'))
        self.PlotSG_ch.pack(side=RIGHT,padx=15)

        self.preview_ch = Button(self.plotsg, text="Preview", command=self.preview, font = ('Arial', 10, 'bold'))
        self.preview_ch.pack(side=LEFT,padx=15)

# Text
        padx=3 ; pady=0
        self.label_l = Label(self.frame2,text='Temperature (K)',font=self.font3).pack()
        self.txt_l = Text(self.frame2,height=29,width=19)
        self.txt_l.pack(fill=BOTH, expand=True,pady=pady,padx=padx)

        self.label_r = Label(self.frame3, text='Rate Constante',font=self.font3).pack()
        self.txt_r = Text(self.frame3,height=29,width=20)
        self.txt_r.pack(fill=BOTH,expand=True,side=LEFT,pady=pady,padx=padx)

        self.scrollbar = Scrollbar(self.frame3)
        self.scrollbar.pack(side=RIGHT, fill=Y)

#RadioButton
        # Theories
        theory_list = [
            ('Arrhenius'),
            ('Aquilanti-Mundim'),
            ('VFT'),
        ]
        self.theory = {}
        self.theoryVar = StringVar()
        for theory in theory_list:
            self.theory[theory] = Radiobutton(self.frame0,text=theory, variable=self.theoryVar, value=theory,command=self.init_labels)
            self.theory[theory].pack(side=LEFT)
        self.theory['Aquilanti-Mundim'].select()

# Changing the settings to make the scrolling work
        self.scrollbar['command'] = self.on_scrollbar
        self.txt_l['yscrollcommand'] = self.on_textscroll
        self.txt_r['yscrollcommand'] = self.on_textscroll

# GSA.in parameters

        self.gsain_list = [
            ('qA', self.frame111, 'Acceptance index','1.1'),
            ('qT', self.frame112, 'Temperature index','1.5'),
            ('qV', self.frame113, 'Visiting index','1.1'),
            ('NStopMax', self.frame114, 'Max number of GSA-loops','10000'),
            ('To', self.frame115, 'Initial Temperature','1.0'),
            ('F', self.frame116, 'Factor', '1')
        ]
        self.gsain = {}

        for ind, frame, txt, value in self.gsain_list:
            self.gsain[ind] = Entry(frame)
            self.gsain[ind].pack(side=LEFT)
            self.gsain[ind].insert(1, value)
            Label(frame, text='('+ind+') - '+txt).pack(side=RIGHT)

#X1,X2 and X3 Entrys

        ed_list = [
            (1, self.frame121),
            (2, self.frame122),
        ]
        self.ed = {}
        self.cb = {}
        self.LockVar = {}
        self.lb_init = {}
        for ind, frame in ed_list:
            self.lb_init[ind] = Label(frame, text="{:<5s}".format(""))
            self.lb_init[ind].pack(side=LEFT)
            self.ed[ind] = Entry(frame)
            self.ed[ind].pack(side=LEFT)
            self.ed[ind].insert(0, '0.1')
            self.LockVar[ind] = BooleanVar()
            self.cb[ind] = Checkbutton(frame, text= 'Lock',variable=self.LockVar[ind])
            self.cb[ind].pack(side=LEFT)
        self.filename = ''
        self.ChiSq = Label(self.frame122,text='')
        self.ChiSq.pack(side=LEFT)
        self.init_labels()

        self.animVar = BooleanVar()
        self.cb_anim = Checkbutton(self.frame1anim,text='Animation',variable=self.animVar,command=self.anim_change)
        self.cb_anim.pack(side=LEFT,anchor=E,padx= 0)
        self.ed['anim'] = Entry(self.frame1anim)
        self.ed['anim'].pack(side=LEFT,padx=10)
        self.anim_lb = Label(self.frame1anim,text='Step Size')
        self.anim_lb.pack(side=LEFT)
        self.anim_change()


    def preview(self):
        invEa, Xexp= self.diff()
        #print(invEa)
        plt.plot([(1000.0 / x) for x in Xexp], invEa, '--o')
        plt.title("Transitivity Plot")
        plt.xlabel('1000/T', fontsize='x-large')
        plt.ylabel('Gama', fontsize='x-large')
        plt.show()

    def SG(self):
        invEa, Xexp= self.diff()
        if self.SGVar.get() == 1:
            order = int(self.ed1.get())
            invEa = signal.savgol_filter(invEa, len(Xexp), order)
        if self.SGVar.get() == 0:
            invEa = invEa
        return invEa, Xexp
    
    def PlotSG(self):
        invEa, Xexp = self.SG()
        #print(invEa)
        plt.plot([(1000.0 / x) for x in Xexp], invEa, 'o')
        plt.title("Transitivity Plot")
        plt.xlabel('1000/T', fontsize='x-large')
        plt.ylabel('Gama', fontsize='x-large')
        plt.show()

    def diff(self): 
        
        ### Temperature
        temp = self.txt_l.get(0.0,END)
        temp = temp.split('\n')
        temp_corr=[]
        for i in range(len(temp)):
            try:temp_corr.append(float(temp[i]))
            except:pass

        ### Rate
        rate = self.txt_r.get(0.0, END)
        rate = rate.split('\n')
        rate_corr = []
        for i in range(len(rate)):
            try:rate_corr.append(float(rate[i]))
            except:pass

        Xexp = temp_corr
        mXexp = [ (1000.0 / x) for x in Xexp ]
        Yexp = [ np.log(x) for x in rate_corr]
        df = []
        for i in range(1, len(mXexp)-1):
            h = mXexp[i+1] - mXexp[i]
            h_ = mXexp[i] - mXexp[i-1]
            df.append(1/2*((Yexp[i+1]-Yexp[i])/h+(Yexp[i]-Yexp[i-1])/h_))
        df = np.array(df)
	    # End points
        df = np.insert(df,0,(Yexp[1]  - Yexp[0]) /(mXexp[1] - mXexp[0]))
        df = np.insert(df,len(df),(Yexp[-1]  - Yexp[-2]) /(mXexp[-1] - mXexp[-2]))
        invEa = -1.0/df
        print("XX",invEa,Xexp)
        return invEa, Xexp
 
    def anim_change(self):
        if self.animVar.get(): value = 1
        else: value = 0
        state, bg, fg = [(DISABLED, 'gray95', 'gray'),(NORMAL, 'white', 'black')][value]

        self.ed['anim'].delete(0, END)
        self.ed['anim']['state'] = state
        self.ed['anim']['bg'] = bg
        self.anim_lb['fg'] = fg
        self.ed['anim'].insert(0, str(int(int(self.gsain['NStopMax'].get())) / 100).split('.')[0])

    def ImportFile(self):
        self.filename = filedialog.askopenfilename(title="Select file",
                                              filetypes=[(".txt files", "*.txt;*.dat;*.csv"), ("all files", "*.*")])
        if not os.path.isfile(self.filename):
            return
        self.txt_l.delete(0.0, END)
        self.txt_r.delete(0.0, END)
        dataset = []

        inputfile = open(self.filename,'r', encoding="utf-8")
        for ln in inputfile:
            delimiter = ' '
            if '\t' in ln: delimiter = '\t'
            if ',' in ln: delimiter = ','
            if ';' in ln: delimiter = ';'
            dataset.append(ln.split(delimiter))

        dataset2 = []
        fl = True
        for x in range(len(dataset)):
            if fl: dataset2.append([])
            fl = False
            for y in range(len(dataset[x])):
                try:
                    dataset2[-1].append(float(dataset[x][y]))
                    fl = True
                except:
                    pass

        for i in range(len(dataset2)):
            self.txt_l.insert(float(i+1), str(dataset2[i][0]) + '\n')
            self.txt_r.insert(float(i+1),str(dataset2[i][1]) + '\n')
            
    def Extract(self):
        ### GSA parameters
        try:
            qA = float(self.gsain['qA'].get())
            qT = float(self.gsain['qT'].get())
            qV = float(self.gsain['qV'].get())
            NStopMax = int(self.gsain['NStopMax'].get())
            To = float(self.gsain['To'].get())
            F = float(self.gsain['F'].get())
        except:
            messagebox.showerror(title='Error',message='Invalid GSA parameters')
            return

        ### Initial Parameters
        try:
            X_0 = [float(self.ed[1].get()), float(self.ed[2].get())]
        except:
            messagebox.showerror(title='Error', message='Invalid Initial parameters')
            return

        ### Diff
        invEa, Xexp = self.SG()

        ### GSA initialization
        #sgVar = self.SGVar.get()
        animVar = self.animVar.get()
        if animVar:
            try:
                step_anim = int(self.ed['anim'].get())
            except:
                messagebox.showerror(title='Error', message='The step size must be an integer')
                return
        else:
            step_anim = 1

        var_lock = []
        for i in range(len(self.LockVar)):
            var_lock.append(self.LockVar[i+1].get())

        theory = self.theoryVar.get()
        #print(len(X_0))
        if theory == 'Arrhenius':
            nDimension = 1
            del X_0[-1]
            var_lock[0] = False
        else:
            var_lock[1] = False
            nDimension = 2
        print('FIT_T',X_0)
        print(invEa)
        return invEa, Xexp, X_0, step_anim, qA, qT, qV, To, var_lock, NStopMax, animVar, theory, nDimension, F

    def Calc(self):
        invEa, Xexp, X_0, step_anim, qA, qT, qV, To, var_lock, NStopMax, animVar, theory, nDimension, F = self.Extract()
        if len(invEa) != len(Xexp):
            messagebox.showerror(title='Error', message='Difference in the number of points between k and T ')
            return
        if len(invEa) == 0 or len(Xexp) == 0:
            messagebox.showerror(title='Error', message='Enter the values of k and T ')
            return

        a = gsa_T.gsa_py()
        a.gsa(Xexp,invEa,nDimension,theory,X_0,var_lock,animVar,step_anim,NStopMax,qA,qT,qV,To,F)
        self.a = a
        self.write_parameters()

    def write_parameters(self):
        a = self.a
        self.ed[1].delete(0,END)
        self.ed[1].insert(1, str(a.X_Min[0]))
        if self.theoryVar.get() != 'Arrhenius':
            self.ed[2].delete(0, END)
            self.ed[2].insert(1, str(a.X_Min[1]))
        self.ChiSq['text'] = ' Chi-square: ' + str(a.func_Min)
    def init_labels(self):
        theory_dict = {
            'Arrhenius':('Ea',''),
            'Aquilanti-Mundim':('Ea','d'),
            'VFT':('B','T0'),
        }
        if self.theoryVar.get() == 'Arrhenius':
            self.ed[2]['state'] = 'disabled'
            self.cb[2]['state'] = 'disabled'

        else:
            self.ed[2]['state'] = 'normal'
            self.cb[2]['state'] = 'normal'

        for theory in theory_dict:
            if self.theoryVar.get() == theory:
                self.lb_init[1]['text'] = "{:<6s}".format(theory_dict[theory][0])
                self.lb_init[2]['text'] = "{:<6s}".format(theory_dict[theory][1])
                return

    def Write(self):
        a = self.a
        
        filename = filedialog.asksaveasfilename(title="Save File",defaultextension='txt',filetypes=(("txt files", "*.txt"), ("dat files", "*.dat"), ("all files", "*.*")))
        out = open(filename, 'w', encoding="utf-8")

        fmt1 = '%20s'
        fmt2 = '%.15f'

        out.writelines(fmt1 % '1000/T' + '\t' + fmt1 % 'Gamma-exp' + '\t' + fmt1 % 'Gamma - Fit\n')
        for i in range(len(a.Xexp)):
            out.writelines(fmt1 % str(fmt2%(1000.0/a.Xexp[i])) + '\t' + fmt1 % str(fmt2%(a.invEa[i])) + '\t' + fmt1 % str(fmt2%(a.YFit[i]))+'\n')
        out.writelines(' Chi-square: ' + str(a.func_Min) + '\n\n')

        if self.theoryVar.get() == 'Arrhenius':
            out.writelines(' E= ' + str((a.X_Min[0])) + '\n')
            out.writelines(' Gamma = 1/E\n')

        elif self.theoryVar.get() == 'Aquilanti-Mundim':
            out.writelines(' E= ' + str((a.X_Min[0])) + '\n')
            out.writelines(' d= ' + str(a.X_Min[1]) + '\n\n')
            out.writelines(' Gamma = (1/E) * (1 - d * E * Beta)\n')

        elif self.theoryVar.get() == 'VFT':
            out.writelines(' E= ' + str((a.X_Min[0])) + '\n')
            out.writelines(' d= ' + str(a.X_Min[1]) + '\n\n')
            out.writelines(' Gamma = (1/E) * (1 - d * E * Beta)^2\n')
        out.close()


    def on_scrollbar(self, *args):
        self.txt_l.yview(*args)
        self.txt_r.yview(*args)

    def on_textscroll(self, *args):
        self.scrollbar.set(*args)
        self.on_scrollbar('moveto', args[0])

'''
if __name__ == '__main__':
    root = Tk()
    root.geometry("1000x650+50+50")
    Fit(root)
    root.mainloop()
'''