# encoding = utf-8

# ALGORITMO DE CONVERSÃO DECIMAL/PONTO FLUTUANTE
# ARQUITETURA DE COMPUTADORES
# POR MATEUS CAPPELLARI VIEIRA
# MATRICULA: 116514


# DECLARAÇÃO DE FUNÇÕES:

# 1.0 FUNÇÕES DE CONVERSÃO DECIMAL -> PONTO FLUTUANTE


def leitura():

    # Realiza a leitura do número em decimal, e retorna-o.

    x = float(input("Digite o número em decimal.\n"))
    return x


def checaSinal(x):

    # Verifica o sinal do número em decimal, e retorna uma booleana para este fim.

    if x < 0:
        xNegativo = True
    else:
        xNegativo = False

    return xNegativo


def modulariza(x):

    # Modulariza o número se for negativo, pois senão o Python converterá para binário errrado (-2 viraria -10).

    x = abs(x)
    return x


def converteBin(x):

    # Converte a parte inteira do número para binário.

    binIntegerInput = format(int(x), 'b')

    return binIntegerInput


def parteFracionaria(x):

    # Faz a operação de multiplicar por 2, pegar a parte inteira, multiplicar por 2 a parte fracionária do resultado,
    # e etc. Após esse processo, retorna a parte fracionária do número convertida para binário.

    x -= int(x)

    binarioF = []

    while x != 0.0:
        x = x * 2
        binarioF.append(str(int(x)))
        x -= int(x)

    return binarioF


def normalizacao(binIntegerInput, binarioF, x):

    # Realiza a normalização da mantissa e as operações envolvendo a polarização do expoente.
    # Também checa se ocorreu overflow ou underflow e finaliza a execução do programa se encontrar qualquer um dos
    # mesmos.

    binIntegerInput = list(binIntegerInput)
    exp = 0

    while len(binIntegerInput) != 1:
        binarioF.insert(0, binIntegerInput[-1])
        binIntegerInput.pop()
        exp += 1

    while binIntegerInput[-1] != '1':
        if binarioF == []:
            break
        else:
            binIntegerInput.append(binarioF[0])
            del binarioF[0]
            exp -= 1

    binIntegerInput = binIntegerInput[-1::]

    if len(binarioF) == 0:
        binarioF.append('0')

    if exp > 16:
        print("\nOverflow! Não é possível representar seu número. Por favor reinicie o programa para tentar"
              "novamente.")
        exit()
    if exp < -15:
        print("\nUnderflow! Não é possível representar seu número. Por favor reinicie o programa para tentar"
              "novamente. ")
        exit()

    if x != 0:
        expoenteReal = exp + (2**(5-1)-1)
    else:
        expoenteReal = 0

    expoenteRealBin = "".join(format(expoenteReal, '05b'))

    return binIntegerInput, binarioF, expoenteRealBin, exp


def completaMantissa(binarioF):

    # Completa a mantissa com 0s a direita, se necessário.
    # Também corta excessos no tamanho da mesma.

    while len(binarioF) < 10:
        binarioF.append('0')

    if len(binarioF) > 10:
        binarioF = binarioF[0:10]

    return "".join(binarioF)


# 2.0 FUNÇÕES DE CONVERSÃO PONTO FLUTUANTE -> BINÁRIO


def leituraPF():

    # Faz a leitura do número na representação completa de ponto flutuante de 16 bits, e o retorna.

    x = input("Digite toda a representação completa, com 1 espaço entre cada segmento"
          ", na forma: Sinal, Expoente, Mantissa. Ex: 0 10011 0110101000\n")

    if len(x) != 18:
        print("\nVocê não inseriu a entrada corretamente.\n")
        return leituraPF()

    return x


def converteMantissaDecimal(binarioF):

    # Faz a soma da mantissa, utilizando a técnica em que percorremos a mesma multiplicando cada bit pela base
    # elevada na posição.

    termosSoma = []
    cont = 0

    while cont < len(binarioF):
        if binarioF[cont] == "1":
            termo = int(binarioF[cont]) * 2.0**(-(cont+1))
            termosSoma.append(termo)
        cont += 1

    soma = sum(termosSoma)
    soma += 1
    return soma


def corrigeExpoente(exp):

    # Faz com que o expoente retorne à sua representação padrão.

    exp = int(exp, 2)
    exp = exp-(2**(5-1)-1)

    return exp


def multiplicaPotencia(soma, exp, sign):

    # Multiplica a soma pela base elevada no expoente, e adiciona o sinal:

    x = soma * 2**exp

    if sign == '1': x = x*-1

    return x


# CÓDIGO SEQUENCIAL:


print("\nAlgoritmo de Conversão Decimal/Ponto Flutuante")
print("Por Mateus Cappellari Vieira")

print("\nEste algoritmo utiliza um bit de sinal e a representação do sinal é condicionada apenas a ele (sinal + "
      "magnitude).")
print("Use ponto '.' ao invés de vírgula ','!")

while True:

    # Laço principal, permite que o menu de escolha de operação re-apareça ao finalizar uma operação.

    decisao = input("\nDigite 1 se deseja transformar de decimal para ponto flutuante, 2 se deseja "
                        "transformar de ponto flutuante para decimal, e outra entrada para encerrar.\n")
    if decisao == '1':

        # Realiza a leitura do número em decimal:

        decimal = leitura()

        # Verifica o sinal do número em decimal:

        decimalIsNegative = checaSinal(decimal)

        # Se o número é negativo, modulariza-o pois senão o Python converterá para binário errrado (-2 viraria -10):

        if decimalIsNegative: decimal = modulariza(decimal)

        # Converte a parte inteira do número para binário:

        inteiroBinario = converteBin(decimal)
        input("\nPressione Enter para ver a parte inteira de seu número convertida para binário.")
        print(inteiroBinario+"\n")

        # Converte a parte fracionária do número para binário:

        fracioBinaria = parteFracionaria(decimal)
        input("Pressione Enter para ver a parte fracionária de seu número convertida para binário.")
        print("Seu número é inteiro!\n") if fracioBinaria == [] else print("".join(fracioBinaria)+"\n")

        # Retorna a forma normalizada, assim como o expoente Real:

        numeroAnterior, mantissa, expoenteBin, expoente = normalizacao(inteiroBinario, fracioBinaria, decimal)

        # Apresenta o resultado parcial na tela do console:

        input("Pressione Enter para ver a representação parcial do resultado.\n")
        print("Representação parcial:")
        print("".join(numeroAnterior) + "," + "".join(mantissa) + " x 2^" + str(expoente))

        # Completa a mantissa com 0s a direita, se necessário:

        mantissa = completaMantissa(mantissa)

        # Condicional para determinar qual será o valor do bit de sinal:

        if decimalIsNegative:
            sinal = 1
        else:
            sinal = 0

        # Apresenta a representação completa na tela:

        input("\nPressione Enter para ver a representação completa do resultado.")
        print("\nRepresentação completa: ")
        print(str(sinal) + " " + str(expoenteBin) + " " + mantissa)

    elif decisao == '2':

        # Faz a leitura do número na representação completa de ponto flutuante de 16 bits:

        representacao = leituraPF()

        # Utiliza list slicing para cortar a entrada e armazenar cada segmento da mesma em seus respectivos arrays:

        sinal = representacao[0:1]
        expoente = representacao[2:7]
        mantissa = representacao[8:]

        # Faz a soma da mantissa, utilizando a técnica em que percorremos a mesma multiplicando cada bit pela base
        # elevada na posição:

        somaTotal = converteMantissaDecimal(mantissa)
        if representacao != "0 00000 0000000000" and representacao != "1 00000 0000000000":
            input("\nPressione Enter para ver o total da mantissa convertida para decimal.")
            print(somaTotal)

        # Faz com que o expoente retorne a sua representação padrão:

        expoente = corrigeExpoente(expoente)

        # Prepara o resultado final multiplicando a soma pela base elevada no expoente, e adiciona o sinal:

        input("\nPressione Enter para ver seu número em decimal.")
        decimal = multiplicaPotencia(somaTotal, expoente, sinal)

        # Apresenta o resultado na tela:

        print("\nSeu número, em decimal:")
        print(decimal) if representacao != "0 00000 0000000000" and representacao != "1 00000 0000000000" else \
            print("0")

    else:

        # Finaliza o programa se nenhuma opção válida for selecionada:

        break
