import streamlit as st
import pandas as pd
import os
import numpy as np
import plotly.graph_objects as go


st.write("# :bar_chart: Gráficos de Operações DayTrade")

if os.path.exists('resultados.csv'):
    resultado = pd.read_csv("resultados.csv", sep=',')
    resultado["Saldo Acumulado"] = resultado["Resultado do Dia"].cumsum()
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

    resultadowin = resultado[resultado['Ativo'] == 'WIN']
    resultadowinF = resultadowin.set_index("Data")

    resultadowdo = resultado[resultado['Ativo'] == 'WDO']
    resultadowdoF = resultadowdo.set_index("Data")

    tabela2 = tabela1.sort_values(['Data', 'Saldo Acumulado'], ascending=False)

    # verde = "#005700"
    vermelho = "b31610"
    azul = "#1389ff"

    ###################################### CORES DOS GRÁFICOS ######################################
    resultadowin['cor'] = resultadowin['Resultado do Dia'].apply(lambda x: 'green' if x > 0 else 'red')
    corwin = resultadowin['cor']

    resultadowdo['cor'] = resultadowdo['Resultado do Dia'].apply(lambda x: 'green' if x > 0 else 'red')
    corwdo = resultadowdo['cor']

    resultado['cor'] = resultado['Resultado do Dia'].apply(lambda x: 'green' if x > 0 else 'red')
    cors = resultado['cor']

    resultado['cor2'] = resultado['Saldo Acumulado'].apply(lambda x: 'green' if x > 0 else 'red')
    corsaldo = resultado['cor2']

    ###################################### GRÁFICOS ######################################

    with st.container(height=550):
        st.markdown("# :chart_with_upwards_trend: Saldo Acumulado")
        GrafArea = go.Figure()
        GrafArea.add_trace(go.Scatter(x=resultado['Saldo Acumulado'].round(2), y=resultado['Saldo Acumulado'],
                                      marker_color=corsaldo, fill='tozeroy', mode='lines+markers'))
        GrafArea.update_traces(marker=dict(color=corsaldo), line=dict(color='darkgreen'))

        GrafArea.update_layout(
            title='',
            xaxis_title='Curva de Patrimônio',
            yaxis_title='Valores',
            xaxis=dict(type='category'),  # Define o tipo de eixo x como categoria

        )
        st.plotly_chart(GrafArea)

    with st.container(height=600):
        st.markdown("# :chart_with_upwards_trend: Resultado Diário Das Operaçõe Mini Índice")

        GrafBar = go.Figure()
        GrafBar.add_trace(go.Bar(x=resultadowin['Data'], y=resultadowin['Resultado do Dia'], marker_color=corwin,
                                 text=resultadowin['Resultado do Dia'],
                                 textposition='auto',
                                 name='Resultado do Dia',
                                 textfont=dict(color='white', size=16)))

        GrafBar.update_layout(
            title='',
            xaxis_title='Data do Pregão',
            yaxis_title='Resultado do Dia',
            xaxis=dict(type='category'),  # Define o tipo de eixo x como categoria
            xaxis_tickangle=-45,  # Rotaciona os rótulos das datas para melhor visualização
            barmode='group',  # (stack, overlay ou group

        )
        st.plotly_chart(GrafBar)

    with st.container(height=600):
        st.markdown("# :chart_with_upwards_trend: Resultado Diário Das Operações Mini Dólar")
        GrafBar = go.Figure()
        GrafBar.add_trace(go.Bar(x=resultadowdo['Data'], y=resultadowdo['Resultado do Dia'], marker_color=corwdo,
                                 text=resultadowdo['Resultado do Dia'],
                                 textposition='auto',
                                 name='Resultado do Dia',
                                 textfont=dict(color='white', size=16)))

        GrafBar.update_layout(
            title='',
            xaxis_title='Data do Pregão',
            yaxis_title='Resultado do Dia',
            xaxis=dict(type='category'),  # Define o tipo de eixo x como categoria
            xaxis_tickangle=-45,  # Rotaciona os rótulos das datas para melhor visualização
            barmode='group',  # (stack, overlay ou group

        )
        st.plotly_chart(GrafBar)

    with st.container(height=700):
        st.markdown("# :chart_with_upwards_trend: Desempenho Trade a Trade ")

        df = resultado

        # Resetar o índice para usar como eixo x
        df.reset_index(inplace=True)

        # Converter o índice para string para categorizar
        # df['index_str'] = df.index.astype(str)

        # Definir cores para valores positivos e negativos
        colors = np.where(df['Resultado do Dia'] >= 0, 'rgba(0, 255, 0, 0.7)', 'rgba(255, 0, 0, 0.7)')

        # Criar o gráfico de barras
        fig = go.Figure()

        # Criar rótulos combinados para Resultado do Dia e Data
        text_labels = df.apply(
            lambda row: f'{row["Resultado do Dia"]:.2f}<br>{row["Ativo"]}',
            axis=1)

        # Adicionar as barras com rótulos
        fig.add_trace(go.Bar(
            x=df.index + 1,
            y=df['Resultado do Dia'],
            marker_color=colors,
            text=text_labels,  # Texto dos rótulos com os valores
            textposition='auto',  # Posicionar os rótulos automaticamente
            name='Resultado do Dia',
            textfont=dict(color='white', size=14)  # Definir a cor do texto dos rótulos
        ))

        # Customizar layout
        fig.update_layout(
            title='',
            xaxis_title='Operações',
            yaxis_title='Resultado do Dia',
            xaxis=dict(type='category'),  # Definir o eixo x como categórico
            yaxis=dict(range=[min(df['Resultado do Dia']) - 1, max(df['Resultado do Dia']) + 1]),
            # Ajustar o intervalo do eixo y
            height=600  # Ajustar a altura do gráfico para fornecer mais espaço vertical
        )

        # Mostrar o gráfico

        st.plotly_chart(fig)

    col1, col2 = st.columns(2)

    with col1:
        with st.container(height=600):  # 00FF00
            st.markdown("## :chart_with_upwards_trend: Resultado Acumulado Por Ativo ")

            GrafBar = go.Figure()
            GrafBar.add_trace(
                go.Bar(x=df_summed1['Ativo'], y=df_summed1['Resultado do Dia'], marker_color=corwin,
                       text=df_summed1['Resultado do Dia'],
                       textposition='auto',
                       name='Resultado do Dia',
                       textfont=dict(color='white', size=16)))

            GrafBar.update_layout(
                title='',
                xaxis_title='Ativo',
                yaxis_title='Resultado Acumulado',
                xaxis=dict(type='category'),  # Define o tipo de eixo x como categoria
                xaxis_tickangle=-45,  # Rotaciona os rótulos das datas para melhor visualização
                barmode='overlay',  # (stack, overlay ou group

            )
            st.plotly_chart(GrafBar)

    with col2:
        with st.container(height=600):
            st.markdown("## :chart_with_upwards_trend: Resultado Último Dia Operado ")

            GrafBar = go.Figure()
            GrafBar.add_trace(
                go.Bar(x=resultfinal['Ativo'], y=resultfinal['Resultado do Dia'], marker_color=corwin,
                       text=resultfinal['Resultado do Dia'],
                       textposition='auto',
                       name='Resultado do Dia',
                       textfont=dict(color='white', size=16)))

            GrafBar.update_layout(
                title='',
                xaxis_title='Ativo',
                yaxis_title='Resultado do Dia',
                xaxis=dict(type='category'),  # Define o tipo de eixo x como categoria
                xaxis_tickangle=-45,  # Rotaciona os rótulos das datas para melhor visualização
                barmode='overlay',  # (stack, overlay ou group

            )
            st.plotly_chart(GrafBar)

else:
    st.error("# Você ainda não cadastrou operações")