import streamlit as st
import pandas as pd
import os
import io
import time

def spinner():
    with st.spinner('Aguarde... carregando a página'):
        # Simule uma tarefa de longa duração
        time.sleep(1)
def titulo():
    st.markdown("# 📢 DASHBOARD DE OPERAÇÕES EM DAY TRADE")
    st.write("---")


def cria_sidebar():
    with st.sidebar:
        link = "logogrande.jpeg"
        link2 = "grafico.png"
        icone = "icone.jpeg"
        st.logo(link2, icon_image=link2)
        st.image(link)
        if os.path.exists('parametros.csv'):
            tabelaconfig = pd.read_csv('parametros.csv', sep=",")
            nome = tabelaconfig['operador'][0]
            if nome != '':
                st.title(f'  :blue[Operador⤵️]')
                st.success(f'# 🧑‍💻 {nome}')


        st.info("# DASHBOARD DAY TRADE")

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

def estilos():
    st.markdown("""
        <style>
        .stButton > button {
            brow-widget stButton #262730; 
            background-color: #000000; 
            padding: 25px 25px;  
            text-align: center;
            display: inline-block;
            font-size: 16px;
            margin: 10px 10px;
            cursor: pointer;
            border: 1px solid;
            border-radius: 8px;
            width: 100%;
        }
        
        .stButton > button:hover {
            background-color: #262730;
            color: white;
        }
        
        .st-emotion-cache-1zhiv0.e1f1d6gn0 {
            background-color:#000000;
            color: gray;
        }

        .st-emotion-cache-q49buc{
            font-size: 24px;
            color: white;
        }
        
        .stAlert{
            text-align: center;
            padding: 3px 3px;
            margin: 3px 3px;
            
        }

        </style>
        """, unsafe_allow_html=True)

def estilos2():
    st.markdown("""
        <style>
        .stButton > button {
            brow-widget stButton #262730; 
            background-color: #000000; 
            padding:30px 30px;  
            text-align: center;
            display: inline-block;
            font-size: 16px;
            margin: 10px 10px;
            cursor: pointer;
            border: 1px solid;margin: 10px 10px;
            border-radius: 8px;
            width: 100%;
        }
        
        .stButton > button:hover {
            background-color: #262730;
            color: black;
        }

        .st-emotion-cache-1zhiv0.e1f1d6gn0 {
            background-color:#000000;
            color: gray;
        }

        .st-emotion-cache-q49buc{
            font-size: 24px;
            color: white;

        }
        
        .stAlert{
            text-align: center;
            padding: 3px 3px;
            margin: 3px 3px;
        }

        .stDownloadButton > button {
            background-color: green; 
            padding: 25px 25px;  
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 10px;
            cursor: pointer;
            border: none;
            border-radius: 8px;
            width: 100%;
        }
        .stDownloadButton > button:hover {
            background-color: #262730;
            color: black;
        </style>
        """, unsafe_allow_html=True)