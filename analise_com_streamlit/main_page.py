from dados import load_data, process_data
from sidebar import render_sidebar
import streamlit as st

if "dados" not in st.session_state:
    st.session_state.dados = load_data("cep_coordinates_per_capita_income.csv")

if "dados_processados" not in st.session_state:
    st.session_state.dados_processados = process_data(st.session_state.dados)

render_sidebar(st.session_state.dados_processados)

st.title("Análise de Renda Per Capita no Brasil")
st.markdown("""
Esta aplicação analisa a renda per capita no Brasil utilizando um dataset que contém
informações de CEP, coordenadas geográficas e renda per capita. A análise inclui:
- Média de renda por região e estado
- Variação de renda por estado
- Distribuição de renda por região
- Mapa geográfico da renda per capita
- Boxplot da renda per capita por região (com e sem outliers)
""")