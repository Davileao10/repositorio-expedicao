import streamlit as st
import pandas as pd

st.set_page_config(page_title="Resumo de Expedição", layout="centered")

st.title("📦 Resumo de Expedição por Item")

st.write("Faça upload do relatório (.csv)")

uploaded_file = st.file_uploader("Selecione o arquivo", type=["csv"])

if uploaded_file:
    try:
        # Ler CSV (padrão Brasil)
        df = pd.read_csv(uploaded_file, sep=';', encoding='utf-8')

        # Caso o CSV venha com outro separador (fallback)
        if df.shape[1] == 1:
            df = pd.read_csv(uploaded_file, sep=',', encoding='utf-8')

        # Limpar dados
        df = df.dropna(subset=["Nome (agrupado)"])

        # Agrupar
        resumo = (
            df.groupby("Nome (agrupado)")["Quantidade"]
            .sum()
            .reset_index()
        )

        # Ajustar sinal
        resumo["Quantidade"] = resumo["Quantidade"].abs()

        st.success("Resumo gerado com sucesso!")

        # Mostrar tabela
        st.dataframe(resumo)

        # Gerar CSV para download
        csv = resumo.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')

        st.download_button(
            label="📥 Baixar resumo em CSV",
            data=csv,
            file_name="resumo_expedicao.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
