import streamlit as st
import pandas as pd
import requests
import datetime


# Lista de icones
# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
# streamlit run main.py no terminal

# Vai ficar em cache por 1 dia
@st.cache_data(ttl="1day")
def get_selic():
    # Funcao para pegar taxa selic da api do banco central
    url = "https://bcb.gov.br/api/servico/sitebcb/historicotaxasjuros"
    resp = requests.get(url)
    conteudo = resp.json()["conteudo"]
    df = pd.DataFrame(conteudo)

    df["DataInicioVigencia"] = pd.to_datetime(df["DataInicioVigencia"]).dt.date
    df["DataFimVigencia"] = pd.to_datetime(df["DataFimVigencia"]).dt.date
    df["DataFimVigencia"] = df["DataFimVigencia"].fillna(
        datetime.datetime.today().date())

    return df


# Funcao para calular estatisticas
def calc_general_estats(df):
    df_data = df.groupby(by="Data")[["Valor"]].sum()
    df_data["lag_1"] = df_data["Valor"].shift(1)
    df_data["Diferença Mensal Abs"] = df_data["Valor"] - df_data["lag_1"]
    # Media movel dos ultimos 6 meses
    df_data["Média 6M - Diferença Mensal"] = df_data["Diferença Mensal Abs"].rolling(6).mean()  # noqa
    df_data["Média 12M - Diferença Mensal"] = df_data["Diferença Mensal Abs"].rolling(12).mean()  # noqa
    df_data["Média 24M - Diferença Mensal"] = df_data["Diferença Mensal Abs"].rolling(24).mean()  # noqa
    # Diferença relativa
    df_data["Diferença Mensal Rel"] = (df_data["Valor"]/df_data["lag_1"]-1)

    df_data.drop("lag_1", axis=1, inplace=True)

    return df_data


st.set_page_config(page_title="Projeto Téo Me Why",
                   page_icon=":woman_technologist:")

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

    # Estatisticas Gerais
    df_stats = calc_general_estats(df)

    # Configuracao de exibicao dos valores
    columns_config = {
        "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
        "Diferença Mensal Abs": st.column_config.NumberColumn(
            "Diferença Mensal Abs", format="R$ %.2f"
        ),
        "Média 6M - Diferença Mensal": st.column_config.NumberColumn(
            "Média 6M - Diferença Mensal", format="R$ %.2f"
        ),
        "Média 12M - Diferença Mensal": st.column_config.NumberColumn(
            "Média 12M - Diferença Mensal", format="R$ %.2f"
        ),
        "Média 24M - Diferença Mensal": st.column_config.NumberColumn(
            "Média 24M - Diferença Mensal", format="R$ %.2f"
        ),
        "Diferença Mensal Rel": st.column_config.NumberColumn(
            "Diferença Mensal Rel", format="percent"
        ),
    }

    exp3 = st.expander("Estatísticas Gerais")
    exp3.dataframe(df_stats, hide_index=False, column_config=columns_config)

    abs_cols = ["Diferença Mensal Abs", "Média 6M - Diferença Mensal",
                "Média 12M - Diferença Mensal", "Média 24M - Diferença Mensal"]
    exp3.line_chart(df_stats[abs_cols])

    with st.expander("Metas"):
        # Dividindo a visualizacao em duas abas
        col1, col2 = st.columns(2)
        data_inicio_meta = col1.date_input("Início de Meta",
                                           max_value=df_stats.index.max())

        # Indices que antecendem a data recebida
        filter_data = df_stats.index <= data_inicio_meta
        data_filtrada = df_stats.index[filter_data][-1]

        custos_fixos = col1.number_input("Custos Fixos", min_value=0.,
                                         format="%.2f")
        salario_bruto = col2.number_input("Salário Bruto", min_value=0.,
                                          format="%.2f")
        salario_liquido = col2.number_input("Salário Líquido", min_value=0.,
                                            format="%.2f")

        valor_inicio = df_stats.loc[data_filtrada]["Valor"]
        col1.markdown(f"**Valor no Início da Meta**: R$ {valor_inicio:.2f}")

        # Atualizando valores pela taxa selic
        selic_gov = get_selic()
        filter_selic_date = (selic_gov["DataInicioVigencia"] < data_inicio_meta) & (selic_gov["DataFimVigencia"] > data_inicio_meta)  # noqa
        selic_default = selic_gov[filter_selic_date]["MetaSelic"].iloc[0]
        selic = st.number_input(
            "Taxa Selic", min_value=0., value=selic_default, format="%.2f"
        )
        selic_ano = selic/100
        selic_mes = (1 + selic_ano)**(1/12) - 1

        rendimento_ano = valor_inicio * selic_ano
        rendimento_mes = valor_inicio * selic_mes

        col1_pot, col2_pot = st.columns(2)
        mensal = salario_liquido - custos_fixos + valor_inicio*selic_mes
        anual = (salario_liquido - custos_fixos)*12 + (valor_inicio*selic_ano)

        # Container com border criar tipo um card com informacao
        with col1_pot.container(border=True):
            st.markdown(f"**Potencial Arrecadação Mês**: \n\nR$ {mensal:.2f}",
                        help=f"{salario_liquido:.2f} - {custos_fixos:.2f} + {rendimento_mes:.2f}")  # noqa

        with col2_pot.container(border=True):
            st.markdown(f"**Potencial Arrecadação Anual**: \n\n R$ {anual:.2f}",  # noqa
                        help=f"12 * ({salario_liquido:.2f} - {custos_fixos:.2f}) + {rendimento_ano:.2f}")  # noqa

        with st.container(border=True):
            col1_meta, col2_meta = st.columns(2)
            with col1_meta:
                meta_estipulada = st.number_input("Meta estipulada",
                                                  min_value=0., format="%.2f",
                                                  value=anual)

            with col2_meta:
                patrimonio = meta_estipulada + valor_inicio
                st.markdown(f"**Patrimônio Estimado pós meta:** \n\n R$ {patrimonio:.2f}")  # noqa
