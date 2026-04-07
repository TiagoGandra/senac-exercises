import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder

# Engenharia

#Utilizar a função carregarArquivo para carregar csv

def carregarArquivo(nomeArquivo):
    print("carga de arquivo")
    dados = None
    try:
        dados = pd.read_csv(nomeArquivo)

    except FileNotFoundError:
        print(f"Não foi possível carregar o arquivo: {nomeArquivo}.")
    
    return dados

dados = carregarArquivo('cep_coordinates_per_capita_income.csv')

print(dados)
# tratar o arquivo
def tratamentoArquivo(dataset):
    print("Tratar os dados")
    # Informações básicas do dataset
    print(dataset.info())
    print(dataset.head())
    print(dataset.describe())
    print(dataset.nunique()) # para ver quais colunas são categoricas
    print(dataset.shape)
    print(dataset.values)

    # limpeza dos dados duplicados e nulos
    dataset.drop_duplicates(inplace=True)
    dataset.dropna(inplace=True)
    dataset = dataset[dataset['POSTCODE'] != 'Sem CEP']
    dataset.drop(columns=["CD_GEOCODI", "LON", "LAT"], inplace=True)

    # Adição da coluna com primeiro caracter do cep para identificar a região
    dataset['Regiao'] = dataset['POSTCODE'].str[0]
    regiao = {
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
    dataset['Regiao'] = dataset['Regiao'].map(regiao)

    # Por estado
    dataset['cep'] = dataset['POSTCODE'].str.replace(r'\D', '', regex=True).astype('int32')

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

    # Codificar os dados que são str
    lb = LabelEncoder()
    dataset['Regiao'] = lb.fit_transform(dataset['Regiao'])
    dataset['uf'] = lb.fit_transform(dataset['uf'])
    
    # Quais são as 5 regiões com maior variação (desvio padrão) por renda?
    desvio_renda = dataset.groupby('Regiao')['renda_per_capita'].std().sort_values(ascending=False)
    print("Regiões com maior variação de renda:")
    print(desvio_renda.head(5))

    # Comparando as médias
    concentracao = dataset.groupby('uf')['renda_per_capita'].mean()
    print(concentracao)
    
    print(dataset.info())

    return dataset

dados = tratamentoArquivo(dados)



# Analise de dados

def visualizarDados(dataset):

    # --- Gráfico 1: Qual a média de renda per capita por região? ---
    media_renda_regiao = dataset.groupby('Regiao')['renda_per_capita'].mean()

    plt.figure(figsize=(10, 6))
    media_renda_regiao.plot(kind='bar')
    plt.title('Renda média por região')
    plt.ylabel('Renda Per Capita (R$)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # --- Gráfico 2: Como se distribui a renda média entre as regiões? ---
    media_renda_regiao.plot(
        kind='pie',
        autopct='%1.1f%%',
        startangle=90,
        figsize=(10, 6),
        ylabel='',
        title='Distribuição da Média por Região'
    )
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

    # --- Gráfico 3: Qual a média de renda per capita por estado? ---
    media_renda_estado = dataset.groupby('uf')['renda_per_capita'].mean()

    plt.figure(figsize=(10, 6))
    media_renda_estado.plot(kind='bar')
    plt.title('Renda média por estado')
    plt.ylabel('Renda Per Capita (R$)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # --- Gráfico 4: Quais são as regiões com maior variação (desvio padrão) de renda? ---
    desvio_renda = dataset.groupby('Regiao')['renda_per_capita'].std().sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    desvio_renda.plot(kind='bar')
    plt.title('Regiões com maior variação de renda')
    plt.ylabel('Desvio Padrão (R$)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # --- Gráfico 5: Como evolui o desvio padrão de renda entre as regiões (ordem decrescente)? ---
    plt.figure(figsize=(10, 5))
    plt.plot(desvio_renda.index, desvio_renda.values, marker='o', linestyle='-', color='teal', linewidth=2)
    plt.title('Desvio Padrão da Renda por Região (Decrescente)', fontsize=14)
    plt.xlabel('Região', fontsize=12)
    plt.ylabel('Desvio Padrão (R$)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # --- Gráfico 6: Como se distribui a renda per capita em cada estado (UF)? ---
    dataset.boxplot(column='renda_per_capita', by='uf', figsize=(10, 6))
    plt.title('Distribuição de Renda por UF')
    plt.suptitle('')
    plt.ylabel('Renda Per Capita (R$)')
    plt.tight_layout()
    plt.show()

    # --- Gráfico 7: Como se distribui a renda por estado ignorando os valores extremos? ---
    dataset.boxplot(column='renda_per_capita', by='uf', showfliers=False, figsize=(10, 6), grid=False)
    plt.title('Distribuição de Renda por UF (Sem Outliers)')
    plt.suptitle('')
    plt.ylabel('Renda Per Capita (R$)')
    plt.tight_layout()
    plt.show()

visualizarDados(dados)
