import streamlit as st
import pandas as pd

# Lista de icones
# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
# streamlit run main.py no terminal

st.set_page_config(page_title="Projeto Téo Me Why",
                   page_icon=":woman_technologist:")

st.text("Olá, mundo")

st.markdown("""
# Boas vindas!

## App financeiro

Estudando Streamlit com o Téo me Why
""")
# Widget de upload de arquivos csv
file_upload = st.file_uploader(label="Faça upload dos dados aqui.",
                               type=['csv'])

# Verifica se foi feito o upload de algum arquivo
if file_upload:
    # Leitura dos dados
    df = pd.read_csv(file_upload)
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y").dt.date
    st.text("Arquivo lido com sucesso.")

    # Exibição dos dados no app
    exp1 = st.expander("Dados Brutos")
    columns_fmt = {"Valor": st.column_config.NumberColumn("Valor",
                                                          format="R$ %.2f")}
    exp1.dataframe(df, hide_index=False, column_config=columns_fmt)

    # Visao Instituicao
    exp2 = st.expander("Instituições")
    df_instituicao = df.pivot_table(index="Data", columns="Instituição",
                                    values="Valor")

    # Abas para diferentes visualizações
    tab_data, tab_history, tab_share = exp2.tabs(
        ["Dados", "Histórico", "Distribuição"]
    )

    # Exibe dataframe
    with tab_data:
        st.dataframe(df_instituicao)

    # Exibe grafico temporal com o historico
    with tab_history:
        st.line_chart(df_instituicao)

    # Exibe distribuicao com filtro de data
    with tab_share:
        # Forma 1
        date = st.selectbox("Filtro Data", options=df_instituicao.index)
        # # Forma 2:  Criando filtro de data
        # date = st.date_input("Data para Distribuição",
        #                      min_value=df_instituicao.index.min(),
        #                      max_value=df_instituicao.index.max())
        # if date not in df_instituicao.index:
        #     st.warning("Entre com uma data válida.")
        # else:
        # Obtem os dados da data escolhida
        # Grafico de Barras
        st.bar_chart(df_instituicao.loc[date])
