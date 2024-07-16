import streamlit as st
import pandas as pd
import os
import time
from funcoes import *


########## CONFIGURAÇÕES
st.set_page_config(
    page_title="Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="auto"
)
titulo()
estilos()

########################################### Barra Lateral #######################################

with st.sidebar:
    cria_sidebar()


spinner()


######### Calculos#################################################################
op = "Operador"
bancainicial = 0
metamensal = 0
numerodepregoesmensal = 0
diasop = 0
nump = 0
Meta = 0
capital = 0
dnop = 0
Status = 'A Iniciar'
dts = 'Boa Sorte'
numdepregoes = 0
saldoatualdabanca = 0
saldo = 0

st.markdown("## 💲 :violet[ SALDO LÍQUIDO A RECEBER]")
st.markdown("---")

if os.path.exists('parametros.csv'):
    tabelaconfig = pd.read_csv('parametros.csv', sep=",")
    parametros = pd.DataFrame(tabelaconfig)
    a = parametros.iloc[0]
    capital = float(a.iloc[1])
    Meta = float(a.iloc[2])
    nump = int(a.iloc[3])
    dnop = int(a.iloc[4])

if os.path.exists('resultados.csv'):
    resultado = pd.read_csv("resultados.csv", sep=',')
    resultado["Saldo Acumulado"] = resultado["Resultado do Dia"].cumsum()

    resultado = pd.DataFrame(resultado)
    unicos = resultado["Data"].unique()
    unicos = pd.DataFrame(unicos)
    numdepregoes = unicos[[0]].value_counts().sum()

    totalacumulado = resultado[["Resultado do Dia"]].sum()
    saldo = totalacumulado.iloc[0]

    mediaporpregao = saldo / numdepregoes
    if nump:
        pregoesrestantes = numdepregoes - nump
    else:
        pregoesrestantes = 0

    faltaparameta = Meta - saldo

    saldoatualdabanca = capital + saldo

    percparameta = (faltaparameta / Meta) * 100

    percalcancado = 100 - percparameta

    percalcancado2 = (mediaporpregao / Meta) * 100

    perf = (saldo * 100) / capital

    metapp = faltaparameta / (nump - numdepregoes - dnop)

    if saldo >= Meta:
        Status = "Meta Feita"
        dts = "Parabéns!"
    else:
        Status = "Operante"
        dts = "Não desista!"



else:
    st.write("")
############################## Parametros #####################################

if os.path.exists('parametros.csv'):

    col1, col2, col3 = st.columns(3)

    imposto = saldo * 20 / 100
    mesa = (saldo - imposto) * 10 / 100
    receber = saldo - imposto - mesa

    with col1:
        st.markdown("## 🏷️ :blue[ Saldo do Mês⤵️]")
        st.success(f'# R$ {saldo:.2f}')

    with col2:
        st.markdown('## 🏷️ :blue[Imposto  [20%]⤵️]️')
        st.error(f'# R$ {imposto:.2f}')

    with col3:
        st.markdown('## 🏷️ :blue[Mesa [10%]⤵️]️')
        st.error(f'# R$ {mesa:.2f}')

    st.info(f"## 💰 :blue[Valor Para Solicitar Saque⤵️]")
    st.success(f" # 📌 R$ {receber:.2f}")

else:
    st.error("## Parâmetros Não Configurados!")