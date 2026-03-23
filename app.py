import streamlit as st
import pandas as pd

st.set_page_config(page_title="Resumo de Expedição", layout="centered")

st.title("📦 Resumo de Expedição por Item")

st.write("Faça upload do relatório (.xlsx)")

uploaded_file = st.file_uploader("Selecione o arquivo", type=["xlsx"])

if uploaded_file:
    try:
        # Ler arquivo
        df = pd.read_excel(uploaded_file, skiprows=6)

        # Limpar dados
        df = df.dropna(subset=["Nome (agrupado)"])

        # Agrupar
        resumo = (
            df.groupby("Nome (agrupado)")["Quantidade"]
            .sum()
            .reset_index()
        )

        # Ajustar sinal (opcional)
        resumo["Quantidade"] = resumo["Quantidade"].abs()

        st.success("Resumo gerado com sucesso!")

        # Mostrar tabela
        st.dataframe(resumo)

        # Botão de download
        from io import BytesIO

        output = BytesIO()
        resumo.to_excel(output, index=False, engine="openpyxl")
        excel_data = output.getvalue()

        st.download_button(
            label="📥 Baixar resumo em Excel",
            data=excel_data,
            file_name="resumo_expedicao.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
