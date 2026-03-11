# ---------------------------------------------------------------------------------------------------------
"""
    1.Tendo como dado de entrada a altura (h) de uma pessoa, construa um
    algoritmo que calcule seu peso ideal, utilizando as seguintes fórmulas:
    1. Para homens: (72.7*h) - 58
    2. Para mulheres: (62.1*h) - 44.7
    Obs: Construir funções independes: uma para homens e outra para
    mulheres. O retorno decimal de cada função deve ser formatado em 2
    casa decimais.

"""
# ---------------------------------------------------------------------------------------------------------

def pesoIdealHomem(h: float):
    """
        Calcula o peso ideal do homem pela altura.

        Args:
            h: Valor da altura(float)
    """
    peso_ideal = (72.7*h) - 58
    rounded_value = round(peso_ideal,2)
    return rounded_value

def pesoIdealMulher(h: float):
    """
        Calcula o peso ideal do mulher pela altura.

        Args:
            h: Valor da altura(float)
    """
    peso_ideal = (62.1*h) - 44.7
    rounded_value = round(peso_ideal,2)
    return rounded_value

# ---------------------------------------------------------------------------------------------------------
"""
    2. Faça um Programa que peça a temperatura em graus Fahrenheit,
    transforme e mostre a temperatura em graus Celsius.
    C = 5 * ((F-32) / 9).
    Obs: Deve-se realiza um tratamento, onde o valor em Fahrenheit não
    deve ser negativo
"""
# ---------------------------------------------------------------------------------------------------------

def fahrenheitToCelsius(F: float):
    """
        Converte o valor de graus Fahrenheit para graus Celsius

        Args:
            F: Valor em Fahrenheit(float)
    """
    if F >= 0:
        C = 5 * ((F-32) / 9)
        rounded_value = round(C, 2)
        return rounded_value
    else: 
        return "Valor em Fahrenheit não deve ser menor que zero."
    
# ---------------------------------------------------------------------------------------------------------    
"""
    3. Faça um programa que leia e valide as seguintes informações:
    1. Nome: maior que 3 caracteres;
    2. Idade: entre 0 e 150;
    3. Salário: maior que zero;
    4. Sexo: 'f' ou 'm';
    5. Estado Civil: 's', 'c', 'v', 'd’;
    Obs: Deve ser criado uma função para cada item a ser verificado.
"""
# ---------------------------------------------------------------------------------------------------------

def validateName(name: str):
    """
        Valida se nome possui mais que 3 caracteres

        Args: 
            name: Valor de nome(string)
    """
    if len(name) > 3:
        return True
    else: 
        return False
    
def validateAge(age: int):
    """
        Valida se a idade está entre 0 e 150 anos.

        Args: 
            age: Valor da idade em anos(int)
    """
    if age >= 0 and age <= 150:
        return True
    else: 
        return False
    
def validateSalary(salary: float):
    """
        Valida se o salário é maior que zero.

        Args: 
            salary: Valor do salário(float)
    """
    if salary > 0:
        return True
    else: 
        return False
    
def validateGender(gender: str):
    """
        Valida se o gênero é feminino ou masculino.

        Args: 
            gender: Valor de gênero(str)
    """
    if gender == 'f':
        return "Feminino"
    elif gender == 'm':
        return "Masculino" 
    else: 
        return False
    
def validateStatus(status: str):
    """
        Valida o estado civil da pessoa, se está solteira('s'), casado('c'), viuvo('v'), divorciado('d').

        Args: 
            status: Valor dos status(str)
    """
    statusDict = {
        's': 'Solteiro',
        'c': 'Casado',
        'v': 'Viuvo',
        'd': 'Divorciado'
    }
    if status in statusDict:
        return statusDict[status]
    else: 
        return "Estado civil inválido"
    
# ---------------------------------------------------------------------------------------------------------
"""
    4. Faça um programa que, determine o maior valor e a soma dos valores.
    Obs: pode-se utiliza a lista = [1,2,3,4,5,6,7,8, 10]
"""
# ---------------------------------------------------------------------------------------------------------

def setHigherValue(values: list):
    """
        Determina o maior valor na lista.

        Args: 
            list: Lista com valores inteiros ou decimais(float)
    """
    numMaior = values[0]
    for i in range(len(values)):
        if values[i] > numMaior:
            numMaior = values[i]
    return numMaior

def sumListValues(values: list):
    """
        Soma os valores da lista

        Args: 
            list: Lista com valores inteiros ou decimais(float)
    """
    soma = 0
    for i in range(len(values)):
        soma += values[i]
    
    return soma

# ---------------------------------------------------------------------------------------------------------

# Valores mockado:
print(f"\n\n ---> Exercício 1: \nHomem: {pesoIdealHomem(1.75)} - Mulher: {pesoIdealMulher(1.75)}\n\n")
print(f" ---> Exercício 2: \nValor em graus Celsius: {fahrenheitToCelsius(30)}\n\n")
print(f" ---> Exercício 3: \nValidação do nome: {validateName("tiago")} - Validação da idade: {validateAge(175)} - Validação do salário: {validateSalary(-10)}...\nValidação do gênero: {validateGender("m")} - Validação do estado civil: {validateStatus("d")}\n\n")
print(f" ---> Exercício 4: \nMaior valor da lista: {setHigherValue([1,2,3,4,5,6,7,8, 10])} - A soma dos valores da lista: {sumListValues([1,2,3,4,5,6,7,8, 10])}")

# # Valores dinâmicos: 
# altura = float(input("Informe a altura: "))
# fahrenheit = float(input("Informe quantos graus fahrenheit: "))
# nome = str(input("Informe o nome: "))
# idade = int(input("Informe a idade: "))
# salario = float(input("Informe o salário: "))
# genero = str(input("Informe o gênero('f' ou 'm'): "))
# estado_civil = str(input("Informe o estado civil('s', 'c', 'v' ou 'd'): "))
# lista = list(input("Informe a lista de valores([1, 2, 3, 4...]): "))

# print(f"\n\n ---> Exercício 1: \nHomem: {pesoIdealHomem(altura)} - Mulher: {pesoIdealMulher(altura)}\n\n")
# print(f" ---> Exercício 2: \nValor em graus Celsius: {fahrenheitToCelsius(fahrenheit)}\n\n")
# print(f" ---> Exercício 3: \nValidação do nome: {validateName(nome)} - Validação da idade: {validateAge(idade)} - Validação do salário: {validateSalary(salario)}...\nValidação do gênero: {validateGender(genero)} - Validação do estado civil: {validateStatus(estado_civil)}\n\n")
# print(f" ---> Exercício 4: \nMaior valor da lista: {setHigherValue([1,2,3,4,5,6,7,8, 10])} - A soma dos valores da lista: {sumListValues([1,2,3,4,5,6,7,8, 10])}")