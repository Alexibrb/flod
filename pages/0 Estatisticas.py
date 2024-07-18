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

st.markdown("## :hammer_and_wrench: :violet[ PARÂMETROS DO OPERACIONAL]")

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
    col1, col2, col3, col4 = st.columns(4)


    with col1:
        with st.container(height=125):
            st.metric(label=" :hammer_and_wrench: Situação:", value=f"  {Status}", delta=dts)
    with col2:
        with st.container(height=125):
            st.metric(label=" :abacus: Pregões no mês:", value=f"{nump} Pregões",
                      delta=f"Não Operados [ {dnop} ]")
    with col3:
        with st.container(height=125):
            st.metric(label=" :dollar: Capital Inicial:", value=f"R$ {capital:.2f}", delta=f"Acumulado: R$ {saldoatualdabanca:.2f}")
    with col4:
        with st.container(height=125):
            if saldo < Meta:
                feito = f"Feito R$ {saldo:.2f}/R${Meta:.2f}"
            else:
                feito = "Meta Batida"
            st.metric(label=" :dollar: Meta Mensal:", value=f"R$ {Meta:.2f}", delta=feito)



if os.path.exists('parametros.csv'):
    delete_confirmation1 = st.checkbox("Marque Para Alterar os Parâmetros.")
    if delete_confirmation1:
        btn_resetp2 = st.button("Alterar Parâmetros", type="primary")
        if btn_resetp2:
            os.remove('parametros.csv')
            st.experimental_rerun()

else:
    st.error("## Parâmetros Não Configurados!")


############### colunas de informações ###############################
st.markdown("## :rotating_light: :violet[STATUS DO OPERACIONAL]")

if os.path.exists('resultados.csv') and os.path.exists('parametros.csv'):


    col1, col2 = st.columns(2)
    with col1:
        with st.container(height=450):
            with st.container(height=125):
                st.metric(label=" :1234: Nº de Pregões Operados:", value=f"{numdepregoes}/{nump} Pregões",
                          delta=f"Faltam [ {nump  - numdepregoes - dnop} ] Pregões")
            with st.container(height=125):
                st.metric(label=" :heavy_dollar_sign: Saldo Acumulado no Mês:", value=f"R$ {saldo:.2f}",
                          delta=f"{percalcancado:.2f}% da meta")
            with st.container(height=125):
                st.metric(label=" :heavy_dollar_sign: Média Por Pregão:", value=f"R$ {mediaporpregao:.2f}",
                          delta=f"{percalcancado2:.2f}% da meta")

    with col2:
        with st.container(height=450):
            with st.container(height=125):
                if percparameta < 0:
                    deltafpm = 0
                else:
                    deltafpm = percparameta
                if saldo < Meta:
                    falta = f"R$ {faltaparameta:.2f}"
                else:
                    falta = "Meta Batida"
                st.metric(label=" :heavy_dollar_sign: Falta Para a Meta:", value=falta,
                          delta=f"{deltafpm:.2f}% para a meta")
            with st.container(height=125):
                st.metric(label=" :heavy_dollar_sign: Total Acumulado:", value=f"R$ {saldoatualdabanca:.2f}",
                          delta=f"Performance: {perf:.2f}%")
            with st.container(height=125):
                if saldo < Meta:
                    prox = f"R$ {metapp:.2f}"
                    ops = "Opere com sabedoria"
                else:
                    prox = "Meta Batida"
                    ops = "Parabéns"
                    st.balloons()
                st.metric(label=" :heavy_dollar_sign: Meta no próximo pregão:", value=prox, delta=ops)
else:
    st.error("## Nenhuma Operação Encontrada")




