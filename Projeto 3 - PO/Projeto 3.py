
'''
Projeto: Cadeia de suprimentos
Autores: Joison Oliveira, Laura Campos, Wendson Carlos
Linguagem: Python
Biblioteca: Pulp 
 
'''
from pulp import *

def crie_matriz(n_linhas, n_colunas, valor):
    
    matriz = [] # lista vazia

    for i in range(n_linhas):
        linha = [] # lista vazia
        for j in range(n_colunas):
            linha += [valor]
        matriz += [linha]

    return matriz

########################################################################
#Leitura de arquivo

file = open("instancia.txt","r")

instancia = []

for line in file:
    instancia.append(line.rstrip())

#Setando as variáveis
pTonelada = instancia[0]
cc = instancia[1]
cf = instancia[2]
nFabricas = instancia[3]
kCentros = instancia[4]
mCidades = instancia[5]

inicio = 6
fim = int(nFabricas) + 6
exp = instancia[inicio:fim]

inicio = fim
fim = fim + int(kCentros)

fcentros = instancia[inicio:fim]

print(fcentros)

lista_f = []
iFabrica = []
cFabrica = []
capFabrica = []
lista = []
custoFab = []
custoCentros = []

for i in exp:
    lista.append(i.split())
    
for i in fcentros:
    lista_f.append(i.split())

print(lista_f)

i=0

while i < len(lista_f):
    custoCentros.append(int(lista_f[i][1]))
    i+=1
    
print(custoCentros)
    
j=0
i=0
   
while i < len(lista): 
    while j < 3:
        if(j==0):
            iFabrica.append(lista[i][j])
        
        if(j==1):
            cFabrica.append(lista[i][j])
        
        if(j==2):
            capFabrica.append(lista[i][j])
        j+=1        
    j=0
    i+=1

i_Fabrica = []
for elemento in iFabrica:
    i_Fabrica.append(int(elemento))

c_Fabrica = []
for elemento in cFabrica:
    c_Fabrica.append(int(elemento))

cap_Fabrica = []
for elemento in capFabrica:
    cap_Fabrica.append(int(elemento))
 
inicio = fim
fim = fim + int(mCidades)
linha = instancia[inicio:fim]

demandas = {}

listaCD = []

for i in linha:
    listaCD.append(i.split())

i = 0
j = 0

while i < len(linha):
    
    if(j == 2):
        j = 0
    demandas[int(listaCD[i][j])] = int(listaCD[i][j+1])

    i+=1

inicio = fim
fim = fim+(int(nFabricas)*int(mCidades))

#lista de distancia entre fabricas e municipios/cidades
listaDFM = instancia[inicio:fim]

lista_DFM = []
for i in listaDFM:
    lista_DFM.append(i.split())

listaDFM = []
j = 0
i = 0

while i < len(lista_DFM):
    listaDFM.append(float(lista_DFM[i][2]))
    i+=1


k = 0
DFM = crie_matriz(int(nFabricas), int(mCidades), 0)
while(k < len(listaDFM)):
    for i in range(int(nFabricas)):
        for j in range(int(mCidades)):
            DFM[i][j] = float(listaDFM[k])
            k+=1
print(DFM)

inicio = fim
fim = fim+(int(nFabricas)*int(kCentros))

#lista de distancia entre fabricas e centros de distribuição
listaDFC = instancia[inicio:fim]

lista_DFC = []
for i in listaDFC:
    lista_DFC.append(i.split())
    
listaDFC = []
j = 0
i = 0

while i < len(lista_DFC):
    listaDFC.append(float(lista_DFC[i][2]))
    i+=1
    
k = 0
DFC = crie_matriz(int(nFabricas), int(kCentros), 0)
while(k < len(listaDFC)):
    for i in range(int(nFabricas)):
        for j in range(int(kCentros)):
            DFC[i][j] = float(listaDFC[k])
            k+=1
print(DFC)

inicio = fim
fim = fim+(int(kCentros)*int(mCidades))

#lista de distancia entre centros de distribuição e cidades
listaDCC = instancia[inicio:fim]

lista_DCC = []
for i in listaDCC:
    lista_DCC.append(i.split())

listaDCC = []
j = 0
i = 0

while i < len(lista_DCC):
    listaDCC.append(float(lista_DCC[i][2]))
    i+=1
    
k = 0
DCC = crie_matriz(int(kCentros), int(mCidades), 0)
while(k < len(listaDCC)):
    for i in range(int(kCentros)):
        for j in range(int(mCidades)):
            DCC[i][j] = float(listaDCC[k])
            k+=1
print(DCC)

########################################################################
#Varivaeis de decisão

var_x = {}
var_y = {}
var_z = {}
var_w = {}

i = 0
j = 0

for i in range(int(nFabricas)):
    for j in range(int(mCidades)):
        var_x[(i,j)]= LpVariable(name = f'x{i}{j}', cat = 'Integer', lowBound=0)
        
    var_x.update(var_x)
        

for i in range(int(nFabricas)):
    for j in range(int(kCentros)):
        var_y[(i,j)]= LpVariable(name = f'y{i}{j}', cat = 'Integer', lowBound=0)
      
    var_y.update(var_y)


for i in range(int(kCentros)):
    for j in range(int(mCidades)):
        var_z[(i,j)]= LpVariable(name = f'z{i}{j}', cat = 'Integer', lowBound=0)
      
    var_z.update(var_z)

for i in range(int(kCentros)):
    var_w[(i)]= LpVariable(name = f'w{i}', cat = 'Binary')
      
    var_w.update(var_w)

########################################################################
#Criação do modelo

model = LpProblem("Cadeia_suprimentos", LpMaximize)

lista_x = []
lista_y = []
lista_z = []
lista_custos_x = []
lista_custos_y = []
lista_distancia_x = []
lista_distancia_y = []
lista_distancia_z = []
lista_custo_centros = []

       
for x in var_x.keys():
    lista_x.append(int(pTonelada)*var_x[x])

for y in var_y.keys():
    lista_y.append(int(pTonelada)*var_y[y])  

custoFab = list(map(int, cFabrica))

for x in var_x.keys():
    lista_custos_x.append(custoFab[x[0]]*var_x[x])
    
for y in var_y.keys():
    lista_custos_y.append(custoFab[y[0]]*var_y[y])
    
for x in var_x.keys():
    lista_distancia_x.append(float(cc)*DFM[x[0]][x[1]]*var_x[x])
    
for y in var_y.keys():
    lista_distancia_y.append(float(cf)*DFC[y[0]][y[1]]*var_y[y])
    
for z in var_z.keys():
    lista_distancia_z.append(float(cc)*DCC[z[0]][z[1]]*var_z[z])

for w in var_w.keys():
    lista_custo_centros.append(custoCentros[w]*var_w[w])

print(lista_custo_centros)
    
    
print('\n')
model += lpSum(lista_x) + lpSum(lista_y) - lpSum(lista_custos_x) - lpSum(lista_custos_y) - lpSum(lista_distancia_x) - lpSum(lista_distancia_y) - lpSum(lista_distancia_z) - lpSum(lista_custo_centros) 

########################################################################
#Restrição da variável de decisão

for i in var_y.keys():
    model += var_y[i] <= cap_Fabrica[i[0]]*var_w[i[1]]

########################################################################
#Restrição de capacidade

lista_rest1 = [[] for _ in range(int(nFabricas))]
lista_rest2 = [[] for _ in range(int(nFabricas))]

for i in range(int(nFabricas)):
    for j in range(int(mCidades)):
        lista_rest1[i].append(var_x[(i,j)])
            
for i in range(int(nFabricas)):
    for k in range(int(kCentros)):
        lista_rest2[i].append(var_y[(i,k)])
   
for i in range(int(nFabricas)):
    model += lpSum(lista_rest1[i]) + lpSum(lista_rest2[i]) <= cap_Fabrica[i]
    
########################################################################
#Restrição de demanda

lista_rest3 = [[] for _ in range(int(mCidades))]
lista_rest4 = [[] for _ in range(int(mCidades))]
lista_demanda = []

for x in demandas.keys():
    lista_demanda.append(demandas[x])

for j in range(int(mCidades)):
    for i in range(int(nFabricas)):
        lista_rest3[j].append(var_x[(i,j)])

for j in range(int(mCidades)):
    for k in range(int(kCentros)):
        lista_rest4[j].append(var_z[(k,j)])

for j in range(int(mCidades)):
    model += lpSum(lista_rest3[j]) + lpSum(lista_rest4[j]) == lista_demanda[j]

########################################################################
#Restrição de conservação de fluxo 

lista_rest5 = [[] for _ in range(int(kCentros))]
lista_rest6 = [[] for _ in range(int(kCentros))]

for k in range(int(kCentros)):
    for i in range(int(nFabricas)):
        lista_rest5[k].append(var_y[(i,k)])

for k in range(int(kCentros)):
    for j in range(int(mCidades)):
        lista_rest6[k].append(var_z[(k,j)])
        
    
for k in range(int(kCentros)):
    model += lpSum(lista_rest5[k]) == lpSum(lista_rest6[k])
        
########################################################################

print(model)
status = model.solve()
print(LpStatus[status])
print(value(model.objective))

for x in var_x.values():
    if(var_x.values != 0):
        print(f'{x} =  {value(x)}')
    
for y in var_y.values():
    if(var_y.values != 0):
        print(f'{y} =  {value(y)}')

for z in var_z.values():
    if(var_z.values != 0):
        print(f'{z} =  {value(z)}')

for w in var_w.values():
    if(var_w.values != 0):
        print(f'{w} =  {value(w)}')
        