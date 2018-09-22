#encoding = utf-8

# ALGORITMO DE CODIFICAÇÃO DE HUFFMAN #
# POR MATEUS CAPPELLARI VIEIRA #
# 116514 #

import heapq


def transformaLista(string):
    stringLista = list(string)

    return stringLista


def contaLetras(lista):

    frequencias = []

    for char in lista:
        encontrado = False
        for i in frequencias:
            if char == i[1]:
                i[0] += 1
                encontrado = True
        if encontrado is False:
            frequencias.append([1, char])
    return frequencias


def ordenaFrequencias(frequencias):
    frequencias.sort(key=lambda lista: lista[0])

    return frequencias


def criaArvore(frequencias):

    heap = []

    for i in frequencias:
        heapq.heappush(heap, [i])

    while len(heap) > 1:

        filhoEsquerdo = heapq.heappop(heap)
        filhoDireito = heapq.heappop(heap)

        freqEsquerdo, nomeEsquerdo = filhoEsquerdo[0]
        freqDireito, nomeDireito = filhoDireito[0]

        freq = freqEsquerdo + freqDireito
        nome = "".join(sorted(nomeDireito + nomeEsquerdo))
        nodo = [(freq, nome), filhoEsquerdo, filhoDireito]

        heapq.heappush(heap, nodo)

    return heap.pop()

def percorreArvore(arvore, dicion, prefixo):

    if (len(arvore) == 1):
        # Ou seja, estamos em um nó folha.
        freq, nome = arvore[0]
        dicion[nome] = prefixo
    else:
        valor, filhoEsquerdo, filhoDireito = arvore
        percorreArvore(filhoEsquerdo, dicion, prefixo + "0")
        percorreArvore(filhoDireito, dicion, prefixo + "1")


def dicionario(arvore):

    dicion = dict()
    percorreArvore(arvore, dicion, '')

    return dicion


def codificacao(mapa, string):
    palavraCodificada = ''.join([mapa[letra] for letra in string])

    return palavraCodificada


def decodificacao(palavraCodificada, arvore):

    arvoreTemp = arvore

    digitosDecodificados = []

    for digito in palavraCodificada:
        if digito == "0":
            arvoreTemp = arvoreTemp[1]
        else:
            arvoreTemp = arvoreTemp[2]
        if (len(arvoreTemp) == 1):
            freq, nome = arvoreTemp[0]
            digitosDecodificados.append(nome)
            arvoreTemp = arvore # Volta ao topo a fim de que a próxima letra possa ser encontrada.

    palavraDecodificada = "".join(digitosDecodificados)

    return palavraDecodificada

print("Algoritmo de codificação de Huffman")
print("por Mateus Cappellari Vieira")
palavra = input("\nDigite a palavra que desejas codificar.\n")

palavraLista = transformaLista(palavra)
ocorrencias = contaLetras(palavraLista)
ocorrencias = ordenaFrequencias(ocorrencias)
ocorrencias = [tuple(x) for x in ocorrencias]
arvoreResultante = criaArvore(ocorrencias)
mapeamentoDaArvore = dicionario(arvoreResultante)
codificado = codificacao(mapeamentoDaArvore, palavra)

print("\nResultado codificado:\n" + str(codificado) + "\n")

while True:
    decisao = int(input("Digite 1 se deseja decodificar a palavra, 2 se deseja ver o dicionário, e qualquer outra entrada"
          " se deseja finalizar o programa.\n"))

    if decisao == 1:
        palavraDecodificada = decodificacao(codificado, arvoreResultante)
        print("\nPalavra decodificada:\n" + str(palavraDecodificada) + "\n")
    elif decisao == 2:
        print("\nDicionário utilizado:\n" + str(mapeamentoDaArvore) + "\n")
    else:
        break