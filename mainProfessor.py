import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder


# carregar o arquivo
def carregarArquivo(nomeArquivo):
    print("carga de arquivo")
    dados = None
    try:
        dados = pd.read_csv(nomeArquivo)

    except:
        print("Não foi possivel carregar o arquivo")
    
    return dados

dados = carregarArquivo('Titanic-Dataset.csv')

print(dados)

# tratamento do arquivo
def tratamentoArquivo(dados):
    print("tratamento do arquivo")

    # descricao basica do arquivo: tipo, nulos, nome
    print(dados.info())

    # retorna as primeiras 5 linhas do arquivo
    print(dados.head())

    # retorna as ultimas 5 linhas do arquivo
    print(dados.tail())

    print(dados.describe())

    # remover os dados duplicados
    # dados = dados.drop_duplicates()
    dados.drop_duplicates(inplace=True)

    # remover as colunas existentes na lista
    dados.drop(columns=["PassengerId", "Name", "Ticket", "Cabin"], inplace=True)

    # remove os dados nulos
    dados.dropna(inplace=True)

    print(dados.info())


    # decodifica dados categoricos em valores numericos
    lb = LabelEncoder()
    dados['Sex'] = lb.fit_transform(dados['Sex'])
    dados['Embarked'] = lb.fit_transform(dados['Embarked'])
    print(dados.info())
    print(dados.head())
    print(dados.shape)
    print(dados.values)

    # mater valores entre 0 e 62 (inclusive)
    dados = dados[dados["Age"].between(0, 60, inclusive="neither")]
    dados = dados[dados["Fare"].between(0, 55, inclusive="neither")]

    return dados

dados = tratamentoArquivo(dados)

def gerarBoxplot(dados):
    fig, ax = plt.subplots()
    ax.set_ylabel('boxplot variáveis do Titanic')

    for n, col in enumerate(dados.columns):
        if col == 'Age' or col == 'Fare':
            ax.boxplot(dados[col], positions=[n+1])

    plt.title("Boxplot da coluna Age e Fare")
    plt.ylabel("Valores")
    plt.show()

# analise de dados
def visualizarDados(dados):

    dados['Age'].hist()
    plt.show()

    dados['Embarked'].hist()
    plt.show()

    dados['Survived'].hist()
    plt.show()

    gerarBoxplot(dados)

visualizarDados(dados)