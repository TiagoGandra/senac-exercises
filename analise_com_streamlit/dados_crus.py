import streamlit as st
if "dados" not in st.session_state:
    st.warning("Acesse a página 'Main_page' para carregar os dados antes de visualizar os dados processados.")
    st.stop()

# Exibindo os dados usando streamlit ao inves de matplotlib(podemos usar o matplotlib dentro do streamlit)
try:
    st.title("Dados")
    st.subheader("Dados originais")
    st.write(st.session_state.dados)
except Exception as e:
    st.error(f"Error displaying data: {e}")