import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Listas para mapear uf por cep e região por uf
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
mapa_estados_regiao = {
    'AM': 'norte',  'AC': 'norte',  'PA': 'norte', 'RR': 'norte', 'AP': 'norte', 'RO': 'norte',
    'AL': 'nordeste', 'BA': 'nordeste', 'CE': 'nordeste', 'MA': 'nordeste', 'PB': 'nordeste',
    'PE': 'nordeste', 'PI': 'nordeste', 'RN': 'nordeste', 'SE': 'nordeste',
    'DF': 'centro-oeste', 'GO': 'centro-oeste', 'MT': 'centro-oeste', 'MS': 'centro-oeste',
    'ES': 'sudeste', 'MG': 'sudeste', 'RJ': 'sudeste', 'SP': 'sudeste',
    'PR': 'sul', 'RS': 'sul', 'SC': 'sul'
}

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

def verificarDados(dataset):
    print("Verificando os dados")
    print(dataset.info())
    print(dataset.head())
    print(dataset.describe())
    print(dataset.nunique()) # para ver quais colunas são categoricas
    print(dataset.shape)
    print(dataset.values)

verificarDados(dados)

def limparDados(dataset):
    print("Limpando os dados")
    dataset.drop_duplicates(inplace=True)
    dataset.dropna(inplace=True)
    dataset['POSTCODE'] = dataset['POSTCODE'].str.replace(r'\D', '', regex=True)
    dataset = dataset[dataset['POSTCODE'] != '']
    dataset.drop(columns=["CD_GEOCODI"], inplace=True)
    return dataset

def criarColunas(dataset):
    print("Criando colunas CEP, UF e Região")
    dataset['cep'] = dataset['POSTCODE'].astype('int32')
    dataset['uf'] = pd.cut(dataset['cep'], bins=limites, labels=estados, ordered=False)
    dataset['regiao'] = dataset['uf'].map(mapa_estados_regiao)
    return dataset

def codificarColunas(dataset):
    print("Codificando as colunas")
    lb = LabelEncoder()
    dataset['Regiao_cod'] = lb.fit_transform(dataset['regiao'])
    dataset['uf_cod'] = lb.fit_transform(dataset['uf'])    
    return dataset

# tratar o arquivo
def tratarArquivo(dataset):
    print("Tratar os dados")
    dataset = limparDados(dataset)
    dataset = criarColunas(dataset)
    dataset = codificarColunas(dataset)

    return dataset

dados = tratarArquivo(dados)

# Analise de dados


def visualizarDados(dataset):

    # --- Slide 0: Apresentação ---
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.axis('off')

    titulo = "Análise de Renda Per Capita por CEP no Brasil"
    descricao = (
        "O Brasil é um dos países com maior desigualdade de renda do mundo.\n"
        "Este estudo utiliza dados de renda per capita associados a CEPs brasileiros\n"
        "para explorar padrões regionais, identificar disparidades entre estados e regiões\n"
        "e construir uma base para modelos preditivos de renda a partir de localização geográfica."
    )
    perguntas = [
        "1. Qual a média e variabilidade da renda per capita por região?",
        "2. Como se distribui proporcionalmente a renda média entre as regiões?",
        "3. Quais estados apresentam maior desigualdade interna de renda?",
        "4. Como se distribui a renda típica por região, sem considerar outliers?",
        "5. A renda per capita apresenta padrão espacial visível no território brasileiro?",
    ]

    ax.text(0.5, 0.93, titulo, transform=ax.transAxes,
            fontsize=18, fontweight='bold', ha='center', va='top', color='#1a1a2e')

    ax.text(0.5, 0.78, descricao, transform=ax.transAxes,
            fontsize=11, ha='center', va='top', color='#333333',
            style='italic', wrap=True)

    ax.text(0.08, 0.58, "Perguntas norteadoras:", transform=ax.transAxes,
            fontsize=12, fontweight='bold', color='#1a1a2e')

    for i, pergunta in enumerate(perguntas):
        ax.text(0.08, 0.50 - i * 0.09, pergunta, transform=ax.transAxes,
                fontsize=11, color='#333333')

    fig.patch.set_facecolor('#f0f4f8')
    plt.tight_layout()
    plt.show()

    # --- Gráfico 1: Qual a média de renda per capita por região? ---
    media_renda_regiao = dataset.groupby('regiao')['renda_per_capita'].mean()
    media_renda_regiao1 = dataset.groupby('regiao')['renda_per_capita'].agg(['mean', 'std'])

    media_renda_regiao1.plot(kind='bar')
    plt.title('Renda média e desvio padrao')
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
        title='Media da Renda Per Capita por região'
    )
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

   
    
    desvio_renda = dataset.groupby('uf')['renda_per_capita'].std().sort_values(ascending=False)
   
    # --- Gráfico 3: Como evolui o desvio padrão de renda entre as regiões (ordem decrescente)? ---
    plt.figure(figsize=(10, 5))
    plt.plot(desvio_renda.index, desvio_renda.values, marker='o', linestyle='-', color='teal', linewidth=2)
    plt.title('Desvio Padrão da Renda por Estado (Decrescente)', fontsize=14)
    plt.xlabel('Região', fontsize=12)
    plt.ylabel('Desvio Padrão (R$)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


    # --- Gráfico 4: Como se distribui a renda por estado ignorando os valores extremos? ---
    dataset.boxplot(column='renda_per_capita', by='regiao', showfliers=False, figsize=(10, 6), grid=False)
    plt.title('Distribuição de Renda por Região (Sem Outliers)')
    plt.suptitle('')
    plt.ylabel('Renda Per Capita (R$)')
    plt.tight_layout()
    plt.show()

    # --- Gráfico 5: Mapa geográfico - Renda Per Capita por Localização ---
    fig, ax = plt.subplots(figsize=(10, 7))
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

def dividirTreinoTeste(dataset):
    print("Dividindo os dados em treino e teste")

    # Divisão treino/teste para Machine Learning
    X = dataset[['Regiao_cod', 'uf_cod', 'cep']]  # entradas (treino)
    y = dataset['renda_per_capita']               # saída (teste)

    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X, y,
        test_size=0.3,
        random_state=42
    )

    print(f"Treino: {len(X_treino)} registros")
    print(f"Teste:  {len(X_teste)} registros")

dividirTreinoTeste(dados)