from dados import DataProcessor
import streamlit as st

dados = DataProcessor("../cep_coordinates_per_capita_income.csv").load_data()
dados_processados = DataProcessor.process_data(dados)

if "dados" not in st.session_state or "dados_processados" not in st.session_state:
    st.session_state["dados"] = dados
    st.session_state["dados_processados"] = dados_processados
    
# Descrição do que a analise em estudo se baseia
try:
    st.title("Testado página principal")
except Exception as e:
    st.error(f"Error displaying data: {e}")