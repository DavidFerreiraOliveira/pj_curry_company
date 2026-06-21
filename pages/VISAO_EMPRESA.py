import streamlit as st 
import plotly.express as px
import pandas as pd 
import folium as fl
from streamlit_folium import folium_static 
from PIL import Image as im

# 1. Configurações Iniciais da Página
# OBS: Remova a linha abaixo se este arquivo for chamado via exec() no HOME.py
st.set_page_config(layout='wide')

# 2. Carregamento dos Dados
df = pd.read_csv('treino.csv')

# ==============================================================================
# BARRA LATERAL (Filtros e Informações - Devem vir ANTES dos gráficos)
# ==============================================================================
# Inserção de Imagem
try:
    imagem_logo = im.open('imagem.jpg')
    st.sidebar.image(imagem_logo, width=250)
except:
    st.sidebar.warning("Imagem 'imagem.jpg' não encontrada.")

st.sidebar.markdown('---')
st.sidebar.markdown('# Projeto de Portfólio')
st.sidebar.markdown('---')
st.sidebar.markdown('## Filtros:')

# Filtro de Linha Temporal (Slider)
date = st.sidebar.slider(
    'Data máxima de entrega:',
    value=pd.Timestamp(2022, 4, 3).date(),
    min_value=pd.Timestamp(2022, 2, 11).date(),
    max_value=pd.Timestamp(2022, 4, 6).date(),
    format='DD-MM-YYYY'
)                              

# Limpeza essencial para o filtro de tráfego funcionar sem travar
df['Road_traffic_density'] = df['Road_traffic_density'].astype(str).str.strip()
df = df[df['Road_traffic_density'] != 'NaN']

# Filtro Multinível de Tráfego
opcoes_trafego = df['Road_traffic_density'].unique()
cond = st.sidebar.multiselect('Condição de Trânsito:', opcoes_trafego, default=list(opcoes_trafego))

st.sidebar.markdown('---')
st.sidebar.markdown('# Criado Por:')
st.sidebar.markdown('### David Ferreira De Oliveira')

# ==============================================================================
# APLICAÇÃO DOS FILTROS NO DATAFRAME
# ==============================================================================
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# Aplica filtro de Data
linhas_filtradas_data = df['Order_Date'].dt.date <= date  
df = df.loc[linhas_filtradas_data, :]

# Aplica filtro de Densidade de Tráfego
linhas_filtradas_trafego = df['Road_traffic_density'].isin(cond)
df = df.loc[linhas_filtradas_trafego, :]

# ==============================================================================
# CORPO PRINCIPAL DA PÁGINA (Cabeçalhos e Menus de Navegação)
# ==============================================================================
# ==============================================================================
# CORPO PRINCIPAL DA PÁGINA (Cabeçalhos e Menus de Navegação)
# ==============================================================================
st.title("🏢 Visão Empresa")
st.caption("##### Esta página apresenta o crescimento operacional da plataforma através de análises temporais, de tráfego e geográficas.")
st.markdown("---")

# 1. Criando as Abas de visualização diretamente no topo da tela (NÃO PRECISA DE IF/ELIF)
v1, v2, v7 = st.tabs(["📊 Visão Gerencial", "📈 Visão Tática", "🌍 Visão Geográfica"])

# ==============================================================================
# CONTEÚDO DAS ABAS (Os gráficos rodam direto dentro de cada 'with')
# ==============================================================================

# ==============================================================================
# CONTEÚDO DAS ABAS WITH INFO
# ==============================================================================

# 📑 ABA 1: VISÃO GERENCIAL
with v1:
    st.markdown("### 📊 Visão Gerencial")
    
    # Gráfico Principal: Pedidos por Dia
    co = df.groupby('Order_Date')['ID'].count().reset_index(name='qtd.day')
    linhas = px.bar(
        co, x='Order_Date', y='qtd.day', 
        labels={'Order_Date': 'Data do Pedido', 'qtd.day': 'Quantidade de Pedidos'}
    )
    st.plotly_chart(linhas, use_container_width=True)
    
    # 💡 INFO DO GRÁFICO DE BARRAS
    st.info("💡 **Análise Temporal:** Este gráfico de barras monitora o volume diário de novos pedidos feitos na plataforma, permitindo identificar picos de demanda ao longo do mês.")
    st.markdown("<br>", unsafe_allow_html=True) # Dá um pequeno espaço vertical

    # Grid com 2 colunas para gráficos menores abaixo
    col1, col2 = st.columns(2)

    # Coluna esquerda: Pizza de Tráfego     
    with col1: 
        trafego = df.groupby('Road_traffic_density')['ID'].count().reset_index(name='total').sort_values('total', ascending=False)
        pizza = px.pie(trafego, values='total', names='Road_traffic_density', title='Percentual de Pedidos por Densidade de Tráfego')
        st.plotly_chart(pizza, use_container_width=True)
        
        # 💡 INFO DO GRÁFICO DE PIZZA
        st.info("🚗 **Densidade de Tráfego:** Mostra a divisão percentual das entregas conforme o fluxo do trânsito (Baixo, Médio, Alto). Ideal para entender o impacto do tráfego na operação.")
        
    # Coluna direita: Dispersão de Cidades       
    with col2:    
        df['City'] = df['City'].astype(str).str.strip()
        df_filtrado_cidade = df[df['City'] != 'NaN']
        trafego_city = df_filtrado_cidade.groupby(['City', 'Road_traffic_density'])['ID'].count().reset_index(name='total2')
        
        dispersao = px.scatter(
            trafego_city, x='City', y='Road_traffic_density', 
            size='total2', color='Road_traffic_density',
            title='Volume de Entregas por Cidade e Tipo de Trânsito'
        )
        st.plotly_chart(dispersao, use_container_width=True)
        
        # 💡 INFO DO GRÁFICO DE DISPERSÃO
        st.info("🏙️ **Distribuição Urbana:** O tamanho das bolhas representa o volume de pedidos. Crucial para mapear em quais tipos de cidades o trânsito impacta mais as vendas.")

# 📑 ABA 2: VISÃO TÁTICA
with v2:
    st.markdown("### 📈 Visão Tática")
    
    df['Semana'] = df['Order_Date'].dt.strftime('%U')
    fg = df.groupby('Semana')['ID'].count().reset_index(name='Quantidade de Pedidos')
    
    # Exibe os dados brutos e o gráfico de evolução semanal
    st.dataframe(fg, hide_index=True)
    linha = px.line(fg, x='Semana', y='Quantidade de Pedidos', title='Evolução de Pedidos por Semana do Ano')
    st.plotly_chart(linha, use_container_width=True)
    
    # 💡 INFO DA EVOLUÇÃO SEMANAL
    st.info("📈 **Evolução Semanal:** Gráfico de tendência que agrupa o volume de entregas pelas semanas do ano. Excelente para identificar sazonalidade e planejar campanhas de marketing.")

# 📑 ABA 3: VISÃO GEOGRÁFICA
with v7:
    st.markdown("### 🌍 Visão Geográfica")
    
    # Limpeza rápida das coordenadas
    df['City'] = df['City'].astype(str).str.strip()
    df_geo = df[df['City'] != 'NaN'].dropna(subset=['Delivery_location_latitude', 'Delivery_location_longitude'])
    
    # Agrupamento para pegar os pontos centrais (Mediana) por Cidade e Tráfego
    dados_mapa = df_geo.groupby(['City', 'Road_traffic_density'])[['Delivery_location_latitude', 'Delivery_location_longitude']].median().reset_index()
    
    if not dados_mapa.empty:
        # Centraliza o mapa na primeira coordenada encontrada
        lat_centro = dados_mapa['Delivery_location_latitude'].iloc[0]
        lon_centro = dados_mapa['Delivery_location_longitude'].iloc[0]
        
        mapa = fl.Map(location=[lat_centro, lon_centro], zoom_start=11)
        
        # Desenha os marcadores no mapa
        for index, row in dados_mapa.iterrows():
            fl.Marker(
                [row['Delivery_location_latitude'], row['Delivery_location_longitude']],
                popup=f"Cidade: {row['City']}<br>Tráfego: {row['Road_traffic_density']}",
                icon=fl.Icon(color='blue', icon='info-sign')
            ).add_to(mapa)
            
        # Mostra o mapa nativo na tela do Streamlit
        folium_static(mapa)
        
        # 💡 INFO DO MAPA GEOGRÁFICO
        st.info("🌍 **Hubs Centrais:** O mapa plota os pontos centrais geográficos (mediana) de entrega de cada cidade com base nas condições de trânsito locais.")
    else:
        st.warning("Não há dados geográficos disponíveis para os filtros selecionados.")
