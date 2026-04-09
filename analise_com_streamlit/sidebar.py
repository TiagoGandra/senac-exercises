import streamlit as st


def render_sidebar(dataset):
    regioes = sorted(dataset['regiao'].dropna().unique().tolist())

    with st.sidebar:
        st.header("Filtros")
        regioes_selecionadas = st.multiselect(
            "Região",
            options=regioes
        )

        # Filtra os estados disponíveis com base nas regiões selecionadas
        dataset_regiao = dataset[dataset['regiao'].isin(regioes_selecionadas)] if regioes_selecionadas else dataset
        ufs = sorted(dataset_regiao['uf'].dropna().unique().tolist())
        ufs_selecionadas = st.multiselect(
            "Estado (UF)",
            options=ufs
        )

    resultado = dataset_regiao
    if ufs_selecionadas:
        resultado = resultado[resultado['uf'].isin(ufs_selecionadas)]

    return resultado
