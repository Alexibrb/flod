import streamlit as st
import pandas as pd
import os
import io
import openpyxl

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
# Função para criar um arquivo xlsx contendo os DataFrames
def create_xlsx_file(dataframes):
    # Cria um buffer de memória para o arquivo xlsx
    buffer = io.BytesIO()

    # Usa o pandas ExcelWriter para salvar múltiplos dataframes em diferentes planilhas
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        for i, df in enumerate(dataframes):
            df.to_excel(writer, index=False, sheet_name=f'DataFrame_{i + 1}')

    buffer.seek(0)
    return buffer

with st.container():
    st.markdown("# :moneybag: RELATÓRIO DE OPERAÇÕES EM DAY TRADE :heavy_dollar_sign: ")
    if os.path.exists('resultados.csv'):
        resultado = pd.read_csv("resultados.csv", sep=',')
        col1, col2 = st.columns(2)
        ############################################################################
        tabela1 = resultado.set_index("Data")
        tabela2 = tabela1.sort_values(by='Data', ascending=False)


        resultfinal = resultado[['Data', 'Ativo', 'Resultado do Dia']].tail(2)
        resultfinal1 = resultfinal.set_index("Data")

        ############################################################################

        df_summed = resultado.groupby('Ativo', as_index=False).sum()
        df_summed1 = df_summed[['Ativo', 'Resultado do Dia']]
        df_summed2 = df_summed1.set_index("Ativo")

        diario = resultado.groupby('Data')['Resultado do Dia'].sum().reset_index()
        diario["Saldo Acumulado"] = diario["Resultado do Dia"].cumsum()
        diario = diario.sort_values(['Data', 'Saldo Acumulado'], ascending=False)

        tabela4 = diario.style.format({'Resultado do Dia': '{:.2f}', 'Saldo Acumulado': '{:.2f}'})

        diario1 = diario[['Data', 'Resultado do Dia']].head(1)
        diario2 = diario1.set_index('Data')




        ########################################  PLANILHAS ##########################################
        with st.expander(" :heavy_dollar_sign: Resultado do Último Dia Operado"):
            st.write('Total por Ativo')
            resultfinal11 = resultfinal1.round(2)
            st.table(resultfinal11.style.format({'Resultado do Dia': '{:.2f}'}))
            st.write('Saldo do dia')
            st.table(diario2.style.format({'Resultado do Dia': '{:.2f}'}))

        with st.expander(" :heavy_dollar_sign: Saldo Acumulado por Ativo"):
            df_summed2.rename(columns={'Resultado do Dia': 'Total Acumulado Por Ativo'}, inplace=True)
            st.table(df_summed2.style.format({'Total Acumulado Por Ativo': '{:.2f}'}))

        with st.expander(" :heavy_dollar_sign: Resultado diário por pregão"):

            btn_resetul1 = st.button(".Apagar Dados do Último Pregão.", type="primary")
            if btn_resetul1:
                resultado = resultado.drop(resultado.index[-1])
                resultado.to_csv('resultados.csv', index=False)
                st.experimental_rerun()
            st.table(tabela4)
        with st.expander(" :heavy_dollar_sign: Resultado diário por ativo"):


            btn_resetul2 = st.button("_Apagar Dados do Último Pregão_", type="primary")
            if btn_resetul2:
                resultado = resultado.drop(resultado.index[-1])
                resultado.to_csv('resultados.csv', index=False)
                st.experimental_rerun()
            tabela3 = tabela2.style.format({'Resultado do Dia': '{:.2f}', 'Saldo Acumulado': '{:.2f}'})
            st.table(tabela3)


        st.markdown('#  :arrow_down: Download dos Resultados')
        col1, col2 = st.columns(2)
        with col1:


            if st.button('  Geral Relatório de Operações', type='primary'):
                dataframes = [diario, tabela2]  # Lista de DataFrames
                xlsx_buffer = create_xlsx_file(dataframes)

                st.download_button(
                    label=" Clique para baixar",
                    data=xlsx_buffer,
                    file_name='Resultado.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            btn_resetr = st.button("Apagar Resultados", type="primary")
            if btn_resetr:
                os.remove('resultados.csv')
                st.experimental_rerun()

        with col2:
            st.success('''# :loudspeaker: ATENÇÃO!!! 
        Antes de Apagar os Resultados, 
        Gere os Relatórios e Faça Download dos dados''')

    else:
        st.error("# Você ainda não cadastrou operações")