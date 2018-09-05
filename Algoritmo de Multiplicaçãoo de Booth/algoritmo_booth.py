# encoding=utf-8

# ALGORITMO DE BOOTH PARA A MULTIPLICAÇÃO DE NÚMEROS BINÁRIOS EM COMPLEMENTO DE DOIS
# POR
# IGOR OLIVEIRA DE SOUSA (118301)
# MATEUS CAPPELLARI VIEIRA (116514)


# DECLARAÇÃO DE FUNÇÕES:


def leitura():

    # Função que realiza a leitura dos dados fornecidos pelo usuário, e os retorna.

    print("")
    print("Digite dois números inteiros em decimal entre -16 e 15, a serem multiplicados entre si.")

    x = int(input())
    y = int(input())

    print("")

    if (x < -16) or (x > 15) or (y < -16) or (y > 15):

        print("Você digitou números fora do intervalo permitido. Por favor, insira números válidos.")
        return leitura()

    else:

        if y == -16 and x != -16:

            # Primeira particularidade do -16: Como estamos trabalhando com 5 bits, o -16 tem seu negativo em comple-
            # mento de dois idêntico ao seu positivo (16), (que inclusive não é representável com 5 bits). Por isso,
            # se este termo se encontrar como "M" (multiplicando), devemos transformá-lo em "Q" (multiplicador) para que
            #  as operações envolvendo complemento de dois internas ao Algoritmo de Booth não percam o sentido.

            print("Detectado multiplicando igual a -16, realizando troca pelo multiplicador.\n")

            aux = x
            x = y
            y = aux

        return x, y


def verificaSinal(x,y):

    # Verifica se os números são negativos, passo importante para o Python não converter erroneamente para binário.
    # Ex.: Se o número fosse -2, por exemplo, o Python converteria para '-00010'.
    # Caso o(s) número(s) seja(m) negativo(s), uma variável booleana guardará essa informação, que é retornada (mesmo
    # que seja(m) positivo(s).

    xIsNegative = False
    yIsNegative = False

    if x < 0:

        xIsNegative = True

    if y < 0:

        yIsNegative = True

    return xIsNegative, yIsNegative


def modulo(x, y, xIsNegative, yIsNegative):

    # Verifica se os operandos são negativos com base nas booleanas, e, se sim, retorna-os em módulo (enquanto seus
    # sinais continuam armazenados nas booleanas, ou seja, essa informação crucial não é perdida). A "modularização"
    # dos termos serve apenas para a conversão não ocorrer erroneamente como anteriormente mostrado.

    if xIsNegative:

        x = abs(x)

    if yIsNegative:

        y = abs(y)

    return x, y


def converteBin(x,y):

    # Utiliza comandos internos do Python 3.6 para converter números em decimal para strings binárias, e retorna-as.

    x = format(x, '05b')
    y = format(y, '05b')

    return x, y


def segmenta(x, y):

    # Separa os caracteres das strings binárias (os bits!) como elementos de listas ("arrays" do Python), e retorna-as.

    listaX = list(x)
    listaY = list(y)

    return listaX, listaY


def inverte(listaX):

    # Realiza o primeiro passo do complemento de dois, a inversão dos bits. (Complemento de um). Retorna uma nova
    # lista com o complemento de um.

    listaAux = listaX[:]

    # Usamos uma nova lista (clone) pois o Python copia por referência, o que significa que a  troca causaria com que
    # o valor inicial fosse perdido ao mudar os elementos dessa forma, o que é indesejável principalmente nos momentos
    # internos ao Algoritmo de Booth em que fazemos operações com complemento de dois.

    for i in range(len(listaAux)):

        if listaAux[i] == '0':
            listaAux[i] = '1'

        else:
            listaAux[i] = '0'

    return listaAux


def complementaUm(listaX):

    # Realiza o complemento de dois adicionando "1" ao resultado do complemento de um, percorrendo a lista e utilizando
    # lógica para produzí-lo: todos os "1"s encontrados se tornam "0", e quando se chega ao primeiro "0", o mesmo é
    # trocado por "1" e o operando, finalmente representado corretamente em complemento de dois, é retornado.

    cont = len(listaX)-1

    while cont > -1:

        if listaX[cont] == '0':

            listaX[cont] = '1'
            return listaX

        elif cont != 0:
            listaX[cont] = '0'

        cont -= 1

    return listaX


def concatena(acumulador, listaX):

    # Cria uma lista que terá como conteúdo o resultado da concatenação do conteúdo de duas outras.
    # Utilizada para produzir uma lista que contém o eventual resultado do algoritmo, concatenando o acumulador com o
    # multiplicador.

    resultado = acumulador + listaX

    return resultado


def deslocamento(resultado, q1):

    # Quando chamada, faz o deslocamento do resultado (acumulador e "Q" (multiplicador)), duplicando o bit mais signifi-
    # cativo e armazenando o último elemento ("Q0") da lista para "Q-1". Retorna ambos com o deslocamento aplicado.

    resultado.insert(0, resultado[0])
    q1 = resultado[-1]
    resultado.pop()

    return resultado, q1


def adicao(acumulador, listaY):

    # Faz a adição do acumulador com "M" (multiplicando), e retorna o resultado, no acumulador.

    termo1 = int("".join(acumulador), 2)
    termo2 = int("".join(listaY), 2)

    acumulador = list(format(termo1 + termo2, '05b'))

    if len(acumulador) == 6:

        # Se ocorrer que o novo acumulador excede o limite de bits, ignora-se o "intruso"!

        del acumulador[0]

    return acumulador


def subtracao(acumulador, listaY):
    
    # Subtrai "M" (multiplicando) do acumulador, e retorna o resultado, no próprio acumulador. Faz-se o complemento de
    # dois de "M" e soma-se ao invés de subtrair, pois as operações se equivalem.

    termo1 = int("".join(acumulador), 2)

    if int("".join(listaY), 2) != 0:

        termo2 = inverte(listaY)
        termo2 = complementaUm(termo2)

        termo2 = int("".join(termo2), 2)

        acumulador = list(format(termo1 + termo2, '05b'))

    else:
        
        # Se "M" for igual a zero, não há necessidade de fazer o complemento de dois e alterar para a soma, pois remover
        # zero de qualquer número é o mesmo que deixá-lo inalterado!
        
        acumulador = list(format(termo1, '05b'))

    if len(acumulador) == 6:
        del acumulador[0]

    return acumulador


def checarPares(q0, q1):

    # Verifica "Q0" e "Q-1", para determinar qual é o passo que deve ser seguido."

    caso = 1

    if (q0 == '0' and q1 == '0') or (q0 == '1' and q1 == '1'):
        return caso
    
    elif q0 == '0' and q1 == '1':
        
        caso = 2
        return caso
    
    else:
        
        caso = 3
        return caso


def algBooth(listaX, listaY):

    # Realiza o algoritmo de Booth, dado multiplicando e multiplicador em complemento de 2, e retorna seu resultado.

    acumulador = ['0', '0', '0', '0', '0']
    resultado = concatena(acumulador, listaX)
    q1 = '0'
    cont = 1

    print("Valores iniciais:")
    print("A:", "".join(acumulador), "Q:", "".join(listaX), "Q-1:", q1, "M:", "".join(listaY))
    print("")

    while cont < 6:

        input("Pressione Enter para realizar o Ciclo " + str(cont) + ".\n")
        print("Ciclo " + str(cont) + str(":"))

        caso = checarPares(resultado[9], q1)

        if caso == 1:

            resultado, q1 = deslocamento(resultado, q1)
            acumulador = resultado[0:5]
            listaX = resultado[5:10]

            print("Deslocamento:")
            print("A:", "".join(acumulador), "Q:", "".join(listaX), "Q-1:", q1, "M:", "".join(listaY))

            acumulador = resultado[0:5]

        elif caso == 2:

            acumulador = adicao(acumulador, listaY)

            print("A <- A + M:")

            novoResultado = []

            for i in resultado[5:10:1]:
                novoResultado.append(i)

            resultado = concatena(acumulador, novoResultado)
            acumulador = resultado[0:5]
            listaX = resultado[5:10]

            print("A:", "".join(acumulador), "Q:", "".join(listaX), "Q-1:", q1, "M:", "".join(listaY))

            resultado, q1 = deslocamento(resultado, q1)
            acumulador = resultado[0:5]
            listaX = resultado[5:10]

            print("Deslocamento:")
            print("A:", "".join(acumulador), "Q:", "".join(listaX), "Q-1:", q1, "M:", "".join(listaY))

            acumulador = resultado[0:5]

        else:

            acumulador = subtracao(acumulador, listaY)

            print("A <- A - M:")

            novoResultado = []

            for i in resultado[5:10:1]:
                novoResultado.append(i)

            resultado = concatena(acumulador, novoResultado)
            acumulador = resultado[0:5]
            listaX = resultado[5:10]

            print("A:", "".join(acumulador), "Q:", "".join(listaX), "Q-1:", q1, "M:", "".join(listaY))

            resultado, q1 = deslocamento(resultado, q1)
            acumulador = resultado[0:5]
            listaX = resultado[5:10]

            print("Deslocamento:")
            print("A:", "".join(acumulador), "Q:", "".join(listaX), "Q-1:", q1, "M:", "".join(listaY))

            acumulador = resultado[0:5]

        print("")
        cont += 1

    input("Pressione Enter para exibir o resultado da multiplicação em decimal e em binário.\n")
    return resultado

def converteParaDecimal(xIsNegative, yIsNegative, resultado):

    # Converte o resultado em complemento de 2 para decimal, e o retorna.

    if "".join(resultado)=='1100000000':

        # Passo 1 da segunda particularidade do -16. (Mais informações no código sequencial, linha 418).

        resultado = inverte(resultado)
        resultado = complementaUm(resultado)

    if (xIsNegative and yIsNegative) or (xIsNegative is False and yIsNegative is False):

        resultado = "".join(resultado)
        resultadoDecimal = int(resultado, 2)

    else:

        resultado = inverte(resultado)
        resultado = complementaUm(resultado)
        resultado = "".join(resultado)
        resultadoDecimal = int(resultado, 2)
        resultadoDecimal = "-" + str(resultadoDecimal)
        resultadoDecimal = int(resultadoDecimal)

    return resultadoDecimal


# -------------------------------------------------------------------------------------------------------------------- #

# CÓDIGO SEQUENCIAL:

# Prints de apresentação:

print("Algoritmo de Multiplicação de Booth")
print("por Igor Oliveira de Sousa, Mateus Cappellari Vieira")
print("")
input("Pressione Enter para começar.")

# Leitura dos multiplicadors em decimal:

multiplicador, multiplicando = leitura()

input("Pressione Enter para converter para complemento de dois.")

# Verificação do sinal dos operandos:

multiplicadorNegativo, multiplicandoNegativo = verificaSinal(multiplicador, multiplicando)

# Converte os operandos em positivos, se negativos, para realizar a conversão corretamente:

multiplicador, multiplicando = modulo(multiplicador, multiplicando, multiplicadorNegativo, multiplicandoNegativo)

# Converte os operandos em strings binárias:

multiplicador, multiplicando = converteBin(multiplicador, multiplicando)

# Segmentação:

multiplicadorLista, multiplicandoLista = segmenta(multiplicador, multiplicando)

# Complemento de 2:

if multiplicadorNegativo:
    multiplicadorLista = inverte(multiplicadorLista)
    multiplicadorLista = complementaUm(multiplicadorLista)
if multiplicandoNegativo:
    multiplicandoLista = inverte(multiplicandoLista)
    multiplicandoLista = complementaUm(multiplicandoLista)

print("Multiplicador(Q): " + "".join(multiplicadorLista))
print("Multiplicando(M): " + "".join(multiplicandoLista))

input("\nPressione Enter para iniciar o algoritmo de Booth.\n")

# Algoritmo de Booth:

resultado = algBooth(multiplicadorLista, multiplicandoLista)

# Prints finais:

print("Resultado final, em decimal:")

multi = converteParaDecimal(multiplicadorNegativo, multiplicandoNegativo, resultado)

print(multi)

if multi/16 == 16:

    # Finalmente, a segunda particularidade do -16: quando ele é multiplicado por ele mesmo no Algoritmo de Booth,
    # o resultado é -256, o que ocorre, novamente, porque -16 em 5 bits (10000) é igual a 16 em 6 bits (010000) quando
    # ignoramos o digito "intruso", o que OCORRE nas operações internas de complemento de dois do Algoritmo de Booth.
    # Por isso, esse bloco de "if" verifica se isso ocorreu, e, se sim, simplesmente faz o complemento de dois do resul-
    # tado, que de -256 vai para 256 (positivo), que é o correto.

    resultado = inverte(resultado)
    resultado = complementaUm(resultado)

resultado = "".join(resultado)

print("Resultado final, em binário (compl. 2):")
print(resultado)
input()