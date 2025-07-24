import numpy as np
import math as mt
from scipy.integrate import quad
import scipy.special as sc
from datetime import datetime
import os
np.seterr(invalid='ignore')
sc.seterr(all='ignore')

def Title():
    title = [
'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@            @@@@@@@@@@@@@@@@@@@@@@@@            @@@@@@@\n',
'@@@@@@                @@@@@@@@@@@@@@@@@@@@@            @@@@@@@@\n',
'@@@@@                  @@@@@@@@@@@@@@@@@@@,           @@@@@@@@@\n',
'@@@@                    @@@@@@@@@@@@@@@@@@           @@@@@@@@@@\n',
'@@@     .@@@@@@@/        @@@@@@@@@@@@@@@@           @@@@@@@@@@@\n',
'@@@    @@@@@@@@@@@&       @@@@@@@@@@@@@@@          @@@@@@@@@@@@\n',
'@@@   @@@@@@@@@@@@@@      @@@@@@@@@@@@@@          @@@@@@@@@@@@@\n',
'@@,  @@@@@@@@@@@@@@@@      @@@@@@@@@@@@&         @@@@@@@@@@@@@@\n',
'@@   @@@@@@@@@@@@@@@@      @@@@@@@@@@@@         #@@@@@@@@@@@@@@\n',
'@@  *@@@@@@@@@@@@@@@@@      @@@@@@@@@@,        #@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@     @@@@@@@@@@        /@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@     &@@@@@@@@         @@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@     @@@@@@@@        @@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@     @@@@@@@        @@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@,    #@@@@@*       @@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@@     @@@@@       @@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@@     @@@@       @@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@@@    @@@@      @@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@@@     @@      @@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@@@     @%     @@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@@@@    @     @@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@@@@         @@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@@@@/       @@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@@@@@      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@@@@@     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@@@@@,   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@@@@,    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@@@#     /@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@@@       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@@        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@          ,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@@  .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n',
'\n',
str(datetime.now())+'\n\n',
'Transitivity - Code\n\n',
'Program developed by:\nHugo Gontijo Machado, Flávio Olimpio Sanches Neto,\nNayara Dantas Coutinho, Kleber Carlos Mundim,\nVincenzo Aquilanti and Valter Henrique Carvalho Silva.\n\n',
]
    return title

class reaction:
    kb = 1.3806503E-23 #J/K
    h = 6.62607004E-34 #J s
    hb = h / (2.0 * np.pi)
    r = 1.9872E0 ## Cal / mol K
    rJ = 8.3144720E0  ## J / mol K
    NA = 6.0221409E23
    m2c = 1.0E6
    c = 2.99793E10
    T = np.array([273.15, 298.15, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1200.0, 1400.0, 1600.0, 1800.0, 2000.0, 2200.0, 2400.0, 2600.0, 2800.0, 3000.0, 3200.0, 3400.0, 3600.0, 3800.0, 4000.0],dtype=np.float64)
    Tinv1000 = 1000/T
    Tinv = 1/T
    LnT = np.log(T)
    LogT = np.log10(T)
    def __init__(self):
        self.reac = []
        self.ts = {}
        self.prod = []
        self.specie = {}
        self.vert = []

        self.reaction = {}

        self.Smol = {}
        self.Kram = {}
        self.solv = {}

    def getTemp(self):
        return self.T
        
    def setTemp(self,temp):
        self.T = np.array(temp, dtype=np.float64)
        self.Tinv1000 = 1000 / self.T
        self.Tinv = 1 / self.T
        self.LnT = np.log(self.T)
        self.LogT = np.log10(self.T)

    def setDefaultTemp(self):
        self.T = np.array([273.15, 298.15, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1200.0, 1400.0, 1600.0, 1800.0, 2000.0, 2200.0, 2400.0, 2600.0, 2800.0, 3000.0, 3200.0, 3400.0, 3600.0, 3800.0, 4000.0],dtype=np.float64)
        self.Tinv1000 = 1000 / self.T
        self.Tinv = 1 / self.T
        self.LnT = np.log(self.T)
        self.LogT = np.log10(self.T)

    def setEnReac(self, En, n):
        self.reac[n]['En'] = En*627.509 + self.reac[n]['zpe']
        self.reac[n]['Ent'] =  self.reac[n]['Ent'] - self.reac[n]['En'] + En*627.509
        self.reac[n]['EnG'] =  self.reac[n]['EnG'] - self.reac[n]['En'] + En*627.509

    def setEnTS(self, En):
        self.ts['En'] = En * 627.509 + self.ts['zpe']
        self.ts['Ent'] = self.ts['Ent'] - self.ts['En'] + En * 627.509
        self.ts['EnG'] = self.ts['EnG'] - self.ts['En'] + En * 627.509

    def setEnProd(self, En, n):
        self.prod[n]['En'] = En*627.509 + self.prod[n]['zpe']
        self.prod[n]['Ent'] =  self.prod[n]['Ent'] - self.prod[n]['En'] + En*627.509
        self.prod[n]['EnG'] =  self.prod[n]['EnG'] - self.prod[n]['En'] + En*627.509

    def add_reactant(self,filename):
        #n = len(self.reac) + 1
        self.reac.append( {} )
        self.add_specie(filename,self.reac[-1])

    def add_ts(self,filename):
        if len(self.ts) > 0:
            self.ts = {}
            print('No more than one transition state is allowed in a chemical reaction. The last one added will overwrite the previous one.')
        self.add_specie(filename,self.ts)

    def add_product(self,filename):
        #n = len(self.prod) + 1
        self.prod.append({})
        self.add_specie(filename,self.prod[-1])

    def add_vert(self,filename):
        self.vert.append({})
        self.add_specie(filename,self.vert[-1], True)

    def add_specie(self, filename, specie=None, marcus=False):
        if specie == None:
            self.specie[os.path.splitext(os.path.basename(filename))[0]] = {}
            specie = self.specie[os.path.splitext(os.path.basename(filename))[0]]
        specie['zpe'] = 0.0 ; specie['En'] = 0.0 ; specie['Ent'] = 0.0 ; specie['EnG'] = 0.0
        specie['DoF'] = 0 ; specie['freqi'] = 0.0 ; specie['Tvib'] = [] ; specie['Trot'] = [] ; specie['NSym'] = 0.0
        specie['mass'] = 0.0 ; specie['masskg'] = 0.0 ; specie['P'] = 0.0
        specie['filename'] = filename
        specie['basefilename'] = os.path.basename(filename)
        specie['rVol'] = 0.0
        specie['SCF'] = 0.0
        ####################################################################################################################
        ############################## Extracting

        file = open(filename, 'r', encoding="utf-8")
        stop_natoms = False
        for ln in file:
            if 'SCF Done:' in ln:
                specie['SCF'] = float(ln.split()[4]) * 627.509
                if marcus: return
            if "Deg. of freedom" in ln:
                specie['DoF'] = int(ln.split()[3])
            # if "NAtoms=" in ln:
            #     specie['NAtoms'] = int(ln.split()[1])
            if "Charge =" in ln and "Multiplicity =" in ln and not stop_natoms:
                natoms = 0
                line = file.readline()
                while line.strip() != '':
                    natoms += 1
                    line = file.readline()
                specie['NAtoms'] = natoms
                stop_natoms = True
                print(filename)
                print("NAtoms = ", specie['NAtoms'])
                print('\n')
            if "Kelvin.  Pressure" in ln:
                specie['P'] = float(ln.split()[4]) * 101325
            if "Molecular mass:" in ln:
                specie['mass'] = float(ln.split()[2])
                specie['masskg'] = specie['mass'] * 1.660538921E-27
            if "Rotational symmetry number" in ln or 'ROTATIONAL SYMMETRY NUMBER' in ln:
                specie['NSym'] = float(ln.split()[3])
            if "Rotational temperature" in ln:
                specie['Trot'].extend([float(tr) for tr in ln.split()[3:]])
            if "Vibrational temperatures:" in ln:
                specie['Tvib'].extend([float(tv) for tv in ln.split()[2:]])
                line = file.readline()
                specie['Tvib'].extend([float(tv) for tv in line.split()[1:]])
                line = file.readline()
                while line.strip() != '':
                    specie['Tvib'].extend([float(tv) for tv in line.split()])
                    line = file.readline()
            if "Zero-point correction" in ln:
                specie['zpe'] = (float(ln.split()[2])) * 627.509
                __zpe = (float(ln.split()[2]))
            if "Sum of electronic and zero-point Energies" in ln:
                specie['En'] = float(ln.split()[6]) * 627.509
            if "Sum of electronic and thermal Enthalpies" in ln:
                specie['Ent'] = (float(ln.split()[6]) + __zpe) * 627.509
            if "Sum of electronic and thermal Free Energies" in ln:
                specie['EnG'] = (float(ln.split()[7]) + __zpe) * 627.509
            if "Electronic      0" in ln:
                specie['Qe'] = float(ln.split()[1].replace('D', 'E'))
            if specie is self.ts:
                if "frequencies ---" in ln:
                    try:
                        errorts += 1
                    except:
                        specie['freqi'] = -float(ln[20:30]); errorts = 1
            if "a0 for SCRF calculation" in ln:
                specie['rVol'] = float(ln.split()[6])


        file.close()
        ####################################################################################################################
        ##############################  For Atoms only
        if specie['NAtoms'] == 1:
            ############ For isotopes
            if specie['mass'] == 0.0 or specie['Qe'] == 0.0 or specie['En'] == 0.0:
                file = open(filename, 'r', encoding="utf-8")
                iso = 0
                for ln in file:
                    if 'iso=' in ln:
                        iso = int(ln.split()[0].split('=')[1].split(')')[0])
                    if 'Input orientation:' in ln:
                        for i in range(5):
                            line = file.readline()
                        atom_n = int(line.split()[1])
                    if 'Multiplicity =' in ln:  # For atoms, the electronic partition coefficient is the multiplicity
                        ln = ln.split()
                        specie['Qe'] = float(ln[ln.index('Multiplicity') + 2])
                    if 'SCF Done:' in ln:
                        specie['En'] = float(ln.split()[4]) * 627.509
                file.close()

                dicc = {
                    1: 1.00783, 2: 4.00260, 3: 7.01600, 4: 9.01218, 5: 11.00931, 6: 12.00000, 7: 14.00307, 8: 15.99491,
                    9: 18.99840, 10: 19.99244,
                    11: 22.98977, 12: 23.98505, 13: 26.98154, 14: 27.97693, 15: 30.97376, 16: 31.97207, 17: 34.96885,
                    18: 39.96238,
                    19: 38.96371, 20: 39.96259, 21: 44.95591, 22: 47.94795, 23: 50.94396, 24: 51.94051, 25: 54.93805,
                    26: 55.93494, 27: 58.93320,
                    28: 57.93535, 29: 62.92960, 30: 63.92915, 31: 68.92558, 32: 73.92118, 33: 74.92160, 34: 79.91652,
                    35: 78.91834, 36: 83.91151,
                    37: 84.91170, 38: 87.90560, 39: 88.90540, 40: 89.90430, 41: 92.90600, 42: 97.90550, 43: 98.90630,
                    44: 101.90370, 45: 102.90480, 46: 105.90320, 47: 106.90509, 48: 113.90360, 49: 114.90410,
                    50: 117.90180, 51: 120.90380, 52: 129.90670, 53: 126.90040, 54: 131.90420
                }
                iso_dicc = {
                    1: {2: 2.01410, 3: 3.01605},
                    6: {13: 13.00335, 14: 14.00324},
                    7: {15: 15.00011},
                    8: {17: 16.99913, 18: 17.99916},
                    17: {37: 36.96590}
                }

                if iso == 0:
                    specie['mass'] = dicc[atom_n]
                else:
                    try:
                        specie['mass'] = iso_dicc[atom_n][iso]
                    except:
                        specie['mass'] = float(iso)

                specie['masskg'] = specie['mass'] * 1.660538921E-27

            ######## For any Atom
            if specie['P'] == 0.0:
                specie['P'] = 1.0 * 101325E0
            if specie['Ent'] == 0 or specie['EnG'] == 0:
                # Enthalpy
                R = (1.9872E-3)  # kcal/(mol*K)
                T = 298.15  # K
                kb = 0.0019872041  # kcal/(mol*K)
                Hcorr = (((3 / 2) * R * T) + (kb * T))  # kcal/mol
                specie['Ent'] = specie['En'] + Hcorr  # kcal/mol

                # En. Gibbs
                qt = (((2.0 * np.pi * specie['masskg'] * self.kb * T) / (self.h ** 2.0)) ** 1.50) * (
                            (self.kb * T) / specie['P'])
                qe = specie['Qe']
                St = R * (np.log(qt) + 1 + (3 / 2))
                Se = R * (np.log(qe))
                Stot = St + Se  # kcal/(mol*K)
                Gcorr = Hcorr - (T * Stot)  # kcal/mol
                specie['EnG'] = specie['En'] + Gcorr  # kcal/mol

        ####################################################################################################################
        ############################## Calculation of partition coefficients
        # ----------------------------- Calculo Q Vibracional-----------------------------------------------------------------
        if specie['DoF'] == 0:
            specie['Qv'] = np.ones([len(self.T)])
        else:
            specie['Qv'] = []
            for j in range(len(self.T)):
                vibT = [-Tvib for Tvib in specie['Tvib']]
                specie['Qv'].append(1.0 / (np.prod(1 - np.exp(np.divide(vibT, self.T[j])))))
            specie['Qv'] = np.array(specie['Qv'], dtype=np.float64)
        # ----------------------------- Calculo Q Translacional---------------------------------------------------------------
        specie['Qt'] = (((2.0 * np.pi * specie['masskg'] * self.kb * self.T) / (self.h ** 2.0)) ** 1.50) * ((self.kb * self.T) / specie['P'])
        # ----------------------------- Calculo Q Rotacional------------------------------------------------------------------
        if specie['DoF'] == 0:
            specie['Qr'] = np.ones([len(self.T)])
        elif specie['DoF'] == 1:
            specie['Qr'] = self.T / (specie['NSym'] * specie['Trot'][0])
        elif specie['DoF'] > 1:
            specie['Qr'] = ((np.pi ** 0.5) / specie['NSym']) * (
                        (self.T ** 1.5) / (np.prod(specie['Trot'][:])) ** 0.5)
        # ----------------------------- Calculo Qp Total------------------------------------------------------------------
        specie['QTot'] = specie['Qt'] * specie['Qr'] * specie['Qv'] * specie['Qe']

    def get_reactant(self,parameter=None):
        if len(self.reac) == 0:
            print('Add a reactant first')
            return

        if parameter is None:
            print('### All reactant attributes: ')
            for n in self.reac[1]:
                print(n)
        else:
            try:
                par = []
                for n in self.reac:
                    par.append(self.reac[n][parameter])
                return par
            except:
                print('Invalid attribute.')
                print('### All reactant attributes: ')
                for n in self.reac[1]:
                    print(n)

    def get_product(self,parameter=None):
        if len(self.prod) == 0:
            print('Add a product first')
            return

        if parameter is None:
            print('### All product attributes: ')
            for n in self.prod[1]:
                print(n)
        else:
            try:
                par = []
                for n in self.prod:
                    par.append(self.prod[n][parameter])
                return par
            except:
                print('Invalid attribute.')
                print('### All product attributes: ')
                for n in self.prod[1]:
                    print(n)

    def get_ts(self,parameter=None):
        if len(self.ts) == 0:
            print('Add a Transition State first')
            return
        if parameter is None:
            print('### All TS attributes: ')
            for n in self.ts:
                print(n)
        else:
            try:
                par =  self.ts[parameter]
                return par
            except:
                print('Invalid attribute.')
                print('### All TS attributes: ')
                for n in self.ts:
                    print(n)

    def sum_reac(self,prop):
        return  sum([self.reac[n][prop] for n in range(len(self.reac) ) ])

    def sum_prod(self,prop):
        return  sum([self.prod[n][prop] for n in range(len(self.prod) ) ])

    def sum_vert_scf(self):
        return sum([self.vert[n]['SCF'] for n in range(len(self.vert))])

    def prod_reac(self,prop):
        prod = np.copy(self.reac[0][prop])
        for n in range(1, len(self.reac)):
            prod = prod * self.reac[n][prop]
        return  prod

    def get_reaction(self,parameter=None):
        if len(self.reac) == 0:
            print("Run method 'run_reaction' first")
            return

        if parameter is None:
            print('### All reaction attributes: ')
            for n in self.reaction:
                print(n)
        else:
            try:              
                return self.reaction[parameter]
            except:
                print('Invalid attribute.')
                print('### All reaction attributes: ')
                for n in self.reaction:
                    print(n)

    def run_reaction_marcus(self):
        self.run_reaction(True)

    def run_reaction(self, marcus=False):

        self.reaction['de'] = self.sum_prod('En') - self.sum_reac('En')
        self.reaction['dh'] = self.sum_prod('Ent') - self.sum_reac('Ent')
        self.reaction['dg'] = self.sum_prod('EnG') - self.sum_reac('EnG')

        if marcus:
            self.reaction['de_set'] = self.sum_vert_scf() - self.sum_reac('SCF')
            self.reaction['lambda'] = self.reaction['de_set'] - self.reaction['dg']
            self.reaction['dg_set'] =  (self.reaction['lambda'] / 4) * (self.reaction['dg'] / self.reaction['lambda'] +1 )**2

            
            X1 = (self.kb * self.T / self.h)
            X2 = (np.exp(-self.reaction['dg_set'] / (self.r * self.T)))

            self.reaction['kmarcus'] = X1 * X2
            self.reaction['Lnkmarcus']  = np.log(self.reaction['kmarcus'])
            self.reaction['Logkmarcus'] = np.log10(self.reaction['kmarcus'])
            return
            



        self.reaction['freqi'] = self.ts['freqi']

        self.reaction['Ef'] = self.ts['En'] - self.sum_reac('En') # kcal
        self.reaction['Efcal'] = self.reaction['Ef'] * 1000  # cal
        self.reaction['Er'] = self.ts['En'] - self.sum_prod('En')  # kcal
        self.reaction['Ercal'] = self.reaction['Er'] * 1000  # cal
        
        self.reaction['H0'] = (self.ts['Ent'] - self.sum_reac('Ent') ) # kcal
        self.reaction['H0cal'] = (self.ts['Ent'] - self.sum_reac('Ent') ) * 1000.0  # Cal
        
        self.reaction['G0'] = (self.ts['EnG'] - self.sum_reac('EnG') ) # kcal
        self.reaction['G0cal'] = (self.ts['EnG'] - self.sum_reac('EnG') ) * 1000.0  # Cal

        self.reaction['Tc'] = (self.c * self.h * self.ts['freqi'] / (np.pi * self.kb))

        self.reaction['d'] = (-0.004769426830E0) * ((self.c * self.h * self.NA * self.ts['freqi']) / self.reaction['Efcal']) ** 2

        self.reaction['di'] = 1.0 / self.reaction['d']
        self.reaction['alpha'] = (2. * np.pi) / (self.h * self.c * self.reaction['freqi'])

        self.reaction['l'] = (self.reaction['Efcal'] ** (-0.5) + self.reaction['Ercal'] ** (-0.5)) ** (-1) * np.sqrt(2.0) / (self.ts['freqi'])
        self.reaction['a'] = max([0, self.reaction['Efcal'] - self.reaction['Ercal']])


        X1 = (self.kb * self.T / self.h)
        X2 = (np.exp(-self.reaction['Efcal'] / (self.r * self.T)))

        # --------------------- Cáclulo do Coeficiente de partição Total da reação p/ cada temperatura------------------------

        self.reaction['QTot'] = np.divide(self.ts['QTot'] , self.prod_reac('QTot'))

        # # --------------------- Cáclulo do Taxa convencional (kTST)-----------------------------------------------------------
        if len(self.reac) == 1:
            self.reaction['ktst'] = X1 * self.reaction['QTot'] * X2
        else:
            self.reaction['ktst'] = self.m2c * X1 * self.reaction['QTot'] * X2

        self.reaction['Lnktst']  = np.log(self.reaction['ktst'])
        self.reaction['Logktst'] = np.log10(self.reaction['ktst'])

        ## --------------------- Cáclulo do Taxa d-TST ------------------------------------------------------------------------
        if len(self.reac) == 1:
            self.reaction['kdtst'] = X1 * self.reaction['QTot'] * np.exp(self.reaction['di'] * np.log(1 - self.reaction['d'] * self.reaction['Efcal'] / (self.r * self.T)))
        else:
            self.reaction['kdtst'] = self.m2c * X1 * self.reaction['QTot'] * np.exp(self.reaction['di'] * np.log(1 - self.reaction['d'] * self.reaction['Efcal'] / (self.r * self.T)))

        self.reaction['Lnkdtst']  = np.log(self.reaction['kdtst'])
        self.reaction['Logkdtst'] = np.log10(self.reaction['kdtst'])
        # --------------------- Correção de Eckart -----------------------------------------------------------------------



        self.reaction['kappa'] = []
        self.reaction['keckart'] = []
        self.reaction['Lnkeckart'] = []
        self.reaction['Logkeckart'] = []
        for j in range(len(self.T)):
            def alpha(E):
                return (4.18 / (self.c * self.NA)) * np.sqrt(2.0 * self.reaction['l'] ** 2 * E / self.h ** 2)

            def beta(E):
                return (4.18 / (self.c * self.NA)) * np.sqrt(
                    2.0 * self.reaction['l'] ** 2 * (
                                E - (self.reaction['Efcal'] - self.reaction['Ercal'])) / self.h ** 2)

            def delta(E):
                return (4.18 / (self.c * self.NA)) * np.sqrt(
                    4.0 * self.reaction['Efcal'] * self.reaction['Ercal'] / (
                                self.h * self.reaction['freqi']) ** 2 - 0.25)

            def P(E):
                return (np.cosh(2.0 * np.pi * (alpha(E) + beta(E))) - np.cosh(2 * np.pi * (alpha(E) - beta(E)))) / (
                        np.cosh(2 * np.pi * (alpha(E) + beta(E))) + np.cosh(2 * np.pi * (delta(E))))
            def integradum(E):
                return P(E) * np.exp(-(E - self.reaction['Efcal']) / (self.r * self.T[j]))


            self.reaction['integral'], self.reaction['error'] = quad(integradum, self.reaction['a'], np.inf)
            self.reaction['kappa'].append((self.reaction['integral']) / (self.r * self.T[j]))
            self.reaction['keckart'].append(self.reaction['kappa'][j] * self.reaction['ktst'][j])
            try:
                self.reaction['Lnkeckart'].append(mt.log(self.reaction['keckart'][j]))
                self.reaction['Logkeckart'].append(mt.log10(self.reaction['keckart'][j]))
            except:
                self.reaction['Lnkeckart'].append(float("NaN"))
                self.reaction['Logkeckart'].append(float("NaN"))

        self.reaction['keckart'] = np.array(self.reaction['keckart'])
        self.reaction['Lnkeckart'] = np.array(self.reaction['Lnkeckart'])
        self.reaction['Logkeckart'] = np.array(self.reaction['Logkeckart'])

        # --------------------- Correção de Bell 1935 -----------------------------------------------------------------------
        self.reaction['bell35'] = (self.kb * self.T - 1.0E0 * self.hb * self.reaction['freqi'] * self.c * np.exp(-(2.0E0 * 4.180E0) * np.pi * self.reaction['Efcal'] / (self.c * self.h * self.reaction['freqi'] * self.NA)) / X2) / (self.kb * self.T - self.hb * self.reaction['freqi'] * self.c)
        self.reaction['kbell35'] = self.reaction['bell35'] * self.reaction['ktst']

        self.reaction['Lnkbell35'] = np.log(self.reaction['kbell35'])
        self.reaction['Logkbell35'] = np.log10(self.reaction['kbell35'])


        # --------------------- Correção de Bell 1958 -----------------------------------------------------------------------
        self.reaction['fator'] = (0.50E0 * self.h * self.reaction['freqi'] * self.c) / (self.kb * self.T)
        self.reaction['bell58'] = self.reaction['fator'] / np.sin(self.reaction['fator'])
        self.reaction['kbell58'] = self.reaction['bell58'] * self.reaction['ktst']
        self.reaction['Lnkbell58']  = np.log(self.reaction['kbell58'])
        self.reaction['Logkbell58'] = np.log10(self.reaction['kbell58'])

        self.reaction['bell2T'] = self.reaction['bell58'] - 1.0E0 * np.exp(-(2.0E0 * 4.180E0) * np.pi * self.reaction['Efcal'] / (self.c * self.h * self.reaction['freqi'] * self.NA)) / (X2 * (1.0E0 * np.pi / self.reaction['fator'] - 1.0E0))
        self.reaction['kbell2T'] = self.reaction['bell2T'] * self.reaction['ktst']
        self.reaction['Lnkbell2T']  = np.log(self.reaction['kbell2T'])
        self.reaction['Logkbell2T'] = np.log10(self.reaction['kbell2T'])
        # --------------------- Correção ST ---------------------------------------------------------------------------------

        self.reaction['beta'] = 1.0E0 / (self.kb * self.T)
        if self.reaction['dh'] <= 0.0E0:
            dh = 0.0E0
        else:
            dh = self.reaction['dh']

        self.reaction['ST'] = []
        for j in range(len(self.T)):
            if self.reaction['beta'][j] <= self.reaction['alpha']:
                self.reaction['ST'].append(self.reaction['bell58'][j] - (self.reaction['beta'][j] / ((self.reaction['alpha']) - self.reaction['beta'][j]) * np.exp(((self.reaction['beta'][j] - (self.reaction['alpha']))) * (self.reaction['Efcal'] - dh) * (4.1868E0 / self.NA))))

            elif self.reaction['beta'][j] > self.reaction['alpha']:
                self.reaction['ST'].append((self.reaction['beta'][j] / (self.reaction['beta'][j] - (self.reaction['alpha']))) * (np.exp(((self.reaction['beta'][j] - (self.reaction['alpha']))) * ((self.reaction['Efcal'] - dh) * (4.1868E0 / self.NA))) - 1.0))

        self.reaction['ST'] = np.array(self.reaction['ST'],dtype=np.float64)
        self.reaction['kST'] = self.reaction['ST'] * self.reaction['ktst']

        self.reaction['LnkST'] = np.log(self.reaction['kST'])
        self.reaction['LogkST'] = np.log10(self.reaction['kST'])

    def set_solvent(self, parameters, water = False):
        if water is True:
            self.solv['epsilon'] = -0.58725 * self.rJ * 1000.0 #J/mol
            self.solv['d'] = -0.3628
            self.solv['eta0'] = np.exp(-8.21619) #Poise or g/cm.s
        else:
            self.solv['epsilon'] = parameters[0]
            self.solv['d'] = parameters[1]
            self.solv['eta0'] = parameters[2]

    def Smoluchowski(self):
        if len(self.solv) == 0:
            self.set_solvent(None,water=True)

        self.Smol['eta']         = self.solv['eta0'] * ((1 - self.solv['d'] * self.solv['epsilon'] / (self.rJ * self.T)) ** (1 / self.solv['d']))

        for n in range(len(self.reac)):
            self.reac[n]['Dif']         = (1.0E15 * self.kb * self.T) / (6.0 * np.pi * self.reac[n]['rVol']) * (1.0/self.Smol['eta'])  # cm²/s
            self.reac[n]['LnDif']      = np.log(self.reac[n]['Dif'])
            self.reac[n]['LogDif']     = np.log10(self.reac[n]['Dif'])



        self.Smol['kD']          = 4.0 * np.pi * self.ts['rVol'] * self.NA * self.sum_reac('Dif') * 1.0E-8 # cm³/mol*s
        self.Smol['LnkD']        = np.log(self.Smol['kD'])
        self.Smol['LogkD']       = np.log10(self.Smol['kD'])
        self.Smol['ktst_obs']    = self.reaction['ktst'] * (self.Smol['kD'] / (self.reaction['ktst'] + self.Smol['kD']))
        self.Smol['kdtst_obs']   = self.reaction['kdtst'] * (self.Smol['kD'] /(self.reaction['kdtst'] + self.Smol['kD']))
        self.Smol['kST_obs']     = self.reaction['kST'] * (self.Smol['kD'] / (self.reaction['kST'] + self.Smol['kD']))
        self.Smol['kbell35_obs'] = self.reaction['kbell35'] * (self.Smol['kD'] / (self.reaction['kbell35'] + self.Smol['kD']))
        self.Smol['kbell58_obs'] = self.reaction['kbell58'] * (self.Smol['kD'] / (self.reaction['kbell58'] + self.Smol['kD']))
        self.Smol['kbell2T_obs'] = self.reaction['kbell2T'] * (self.Smol['kD'] / (self.reaction['kbell2T'] + self.Smol['kD']))

    def get_Smoluchowski(self, parameter=None):
        if len(self.Smol) == 0:
            print("Run method 'Smoluchowski' first")
            return

        if parameter is None:
            print('### All Smoluchowski attributes: ')
            for n in self.Smol:
                print(n)

        else:
            try:
                return self.Smol[parameter]

            except:
                print('Invalid attribute.')
                print('### All Smoluchowski attributes: ')
                for n in self.Smol:
                    print(n)

    def Kramer(self):
        if len(self.solv) == 0:
            self.set_solvent(None,water=True)
        Acm = 1.0E-8 #cm
        mau = 1.660538E-24  #g
        RES = self.ts['rVol'] * Acm #cm
        M = self.ts['mass'] * mau    # Massa do TS em g

        self.Kram['wFreqi'] = 2 * np.pi * self.c * self.reaction['freqi'] #s^-1 angular

        self.Kram['eta'] = self.solv['eta0'] * ((1 - self.solv['d'] * self.solv['epsilon'] / (self.rJ * self.T)) ** (1 / self.solv['d']))

        self.Kram['Fric'] = (6.0 * np.pi) * self.Kram['eta'] * RES / M
        self.Kram['LnFric'] = np.log( self.Kram['Fric'])
        self.Kram['LogFric'] = np.log10( self.Kram['Fric'])

        self.Kram['Kr'] = ((((( self.Kram['Fric']**2.0)/4.0) + ( self.Kram['wFreqi']**2))**(1.0/2.0)) - ( self.Kram['Fric']/2.0)) /  self.Kram['wFreqi']
        self.Kram['LnKr'] = np.log(self.Kram['Kr'])
        self.Kram['LogKr'] = np.log10(self.Kram['Kr'])

        self.Kram['ktst_obs'] = self.Kram['Kr'] * self.reaction['ktst']
        self.Kram['kdtst_obs'] = self.Kram['Kr'] * self.reaction['kdtst']
        self.Kram['kST_obs'] = self.Kram['Kr'] * self.reaction['kST']

        self.Kram['kbell35_obs'] = self.Kram['Kr'] * self.reaction['kbell35']
        self.Kram['kbell58_obs'] = self.Kram['Kr'] * self.reaction['kbell58']
        self.Kram['kbell2T_obs'] = self.Kram['Kr'] * self.reaction['kbell2T']

    def get_Kramer(self, parameter=None):
        if len(self.Kram) == 0:
            print("Run method 'Krammer' first")
            return

        if parameter is None:
            print('### All Krammer attributes: ')
            for n in self.Kram:
                print(n)
        else:
            try:
                return self.Kram[parameter]
            except:
                print('Invalid attribute.')
                print('### All Krammer attributes: ')
                for n in self.Kram:
                    print(n)

    def __str__(self):
        title = ""
        try:
            title += "  {}".format(os.path.basename(self.reac[1]['filename']))
            for n in range(2, len(self.reac)+1):
                title += " + {}".format(os.path.basename(self.reac[n]['filename']))
        except:
            title += 'No Reactants'

        try:
            title += " ---> {}".format(os.path.basename(self.prod[1]['filename']))
            for n in range(2, len(self.prod)+1):
                title += " + {}".format(os.path.basename(self.prod[n]['filename']))

        except:
            title += "  ---> No Products"


        title += '\n\nReactional properties in kcal/mol \n'

        return title