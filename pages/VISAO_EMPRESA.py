import streamlit as st 

#====================================
# importaçao de bibliotecaas 
#====================================
import plotly.express as px
import pandas as pd 

from streamlit_folium import folium_static 
import folium as fl
# bibliotea utilizada para adiçao de imagens 
from PIL import Image as im
st.set_page_config(layout ='wide')
df = pd.read_csv('treino.csv')


 
#====================================
# Criaçao de abas e estruturaçao da pagina 
#====================================

# funçao serve ára criar titulos
st.header('Visão Empresa')

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
df['Road_traffic_density'] = df.loc[df['Road_traffic_density']!= 'NaN ','Road_traffic_density']

# filtro para multiplas condiçoes 
cond = st.sidebar.multiselect( 'Condiçao do Veiculo ', df['Road_traffic_density'].unique() ,default = df['Road_traffic_density'].unique())


st.sidebar.markdown('''------''')


st.sidebar.markdown('# Criado Por:')

st.sidebar.markdown('### David Ferreira De Oliveira')


# para que o fliltro de linha temporal seja aplicado nos graficos

## transforma a coluna do date frame em data
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
# cria uma variavel que recebe a condiçao para o filtro ser aplicado
var = df['Order_Date'].dt.date < date  
# usar a varivel( var ) para que o filtro funcione linha a linha 
df = df.loc[var, :]

# visualzar o grafico co o filro aplicado 


# para que os fltro do tipo selecionavel seja aplicado nos graficos 
var1 = df['Road_traffic_density'].isin (cond)
df = df.loc[var1,:]

# criar abas 

v1, v2 , v7 = st.tabs (['Visão Gerencial', 'Visão Tatica', 'Visão Geofrafica', ])

#====================================
# VISÃO EMPRRESA  
#====================================


with st.container():
    with v1 :
        df['Order_Date'] = pd.to_datetime (df['Order_Date'])
        co =  df.groupby('Order_Date')['Order_Date'].count().reset_index(name='qtd.day')
        

        
    # cria grafico de linha
    
        linhas = px.bar(co, x='Order_Date', y='qtd.day')
        st.plotly_chart(linhas ,use_container_width = True)
        
        with st.container():    
            v1 , v4 = st.columns(2)

     # GRAFICO DE PIZZA        
            with v1 : 
                    df['Road_traffic_density'] = df['Road_traffic_density'].str.strip()
                    trafego = df.loc[df['Road_traffic_density'] != 'NaN'].groupby('Road_traffic_density')['ID'].count().reset_index(name = 'total').sort_values('total', ascending=False)
                    
                    # criar grafico de pizza 
                    pizza = px.pie(trafego,values='total', names= 'Road_traffic_density' )
                    st.plotly_chart(pizza ,use_container_width = True)
        # GRAFICO DE DISPERSÃO       
            with v4 :    
                    df['City'] = df['City'].str.strip()
                    trafego_city = df.loc[(df['Road_traffic_density'] != 'NaN') & (df['City'] != 'NaN')].groupby(['City','Road_traffic_density'])['ID'].count().reset_index(name='total2')
                # CRISR GRAFICO DE DISPERSÃO 
                    dispersao = px.scatter(trafego_city, x='City', y='Road_traffic_density', size='total2',color='Road_traffic_density')
                # CODIGO USADO PARA VISUALIZAR O CRAFICO CRIADO 
                    st.plotly_chart(dispersao ,use_container_width = True)

    with v2: 
        with st.container(): 
                    # aqui vc tranforma a coluna data de texto para data
            df['Order_Date'] = pd.to_datetime(df['Order_Date'])
            #aqui vc esta extraindo o dia da senmana
            df['Semana'] = df['Order_Date'].dt.strftime('%U')
            # df['semana'] = df['Order_Date'].dt.weekday
            # df['semana'] = df['Order_Date'].dt.day_of_week
            fg = df.groupby('Semana' )['ID'].count().reset_index(name='Quantidade de Pedidos')
            st.dataframe(fg, hide_index = True)
            # grafico de linhas
            linha = px.line(fg , x='Semana',y= 'Quantidade de Pedidos')
            st.plotly_chart(linha ,use_container_width = True)
    with v7: 
        with st.container():
            gh = (df.loc[(df['Road_traffic_density'] != 'NaN') & 
                  (df['City'] != 'NaN'),
['City','Road_traffic_density',
 'Delivery_location_latitude',
 'Delivery_location_longitude']]
                  .groupby(['City','Road_traffic_density'])          [['Delivery_location_latitude','Delivery_location_longitude']]
                  .median()
                  .reset_index())
            map = fl.Map()
            for index, location_info in gh.iterrows():
                    fl.Marker([location_info['Delivery_location_latitude'],
                     location_info['Delivery_location_longitude']]).add_to(map)
                   # JEITO CORRETO DE EXIBIR NO STREAMLIT
            folium_static(map, width=1024, height=600)
                    
                

                
      

        

