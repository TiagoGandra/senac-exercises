import streamlit as st

# Define the pages
main_page = st.Page("main_page.py", title="Main Page")
dados_crus = st.Page("dados_crus.py", title="Dados")
dados_processados = st.Page("dados_processados.py", title="Dados Processados")

# Set up navigation
pg = st.navigation([main_page, dados_crus, dados_processados])

# Run the selected page
pg.run()