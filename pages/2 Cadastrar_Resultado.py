import streamlit as st
import pandas as pd
import os
import openpyxl
import time
from funcoes import *

########## CONFIGURAÇÕES
st.set_page_config(
    page_title="Dashboard",
    page_icon=":bar_chart:",
    layout="wide")
titulo()
# CSS para personalizar o botão
estilos2()

############################# Barra Lateral #######################################

with st.sidebar:
    cria_sidebar()

spinner()


saldo = 0
Meta = 10000000
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

    tabela1 = resultado.set_index("Data")
    tabela2 = tabela1.sort_values(by=['Data', 'Ativo'], ascending=False)
    diario = resultado.groupby('Data')['Resultado do Dia'].sum().reset_index()

    diario["Saldo Acumulado"] = diario["Resultado do Dia"].cumsum()
    diario = diario.sort_values('Data', ascending=False)
    diario1 = diario[['Data', 'Resultado do Dia']].head(1)
    diario2 = diario1.set_index('Data')

if saldo >= Meta:
    st.balloons()
    st.success("# META BATIDA PARABÉNS !!")
    st.markdown('#  :arrow_down: :green[Download dos Resultados]')
    col1, col2 = st.columns(2)
    with col1:

        if st.button('  Gerar Relatório de Operações', type='primary'):
            dataframes = [diario, tabela2]  # Lista de DataFrames
            xlsx_buffer = create_xlsx_file(dataframes)

            st.download_button(
                label=" Baixar Relatório",
                data=xlsx_buffer,
                file_name='Resultado.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        btn_resetr = st.button("Apagar Resultados", type="primary")

        if btn_resetr:
            os.remove('resultados.csv')
            st.experimental_rerun()

    with col2:
        st.info('# :loudspeaker: ATENÇÃO!!! ')
        st.success('''## Antes de Apagar os Resultados, Gere os Relatórios e Faça Download dos dados''')

st.markdown("# :date: :violet[Cadastrar Resultados Diários]")

if os.path.exists('parametros.csv'):
    tabelaconfig = pd.read_csv('parametros.csv', sep=",")

    if os.path.exists('resultados.csv'):
        resultado = pd.read_csv("resultados.csv", sep=',')

        with st.form('resultado', clear_on_submit=True):
            ativo = st.selectbox(label="Selecione o Ativo:", options=["WIN", "WDO"])
            data = st.date_input("Escolha a Data:")
            resultadodia = st.number_input('Resultado do Dia:')
            btn_enviar = st.form_submit_button("Cadastrar Resultado", type="primary")

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
                time.sleep(1)
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
    st.error("## Parâmentros não Configurados")

