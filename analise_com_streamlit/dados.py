import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder

LIMITES_CEP = [
    -1, 19999999, 28999999, 29999999, 39999999, 48999999, 49999999,
    56999999, 57999999, 58999999, 59999999, 63999999, 64999999,
    65999999, 68899999, 68999999, 69299999, 69399999, 69899999,
    69999999, 72799999, 72999999, 73699999, 76799999, 76999999,
    77999999, 78899999, 79999999, 87999999, 89999999, 99999999
]

ESTADOS = [
    "SP", "RJ", "ES", "MG", "BA", "SE", "PE", "AL", "PB", "RN",
    "CE", "PI", "MA", "PA", "AP", "AM", "RR", "AM", "AC", "DF",
    "GO", "DF", "GO", "RO", "TO", "MT", "MS", "PR", "SC", "RS"
]

MAPA_ESTADOS_REGIAO = {
    'AM': 'norte',  'AC': 'norte',  'PA': 'norte', 'RR': 'norte', 'AP': 'norte', 'RO': 'norte',
    'AL': 'nordeste', 'BA': 'nordeste', 'CE': 'nordeste', 'MA': 'nordeste', 'PB': 'nordeste',
    'PE': 'nordeste', 'PI': 'nordeste', 'RN': 'nordeste', 'SE': 'nordeste',
    'DF': 'centro-oeste', 'GO': 'centro-oeste', 'MT': 'centro-oeste', 'MS': 'centro-oeste',
    'ES': 'sudeste', 'MG': 'sudeste', 'RJ': 'sudeste', 'SP': 'sudeste',
    'PR': 'sul', 'RS': 'sul', 'SC': 'sul'
}


@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    dataset = None
    try:
        dataset = pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Error Loading data: {e}")
    return dataset

def clean_data(dataset: pd.DataFrame) -> pd.DataFrame:
    # dataset = dataset.copy() vou me arriscar a não usar isso e ver se resultará em erro
    dataset.drop_duplicates(inplace=True)
    dataset.dropna(inplace=True)
    dataset = dataset[dataset['POSTCODE'] != 'Sem CEP']
    dataset.drop(columns=["CD_GEOCODI"], inplace=True)
    return dataset


def add_geographic_features(dataset: pd.DataFrame) -> pd.DataFrame:
    dataset['cep'] = dataset['POSTCODE'].str.replace(r'\D', '', regex=True).astype('int32')
    dataset['uf'] = pd.cut(dataset['cep'], bins=LIMITES_CEP, labels=ESTADOS, right=True, ordered=False)
    dataset['regiao'] = dataset['uf'].map(MAPA_ESTADOS_REGIAO)
    return dataset


def encode_categorical_features(dataset: pd.DataFrame) -> pd.DataFrame:
    lb = LabelEncoder()
    dataset['regiao_cod'] = lb.fit_transform(dataset['regiao'])
    dataset['uf_cod'] = lb.fit_transform(dataset['uf'])
    return dataset


def process_data(dataset: pd.DataFrame) -> pd.DataFrame:
    dataset = clean_data(dataset)
    dataset = add_geographic_features(dataset)
    dataset = encode_categorical_features(dataset)
    return dataset