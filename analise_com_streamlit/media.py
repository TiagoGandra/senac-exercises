import streamlit as st
import matplotlib.pyplot as plt
from sidebar import render_sidebar

if "dados_processados" not in st.session_state:
    st.warning("Acesse a página 'Main Page' para carregar os dados primeiro.")
    st.stop()

dataset = render_sidebar(st.session_state.dados_processados)

st.title("Média de Renda Per Capita")

media_renda_regiao = dataset.groupby('regiao')['renda_per_capita'].mean()

# Gráfico 1: Média de renda por região (barra) — nativo Streamlit
st.subheader("Renda média por região")
st.bar_chart(media_renda_regiao)

# Gráfico 2: Distribuição da média por região (pizza) — sem suporte nativo, usa matplotlib
st.subheader("Distribuição da média por região")
fig, ax = plt.subplots(figsize=(7, 7))
media_renda_regiao.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
ax.set_ylabel('')
plt.tight_layout()
st.pyplot(fig)

# Gráfico 3: Média de renda por estado (barra) — nativo Streamlit
media_renda_estado = dataset.groupby('uf')['renda_per_capita'].mean()
st.subheader("Renda média por estado")
st.bar_chart(media_renda_estado)
