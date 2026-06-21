import streamlit as st 
import pandas as pd
from PIL import Image as im

# 1. Configurações Iniciais da Página
# OBS: Remova a linha abaixo se este arquivo for chamado via exec() no HOME.py
st.set_page_config(layout='wide')

# 2. Carregamento dos Dados
df = pd.read_csv('treino.csv')

# ==============================================================================
# BARRA LATERAL (Criação de Todos os Filtros na Ordem Correta)
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

# 1. Filtro de Linha Temporal (Slider)
date = st.sidebar.slider(
    'Data máxima de entrega:',
    value=pd.Timestamp(2022, 4, 3).date(),
    min_value=pd.Timestamp(2022, 2, 11).date(),
    max_value=pd.Timestamp(2022, 4, 6).date(),
    format='DD-MM-YYYY',
    key='slider_data_entregadores'
)                              

# Limpezas prévias essenciais para evitar falhas de texto 'NaN' nos componentes
df['Road_traffic_density'] = df['Road_traffic_density'].astype(str).str.strip()
df = df[df['Road_traffic_density'] != 'NaN']

df['Delivery_person_Age'] = df['Delivery_person_Age'].astype(str).str.strip()
df_idades_validas = df[df['Delivery_person_Age'] != 'NaN']

df['Vehicle_condition'] = df['Vehicle_condition'].astype(str).str.strip()
df_veiculos_validos = df[df['Vehicle_condition'] != 'NaN']

# 2. Filtro de Densidade de Tráfego
cond = st.sidebar.multiselect(
    'Condição de Trânsito:', 
    df['Road_traffic_density'].unique(), 
    default=list(df['Road_traffic_density'].unique())
)

# 3. Filtro de Intervalo de Idade (Slider Duplo) - Tratamento seguro de float
menor_idade_base = int(df_idades_validas['Delivery_person_Age'].astype(float).astype(int).min())
maior_idade_base = int(df_idades_validas['Delivery_person_Age'].astype(float).astype(int).max())

idades_selecionadas = st.sidebar.slider(
    'Filtrar por Idade dos Entregadores:',
    min_value=menor_idade_base,
    max_value=maior_idade_base,
    value=(menor_idade_base, maior_idade_base),
    key='slider_idade_entregadores'
)

# 4. Filtro de Condição do Veículo (Multiselect)
opcoes_veiculo = sorted(df_veiculos_validos['Vehicle_condition'].unique())
cond_veiculo = st.sidebar.multiselect(
    'Condição do Veículo:', 
    opcoes_veiculo, 
    default=list(opcoes_veiculo)
)

st.sidebar.markdown('---')
st.sidebar.markdown('# Criado Por:')
st.sidebar.markdown('### David Ferreira De Oliveira')

# ==============================================================================
# APLICAÇÃO DE TODOS OS FILTROS NO DATAFRAME
# ==============================================================================
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# 1. Filtro de linha temporal (Data)
var_data = df['Order_Date'].dt.date <= date 
df = df.loc[var_data, :]

# 2. Filtro de Densidade de Tráfego
var_trafego = df['Road_traffic_density'].isin(cond)
df = df.loc[var_trafego, :]

# 3. Filtro de Intervalo de Idade
df['Delivery_person_Age'] = pd.to_numeric(df['Delivery_person_Age'], errors='coerce')
var_idade = (df['Delivery_person_Age'] >= idades_selecionadas[0]) & (df['Delivery_person_Age'] <= idades_selecionadas[1])
df = df.loc[var_idade, :]

# 4. Filtro de Condição do Veículo
df['Vehicle_condition'] = df['Vehicle_condition'].astype(str).str.strip()
var_veiculo = df['Vehicle_condition'].isin(cond_veiculo)
df = df.loc[var_veiculo, :]

# ==============================================================================
# CORPO PRINCIPAL DA PÁGINA (Cabeçalhos)
# ==============================================================================
st.title("🚚 Visão Entregadores")
st.caption("##### Acompanhamento do perfil operacional, eficiência e métricas de desempenho dos entregadores parceiros.")
st.markdown("---")

# ==============================================================================
# SEÇÃO 1: CARDS DE MÉTRICAS GERAIS (Idade e Veículo)
# ==============================================================================
with st.container():
    col_esquerda, col_direita = st.columns(2)

    with col_esquerda:
        st.markdown("#### 🎂 Idades dos Entregadores")
        sub_col1, sub_col2 = st.columns(2)
        
        df_idades_cards = df.dropna(subset=['Delivery_person_Age'])
        if not df_idades_cards.empty:
            idades = df_idades_cards['Delivery_person_Age'].astype(float).astype(int)
            sub_col1.metric('Mínima', f"{idades.min()} anos")
            sub_col2.metric('Máxima', f"{idades.max()} anos")

    with col_direita:
        st.markdown('#### 🚗 Condição do Veículo')
        sub_col3, sub_col4 = st.columns(2)
        
        df_veiculo_cards = df[df['Vehicle_condition'] != 'NaN']
        if not df_veiculo_cards.empty:
            veiculo = df_veiculo_cards['Vehicle_condition'].astype(int)
            sub_col3.metric('Pior Estado', veiculo.min())
            sub_col4.metric('Melhor Estado', veiculo.max())
     
st.markdown('''---''')
                
# ==============================================================================
# SEÇÃO 2: AVALIAÇÕES (Tabelas de Médias e Desvios Padrão)
# ==============================================================================
with st.container():
    col_tabela1, col_tabela2 = st.columns(2, gap='large')
    
    with col_tabela1:
        st.markdown('#### 🏅 Média de avaliações por Entregador')
         
        df['ID Entregadores Unicos'] = df['Delivery_person_ID']
        df['Media de Avaliçoes'] = pd.to_numeric(df['Delivery_person_Ratings'], errors='coerce')
        
        df_avaliacoes_limpo = df.dropna(subset=['Media de Avaliçoes'])
        avaliaçoes = df_avaliacoes_limpo.groupby('ID Entregadores Unicos')['Media de Avaliçoes'].mean().reset_index().round(2)
        st.dataframe(avaliaçoes, hide_index=True, use_container_width=True)
        st.info("📊 **Avaliação Individual:** Nota média histórica acumulada por cada entregador cadastrado na plataforma.")
         
    with col_tabela2:
        st.markdown('#### 🌤️ Avaliação Média por Condições Climáticas')
        
        df['Delivery_person_Ratings'] = pd.to_numeric(df['Delivery_person_Ratings'], errors='coerce')     
        df['Weatherconditions'] = df['Weatherconditions'].astype(str).str.strip()
        
        avm = (df[df['Weatherconditions'] != 'NaN']
               .groupby('Weatherconditions')['Delivery_person_Ratings']
               .agg(Média='mean', Desvio_Padrão='std')
               .reset_index() 
               .round(2)) 
        st.dataframe(avm, hide_index=True, use_container_width=True)
        
        st.markdown('#### 🚦 Avaliação Média por Tipo de Tráfego')
        
        df['Road_traffic_density'] = df['Road_traffic_density'].astype(str).str.strip()
        trafeg_av = (df[df['Road_traffic_density'] != 'NaN']
                      .groupby('Road_traffic_density')['Delivery_person_Ratings']
                      .agg(Média='mean', Desvio_Padrão='std')
                      .reset_index()
                      .round(2))
        st.dataframe(trafeg_av, hide_index=True, use_container_width=True)
        st.info("💡 **Desempenho por Contexto:** Compara como fatores externos (clima e trânsito) afetam diretamente as notas dadas pelos clientes.")

st.markdown('''---''')

# ==============================================================================
# SEÇÃO 3: VELOCIDADE OPERACIONAL (Ranking Top 10)
# ==============================================================================
st.markdown('#### ⚡ Os 10 entregadores mais rápidos por cidade')

df['Time_taken(min)'] = df['Time_taken(min)'].astype(str).str.strip().str.replace('(min)', '', regex=False)
df['Time_taken(min)'] = pd.to_numeric(df['Time_taken(min)'], errors='coerce')
df['City'] = df['City'].astype(str).str.strip()
df_velocidade = df[(df['Time_taken(min)'].notna()) & (df['City'] != 'NaN')]

if not df_velocidade.empty:
    fgh = df_velocidade.groupby(['City', 'Delivery_person_ID'])['Time_taken(min)'].mean().reset_index()
    fg = fgh.sort_values(['City', 'Time_taken(min)']).groupby('City').head(10) 
    fg.columns = ['Cidades', 'ID Entregador', 'Tempo Médio (min)']    
    st.dataframe(fg, hide_index=True, use_container_width=True)
    st.info("🏆 **Eficiência Operacional:** Ranking dos profissionais que realizam as entregas no menor tempo médio, segmentados por tipo de região.")
else:
    st.warning("Sem dados suficientes para calcular o ranking de velocidade.")
