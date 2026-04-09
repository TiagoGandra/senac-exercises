import streamlit as st
from sidebar import render_sidebar

if "dados_processados" not in st.session_state:
    st.warning("Acesse a página 'Main_page' para carregar os dados antes de visualizar os dados processados.")
    st.stop()
dataset = render_sidebar(st.session_state.dados_processados)
# Exibindo os dados usando streamlit ao inves de matplotlib(podemos usar o matplotlib dentro do streamlit)
try:
    st.title("Dados Processados")
    st.subheader("Dados processados")
    st.write(dataset)
    st.write("Informações básicas do dataset:")
    st.write(dataset.info())
    st.write("Primeiras linhas do dataset:")
    st.write(dataset.head())
    st.write("Estatísticas descritivas do dataset:")
    st.write(dataset.describe())
    st.write("Número de valores únicos por coluna:")
    st.write(dataset.nunique())
    st.write("Dimensão do dataset:")
    st.write(dataset.shape)
except Exception as e:
    st.error(f"Error displaying data: {e}")