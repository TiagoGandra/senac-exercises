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
    'DF': 'centro-oeste', 'GO': 'centro-oeste', 'MT': 'centro-oeste', 'MS': 'centro-oeste', 'TO': 'norte',
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
    verificarDados(dataset)

    return dataset

dados = tratarArquivo(dados)

# Analise de dados

def visualizarDados(dataset):

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
        "1. Como cada região se posiciona em relação à média nacional de renda?",
        "2. Existe equilíbrio de renda entre os estados de uma mesma região?",
        "3. Quais regiões têm renda acima ou abaixo da média nacional e em quanto?",
        "4. Quais estados concentram maior desigualdade interna de renda?",
        "5. Como se distribui a renda típica por região, sem considerar outliers?",
        "6. A renda per capita apresenta padrão espacial visível no território brasileiro?",
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

    media_nacional = dataset['renda_per_capita'].mean()
    media_regiao = dataset.groupby('regiao')['renda_per_capita'].mean().sort_values(ascending=False)
    desvio_regiao = dataset.groupby('regiao')['renda_per_capita'].std().sort_values(ascending=False)
    desvio_estado = dataset.groupby('uf', observed=True)['renda_per_capita'].std().sort_values(ascending=False)

    # Gráfico 1: Renda média por região vs média nacional
    plt.figure(figsize=(10, 6))
    media_regiao.plot(kind='bar', color='steelblue', edgecolor='black')
    plt.axhline(media_nacional, color='red', linestyle='--', label=f'Média Nacional: R$ {media_nacional:.2f}')
    plt.title('Renda Média por Região vs Média Nacional')
    plt.ylabel('Renda Per Capita (R$)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Gráfico 2: Drill-down — renda média por estado dentro de cada região
    regioes = dataset['regiao'].dropna().unique()
    fig, axes = plt.subplots(3, 2, figsize=(14, 12))
    axes = axes.flatten()

    for i, reg in enumerate(regioes):
        if i < 6:
            df_reg = dataset[dataset['regiao'] == reg]
            m_reg = df_reg['renda_per_capita'].mean()
            df_reg.groupby('uf', observed=True)['renda_per_capita'].mean().sort_values().plot(
                kind='barh', ax=axes[i], color='teal')
            axes[i].axvline(m_reg, color='orange', linestyle='--', alpha=0.8, label=f'Média: R${m_reg:.0f}')
            axes[i].set_title(reg.upper())
            axes[i].set_xlabel('Renda Per Capita (R$)')
            axes[i].legend(fontsize=8)

    plt.suptitle('Renda Média por Estado dentro de cada Região', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

    # --- Gráfico 3: Desvio % em relação à média nacional por região ---
    desvio_pct = ((media_regiao - media_nacional) / media_nacional * 100).sort_values()
    cores = ['seagreen' if v >= 0 else 'tomato' for v in desvio_pct]
    plt.figure(figsize=(10, 5))
    desvio_pct.plot(kind='barh', color=cores, edgecolor='black')
    plt.axvline(0, color='black', linewidth=1)
    plt.title('Desvio da Renda Regional em Relação à Média Nacional (%)', fontsize=13)
    plt.xlabel('Desvio (%)')
    plt.tight_layout()
    plt.show()

    # --- Gráfico 4: Ranking de desigualdade interna por estado ---
    plt.figure(figsize=(12, 7))
    desvio_estado.plot(kind='barh', color='salmon', edgecolor='black')
    plt.title('Ranking de Desigualdade Interna por Estado (Desvio Padrão da Renda)', fontsize=13)
    plt.xlabel('Desvio Padrão (R$)')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

    # --- Gráfico 5: Distribuição da renda por região sem outliers (boxplot) ---
    dataset.boxplot(column='renda_per_capita', by='regiao', showfliers=False, figsize=(10, 6), grid=False)
    plt.title('Distribuição de Renda por Região (Sem Outliers)')
    plt.suptitle('')
    plt.ylabel('Renda Per Capita (R$)')
    plt.tight_layout()
    plt.show()

    # --- Gráfico 6: Mapa geográfico — Renda Per Capita por Localização ---
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