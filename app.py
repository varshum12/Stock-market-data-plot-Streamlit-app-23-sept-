from  client import STOCK_API
import streamlit as st
import plotly.graph_objects as go


## add  page  title
st.set_page_config('Stock market  app deployment')

##  add  title
st.title('Stock market  candelstick  chart ploting')

st.subheader('By varsha Mhetre')

company =  st.text_input('Company Name')

@st.cache_resource(ttl  =  3600)
def fetch_data():
    return STOCK_API()

stock_api  =  fetch_data()


## create  function to search symbol
@st.cache_data(ttl  =  3600)
def get_symbol(company_name):
    return stock_api.search_symbol(company_name)





## create function  for  plot
@st.cache_data(ttl  =  3600)
def graph(symbol):
   df1  =  stock_api.time_series_daily(symbol)
   return stock_api.plot(df1)

## make  it functional 
if  company:
    company_data  =  get_symbol(company_name=company)
    if  company_data :
        company_symbols  =  list(company_data.keys())
        option  =  st.selectbox('Symbol' ,  company_symbols)
        company_name  =  st.success(f'**Company Name**, {company_data[option][0]}')
        company_region  =  st.success(f'**Company region**, {company_data[option][1]}')
        company_Currency  =  st.success(f'**Company Name**, {company_data[option][2]}')


        plot_graph  =  st.button('Plot' ,  type= 'primary')

        if  plot_graph:
            fig  =  graph(symbol =  option)
            st.plotly_chart(fig)
    else:
        st.warning('Company doesn"t  exists')



 