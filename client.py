import  requests
import  streamlit as st 
import pandas as pd
class  STOCK_API:
    def __init__(self ):
        self.api_key  =  st.secrets['API_KEY']
        self.url  = "https://alpha-vantage.p.rapidapi.com/query"
        self.headers = {
	                "x-rapidapi-key": self.api_key,
	              "x-rapidapi-host": "alpha-vantage.p.rapidapi.com"
        }  



#  create method to fetcj company symbol
    def  search_symbol(self, keyword):
        querystring = {"datatype":"json",
                       "keywords":keyword,
                     "function":"SYMBOL_SEARCH"}
        response = requests.get(self.url,
                     headers=self.headers, 
                     params=querystring)
        data  = response.json()
        company_info  =  {}
        for  i  in  data['bestMatches']:
            symbol =  i['1. symbol'] 
            company_info[symbol] =  [i['2. name'] ,  i['4. region'] , i['8. currency']]
        return company_info



    #  fetch time  series daily data
    def  time_series_daily(self , symbol):
        querystring = {"function":"TIME_SERIES_DAILY",
        "symbol":symbol,
        "outputsize":"compact",
        "datatype":"json"}

        response = requests.get(self.url, 
        headers=self.headers, params=querystring)
        data2  = response.json()

        df  =  pd.DataFrame(data2['Time Series (Daily)'])
        df =  df.T

        #  change data type
        df =  df.astype('float')

        # change data type  of index

        df.index =  pd.to_datetime(df.index)

        # add name  to  index

        df.index.name= 'date'
        return  df

    #  plot candelstick chart
    def  plot(self , symbol ):
        df  =  self.time_series_daily(symbol)
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['1. open'],
                high=df['2. high'],
                low=df['3. low'],
                close=df['4. close'])])
        fig.update_layout(title =  'cadelstick chart' , 
        xaxis_title  =  'Date' ,
        yaxis_title  =  'Price' )
        return  fig



