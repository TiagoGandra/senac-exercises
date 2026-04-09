import streamlit as st
if "dados_processados" not in st.session_state:
    st.warning("Acesse a página 'Main_page' para carregar os dados antes de visualizar os dados processados.")
    st.stop()

# Exibindo os dados usando streamlit ao inves de matplotlib(podemos usar o matplotlib dentro do streamlit)
try:
    st.title("Dados Processados")
    st.subheader("Dados processados")
    st.write(st.session_state.dados_processados)
except Exception as e:
    st.error(f"Error displaying data: {e}")