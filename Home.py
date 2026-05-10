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
#if paginas == "🏠 Home":
    #st.title("Dashboard Curry Company")
    #st.markdown("### Selecione uma das opções no menu lateral.")

#elif paginas == "🏢 Visão Empresa":
    # Em vez de switch_page, vamos rodar o código do arquivo direto aqui
 #   with open("pages/VISAO_EMPRESA.py", encoding="utf-8") as f:
  #      exec(f.read())

#elif paginas == "🚚 Visão Entregadores":
 #   with open("pages/VISAO_ENTREGADORES.py", encoding="utf-8") as f:
  #      exec(f.read())

#elif paginas == "🍴 Visão Restaurantes":
 #   with open("pages/VISAO_RESTAURANTE.py", encoding="utf-8") as f:
  #      exec(f.read())
