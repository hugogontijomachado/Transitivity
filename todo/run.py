from RateLib import reaction
from Rate_Module import Rate_Calc, Extract
########################################################################################################################
### Utilizando o RateLib
a = reaction()
a.add_reactant('E:/GitHub/Transitivity/example/h2o_m062x.out')
a.add_reactant('example/nh2_m062x.out')
a.add_ts('example/nh3oh_ts_m062x.out')
a.add_product('example/oh_m062x.out')
a.add_product('example/nh3_m062x.out')
a.run_reaction()
a.Smoluchowski()
a.Kramer()


print('###############################\n #### RateLib\n')
print('En Reac1: ', a.reac[1]['En'])
print('freqi TS', a.ts['freqi'])
print('EnG do Prod2', a.prod[2]['EnG'])

print('ktst: ', a.reaction['ktst'])
print('\n###############################\n\n')


########################################################################################################################
### Utilizando o RateModule
reac1 = Extract('example/h2o_m062x.out','reactant',-1)
reac1.ext() ; reac1.calc_Q()
reac2 = Extract('example/nh2_m062x.out','reactant',-1)
reac2.ext() ; reac2.calc_Q()
ts = Extract('example/nh3oh_ts_m062x.out','ts',-1)
ts.ext() ; ts.calc_Q()
prod1 = Extract('example/oh_m062x.out','product',-1)
prod1.ext() ; prod1.calc_Q()
prod2 = Extract('example/nh3_m062x.out','product',-1)
prod2.ext() ; prod2.calc_Q()

b = Rate_Calc(reac1,reac2,ts,prod1,prod2)
b.Calc()

print('###############################\n ####Rate_Module\n')
print('En Reac1: ', reac1.p['En'])
print('freqi TS', ts.p['freqi'])
print('EnG do Prod2', prod2.p['EnG'])

print('ktst: ', b.p['ktst'])
print('\n###############################\n\n')
########################################################################################################################


#for x in a.Kram:
#    print("a) {} --> {}\n".format(x,a.Kram[x]))


#x = 'QTot'
#print("b) {} --> {}".format(x,b.p[x]))


#print(a.ts['QTot'][0])
#print(a.reac[1]['QTot'][0]* a.reac[2]['QTot'][0])
#print(a.reac[1]['Qt'][0] * a.reac[1]['Qv'][0] *a.reac[1]['Qr'][0] * a.reac[1]['Qe'])


#print(ts.p['QTot'][0])
#print(reac1.p['QTot'][0] * reac2.p['QTot'][0])
#print(reac1.p['Qt'][0] * reac1.p['Qv'][0] * reac1.p['Qr'][0] * reac1.p['Qe'])

