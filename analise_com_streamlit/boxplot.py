import streamlit as st
import matplotlib.pyplot as plt
from sidebar import render_sidebar

if "dados_processados" not in st.session_state:
    st.warning("Acesse a página 'Main Page' para carregar os dados primeiro.")
    st.stop()

dataset = render_sidebar(st.session_state.dados_processados)

st.title("Distribuição de Renda por Região")

# Gráfico 6 e 7: Boxplot — sem suporte nativo no Streamlit, usa matplotlib
fig, (ax6, ax7) = plt.subplots(1, 2, figsize=(14, 6))

dataset.boxplot(column='renda_per_capita', by='regiao', ax=ax6)
ax6.set_title('Com outliers')
ax6.set_ylabel('Renda Per Capita (R$)')
plt.sca(ax6)
plt.xticks(rotation=45)

dataset.boxplot(column='renda_per_capita', by='regiao', showfliers=False, ax=ax7, grid=False)
ax7.set_title('Sem outliers')
ax7.set_ylabel('')
plt.sca(ax7)
plt.xticks(rotation=45)

plt.suptitle('')
plt.tight_layout()
st.pyplot(fig)
