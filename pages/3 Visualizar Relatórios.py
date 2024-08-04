import streamlit as st
import pandas as pd
import os
import io
import openpyxl
import time
from funcoes import *




########## CONFIGURAÇÕES
st.set_page_config(
    page_title="Dashboard",
    page_icon=":bar_chart:",
    layout="wide")
titulo()
###### CSS
estilos2()

####### Barra Lateral
with st.sidebar:
    cria_sidebar()
# CSS para personalizar o botão
spinner()




if os.path.exists('parametros.csv'):
    tabelaconfig = pd.read_csv('parametros.csv', sep=",")
    parametros = pd.DataFrame(tabelaconfig)
    a = parametros.iloc[0]
    capital = float(a.iloc[1])
    Meta = float(a.iloc[2])
    nump = int(a.iloc[3])
    dnop = int(a.iloc[4])

with st.container():
    st.markdown("# :moneybag:  :violet[RELATÓRIO DE OPERAÇÕES EM DAY TRADE] ")
    if os.path.exists('resultados.csv'):
        resultado = pd.read_csv("resultados.csv", sep=',')
        col1, col2 = st.columns(2)
        ############################################################################
        tabela1 = resultado.set_index("Data")
        tabela2 = tabela1.sort_values(by=['Data', 'Ativo'], ascending=False)


        resultfinal = resultado[['Data', 'Ativo', 'Resultado do Dia']].tail(2)
        resultfinal1 = resultfinal.set_index("Data")

        ############################################################################

        df_summed = resultado.groupby('Ativo', as_index=False).sum()
        df_summed1 = df_summed[['Ativo', 'Resultado do Dia']]
        df_summed2 = df_summed1.set_index("Ativo")

        diario = resultado.groupby('Data')['Resultado do Dia'].sum().reset_index()

        diario["Saldo Acumulado"] = diario["Resultado do Dia"].cumsum()
        diario = diario.sort_values('Data', ascending=False)

        diario1 = diario[['Data', 'Resultado do Dia']].head(1)
        diario2 = diario1.set_index('Data')

        tabela4 = diario.style.format({'Resultado do Dia': '{:.2f}', 'Saldo Acumulado': '{:.2f}'})




        ########################################  PLANILHAS ##########################################

        ##### Planilha 1
        with st.expander(" :heavy_dollar_sign: Resultado do Último Dia Operado"):
            st.write('### :blue[Total por Ativo]')
            resultfinal11 = resultfinal.round(2)
            st.table(resultfinal11.style.format({'Resultado do Dia': '{:.2f}'}))
            st.write('### :blue[Saldo do dia]')
            st.table(diario2.style.format({'Resultado do Dia': '{:.2f}'}))

        ##### Planilha 2
        with st.expander(" :heavy_dollar_sign: Saldo Acumulado"):
            st.write('### :blue[Por Ativo]')
            df_summed2.rename(columns={'Resultado do Dia': 'Total Acumulado Por Ativo'}, inplace=True)
            st.table(df_summed2.style.format({'Total Acumulado Por Ativo': '{:.2f}'}))

        ##### Planilha 3
        with st.expander(" :heavy_dollar_sign: Resultado diário"):
            st.write('### :blue[Por Pregão]')
            btn_resetul1 = st.button(".Apagar Dados do Último Pregão.", type="primary")
            if btn_resetul1:
                resultado = resultado.drop(resultado.index[-1])
                resultado.to_csv('resultados.csv', index=False)
                
            st.table(tabela4)

        ##### Planilha 4
        with st.expander(" :heavy_dollar_sign: Resultado diário"):
            st.write('### :blue[Por Ativo]')
            btn_resetul2 = st.button("_Apagar Dados do Último Pregão_", type="primary")
            if btn_resetul2:
                resultado = resultado.drop(resultado.index[-1])
                resultado.to_csv('resultados.csv', index=False)
                
            tabela3 = tabela2.style.format({'Resultado do Dia': '{:.2f}', 'Saldo Acumulado': '{:.2f}'})
            st.table(tabela3)


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
                

        with col2:
            st.info('# :loudspeaker: ATENÇÃO!!! ')
            st.success('''## Antes de Apagar os Resultados, Gere os Relatórios e Faça Download dos dados''')

    else:
        st.error("# Você ainda não cadastrou operações")



