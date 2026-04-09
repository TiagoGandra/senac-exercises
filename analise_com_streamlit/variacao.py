import streamlit as st
from sidebar import render_sidebar

if "dados_processados" not in st.session_state:
    st.warning("Acesse a página 'Main Page' para carregar os dados primeiro.")
    st.stop()

dataset = render_sidebar(st.session_state.dados_processados)

st.title("Variação de Renda Per Capita")

desvio_renda = dataset.groupby('uf')['renda_per_capita'].std().sort_values(ascending=False)

# Gráfico 4: Estados com maior variação (barra) — nativo Streamlit
st.subheader("Estados com maior variação de renda")
st.bar_chart(desvio_renda)

# Gráfico 5: Evolução do desvio padrão (linha) — nativo Streamlit
st.subheader("Evolução do desvio padrão por estado")
st.line_chart(desvio_renda)
