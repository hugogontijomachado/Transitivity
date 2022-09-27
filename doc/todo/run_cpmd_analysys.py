import CPMD_Analysis as cpmd
import os
import gjf2pov as g2p

trajetorias = [str(x) for x in range(1,100)]
trajetorias.extend(['49_500','49_100000'])

atoms = [('N', 1), ('O', 2), ('Cl', 3), ('F', 4)]

bonds = [('N', 'F'), ('Cl', 'F'), ('Cl','N')]

angles = [('O','N','Cl'),('O','N','F'),('N','F','Cl')]



for trajec in trajetorias:
    a = cpmd.adiabaticity()
    a.run(dir='conf_'+trajec)
    a.plot(title='Trajectory '+trajec,save='save',savename=trajec)

    color = ['darkblue', 'red', 'yellowgreen']
    color2 = ['black','goldenrod','red']

    a = cpmd.bond()
    a.run(atoms=atoms, bonds=bonds,dir='conf_'+trajec)
    a.plot(color_bond=color,save='save',savename=trajec,title="Trajetoria: "+trajec)



