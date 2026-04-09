import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    @st.cache_data
    def load_data(_self):
        """Load data from a CSV file.
        
        Returns:
            pd.DataFrame: The loaded dataset.
        """
        dataset = None
        try:
            dataset = pd.read_csv(_self.file_path)
        except Exception as e:
            print(f"Error loading data: {e}")
        return dataset

    def process_data(dataset):
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