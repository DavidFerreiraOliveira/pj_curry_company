


import streamlit as st 
#====================================
# importaçao de bibliotecaas 
#====================================
import plotly.express as px
import pandas as pd 
from haversine import haversine
import numpy as np # Importa a biblioteca NumPy
# bibliotea utilizada para adiçao de imagens 
from PIL import Image as im

st.set_page_config(layout = 'wide')
df = pd.read_csv('treino.csv')


#====================================
# Criaçao de abas e estruturaçao da pagina 
#====================================

# funçao serve ára criar titulos
st.header('Visão Restaurante')

# para a inserçao e imagems a pagina
#image= r'C:\Users\ddfer\PYTHON\PYTHON\imagem.jpg'
im = im.open('imagem.jpg')
st.sidebar.image(im, width = 250)

# 1 funcao serve psara criar uma barra lateral e adiconar conforme a necessidade
# 2 funçao serve para criar titulos e subtitulos usando o ### como forma de grau de subordinaçao 
st.sidebar.markdown('''------''')
st.sidebar.markdown('# Projeto de Portifolio')
# aqui e possivel fazer separeçoes com linhas 
st.sidebar.markdown('''------''')

st.sidebar.markdown('##  Filtros: ')
# funcao criar um filtro de data em forma de linha na barra lateral 

#====================================
# CRIAÇAO DE FILTROS  
#====================================

date = st.sidebar.slider(
    'Data',
    # aqui eu falo em qual data ficara quando esta em repouso 
    value=pd.Timestamp(2022, 4, 3).date(),
    # me retorna a menor data do dataframe 
    min_value=pd.Timestamp(2022, 2, 11).date(),
    # retorna a data maxima do dataframe 
    max_value=pd.Timestamp(2022, 4, 6).date(),
    # formato com que a data vai ficar sendo dia - mes - ano 
    format='DD-MM-YYYY'
)                              
# para visualizar o resultado final do codigo na  pagina  
st.header(date )
# serve para visulalizar o dataframe direto na paginas
df.dropna(subset= 'Road_traffic_density', inplace= True ) 
df['Road_traffic_density'] = df.loc[(df['Road_traffic_density']!= 'NaN ') & (df['Road_traffic_density']!= 'nan '),'Road_traffic_density']

# filtro para multiplas condiçoes 
cond = st.sidebar.multiselect( 'Condiçao do Veiculo ', df['Road_traffic_density'].unique() ,default = df['Road_traffic_density'].unique())


st.sidebar.markdown('''------''')


st.sidebar.markdown('# Criado Por:')

st.sidebar.markdown('### David Ferreira De Oliveira')


# para que o fliltro de linha temporal seja aplicado nos graficos

## transforma a coluna do date frame em data
df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%d-%m-%Y')

# cria uma variavel que recebe a condiçao para o filtro ser aplicado
var = df['Order_Date'].dt.date < date  
# usar a varivel( var ) para que o filtro funcione linha a linha 
df = df.loc[var, :]

# visualzar o grafico co o filro aplicado 


# para que os fltro do tipo selecionavel seja aplicado nos graficos 
var1 = df['Road_traffic_density'].isin (cond)
df = df.loc[var1,:]


# criar abas 

v1, = st.tabs (['Visão Restaurante'])


with st.container():
    
   esc, meio , dire = st.columns(3)
    
   with esc : 
       st. markdown('Entregadores')
       with st.container():
        v1,v2  = st.columns(2)
       with v1 : 
           df['Delivery_person_ID'] = df['Delivery_person_ID'].str.strip()
           entregadores = df['Delivery_person_ID'].nunique()
           v1.metric('Quantidade', entregadores )
       with v2 : 
          
           distancia = ((df.apply(lambda x:
                           haversine((x['Restaurant_latitude']	,
                                      x['Restaurant_longitude'] ),
                                       ( x['Delivery_location_latitude'],
                                      x['Delivery_location_longitude'])),axis =1)
                         .reset_index()
                         .mean()))
# para arredondar comm 2 casa decimais e selecionar apenas o indice [0]
           dist = distancia.round(2)[0] 
           v2.metric('distancia KH ', dist)
           
   with meio : 
        st. markdown(' Festival_Yes ')
        v1,v2  = st.columns (2)
       
      
        with v1: 
            
            df['Time_taken(min)'] = df['Time_taken(min)'].astype(str)
            df['Time_taken(min)'] = df['Time_taken(min)'].str.strip()
            df['Time_taken(min)'] = df['Time_taken(min)'].str.replace('(min)','')
            df['Time_taken(min)'] = df['Time_taken(min)'].astype(float)
            df.dropna(subset='Time_taken(min)' ,inplace=True)
            festiva = (df.loc[(df['Festival']== 'Yes ') & (df['Road_traffic_density']!= 'NaN') ]
             .groupby('Festival')['Time_taken(min)']
             .mean().reset_index().round(2))
            gb = festiva.iloc[0, 1]
            v1.metric('Tempo ( Min ) ', gb)
            
        with v2 :
            df['Time_taken(min)'] = df['Time_taken(min)'].astype(str)
            df['Time_taken(min)'] = df['Time_taken(min)'].str.strip()
            df['Time_taken(min)'] = df['Time_taken(min)'].str.replace('(min)','')
            df['Time_taken(min)'] = df['Time_taken(min)'].astype(float)
            df.dropna(subset='Time_taken(min)' ,inplace=True)
            festiva = (df.loc[(df['Festival']== 'Yes ') & (df['Road_traffic_density']!= 'NaN') ]
             .groupby('Festival')['Time_taken(min)']
             .std().reset_index().round(2))
            gb = festiva.iloc[0, 1]
            v2.metric('Desvio pd', gb)
            
        with dire: 
            st.markdown ('Festival_No')
            v1, v2 = st.columns(2)
          
            with v1:
                            
                    df['Time_taken(min)'] = df['Time_taken(min)'].astype(str)
                    df['Time_taken(min)'] = df['Time_taken(min)'].str.strip()
                    df['Time_taken(min)'] = df['Time_taken(min)'].str.replace('(min)','')
                    df['Time_taken(min)'] = df['Time_taken(min)'].astype(float)
                    df.dropna(subset='Time_taken(min)' ,inplace=True)
                    festiva = (df.loc[(df['Festival']== 'No ') & (df['Road_traffic_density']!= 'NaN') ]
                     .groupby('Festival')['Time_taken(min)']
                     .mean().reset_index().round(2))
                    gb = festiva.iloc[0, 1]
                    v1.metric('Tempo ( Min ) ', gb)
                
            with v2:
                
                df['Time_taken(min)'] = df['Time_taken(min)'].astype(str)
                df['Time_taken(min)'] = df['Time_taken(min)'].str.strip()
                df['Time_taken(min)'] = df['Time_taken(min)'].str.replace('(min)','')
                df['Time_taken(min)'] = df['Time_taken(min)'].astype(float)
                df.dropna(subset='Time_taken(min)' ,inplace=True)
                festiva = (df.loc[(df['Festival']== 'No ') & (df['Road_traffic_density']!= 'NaN') ]
                 .groupby('Festival')['Time_taken(min)']
                 .std().reset_index().round(2))
                gb = festiva.iloc[0, 1]
                v2.metric('Desvio pd', gb)
                  
with st.container() :               
    st.markdown('''---''') 
    st.markdown(' ## Distância Média da Comida do Restaurante até a Casa do Cliente por Cidade')
    df= df.loc[(df['City']!= 'NaN ') ]
    df['distance'] = df.apply(lambda x:                               haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), 
(x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1) #
    avg_distancia_per_city = df.groupby('City')['distance'].mean().reset_index() 
    avg_distancia_per_city = avg_distancia_per_city.dropna(subset=['City'])
    
    
    fig = px.pie( 
        avg_distancia_per_city,
        names='City',
        values='distance',
        
    )
    
    
    pull_values = [0] * len(avg_distancia_per_city) 
    if len(pull_values) > 1: 
        pull_values[2] = 0.2 
    
    
    fig.update_traces(pull=pull_values) 


    st.plotly_chart(fig) 
                  
with st.container() :               
    st.markdown('''---''') 
    st.markdown(' ##  Distribuição do Tempo de Entrega por Cidade') 
    df.dropna(subset='Time_taken(min)' ,inplace=True)
    df.loc[(df['City']!= 'NaN') ].groupby('City')['Time_taken(min)'].agg(media = 'mean', desvpd = 'std').reset_index().round(2)
    fig = px.box(
    df.loc[(df['City'] != 'NaN ')], # Filtra o DataFrame para incluir apenas as linhas onde a coluna 'City' não é 'NaN'.
    x='City', # Define a coluna 'City' para o eixo X, representando as categorias (cidades).
    y='Time_taken(min)', # Define a coluna 'Time_taken(min)' para o eixo Y, representando os valores numéricos cuja distribuição será analisada.
    
    labels={'City': 'Cidade', 'Time_taken(min)': 'Tempo de Entrega (min)'} # Define os rótulos dos eixos para melhor clareza.
)




# 3. Exibe o gráfico.
    st.plotly_chart(fig)
       
with st.container ():   
    st.markdown('''---''') 
    st.markdown(' ##  O tempo médio e o desvio padrão de entrega por cidade e tipo de pedido') 
    
    tabela  = (df.loc[(df['City']!= 'NaN ') ].
         groupby(['City', 'Type_of_order'])['Time_taken(min)']
         .agg(media_min = 'mean', desvpd_mim = 'std').reset_index().round(2).rename(columns={
                  'City': 'Cidade', 
                  'Type_of_order': 'Tipo de Pedido',
                  'media_min': 'Média de Tempo',
                  'desvpd_mim': 'Desvio Padrão'
              }))
    st.dataframe(tabela, hide_index= True  )
with st.container ():   
    st.markdown('''---''') 
    st.markdown(' ##  O tempo médio e o desvio padrão de entrega por cidade e tipo de pedido') 
  
    df_aux = (df.groupby(['City', 'Road_traffic_density'])['Time_taken(min)'] 
                .agg(media_min='mean', desvpd_min='std') 
                .reset_index()) 
    
    
    gb =px.sunburst( 
        df_aux, 
        path=['City', 'Road_traffic_density'], 
        values='media_min',                     
        color='desvpd_min',                      
        color_continuous_scale='RdBu', 
        color_continuous_midpoint=np.average(df_aux['desvpd_min']) )

    # 3. Mostrar o gráfico
    st.plotly_chart(gb)
            