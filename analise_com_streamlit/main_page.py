from dados import load_data, process_data
import streamlit as st

if "dados" not in st.session_state:
    st.session_state.dados = load_data("cep_coordinates_per_capita_income.csv")

if "dados_processados" not in st.session_state:
    st.session_state.dados_processados = process_data(st.session_state.dados)
    
# Descrição do que a analise em estudo se baseia
try:
    st.title("Testado página principal")
except Exception as e:
    st.error(f"Error displaying data: {e}")