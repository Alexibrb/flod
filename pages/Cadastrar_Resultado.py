import streamlit as st
import pandas as pd
import os
from time import sleep




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



if os.path.exists('resultados.csv'):
    resultado = pd.read_csv("resultados.csv", sep=',')
    st.write("# :date: Cadastrar Resultados Diários")
    with st.form('resultado', clear_on_submit=True):
        ativo = st.selectbox(label="Selecione o Ativo:", options=["WIN", "WDO"])
        data = st.date_input("Escolha a Data:")
        resultadodia = st.number_input('Resultado do Dia:')
        btn_enviar = st.form_submit_button("Enviar", type="primary")

    if btn_enviar:
        caminho_arquivo2 = 'resultados.csv'

        if os.path.exists(caminho_arquivo2):
            resultado = pd.read_csv("resultados.csv", sep=',')
            data2 = pd.DataFrame(resultado)
            dados2 = {'Ativo': ativo, 'Data': data, 'Resultado do Dia': resultadodia}
            df2 = pd.DataFrame(dados2, index=[0])
            data2 = pd.concat([data2, df2], ignore_index=True)
            data2.to_csv('resultados.csv', index=False)
            st.success("# Cadastro Efetuado com sucesso!!!!")
            st.table(resultado.tail(2))
            sleep(2)
            st.experimental_rerun()




else:
    with st.form('resultado', clear_on_submit=True):
        ativo = st.selectbox(label="Selecione o Ativo:", options=["WIN", "WDO"])
        data = st.date_input("Escolha a Data:")
        resultadodia = st.number_input('Resultado do Dia:')
        btn_enviar = st.form_submit_button("Enviar", type="primary")
        if btn_enviar:
            data2 = pd.DataFrame(columns=['Ativo', 'Data', 'Resultado do Dia'])
            dados2 = {'Ativo': ativo, 'Data': data, 'Resultado do Dia': resultadodia}
            df2 = pd.DataFrame(dados2, index=[0])
            data2 = pd.concat([data2, df2], ignore_index=True)
            data2.to_csv('resultados.csv', index=False)
            st.success("# Cadastro Efetuado com sucesso!!!!")
            st.experimental_rerun()
        else:
            st.error("# Insira os dados")
