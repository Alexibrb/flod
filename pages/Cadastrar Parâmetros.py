import streamlit as st
import pandas as pd
import os

########## CONFIGURAÇÕES
st.set_page_config(
    page_title="Dashboard",
    page_icon=":bar_chart:",
    layout="wide")
# CSS para personalizar o botão
st.markdown("""
    <style>
    .stDownloadButton > button {
        background-color: #4CAF50; color: white; padding: 10px 24px;  text-align: center;text-decoration: none;
        display: inline-block;font-size: 16px;margin: 4px 2px;cursor: pointer;border: none;border-radius: 8px;width: 215px;
    }
    .stDownloadButton > button:hover {
        background-color: #cccccc;
        color: black;
    }


    </style>
    """, unsafe_allow_html=True)

if os.path.exists('parametros.csv'):
    tabelaconfig = pd.read_csv('parametros.csv', sep=",")
    st.write("# :hammer_and_wrench: Cadastrar Parâmetros do Operacional")
    parametros = pd.DataFrame(tabelaconfig)
    a = parametros.iloc[0]
    capital = float(a.iloc[0])
    Meta = float(a.iloc[1])
    nump = int(a.iloc[2])
    dnop = int(a.iloc[3])
    st.success("## Parâmetros já configurados")
    if os.path.exists('parametros.csv'):
        btn_resetp1 = st.button("Alterar Parâmetros", type="primary")
        if btn_resetp1:
            os.remove('parametros.csv')
            st.experimental_rerun()



else:
    st.error("# :hammer_and_wrench: Cadastrar Parâmetros do Operacional")
    with st.form("configp", clear_on_submit=True):

        capitalinicial = st.number_input("Digite o Capital")
        meta = st.number_input("Digite a meta mensal")
        nopm = st.number_input("Digite o número de operações no mês", 1)
        dnop = st.number_input("Digite os dias não operados", )
        btn_cadastro = st.form_submit_button("Cadastrar")

    if btn_cadastro:

        capitali = capitalinicial
        metam = meta
        nopmi = nopm
        dnopi = dnop
        d = {"Capital": capitali, "Meta": metam, "Número de operações": nopmi, "Dias não operados": dnop}
        df = pd.DataFrame(data=d, index=[0])
        tabela1 = df.to_csv("parametros.csv", index=False)

        st.success("# Dados cadastros com sucesso!")
        st.experimental_rerun()

    else:
        st.error("# Insira os dados")