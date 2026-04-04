import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder

# Engenharia

#Utilizar a função carregarArquivo para carregar csv
def carregarArquivo(nomeArquivo):
    print("Carga do arquivo")
    dataset = None
    try:
        dataset = pd.read_csv(nomeArquivo)
    except:
        print("Não deu")
    return dataset

dados = carregarArquivo("cep_coordinates_per_capita_income.csv")
print(dados)

# tratar o arquivo
def tratamentoArquivo(dataset):
    print("Tratar os dados")
    # limpeza dos dados duplicados e nulos
    dataset.drop_duplicates(inplace=True)
    dataset.dropna(inplace=True)
    print(dataset.info())

    # Limpeza de dados sem CEP
    dataset = dataset[dataset['POSTCODE'] != 'Sem CEP']
    print(dataset.info())

    # remoção de tabelas que não serão utilizadas(a principio)
    dataset.drop(columns=["CD_GEOCODI", "LON", "LAT"], inplace=True)
    print(dataset.info())

    # Adição da coluna com primeiro caracter do cep para identificar a região
    dataset['Regiao'] = dataset['POSTCODE'].str[0]
    dict = {
        '0': 'Sede São Paulo',
        '1': 'Sede Santos',
        '2': 'Sede Rio de Janeiro',
        '3': 'Sede Belo Horizonte',
        '4': 'Sede Sede Salvador',
        '5': 'Sede Recife',
        '6': 'Sede Fortaleza',
        '7': 'Sede Brasília',
        '8': 'Sede Curitiba',
        '9': 'Sede Porto Alegre'
    }
    dataset['Regiao'] = dataset['Regiao'].map(dict)

    # Por estado
    dataset['cep'] = dataset['POSTCODE'].str.replace('-', '', regex=False).astype('int32') #criar a coluna cep númerica e sem "-"

    limites = [
        -1, 19999999, 28999999, 29999999, 39999999, 48999999, 49999999, 
        56999999, 57999999, 58999999, 59999999, 63999999, 64999999, 
        65999999, 68899999, 68999999, 69299999, 69399999, 69899999, 
        69999999, 72799999, 72999999, 73699999, 76799999, 76999999, 
        77999999, 78899999, 79999999, 87999999, 89999999, 99999999
    ]

    estados = [
        "SP", "RJ", "ES", "MG", "BA", "SE", "PE", "AL", "PB", "RN", 
        "CE", "PI", "MA", "PA", "AP", "AM", "RR", "AM", "AC", "DF", 
        "GO", "DF", "GO", "RO", "TO", "MT", "MS", "PR", "SC", "RS"
    ]

    dataset['uf'] = pd.cut(dataset['cep'], bins=limites, labels=estados, right=True, ordered=False)

    # entendendo o dataset
    print(dataset.info())
    print(dataset.head())
    print(dataset.describe())
    print(dataset.nunique()) # para ver quais colunas são categoricas
    print(dataset.shape)
    print(dataset.values)

    # Codificar os dados que são str
    lb = LabelEncoder()
    #dataset['POSTCODE'] = lb.fit_transform(dataset['POSTCODE']) # não vejo necessidade pois não é um dado categorico
    #dataset['Regiao'] = lb.fit_transform(dataset['Regiao'])
    print(dataset.info())

    return dataset

dados = tratamentoArquivo(dados)

"""
Isso aqui é código do professor, apenas copiei e colei, temos que modificar para usar no nosso código
def gerarBoxplot(dataset):
    fig, ax = plt.subplots()
    ax.set_ylabel("boxplot variáveis do Titanic")

    for n, col in enumerate(dataset.columns):
        if col == 'Age' or col == 'Fare':
            ax.boxplot(dataset[col], positions=[n+1])

    plt.title("Boxplot da coluna Age e Fare")
    plt.ylabel("Valores")
    plt.show()
"""

# Analise de dados

def visualizarDados(dataset):
    # Qual a média de renda per capita por região?
    media_renda = dataset.groupby('Regiao')['renda_per_capita'].mean()
    plt.figure(figsize=(10,6))
    media_renda.plot(kind='bar')
    plt.tight_layout
    plt.title('Renda por região')
    plt.show()

    # Qual a média de renda per capita por estado?
    media_renda = dataset.groupby('uf')['renda_per_capita'].mean()
    plt.figure(figsize=(10,6))
    media_renda.plot(kind='bar')
    plt.tight_layout
    plt.title('Renda por estado')
    plt.show()

    # Quais são as 5 regiões com maior ou menor variação (desvio padrão) por renda?


    # Existe uma concentração visual de renda em capitais comparado ao interior?

    #gerarBoxplot(dataset)

visualizarDados(dados)
