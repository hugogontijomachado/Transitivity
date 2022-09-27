# -*- coding: UTF-8 -*-
import os
class Molecular_Dynamic:
    def __init__(self,inputfile,typecalc,charge,dftfunc,temp,pseudopot,lsdVar,maxstep,timestep,latt_a,latt_b,latt_c,cos_a,cos_b,cos_c,multiple,cartesian):
        if multiple == True:
            self.inputfilename = inputfile.replace(".","")
        else:
            self.inputfilename = inputfile
        self.inputfile = inputfile
        self.typecalc = typecalc.upper()
        self.charge = charge
        self.dftfunc = dftfunc.upper()
        self.temp = temp
        self.pseudopot = pseudopot
        self.lsdVar = lsdVar
        self.maxstep = maxstep
        self.timestep = timestep
        self.latt_a = float(latt_a)
        self.latt_b = float(latt_b)
        self.latt_c = float(latt_c)
        self.cos_a = float(cos_a)
        self.cos_b = float(cos_b)
        self.cos_c = float(cos_c)
        self.multiple = multiple


        self.wf_file = os.path.dirname(self.inputfilename) + '/' + str(os.path.basename(self.inputfilename)).split(".")[0] + '_WafeFunction_' + str(self.typecalc) + '.inp'
        self.run_file =  os.path.dirname(self.inputfilename) + '/' + str(os.path.basename(self.inputfilename)).split(".")[0] + '_Run_' + str(self.typecalc) + '.inp'

        if self.typecalc != "BOMD":
            self.wf = open(self.wf_file,'w', encoding="utf-8")
        self.run = open(self.run_file,'w', encoding="utf-8")
        self.cartesian = cartesian
        self.Atom_Count()
# Wafe Function Output File Write
        if self.typecalc != "BOMD":
            self.INFOSection('OPTIMIZE WAVEFUNCTION',self.wf)
            self.wfCPMDSection()
            if self.typecalc == 'PIMD': self.PIMDSection(self.wf)
            if self.typecalc == 'SHMD': self.TDDFTSection(self.wf)
            self.wfDFTSection(self.wf)
            self.SYSTEMSection(self.wf)
            self.ATOMSection(self.wf)

# Run Output Write
        self.INFOSection('MOLECULAR DYNAMICS',self.run)
        self.runCPMDSection()
        if self.typecalc == 'PIMD': self.PIMDSection(self.run)
        if self.typecalc == 'SHMD': self.TDDFTSection(self.run)
        self.runDFTSection(self.run)
        self.SYSTEMSection(self.run)
        self.ATOMSection(self.run)
        if self.typecalc == 'MTD': self.FinalMTDSection()
        if self.typecalc != "BOMD": self.wf.close()
        self.run.close()

# Generate GV File
        self.GaussViewFile()
    def Atom_Count(self):
        if self.multiple == True:
            self.inputtxt = self.cartesian
            self.inputtxt = self.inputtxt.split('\n')
            self.inputtxt = ["  " + x for x in self.inputtxt]
        else:
            if self.inputfile.split('.')[-1] == 'log' or self.inputfile.split('.')[-1] == 'out':
                atom_dicc = {
                    "1":"H","2":"He",
                    "3":"Li","4":"Be","5":"B","6":"C","7":"N","8":"O","9":"F","10":"Ne",
                    "11":"Na","12":"Mg","13":"Al","14":"Si","15":"P","16":"S","17":"Cl","18":"Ar",
                    "19":"K","20":"Ca","21":"Sc","22":"Ti","23":"V","24":"Cr","25":"Mn","26":"Fe","27":"Co","28":"Ni","29":"Cu","30":"Zn","31":"Ga","32":"Ge","33":"As","34":"Se","35":"Br","36":"Kr",
                    "37":"Rb","38":"Sr","39":"Y","40":"Zr","41":"Nb","42":"Mo","43":"Tc","44":"Ru","45":"Rh","46":"Pd","47":"Ag","48":"Cd","49":"In","50":"Sn","51":"Sb","52":"Te","53":"I","54":"Xe"
                }
                inp = open(self.inputfile, 'r', encoding="utf-8")
                for ln in inp:
                    if 'Standard orientation:' in ln:
                        inp.readline();inp.readline();inp.readline();inp.readline()
                        line = inp.readline()
                        line_split = line.split()
                        i = 1
                        self.inputtxt = []
                        while '---' not in line:
                            self.inputtxt.append(" "+atom_dicc[line_split[1]]+"  "+line_split[3]+" "+line_split[4]+" "+ line_split[5])
                            i += 1
                            line = inp.readline()
                            line_split = line.split()
                inp.close()
            else:
                inp = open(self.inputfile, 'r', encoding="utf-8")
                self.inputtxt = inp.readlines()
                inp.close()

        self.atom_list={
                "H":0,"He":0,
                "Li":0,"Be":0,"B":0,"C":0,"N":0,"O":0,"F":0,"Ne":0,
                "Na":0,"Mg":0,"Al":0,"Si":0,"P":0,"S":0,"Cl":0,"Ar":0,
                "K":0,"Ca":0,"Sc":0,"Ti":0,"V":0,"Cr":0,"Mn":0,"Fe":0,"Co":0,"Ni":0,"Cu":0,"Zn":0,"Ga":0, "Ge":0,"As":0,"Se":0,"Br":0,"Kr":0,
                "Rb":0,"Sr":0,"Y":0,"Zr":0,"Nb":0,"Mo":0,"Tc":0,"Ru":0,"Rh":0,"Pd":0,"Ag":0,"Cd":0,"In":0,"Sn":0,"Sb":0,"Te":0,"I":0,"Xe":0
        }
        for atom in self.atom_list:
            self.atom_list[atom] = ('  '+' '.join(self.inputtxt)).count(" "+atom+" ")

    def INFOSection(self,title,file):
        file.writelines(["&INFO\n",
                            '  INPUT FILE CREATED BY TRANSITIVITY CODE\n',
                            '  '+title+' WITH:  '+self.typecalc+' METHOD\n',
                            '  '+ str(os.path.basename(self.inputfile)) +'\t',
                            'Temperature  '+str(self.temp)+'K\t',
                            'CELL:  L1 = '+str(self.latt_a)+'  L2 = '+str(self.latt_b)+"  L3 = "+str(self.latt_c)+'\n',
                            '&END\n\n'])

    def wfCPMDSection(self):
        if self.typecalc == 'PIMD':
            self.wf.writelines([
                '&CPMD\n',
                '  PATH INTEGRAL\n'])
            if self.lsdVar == 1:
                self.wf.writelines('  LSD\n')
            self.wf.writelines([
                '  OPTIMIZE WAVEFUNCTION\n',
                '  CONVERGENCE ORBITALS\n',
                '  \t1.0d-7\n',
                '  CENTER MOLECULE ON\n',
                '  PRINT FORCES ON\n',
                '&END\n\n'
            ])
        elif self.typecalc == 'SHMD':
            self.wf.writelines([
                '&CPMD\n'])
            if self.lsdVar == 1:
                self.wf.writelines('  LSD\n')
            self.wf.writelines([
                '  ELECTRONIC SPECTRA\n',
                '  DIAGONALIZATION LANCZOS\n',
                '  COMPRESS WRITE32\n',
                '  MEMORY BIG\n'
                '&END\n\n'
            ])
        else:
            self.wf.writelines([
                '&CPMD\n',
                '  OPTIMIZE WAVEFUNCTION\n'])
            if self.lsdVar == 1:
                self.wf.writelines('  LSD\n')
            self.wf.writelines([
                '  PCG MINIMIZE\n',
                '  TIMESTEP\n',
                '  \t20\n',
                '  CONVERGENCE ORBITALS\n',
                '  \t1.0d-7\n',
                '  CENTER MOLECULE ON\n',
                '  PRINT FORCES ON\n',
                '  MEMORY BIG\n',
                '  SPLINE POINTS\n',
                '  \t5000\n',
                '&END\n\n'
            ])

    def PIMDSection(self,file):
        file.writelines('&PIMD\n')
        if file == self.wf:
            file.writelines([
                '  GENERATE REPLICAS\n',
                '  DEBROGLIE CENTROID\n',
                '  \t'+str(self.temp)+'\n'
            ])
        file.writelines([
            '  TROTTER DIMENSION\n',
            '  \t8\n',
            '  STAGING\n',
            '  \t1.0\n',
            '&END\n\n'
        ])
    def TDDFTSection(self,file):
        file.writelines([
            '&TDDFT\n',
            '  STATES SINGLET\n',
            '  \t3\n',
        ])
        if file == self.run:
            file.writelines([
                '  T-SHTDDFT\n',
                '  FORCE STATE\n',
                '  \t3\n',
                '  TAMM-DANCOFF\n'
            ])
        file.writelines([
            '  DAVIDSON PARAMETER\n',
            '  \t150\t1.0D-7\t50\n',
            '&END\n\n'
        ])

    def wfDFTSection(self,file):
        file.writelines([
            '&DFT\n',
            '  GC-CUTOFF\n',
            '  \t1.0d-6\n',
            '  NEWCODE\n',
            '  FUNCTIONAL '+self.dftfunc+'\n',
            '&END\n\n'
        ])

    def runDFTSection(self,file):
        file.writelines([
            '&DFT\n',
            '  NEWCODE\n',
            '  FUNCTIONAL '+self.dftfunc+'\n',
            '&END\n\n'
        ])

    def SYSTEMSection(self,file):
        file.writelines([
            '&SYSTEM\n',
            '  CHARGE\n',
            '  \t'+str(self.charge)+'\n',
            '  SYMMETRY\n',
            '  \t1\n',
            '  ANGSTROM\n'
            '  CELL\n'
            '  \t'+str(self.latt_a)+' '+str(self.latt_b/self.latt_a)+' '+str(self.latt_c/self.latt_a)+'\t'+str(self.cos_a)+" "+str(self.cos_b)+" "+str(self.cos_c)+'\n',
            '  CUTOFF\n'])
        if self.typecalc == "SHMD":
            file.writelines('  \t75.0\n')
        else:
            file.writelines('  \t70.0\n')
        file.writelines([
            '&END\n\n'
        ])
    def ATOMSection(self,file):
        file.writelines('&ATOMS\n\n')
        for atom in self.atom_list:
            if (self.atom_list[atom] != 0):
                #if self.typecalc == "SHMD":
                #    file.writelines('*'+atom+'_MT_'+str(self.dftfunc)+'.psp\n')
                #else:
                file.writelines('*' + atom + '_'+self.pseudopot+'_' + str(self.dftfunc) + '.psp')
                if self.pseudopot != 'MT':
                    file.writelines(' FORMATTED\n')
                else:
                    file.writelines(' \n')

                file.writelines([
                    '  LMAX=P\n',
                    '  \t'+str(self.atom_list[atom])+'\n',
                ])
                for ln in self.inputtxt:
                    if " "+atom+" " in ln:
                        file.writelines('             '+"%12s"%str(ln.split()[1])+'\t'+"%12s"%str(ln.split()[2])+'  '+"%12s"%str(ln.split()[3])+'\n')
                file.writelines('\n')
        if self.typecalc != "MTD" or file == self.wf:
            file.writelines('&END')

    def runCPMDSection(self):
        if self.typecalc == "CPMD" or self.typecalc == "BOMD":
            self.run.writelines([
                '&CPMD\n',
                '  MOLECULAR DYNAMICS '+self.typecalc[:2]+'\n'
            ])
            if self.lsdVar == 1:
                self.run.writelines('  LSD\n')
            if self.typecalc == "CPMD":
                self.run.writelines([
                    '  RESTART WAVEFUNCTION COORDINATES VELOCITIES NOSEP NOSEE LATEST\n',
                ])
            self.run.writelines([
                '  MEMORY BIG\n',
                '  TRAJECTORY SAMPLE XYZ\n',
                '  \t5\n',
                '  RESTFILE\n',
                '  \t1\n',
                '  STORE\n',
                '  \t200\n',
                '  CENTER MOLECULE ON\n',
                '  MAXSTEP\n',
                '  \t'+str(self.maxstep)+'\n',
                '  TIMESTEP\n',
                '  \t'+str(self.timestep)+'\n',
                '  NOSE IONS MASSIVE\n',
                '  \t'+str(self.temp)+'\t2000.0\n'
            ])
            if self.typecalc == "CPMD":
                self.run.writelines([
                    '  NOSE ELECTRONS\n'
                    '  \t0.007\t15000.0\n'
                ])
            self.run.writelines([
                '  SPLINE POINTS\n'
                '  \t5000\n'
                '&END\n\n'
            ])
        elif self.typecalc == "PIMD":
            self.run.writelines([
                '&CPMD\n',
                '  MOLECULAR DYNAMICS\n'])
            if self.lsdVar == 1:
                self.run.writelines('  LSD\n')
            self.run.writelines([
                '  RESTART WAVEFUNCTION COORDINATES LATEST\n',
                '  PRINT FORCE ON\n',
                '  STORE\n',
                '  \t50\n',
                '  PATH INTEGRAL\n',
                '  CENTER MOLECULE ON\n',
                '  MAXSTEP\n',
                '  \t'+str(self.maxstep)+'\n',
                '  TIMESTEP\n',
                '  \t'+str(self.timestep)+'\n',
                '  NOSE IONS MASSIVE\n',
                '  \t'+str(self.temp)+'\t2800.0\n'
                '  NOSE ELECTRONS\n'
                '  \t0.007\t10000.0\n'
                '&END\n\n'
            ])
        elif self.typecalc == "SHMD":
            self.run.writelines([
                '&CPMD\n',
                '  MOLECULAR DYNAMICS BO\n'])
            if self.lsdVar == 1:
                self.run.writelines('  LSD\n')
            self.run.writelines([
                '  RESTART COORDINATES LINRES LATEST\n',
                '  TDDFT\n',
                '  TRAJECTORY XYZ\n',
                '  STORE\n',
                '  \t200\n',
                '  CENTER MOLECULE ON\n',
                '  MAXSTEP\n',
                '  \t'+str(self.maxstep)+'\n',
                '  TIMESTEP\n'
                '  \t'+str(self.timestep)+'\n',
                '  NOSE IONS MASSIVE\n'
                '  \t'+str(self.temp)+'\t2000.0\n',
                '&END\n\n'
            ])
        elif self.typecalc == "MTD":
            self.run.writelines([
                '&CPMD\n',
                '  MOLECULAR DYNAMICS CP\n'])
            if self.lsdVar == 1:
                self.run.writelines('  LSD\n')
            self.run.writelines([
                '  RESTART WAVEFUNCTION  LATEST\n',
                '  PRINT FORCES ON\n',
                '  MEMORY BIG\n',
                '  TRAJECTORY SAMPLE XYZ\n',
                '  \t5\n',
                '  RESTFILE\n',
                '  \t1\n',
                '  CENTER MOLECULE ON\n',
                '  MAXSTEP\n',
                '  \t'+str(self.maxstep)+'\n',
                '  TIMESTEP\n',
                '  \t' + str(self.timestep) + '\n',
                '  NOSE IONS MASSIVE\n',
                '  \t'+str(self.temp)+'\t1000.0\n',
                '  NOSE ELECTRONS\n',
                '  \t0.007\t15000.0\n',
                '&END\n\n',
            ])
    def FinalMTDSection(self):
        self.run.writelines([
            '  META DYNAMICS COLLECTIVE VARIABLE\n',
            '  DEFINE VARIABLES\n',
            '  \t2\n',
            '  TORSION\t37\t24\t29\t34\n',
            '  TORSION\t23\t37\t25\t33\n',
            '  END  DEFINE\n\n',
            '  METASTEPNUM\n',
            '  \t2000\n',
            '  TUNING HEIGHT = 0.0008\t0.016\n',
            '  LAGRANGE  TEMPERATURE\n',
            '  \t200.00\n',
            '  LAGRANGE TEMPCONT\n',
            '  \t200.00 100.00\n',
            '  MAXSTEPNUM  INTERMETA\n',
            '  \t50\n',
            '  MINSTEPNUM  INTERMETA\n',
            '  \t50\n',
            '  MOVEMENT CHECK\n',
            '  \t0.01\n',
            '  MAXKINEN\n',
            '  \t0.06\n',
            '  METASTORE\n',
            '  \t20\t1\t100000\n\n',
            '  END METADYNAMICS\n',
            '&END\n'
        ])

    def GaussViewFile(self):
        self.gv = open( os.path.dirname(self.inputfilename) + '/' + str(os.path.basename(self.inputfilename)).split(".")[0] +'_GVcheck.gjf', 'w', encoding="utf-8")
        self.gv.writelines([
            '%chk=checkgv.chk\n'
            '# opt=(calcfc,noeigentest,maxcycle=10000) freq=noraman uwb97xd/6-311++g** scf=(novaracc,xqc)\n\n'
            'Title Card Required\n\n'
            '0 2\n'
        ])
        for atom in self.atom_list:
            for ln in self.inputtxt:
                if " "+atom+" " in ln:
                   # print(type())
                    self.gv.writelines(["{:<2s} {} {:^12s} {} {:^12s} {} {:^12s} {}".format(ln.split()[0],'\t',ln.split()[1],'\t',ln.split()[2],'\t',ln.split()[3],'\t\n')])
                    #self.gv.writelines("%2s" % str(ln.split()[0]) + "   " + "%12s" % str(ln.split()[1]) + '\t' + "%12s" % str(ln.split()[2]) + '  ' + "%12s" % str(ln.split()[3]) + '\n')
        self.gv.writelines('\n\n\n')
