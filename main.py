import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

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
    dataset.drop(columns=["CD_GEOCODI"], inplace=True)

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

    mapa_estados_regiao = {
        'AM': 'norte',  'AC': 'norte',  'PA': 'norte', 'RR': 'norte', 'AP': 'norte', 'RO': 'norte',
        'AL': 'nordeste', 'BA': 'nordeste', 'CE': 'nordeste', 'MA': 'nordeste', 'PB': 'nordeste',
        'PE': 'nordeste', 'PI': 'nordeste', 'RN': 'nordeste', 'SE': 'nordeste',
        'DF': 'centro-oeste', 'GO': 'centro-oeste', 'MT': 'centro-oeste', 'MS': 'centro-oeste',
        'ES': 'sudeste', 'MG': 'sudeste', 'RJ': 'sudeste', 'SP': 'sudeste',
        'PR': 'sul', 'RS': 'sul', 'SC': 'sul'
    }

    dataset['regiao'] = dataset['uf'].map(mapa_estados_regiao)
    
    print(dataset['regiao'])

    # Codificar os dados que são str para machine learning
    lb = LabelEncoder()
    dataset['Regiao_cod'] = lb.fit_transform(dataset['regiao'])
    dataset['uf_cod'] = lb.fit_transform(dataset['uf'])    
    
    # Quais são as 5 regiões com maior variação (desvio padrão) por renda?
    desvio_renda = dataset.groupby('regiao')['renda_per_capita'].std().sort_values(ascending=False)
    print("Regiões com maior variação de renda:")
    print(desvio_renda.head(5))

    # Comparando as médias
    concentracao = dataset.groupby('uf')['renda_per_capita'].mean()
    print(concentracao)
    
    print(dataset.info())

    return dataset

dados = tratamentoArquivo(dados)

# Divisão treino/teste para Machine Learning
X = dados[['Regiao_cod', 'uf_cod', 'cep']]  # entradas (treino)
y = dados['renda_per_capita']               # saída (teste)

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42
)

print(f"Treino: {len(X_treino)} registros")
print(f"Teste:  {len(X_teste)} registros")


# Analise de dados

def visualizarDados(dataset):

    # --- Gráfico 1: Qual a média de renda per capita por região? ---
    media_renda_regiao = dataset.groupby('regiao')['renda_per_capita'].mean()

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
    desvio_renda = dataset.groupby('uf')['renda_per_capita'].std().sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    desvio_renda.plot(kind='bar')
    plt.title('Estados com maior variação de renda')
    plt.ylabel('Desvio Padrão (R$)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # --- Gráfico 5: Como evolui o desvio padrão de renda entre as regiões (ordem decrescente)? ---
    plt.figure(figsize=(10, 5))
    plt.plot(desvio_renda.index, desvio_renda.values, marker='o', linestyle='-', color='teal', linewidth=2)
    plt.title('Desvio Padrão da Renda por Estado (Decrescente)', fontsize=14)
    plt.xlabel('Região', fontsize=12)
    plt.ylabel('Desvio Padrão (R$)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # --- Gráfico 6: Como se distribui a renda per capita em cada estado (UF)? ---
    dataset.boxplot(column='renda_per_capita', by='regiao', figsize=(10, 6))
    plt.title('Distribuição de Renda por Região')
    plt.suptitle('')
    plt.ylabel('Renda Per Capita (R$)')
    plt.tight_layout()
    plt.show()

    # --- Gráfico 7: Como se distribui a renda por estado ignorando os valores extremos? ---
    dataset.boxplot(column='renda_per_capita', by='regiao', showfliers=False, figsize=(10, 6), grid=False)
    plt.title('Distribuição de Renda por Região (Sem Outliers)')
    plt.suptitle('')
    plt.ylabel('Renda Per Capita (R$)')
    plt.tight_layout()
    plt.show()

    # --- Gráfico 8: Mapa geográfico - Renda Per Capita por Localização ---
    fig, ax = plt.subplots(figsize=(12, 10))
    sc = ax.scatter(
        dataset['LON'], dataset['LAT'],
        c=dataset['renda_per_capita'],
        cmap='RdYlGn',
        s=2,
        alpha=0.6,
        vmin=dataset['renda_per_capita'].quantile(0.05),
        vmax=dataset['renda_per_capita'].quantile(0.95)
    )
    plt.colorbar(sc, ax=ax, label='Renda Per Capita (R$)')
    ax.set_title('Renda Per Capita por Localização Geográfica', fontsize=14)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_aspect('equal')
    plt.tight_layout()
    plt.show()

visualizarDados(dados)
