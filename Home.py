import streamlit as st
from PIL import Image
import pandas as pd

# 1. Configuração ÚNICA (sempre no topo)
st.set_page_config(page_title='Home', layout='wide')


# 2. Carregamento de dados (para a página Home, se precisar)
df = pd.read_csv('treino.csv')


st.sidebar.title("Navegação")
paginas = st.sidebar.radio("Selecione a visão:", 
    ["🏠 Home", "🏢 Visão Empresa", "🚚 Visão Entregadores", "🍴 Visão Restaurantes"])

# 4. LÓGICA DE CONEXÃO (Substitua seu bloco por este)
import os

# No seu Home.py, mude a lógica para isto:
caminho_base = os.path.dirname(__file__) # Descobre onde o Home.py está

if paginas == "🏠 Home":
    st.title("Dashboard Curry Company")
    st.markdown("### Selecione uma das opções no menu lateral.")

elif paginas == "🏢 Visão Empresa":
    # Monta o caminho correto para o servidor
    path_empresa = os.path.join(caminho_base, "pages", "VISAO_EMPRESA.py")
    with open(path_empresa, encoding="utf-8") as f:
        exec(f.read())

elif paginas == "🚚 Visão Entregadores":
    path_entregadores = os.path.join(caminho_base, "pages", "VISAO_ENTREGADORES.py")
    with open(path_entregadores, encoding="utf-8") as f:
        exec(f.read())

elif paginas == "🍴 Visão Restaurantes":
    path_restaurante = os.path.join(caminho_base, "pages", "VISAO_RESTAURANTE.py")
    with open(path_restaurante, encoding="utf-8") as f:
        exec(f.read())

