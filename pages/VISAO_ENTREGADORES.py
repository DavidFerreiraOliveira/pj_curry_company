import streamlit as st 
#====================================
# importaçao de bibliotecaas 
#====================================
import pandas as pd


# bibliotea utilizada para adiçao de imagens 
from PIL import Image as im
st.set_page_config(layout = 'wide')

df = pd.read_csv('treino.csv')


#====================================
# Criaçao de abas e estruturaçao da pagina 
#====================================

# funçao serve ára criar titulos
st.header('Visão Entregadores')

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

v1 = st.tabs (['Visão Restaurante'])

#====================================
# IDADES DOS ENTREGADORES   
#====================================


with st.container():
    # Criamos duas colunas principais (uma para Idade, outra para Veículo)
    col_esquerda, col_direita = st.columns(2)

    with col_esquerda:
        st.markdown("Idades dos Entregadores", unsafe_allow_html=True)
        # Criamos sub-colunas dentro da coluna da esquerda
        v1, v2 = st.columns(2)
        
        df['Delivery_person_Age'] = df['Delivery_person_Age'].str.strip()
        idades = df.loc[df['Delivery_person_Age'] != 'NaN', 'Delivery_person_Age'].astype(int)
        
        v1.metric('Mínima', idades.min())
        v2.metric('Máxima', idades.max())

    with col_direita:
        st.markdown('Condição do Veículo', unsafe_allow_html=True)
        # Criamos sub-colunas dentro da coluna da direita
        v3, v4 = st.columns(2)
        
        veiculo = df.loc[df['Vehicle_condition'] != 'NaN', 'Vehicle_condition'].astype(int)
        
        v3.metric('Pior', veiculo.min())
        v4.metric('Melhor', veiculo.max())
     

st.markdown('''---''')
                
#====================================
# MEDIA DE AVALIAÇÃO POR ENTREGADOR   
#====================================


with st.container():
     v1,v2= st.columns(2, gap='large' )
     st.markdown('''---''')        
     with v1:
        st.markdown('Média de avaliações por Entregador')
         
        df['ID Entregadores Unicos'] = df['Delivery_person_ID']
        df['Media de Avaliçoes'] = df['Delivery_person_Ratings'].astype(float)
        avaliaçoes = df.dropna(subset='Media de Avaliçoes',inplace=True)
        avaliaçoes = df.groupby('ID Entregadores Unicos')['Media de Avaliçoes'].mean().reset_index().round(2)
        st.dataframe(avaliaçoes, hide_index= True,)
         
         
        with v2 :
            st.markdown('A avaliação média e o desvio padrão por condições climáticas')
            
            df['Delivery_person_Ratings'] = pd.to_numeric(df['Delivery_person_Ratings'], errors='coerce')     
            df['Weatherconditions'] = df['Weatherconditions'].str.strip()
            df['Condições de Tempo' ] = df['Weatherconditions'] 
            avm = (df.loc[df['Condições de Tempo' ] != 'conditions NaN']
                   .groupby('Condições de Tempo' )['Delivery_person_Ratings']
                   .agg( Média = 'mean', Despd = 'std')
                   .reset_index() 
                   .round(2)) 
            st.dataframe(avm, hide_index= True )
            
            st.markdown('A avaliação média e o desvio padrão por tipo de tráfego')
            
            df['Road_traffic_density'] = df['Road_traffic_density'].str.strip()
            avaliaçoes = (df.loc[df['Road_traffic_density'] !='NaN']
                          .groupby('Road_traffic_density')['Delivery_person_Ratings']
                          .agg( media = 'mean', despd = 'std').reset_index()).round(2)
            st.dataframe(avaliaçoes, hide_index= True )

with st.container(width = 800):
            st.markdown( 'Os 10 entregadores mais rápidos por cidade')

            df['Time_taken(min)'] = df['Time_taken(min)'].astype(str)
            df['Time_taken(min)'] = df['Time_taken(min)'].str.strip()
            df['Time_taken(min)'] = df['Time_taken(min)'].str.replace('(min)','')
            df['Time_taken(min)'] = df['Time_taken(min)'].astype(float)
            df.dropna(subset='Time_taken(min)' ,inplace=True)
            fgh = (df.loc[(df['Time_taken(min)'].notna()) & 
    (df['City']!= 'NaN ') ,['City', 'Delivery_person_ID','Time_taken(min)']].groupby(['City', 'Delivery_person_ID'])['Time_taken(min)'].sum().reset_index())
            # Note: The output from the last execution of this cell suggests that 'NaN ' might not be the only non-numeric value or that there are issues with the `astype(float)` if it was not assigned back. I've corrected the assignment. Also, 'NaN ' in the original condition might need to be `df['Time_taken(min)'].notna()` if the column is already float.
            fg = fgh.sort_values(['City','Time_taken(min)']).groupby('City').head(10) 
            fg.columns = [ 'Cidades' , 'ID Entregadores', 'Tempo']    
            st.dataframe(fg , hide_index= True )
