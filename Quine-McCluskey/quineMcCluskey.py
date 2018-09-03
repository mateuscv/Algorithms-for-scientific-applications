#encoding=UTF-8

# Este é o código que realiza o método de Quine McCluskey em minitermos de até quatro variáveis. (A, B, C, D).
# Por:
# MATEUS CAPPELLARI VEIRA 116514
# IGOR OLIVEIRA DE SOUSA 118301
# THIAGO JANSEN SAMPAIO COSTA 116502


#------------------# DECLARAÇÃO DE FUNÇOES #-----------------------#

# FUNÇÃO QUE DIVIDE LISTAS DE MINITERMOS DESORDENADAS EM GRUPOS DE ACORDO COMO NÚMERO DE "UNS" : #

def separa(listaminitermos):
    grupo0 = []
    grupo1 = []
    grupo2 = []
    grupo3 = []
    grupo4 = []
    for minitermos in listaminitermos:
        cont=0
        for digitos in minitermos:
            if digitos=="1":
                cont+=1
        if cont == 0:
            grupo0.append(minitermos)
        if cont == 1:
            grupo1.append(minitermos)
        if cont == 2:
            grupo2.append(minitermos)
        if cont == 3:
            grupo3.append(minitermos)
        if cont == 4:
            grupo4.append(minitermos)
    return [grupo0, grupo1, grupo2, grupo3, grupo4]

#---------------------------------------------------------------------------------#

# FUNÇÃO QUE COMPARA OS MINITERMOS E ADICIONA LACUNAS ONDE HÁ DIFERENÇA DE BIT : #

def compara(matriz):
    lacuninhas = []
    termos_utilizados = []
    cont = 0
    while (cont<4):
        indice=0
        diferente=0
        for minitermos1 in matriz[cont]:
            for minitermos2 in matriz[cont+1]:
                while (indice<len(minitermos1)):
                    if minitermos1[indice]!=minitermos2[indice]:
                        diferente+=1
                        valor = indice
                    indice += 1

                if diferente == 1:
                    termos_utilizados.append(minitermos1)
                    termos_utilizados.append(minitermos2)
                    aux = minitermos1[valor]
                    minitermos1 = list(minitermos1)
                    minitermos1[valor]="_"
                    if "".join(minitermos1) not in lacuninhas:
                        lacuninhas.append("".join(minitermos1))
                    minitermos1[valor] = aux
                    minitermos1 = "".join(minitermos1)
                diferente = 0
                indice = 0
            if "_" in minitermos1 and minitermos1 not in termos_utilizados:
                lacuninhas.append(minitermos1)
        cont+=1
    return lacuninhas

#---------------------------------------------------------------------------------#

# FUNÇÃO QUE UTILIZA A LISTA DE MINITERMOS ORIGINAL E A LISTA COM OS MINITERMOS JÁ COM LACUNAS PARA RETORNAR
# OS MINITERMOS DA FORMA MAIS SIMPLIFICADA POSSÍVEL : #

def reduz_termos(lacuninhas, listaminitermos):
    nova_matriz=[]
    for i in range(0,len(lacuninhas)):
        nova_matriz.append([])
    diferente = 0
    for minitermos1 in lacuninhas:
        for minitermos2 in listaminitermos:
            indice = 0
            while (indice < len(minitermos1)):
                if minitermos1[indice] != minitermos2[indice]:
                    diferente += 1
                indice += 1
            if (diferente ==1 or (diferente == 2 and minitermos1.count("_")== 2)):
                nova_matriz[lacuninhas.index(minitermos1)].append(minitermos2)
            diferente = 0
    i = 0
    j = 0
    resposta = []
    diferente = 0
    while (i<len(nova_matriz)):
        minitermo = nova_matriz[i][j]
        aparicoes = 0
        for x in nova_matriz:
            aparicoes += x.count(minitermo)
        if aparicoes == 1:
            for minitermos1 in lacuninhas:
                indice = 0
                while indice < len(minitermos1):
                    if minitermos1[indice]!=minitermo[indice]:
                        diferente +=1
                    indice += 1
                if (diferente == 1 or (diferente==2 and minitermos1.count("_")==2)) and (minitermos1 not in resposta):
                    resposta.append(minitermos1)
                diferente = 0
        j+=1
        if j==len(nova_matriz[i]):
            j=0
            i+=1
    return resposta

#---------------------------------------------------------------------------------#

# FUNÇÃO QUE TRANSFORMA A RESPOSTA EM UMA EXPRESSÃO LÓGICA: #

def transforma(resposta):
    formula=[]
    for i in range(0, len(resposta)):
        for j in range(0, len(resposta[i])):
            if resposta[i][j]=="1":
                if j==0:
                    formula.append("A")
                elif j==1:
                    formula.append("B")
                elif j==2:
                    formula.append("C")
                elif j==3:
                    formula.append("D")
            elif resposta[i][j]=="0":
                if j==0:
                    formula.append("¬A")
                elif j==1:
                    formula.append("¬B")
                elif j==2:
                    formula.append("¬C")
                elif j==3:
                    formula.append("¬D")
        formula.append("+")
    return formula

#------------------# CÓDIGO SEQUENCIAL #-----------------------#

# Declaração da lisa de minitermos:

listaminitermos=["0100","1000","1001","1010","1100","1011","1110","1111", "0001", "0110", "1101"]

# Criação de matriz com os grupos separados em ordem, como especificado:

matriz = separa(listaminitermos)

# Criação de lista com os minitermos já com lacunas e separação da mesma de acordo com a quantia de "uns":

lacuninhas = compara(matriz)
matriz = separa(lacuninhas)
lacuninhas = compara(matriz)

# Pega-se a resposta da função de redução dos termos e transforma-se a mesma em expressão lógica:

resposta = reduz_termos(lacuninhas, listaminitermos)
formula = transforma(resposta)

# Mostra na tela o resultado final em expressão lógica:

print("y = ", end="")
for i in range(0, len(formula)):
    if i < len(formula)-1 and formula[i]!="+":
        print(formula[i],end="")
    if formula[i]=="+" and i < len(formula)-1:
        print(" + ", end="")
input()