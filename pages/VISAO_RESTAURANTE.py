

import streamlit as st 
import plotly.express as px
import pandas as pd 
from haversine import haversine
import numpy as np
from PIL import Image as im

# 1. Carregamento dos Dados
df = pd.read_csv('treino.csv')

# ==============================================================================
# BARRA LATERAL (Filtros)
# ==============================================================================
try:
    imagem_logo = im.open('imagem.jpg')
    st.sidebar.image(imagem_logo, width=250)
except:
    st.sidebar.warning("Imagem 'imagem.jpg' não encontrada.")

st.sidebar.markdown('---')
st.sidebar.markdown('# Projeto de Portfólio')
st.sidebar.markdown('---')
st.sidebar.markdown('## Filtros:')

date = st.sidebar.slider(
    'Data máxima de entrega:',
    value=pd.Timestamp(2022, 4, 3).date(),
    min_value=pd.Timestamp(2022, 2, 11).date(),
    max_value=pd.Timestamp(2022, 4, 6).date(),
    format='DD-MM-YYYY'
)                              

# Limpezas prévias essenciais
df['Road_traffic_density'] = df['Road_traffic_density'].astype(str).str.strip()
df = df[(df['Road_traffic_density'] != 'NaN') & (df['Road_traffic_density'] != 'nan')]

cond = st.sidebar.multiselect('Condição de Trânsito:', df['Road_traffic_density'].unique(), default=list(df['Road_traffic_density'].unique()))

st.sidebar.markdown('---')
st.sidebar.markdown('# Criado Por:')
st.sidebar.markdown('### David Ferreira De Oliveira')

# ==============================================================================
# APLICAÇÃO DOS FILTROS E LIMPEZA GERAL DE VARIÁVEIS
# ==============================================================================
df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%d-%m-%Y')
df = df[df['Order_Date'].dt.date <= date]
df = df[df['Road_traffic_density'].isin(cond)]

# Limpeza única da coluna de tempo (Evita repetição de código)
df['Time_taken(min)'] = df['Time_taken(min)'].astype(str).str.strip().str.replace('(min)', '', regex=False)
df['Time_taken(min)'] = pd.to_numeric(df['Time_taken(min)'], errors='coerce')
df = df.dropna(subset=['Time_taken(min)'])

# Limpeza de texto das colunas categóricas
df['Festival'] = df['Festival'].astype(str).str.strip()
df['City'] = df['City'].astype(str).str.strip()

# ==============================================================================
# CORPO PRINCIPAL DA PÁGINA
# ==============================================================================
st.title("🍲 Visão Restaurantes")
st.caption("##### Esta página avalia a dinâmica dos estabelecimentos parceiros com foco em distância média e tempo de entrega.")
st.markdown("---")

v1, = st.tabs(['Visão Restaurante'])

with v1:
    # ==============================================================================
    # SEÇÃO 1: CARDS EXECUTIVOS (Métricas Principais)
    # ==============================================================================
    with st.container():
        esc, meio, dire = st.columns(3)
        
        with esc: 
            st.markdown('#### 👥 Operação Geral')
            c1, c2 = st.columns(2)
            
            # Quantidade de restaurantes únicos
            df['Delivery_person_ID'] = df['Delivery_person_ID'].astype(str).str.strip()
            entregadores = df['Delivery_person_ID'].nunique()
            c1.metric('Entregadores Únicos', entregadores)
            
            # 🚨 FILTRO DE SEGURANÇA: Remove linhas onde as coordenadas são zero ou nulas
            df_dist = df[(df['Restaurant_latitude'] != 0) & (df['Restaurant_longitude'] != 0) &
                         (df['Delivery_location_latitude'] != 0) & (df['Delivery_location_longitude'] != 0)].copy()
            
            # Garante que as latitudes de entrega sejam negativas (se for o caso da região dos dados)
            # Para corrigir o sinal invertido que deforma o cálculo:
            df_dist['Restaurant_latitude'] = df_dist['Restaurant_latitude'].apply(lambda x: -abs(x) if x > 0 and x < 40 else x)
            df_dist['Delivery_location_latitude'] = df_dist['Delivery_location_latitude'].apply(lambda x: -abs(x) if x > 0 and x < 40 else x)
            
            # Aplica a fórmula apenas nas coordenadas válidas
            if not df_dist.empty:
                df_dist['distance'] = df_dist.apply(lambda x: haversine(
                    (x['Restaurant_latitude'], x['Restaurant_longitude']),
                    (x['Delivery_location_latitude'], x['Delivery_location_longitude'])
                ), axis=1)
                
                # Filtra distâncias absurdas que são erros de digitação do sistema (ex: entregas maiores que 50km)
                df_dist = df_dist[df_dist['distance'] < 50]
                
                dist_media = df_dist['distance'].mean()
                c2.metric('Distância Média', f"{dist_media:.2f} km")
                
                # Salva de volta no df original para o gráfico de pizza não quebrar
                df['distance'] = df_dist['distance']
            else:
                c2.metric('Distância Média', "0.00 km")


        with meio: 
            st.markdown('#### 🎉 Dias Com Festival')
            c3, c4 = st.columns(2)
            
            df_fest_yes = df[df['Festival'] == 'Yes']
            if not df_fest_yes.empty:
                c3.metric('Tempo Médio', f"{df_fest_yes['Time_taken(min)'].mean():.2f} min")
                c4.metric('Desvio Padrão', f"{df_fest_yes['Time_taken(min)'].std():.2f} min")
            else:
                c3.metric('Tempo Médio', "0.00 min")
                c4.metric('Desvio Padrão', "0.00 min")
                
        with dire: 
            st.markdown('#### 📅 Dias Sem Festival')
            c5, c6 = st.columns(2)
            
            df_fest_no = df[df['Festival'] == 'No']
            if not df_fest_no.empty:
                c5.metric('Tempo Médio', f"{df_fest_no['Time_taken(min)'].mean():.2f} min")
                c6.metric('Desvio Padrão', f"{df_fest_no['Time_taken(min)'].std():.2f} min")
            else:
                c5.metric('Tempo Médio', "0.00 min")
                c6.metric('Desvio Padrão', "0.00 min")

     # ==============================================================================
    # SEÇÃO 2: GRÁFICOS ANALÍTICOS (Distâncias e Tempos)
    # ==============================================================================
    with st.container():               
        st.markdown('''---''') 
        st.markdown('### 🏢 Distância Média das Entregas por Cidade')
        
        df_dist_city = df[df['City'] != 'NaN']
        avg_distancia_per_city = df_dist_city.groupby('City')['distance'].mean().reset_index() 
        
        fig_pie = px.pie( 
            avg_distancia_per_city,
            names='City',
            values='distance',
            title='Proporção da Distância Média Percorrida por Tipo de Cidade'
        )
        
        pull_values = [0] * len(avg_distancia_per_city) 
        if len(pull_values) > 2: 
            pull_values[2] = 0.1 
        fig_pie.update_traces(pull=pull_values) 

        st.plotly_chart(fig_pie, use_container_width=True) 
        st.info("📊 **Logística Urbana:** Avalia o raio médio de distância das entregas. Cidades com fatias maiores exigem maior deslocamento dos entregadores para levar a comida até o cliente.")
                      
    with st.container():               
        st.markdown('''---''') 
        st.markdown('### ⏱️ Distribuição do Tempo de Entrega por Cidade') 
        
        df_tempo_city = df[df['City'] != 'NaN']
        
        # 📊 TABELA: Agrupamento por Cidade e Tipo de Pedido (Parte recuperada)
        tabela = (df_tempo_city.groupby(['City', 'Type_of_order'])['Time_taken(min)']
                  .agg(media_min='mean', desvpd_mim='std')
                  .reset_index()
                  .round(2)
                  .rename(columns={
                      'City': 'Cidade', 
                      'Type_of_order': 'Tipo de Pedido',
                      'media_min': 'Média de Tempo (min)',
                      'desvpd_mim': 'Desvio Padrão'
                  }))
        st.dataframe(tabela, hide_index=True, use_container_width=True)
        st.info("📉 **Detalhamento por Categoria:** Tabela analítica cruzando os tempos de entrega médios conforme o tipo de prato pedido e a região do restaurante.")

    with st.container():   
        st.markdown('''---''') 
        st.markdown('### ☀️ O tempo médio e o desvio padrão de entrega por cidade e tipo de tráfego') 
      
        # 🗺️ GRÁFICO SUNBURST: Agrupamento por Cidade e Tráfego (Parte recuperada)
        df_aux = (df_tempo_city.groupby(['City', 'Road_traffic_density'])['Time_taken(min)'] 
                    .agg(media_min='mean', desvpd_min='std') 
                    .reset_index()) 
        
        gb = px.sunburst( 
            df_aux, 
            path=['City', 'Road_traffic_density'], 
            values='media_min',                     
            color='desvpd_min',                      
            color_continuous_scale='RdBu', 
            color_continuous_midpoint=np.average(df_aux['desvpd_min'])
        )

        st.plotly_chart(gb, use_container_width=True)
        st.info("☀️ **Mapa Multidimensional:** Gráfico que mapeia a hierarquia das cidades cruzada com as condições de trânsito. O tamanho das áreas indica o tempo médio e a variação de cor representa o desvio padrão (consistência dos tempos).")
