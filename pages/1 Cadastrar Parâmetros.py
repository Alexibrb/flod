import streamlit as st
import pandas as pd
import os
import time
from funcoes import *


########## CONFIGURAÇÕES
st.set_page_config(
    page_title="Dashboard",
    page_icon=":bar_chart:",
    layout="wide")
titulo()
# CSS para personalizar o botão
estilos()

########################################### Barra Lateral #######################################

with st.sidebar:
    cria_sidebar()

spinner()



st.markdown("# :hammer_and_wrench: :violet[Cadastrar Parâmetros do Operacional]")

if os.path.exists('parametros.csv'):
    tabelaconfig = pd.read_csv('parametros.csv', sep=",")

    parametros = pd.DataFrame(tabelaconfig)
    a = parametros.iloc[0]
    capital = float(a.iloc[1])
    Meta = float(a.iloc[2])
    nump = int(a.iloc[3])
    dnop = int(a.iloc[4])
    st.success("## Parâmetros já configurados")
    if os.path.exists('parametros.csv'):
        btn_resetp1 = st.button("Alterar Parâmetros", type="primary")
        if btn_resetp1:
            os.remove('parametros.csv')
            



else:

    with st.form("configp", clear_on_submit=True):
        operador = st.text_input("Digite seu nome")
        capitalinicial = st.number_input("Digite o Capital")
        meta = st.number_input("Digite a meta mensal")
        nopm = st.number_input("Digite o número de operações no mês", 1)
        dnop = st.number_input("Digite os dias não operados", 1)
        btn_cadastro = st.form_submit_button("Cadastrar")

    if btn_cadastro:
        op = operador
        capitali = capitalinicial
        metam = meta
        nopmi = nopm
        dnopi = dnop
        d = {"operador": op, "Capital": capitali, "Meta": metam, "Número de operações": nopmi, "Dias não operados": dnop}
        df = pd.DataFrame(data=d, index=[0])
        tabela1 = df.to_csv("parametros.csv", index=False)

        st.success("# Dados cadastros com sucesso!")
        

    else:
        st.error("# Insira os dados")


