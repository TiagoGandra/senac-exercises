import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder # talvez nem precise

# Engenharia

# Carregando os dados
def carregarArquivo(arquivo):
    print("Carregando o dataset")
    dataset = None
    try:
        dataset = pd.read_csv(arquivo)
    except:
        print("Deu não")
    return dataset

dados = carregarArquivo("dataset.csv")
#print(dados)

def limparDados(dataset):
    dataset.dropna(inplace=True)

def contarDadosNulos(dataset):
    #df is your dataframe
    dataset_filtrado = dataset[dataset.Risco_cod == 2]
    rows_count = dataset_filtrado.shape
    print(rows_count)

def verificarDados(dataset):
    print(dataset.info())
    print(dataset.describe())
    print(dataset.head())
    print(dataset.tail())
    print(dataset.nunique()) # Identificar as colunas categoricas
    print(dataset.shape)
    print(dataset.values)   

def tratarDados(dataset):
    traducao = {
    'Age': 'Idade',
    'Systolic BP': 'PressaoSistolica',
    'Diastolic': 'PressaoDiastolica',
    'BS': 'Glicemia',
    'Body Temp': 'TemperaturaCorporal',
    'BMI': 'IMC',
    'Previous Complications': 'JaTeveComplicacoes',
    'Preexisting Diabetes': 'PredisposicaoADiabetes',
    'Gestacional Diabetes': 'TeveDiabetesGestacional',
    'Mental Health': 'SaudeMental',
    'Heart Rate': 'FrequenciaCardiaca',
    'Risk Level': 'Risco'
    }
    dataset = dataset.rename(columns=traducao)

    # Criar coluna pressão para label
    dataset['PressaoSistolica'] = dataset['PressaoSistolica'] / 10
    dataset['PressaoDiastolica'] = dataset['PressaoDiastolica'] / 10
    dataset['Pressao'] = dataset['PressaoSistolica'].astype(str) + '/' + dataset['PressaoDiastolica'].astype(str)

    # Modificar a coluna temperatura de Fahreinheit para celsius
    dataset['TemperaturaCorporal'] = (dataset['TemperaturaCorporal'] - 32) * 5 / 9
    dataset['TemperaturaCorporal'] = dataset['TemperaturaCorporal'].round(2)

    #limparDados(dataset) -> remover as colunas nulas
    codificarDados(dataset)
    verificarDados(dataset)

    return dataset

def codificarDados(dataset):
    lb = LabelEncoder()
    dataset['Risco_cod'] = lb.fit_transform(dataset['Risco'])

# Analise de dados
def analisarDados(dataset):
    # Qual a relação da idade com o risco durante a gravidez?
    print("Analisando os dados tratados")
    #df is your dataframe
    dataset_filtrado = dataset[dataset.Risco_cod == 2]
    contarDadosNulos(dataset_filtrado)
    print(dataset_filtrado.info())
    print(dataset_filtrado)
    
    """
    teste = dataset.groupby('Age')['Risk Level']
    plt.figure(figsize=(10,6))
    teste.plot(kind='bar')
    plt.tight_layout
    plt.title('Relação de idade com risco durante gravidez')
    plt.show()
    """
dados = tratarDados(dados)
analisarDados(dados)
