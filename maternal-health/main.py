import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder # talvez nem precise

# Engenharia

# Carregando os dados
def carregandoArquivo(arquivo):
    print("Carregando o dataset")
    dataset = None
    try:
        dataset = pd.read_csv(arquivo)
    except:
        print("Deu não")
    return dataset

dados = carregandoArquivo("dataset.csv")
print(dados)

# Tratando os dados
def tratamentoDados(dataset):

    # Verificando a saúde dos dados
    print(dataset.info())
    print(dataset.describe())
    print(dataset.head())
    print(dataset.tail())
    print(dataset.nunique()) # Identificar as colunas categoricas
    print(dataset.shape)
    print(dataset.values)

    # Traduzindo as colunas
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

    # Juntando a coluna sistólica e disatólica dividida por 10 para termos a
    # pressão com visualização padrão, exemplo, 12/8 -> 12 por 8

    dataset['PressaoSistolica'] = dataset['PressaoSistolica'] / 10
    dataset['PressaoDiastolica'] = dataset['PressaoDiastolica'] / 10
    dataset['Pressao'] = dataset['PressaoSistolica'].astype(str) + '/' + dataset['PressaoDiastolica'].astype(str)
    #dataset.drop(columns=['PressaoSistolica', 'PressaoDiastolica'], inplace=True) -> Melhor não dropar essas colunas
    # Elas podem ser uteis para analise, a coluna pressão só serve para label

    # Modificando a coluna 'Body Temp' de F para C com 2 casas decimais
    dataset['TemperaturaCorporal'] = (dataset['TemperaturaCorporal'] - 32) * 5 / 9
    dataset['TemperaturaCorporal'] = dataset['TemperaturaCorporal'].round(2)

    # Codificando a coluna categorica 'risk level'
    lb = LabelEncoder()
    dataset['Risco'] = lb.fit_transform(dataset['Risco'])
    print(dataset)

tratamentoDados(dados)

# Analise de dados
def analisandoDados(dataset):
    # Qual a relação da idade com o risco durante a gravidez?
    print("Analisando os dados tratados")
    """
    teste = dataset.groupby('Age')['Risk Level']
    plt.figure(figsize=(10,6))
    teste.plot(kind='bar')
    plt.tight_layout
    plt.title('Relação de idade com risco durante gravidez')
    plt.show()
    """
analisandoDados(dados)