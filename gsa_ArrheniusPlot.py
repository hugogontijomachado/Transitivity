import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import random
from tkinter import messagebox

class gsa_py:
    def __init__(self):
        self.XMin = []
        self.func_Min = 0.0

    def GSAini(self, qA, qT, qV, To):
        D = 0
        Pi = np.pi

        # Acceptance probability
        qA1 = qA - 1.0

        # Temperature
        qT1 = qT - 1.0
        Tqt = To * (2.0E0 ** qT1 - 1.0)

        # Visiting Probability
        qV1 = qV - 1.0

        exp1 = 2.0E0 / (3.0 - qV)
        exp2 = 1.0 / qV1 + 0.5E0 * D - 0.5E0

        if D == 0:
            coef = 1.0
        else:
            gammaUp = math.gamma(exp2)
            gammaDown = math.gamma(1.0 / qV1 - 0.5)
            coef = (qV1 / Pi) ** (D * 0.5) * gammaUp / gammaDown

        return D, qA1, qT1, qV1, Tqt, coef, exp1, exp2

    def Temperature(self,Tqt,qT1):
        def Temperature(t):
            return Tqt / ((1.0 + t) ** qT1 - 1.0)
        return Temperature

    def Delta_X(self,D,qT,coef,qV1,exp1,exp2,F):
        def Delta_X(T):
            Tup = T ** (D / (qT - 3.0))
            R = random.random()
            DeltaX = coef * Tup / ( 1.0 + qV1 * R * R / T ** exp1) ** exp2
            DeltaX *= random.choice([-1, 1]) * F
            return DeltaX
        return Delta_X

    def draw_ini(self,Xexp,lnYexp,theory):
        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(121)
        ax.scatter([1000 / x for x in Xexp], lnYexp, label='Experimental')
        line1, = ax.plot([1000 / x for x in Xexp], lnYexp, label='Fitted', color='r')
        ax.set(xlabel="1000/T (K^-1)", ylabel='Ln(k)')
        line2 = ''
        if theory == "NTS" or theory == 'ASCC':
            ax2 = fig.add_subplot(122)
            ax2.scatter([np.log(x) for x in Xexp], lnYexp, label='Experimental')
            line2, = ax2.plot([np.log(x) for x in Xexp], lnYexp, label='Fitted', color='r')
            ax2.set(xlabel="Ln(T) (K)")

        plt.legend(loc='best', shadow=False, fontsize='x-large')

        return fig, line1, line2


    def draw(self,theory,fig,line1,line2):
        """ This routine updates the graph while the fitting is performed """
        def draw1(YFit):
            line1.set_ydata(YFit)
            fig.canvas.draw()
        def draw2(YFit):
            line1.set_ydata(YFit)
            line2.set_ydata(YFit)
            fig.canvas.draw()
        return {'Arrhenius':draw1,'Aquilanti-Mundim':draw1,'NTS':draw2,'VFT':draw1,'ASCC':draw2}[theory]

    def gsa(self,X,Y,nDimension,theory,X_0,lock,anim,step_anim,NStopMax,qA,qT,qV,To,F):
        """ This routine initializes the gsa loop """

        qA, qT, qV, To = np.array(qA,dtype='float64'),np.array(qT,dtype='float64'), np.array(qV,dtype='float64'), np.array(To,dtype='float64')
        D, qA1, qT1, qV1, Tqt, coef, exp1, exp2 = self.GSAini(qA, qT, qV, To)

        Xexp = np.array(X)
        self.X = X
        Yexp = np.array(Y)
        self.Y = Y
        lnYexp = np.array([ np.log(x) for x in Yexp ])
        self.lnY = list(lnYexp)

        func = self.func(theory, Xexp, lnYexp)                      #Definindo a função objetivo

        X_0[0] = np.log(X_0[0])                                     #O fator pré exponencial A será ajustado como ln(A)
        X_0 = np.array(X_0)
        X_ini = np.array(X_0)
        self.X_Min = np.copy(X_0)
        func_0, YFit = func(X_0)
        self.func_Min = func_0

        Temperature = self.Temperature(Tqt,qT1)                     #Definindo a função da temperatura
        Delta_X = self.Delta_X(D, qT, coef, qV1, exp1, exp2, F)        #Definindo a função Delta_X
        VarLock = self.VarLock(lock,X_ini)                          #Definindo a função VarLock

        if anim == True:
            fig, line1, line2 = self.draw_ini(Xexp,lnYexp,theory)
            draw = self.draw(theory, fig, line1, line2)

        for t in range(1,NStopMax+1):
            T = Temperature(t)
            X_t = X_0 + np.array([Delta_X(T) for x in range(nDimension)])
            X_t = VarLock(X_t)
            func_t, YFit = func(X_t)
            if anim and t % step_anim == 0:
                draw(YFit)

            if func_t <= func_0:
                X_0 = X_t.copy()
                func_0 = func_t
                if func_t <= self.func_Min:
                    self.func_Min = func_t
                    self.X_Min = X_t.copy()
                    self.YFit = YFit
            elif qA != 1.0:
                DeltaE = func_t - func_0
                PqA =  1.0 / (( 1.0 + qA1 * DeltaE / T) ** (1.0 / qA1))
                if random.random() < PqA:
                    X_0 = X_t.copy()
                    func_0 = func_t

        if anim == True:
            draw(self.YFit)

        #print(lnYexp)
        #print(YFit)
        #print((sum(lnYexp - YFit) ** 2) / len(YFit))
        #print((sum((lnYexp - YFit) ** 2)) / len(YFit))
    def VarLock(self,lock,X_ini):
        def VarLock(X_t):
            if lock[0]: X_t[0] = X_ini[0]
            if lock[1]: X_t[1] = X_ini[1]
            if lock[2]: X_t[2] = X_ini[2]
            if lock[3]: X_t[3] = X_ini[3]
            return X_t
        return VarLock

    def func(self,theory,Xexp,lnYexp):
        r = 1.9872
        def Arrhenius(X):
            YFit = (X[0] - (X[1] / (r * Xexp)))
            return ((sum((lnYexp - YFit) ** 2)) / len(Xexp)), YFit
        def AquilantiMundim(X):
            YFit = (X[0] + (np.log(1 - ((X[2] * X[1]) / (r * Xexp)))) / X[2])
            return ((sum((lnYexp - YFit) ** 2)) / len(Xexp)), YFit
        def NTS(X):
            YFit = (X[0] - (X[1] / (r * (((Xexp ** 2) + (X[2] ** 2)) ** 0.5))))
            return ((sum((lnYexp - YFit) ** 2)) / len(Xexp)), YFit
        def VFT(X):
            YFit = (X[0] + (X[1] / (Xexp - X[2])))
            return ((sum((lnYexp - YFit) ** 2)) / len(Xexp)), YFit
        def ASCC(X):
            #d = (-1.0 / 3.0) * ((X[2] / (2.0 * X[1])) ** 2)
            YFit = (X[0] + (np.log(1 - (X[3] * X[1] / (r * Xexp + X[2]))) / X[3]))
            return ((sum((lnYexp - YFit) ** 2)) / len(Xexp)), YFit
        return {'Arrhenius':Arrhenius,'Aquilanti-Mundim':AquilantiMundim,'NTS':NTS,'VFT':VFT,'ASCC':ASCC}[theory]





