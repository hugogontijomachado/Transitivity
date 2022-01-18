from converter import Converter
import numpy as np
import MD_module as MDM
import os
import random
#lastversion

class system_generator:
    def __init__(self,file1,file2):

        self.file1 = file1
        self.file2 = file2
        self.mol1 = Converter()
        #self.mol1.run_cartesian(file1)
        self.mol1.read_cartesian(file1)
        #self.mol1.cartesian_to_zmatrix()

        self.mol2 = Converter()
        # self.mol2.run_cartesian(file2)
        self.mol2.read_cartesian(file2)
        self.mol2.cartesian_to_zmatrix()
        self.qt_mol2 = len(self.mol2.zmatrix)
        self.xyz = []

        x_mean = 0
        y_mean = 0
        z_mean = 0
        # print(self.mol1.cartesian)
        for i in range(len(self.mol1.cartesian)):
            x_mean += self.mol1.cartesian[i][1][0]
            y_mean += self.mol1.cartesian[i][1][1]
            z_mean += self.mol1.cartesian[i][1][2]
        x_mean = x_mean / len(self.mol1.cartesian)
        y_mean = (y_mean / len(self.mol1.cartesian))+0.1
        z_mean = (z_mean / len(self.mol1.cartesian))+0.1
        self.mean = np.array([x_mean, y_mean, z_mean],dtype='f8')



    def run(self,typecalc,charge,dftfunc,pseudopot,lsdVar,maxstep,timestep,latt_a,latt_b,latt_c,cos_a,cos_b,cos_c,bi,bf,stepsb,ai,af,stepsa,di,df,stepsd,Ti,Tf,stepsT,Chiral_Var):
        head = ["%chk=test.chk\n",
                "# hf/3-21g\n",
                "\n",
                "Title Card Required\n",
               "\n",
                "0 2\n"]
        step = 1

        if int(stepsT) == 0:
            list_T = [Ti]
        else:
            list_T = []
            for i in range(int(stepsT)):
                list_T.append(random.random() * (Tf - Ti) + Ti)

        if int(stepsd) == 0:
            list_d = [di]
        else:
            list_d = []
            for i in range(int(stepsd)):
                list_d.append(random.random() * (df - di) + di)

        if int(stepsa) == 0:
            list_a = [ai]
        else:
            list_a = []
            for i in range(int(stepsa)):
                list_a.append(random.random() * (af - ai) + ai)

        if int(stepsb) == 0:
            list_b = [bi]
        else:
            list_b = []
            for i in range(int(stepsb)):
                list_b.append(random.random()*(bf-bi) + bi)

        for T in list_T:
            for d in list_d:
                for a in list_a:
                    for b in list_b:


                        self.mol1.cartesian.append(['He', self.mean, 0.0])
                        self.mol1.cartesian_to_zmatrix()
                        self.qt_mol1 = len(self.mol1.zmatrix)

                        mol_sist = Converter()
                        mol_sist.zmatrix = self.mol1.zmatrix +self.mol2.zmatrix

                        mol_sist.zmatrix[self.qt_mol1][1][0].extend([self.qt_mol1-1,b])
                        mol_sist.zmatrix[self.qt_mol1][1][1].extend([self.qt_mol1-2,a])
                        mol_sist.zmatrix[self.qt_mol1][1][2].extend([self.qt_mol1-3,d])

                        if self.qt_mol2 > 1:
                            mol_sist.zmatrix[self.qt_mol1+1][1][0][0] = self.qt_mol1

                            mol_sist.zmatrix[self.qt_mol1+1][1][1].extend([self.qt_mol1-1,random.random()*360.0])

                            mol_sist.zmatrix[self.qt_mol1+1][1][2].extend([self.qt_mol1-2,random.random()*360.0])
                        if self.qt_mol2 > 2:
                            mol_sist.zmatrix[self.qt_mol1+2][1][0][0] = self.qt_mol1
                            mol_sist.zmatrix[self.qt_mol1+2][1][1][0] = self.qt_mol1+1

                            mol_sist.zmatrix[self.qt_mol1+2][1][2].extend([self.qt_mol1-1,random.random()*360.0])

                        if self.qt_mol2 > 3:
                            for i in range(3,self.qt_mol2):
                                mol_sist.zmatrix[self.qt_mol1 + i][1][0][0] = self.qt_mol1
                                mol_sist.zmatrix[self.qt_mol1 + i][1][1][0] = self.qt_mol1 + 1
                                mol_sist.zmatrix[self.qt_mol1 + i][1][2][0] = self.qt_mol1 + 2

                        if self.qt_mol1+self.qt_mol2 > 2:
                            mol_sist.zmatrix[2][1][1][1] = np.radians(mol_sist.zmatrix[2][1][1][1])

                            if self.qt_mol1 + self.qt_mol2 > 3:
                                for i in range(3,self.qt_mol1+self.qt_mol2):
                                    for j in range(1,3):
                                        mol_sist.zmatrix[i][1][j][1] = np.radians(mol_sist.zmatrix[i][1][j][1])
                        mol_sist.zmatrix_to_cartesian()
                        mol_sist.cartesian_to_zmatrix()

                        del(mol_sist.zmatrix[self.qt_mol1 - 1])
                        del(mol_sist.cartesian[self.qt_mol1 - 1])


                        self.xyz.append(str(self.qt_mol1 + self.qt_mol2-1) + '\n')
                        self.xyz.append('Step ' + str(step) + '\n')
                        self.xyz.append(mol_sist.str_cartesian())
                        MDM.Molecular_Dynamic(
                            os.path.dirname(self.file1) + '/' + str(os.path.basename(self.file1)).split(".")[0] + "_" + str(os.path.basename(self.file2)).split(".")[0]+"_"+str(step),
                            typecalc,
                            charge,
                            dftfunc,
                            T,
                            pseudopot,
                            lsdVar,
                            maxstep,
                            timestep,
                            latt_a,
                            latt_b,
                            latt_c,
                            cos_a,
                            cos_b,
                            cos_c,
                            True,
                            mol_sist.str_cartesian()
                        )

                        if Chiral_Var is True:
                            caart =[]
                            for atom,coord,mass in mol_sist.cartesian:
                                caart.append([atom,coord*-1,mass])
                            mol_sist.cartesian = caart
                            MDM.Molecular_Dynamic(
                                os.path.dirname(self.file1) + '/' + str(os.path.basename(self.file1)).split(".")[0] + "_" + str(os.path.basename(self.file2)).split(".")[0]+"_"+str(step)+'_Chiral_Inv',
                                typecalc,
                                charge,
                                dftfunc,
                                T,
                                pseudopot,
                                lsdVar,
                                maxstep,
                                timestep,
                                latt_a,
                                latt_b,
                                latt_c,
                                cos_a,
                                cos_b,
                                cos_c,
                                True,
                                mol_sist.str_cartesian()
                            )

                        step += 1
                        self.mol1.run_cartesian(self.file1)
                        self.mol2.run_cartesian(self.file2)
        xyz_file = open(os.path.dirname(self.file1) + '/xyz_file.xyz', 'w')
        xyz_file.writelines(self.xyz)
        xyz_file.close()

if __name__ == '__main__':
    obj = system_generator('OH.gjf','eteno.gjf')
    obj.run('cpmd', '0', 'pbe', '1000', '3', '1.0', '1.0', '1.0', '0.0', '0.0', '0.0', 4.0, 5.0, 1, 0.1, 360.1, 1, 0.1, 360.1, 1, 300.0, 300.0, 0.0)
    #obj.run('cpmd', '0', 'pbe', '1000', '3', '1.0', '1.0', '1.0', '0.0', '0.0', '0.0', 5.0, 5.0, 0.0, 0.1, 180.1, 45.0,180.1, 180.1, 0.0, 300.0, 300.0, 0.0)
    #obj.run('cpmd', '0', 'pbe', '1000', '3', '1.0', '1.0', '1.0', '0.0', '0.0', '0.0', 5.0, 5.0, 0.0, 180.1, 180.1, 0.0,0.1, 180.1, 45.0, 300.0, 300.0, 0.0)
