import Rate_Module as RM

a = {}
filenames = []
especies = []
a['none'] = RM.Extract('','',-1)
path='C:/Users/flavi/OneDrive/Flavio/Doutorado/Colaboracoes/VDTST/CH3OH/M062X/6-311mmgaa/'
arqs = open(path + 'files.dat', 'r')

for x in arqs:
    especies.append(path + x)

for y in especies:
    filenames.append(y.replace('\n', ''))
for n in range(1,len(filenames)):
    a[filenames[n-1]] = RM.Extract(filenames[n-1],'reactant',-1)
    a[filenames[n-1]].ext()
    a[filenames[n-1]].calc_Q()
    a[filenames[n]] = RM.Extract(filenames[n],'ts',-1)
    a[filenames[n]].ext()
    a[filenames[n]].calc_Q()
    
    if a[filenames[n-1]].p['En'] != a[filenames[n]].p['En']:
        b = RM.Rate_Calc(a[filenames[n-1]],a['none'],a[filenames[n]],a['none'], a['none'])
        b.Calc()
        reaction = b
        taxa = RM.Variational_TST(reaction,filenames)
        #taxa.Calc()

#print(taxa.p['kvtst'])






