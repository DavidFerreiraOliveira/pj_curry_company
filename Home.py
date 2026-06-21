import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
# q='wide')
import pandas as pd
import streamlit as st
import plotly.express as px

# 1. Configura a página para o modo Wide básico
st.set_page_config(
    page_title="Dashboard Cury Company",
    page_icon="📊",
    layout="wide"
)


# Código de leitura e limpeza de dados...
# Criação do seu menu lateral personalizado (paginas = st.sidebar.radio...)
# 2. Injeta CSS para zerar as margens e forçar 100% de largura real
st.markdown("""
    <style>
        /* Remove o espaçamento do topo e das laterais do bloco principal */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 90% !important;
        }
        /* Remove espaços extras acima do título principal */
        #root > div:nth-child(1) > div:nth-child(1) > div > div > div > section > div {
            padding-top: 50px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- DAQUI PARA BAIXO SEGUE O SEU CÓDIGO NORMAL ---


# 2. Carregamento de dados (para a página Home, se precisar)
df = pd.read_csv('treino.csv')



# 4. LÓGICA DE CONEXÃO (Substitua seu bloco por este)
# 4. LÓGICA DE CONEXÃO (Versão Otimizada)
st.title("📊 Dashboard Cury Company")
st.markdown('---')
    
    # Seções com boa hierarquia de tamanhos
st.header("🎯 Sobre o Projeto")
st.markdown(
        "#### Este aplicativo foi desenvolvido como o meu **primeiro projeto de portfólio em Ciência de Dados**, "
        "utilizando dados operacionais da **Cury Company** — uma empresa de tecnologia que atua no modelo de Marketplace."
    )
    
st.markdown(
        "#### A plataforma realiza o intermédio de negócios conectando três pilares essenciais: "
        "**Restaurantes**, **Entregadores** e **Compradores**."
    )
    # Insira este bloco logo após a introdução da Home
with st.expander("💼 O Problema de Negócio"):
        st.markdown(
            "##### Apesar do crescimento acelerado no volume de entregas e da forte expansão da **Cury Company**, "
            "a liderança enfrentava um grande obstáculo estratégico: **a falta de visibilidade centralizada**."
        )
    
        st.markdown(
            "##### Como a operação gera milhões de dados diariamente através da interação entre restaurantes, entregadores "
            "e clientes, as informações ficavam dispersas. Sem um ponto único de verdade, o CEO não conseguia acompanhar "
            "os Indicadores-Chave de Performance (KPIs) essenciais para guiar o futuro da empresa."
        )

        
with st.expander("🎯 O Objetivo do Projeto"):
        st.markdown("#### O objetivo principal deste projeto foi coletar, limpar e organizar essas métricas estratégicas, consolidando-as em uma **única ferramenta visual, interativa e de fácil acesso**.") 
        
        st.markdown("#### Com este painel, a liderança agora tem o poder de:")
        st.markdown("##### 📉 **Monitorar o crescimento** temporal e geográfico dos pedidos.")
        st.markdown("##### ⚡ **Identificar gargalos operacionais** na velocidade das entregas.")
        st.markdown("##### 💡 **Tomar decisões rápidas** e totalmente orientadas a dados (Data-Driven).")

            


 # ==============================================================================
# 4. LÓGICA DE NAVEGAÇÃO DO MENU LATERAL
# ==============================================================================
# Caixa de informação destacada para guiar o usuário
    


    
    
    # Aqui fica a estrutura completa que você me mandou (dentro da Home)
with st.expander("📋 Veja a Estrutura Completa do Dashboard"):
        st.markdown("##### 1. **Visão Empresa:** Análise Temporal, Distribuição de Tráfego e Geográfica.")
        st.markdown("##### 2. **Visão Entregadores:** Perfil Operacional, Desempenho e Eficiência.")
        st.markdown("##### 3. **Visão Restaurantes:** Indicadores Gerais, Impacto de Festivais e Distribuição de Tempo.")
    
    # Caixa de informação destacada para guiar o usuário (fora do expander
st.info("##### 👈 **Como navegar:** Selecione uma das visões de negócio no menu lateral para explorar os gráficos e mapas.")

       



    
  