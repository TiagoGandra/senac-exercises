import streamlit as st

main_page = st.Page("main_page.py", title="Main Page")
dados_processados = st.Page("dados_processados.py", title="Dados Processados")
media = st.Page("media.py", title="Média de Renda")
variacao = st.Page("variacao.py", title="Variação de Renda")
boxplot = st.Page("boxplot.py", title="Boxplot")
mapa = st.Page("mapa.py", title="Mapa Geográfico")

pg = st.navigation([main_page, dados_processados, media, variacao, boxplot, mapa])

pg.run()
