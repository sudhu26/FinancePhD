
import pandas as pd
import seaborn as sns
from pymongo import MongoClient
from datetime import datetime
from arctic import Arctic
from pandas_highcharts.core import serialize



def equity_markets_charts(div):
    store = Arctic('localhost')
    store.initialize_library('FUTURES')
    library = store['FUTURES']
    key_markets=['FTSE 100','S&P 500','Russell 2000','EuroStoxx 50']
    df=pd.DataFrame()
    for mkt in key_markets:
        try:
            df[mkt]=library.read(mkt).data.Price
        except:
            print mkt        
    data=df.ffill()['2016-6-30':]/df.ffill()['2016-6-30':].ix[0]
    return serialize(data,render_to=div,title='Equities YTD',output_type='json')

def zscore_ranked(div):
    store = Arctic('localhost')
    store.initialize_library('FUTURES')
    library = store['FUTURES']
    data=pd.DataFrame()
    for mkt in library.list_symbols():
        try:
            data[mkt]=library.read(mkt).data.Price
        except:
            print mkt
    zscores=(data-pd.ewma(data,20))/pd.ewmstd(data,20)
    latest=zscores.tail(2)
    zscore_ranked=latest.T.sort_values(by=latest.T.columns[0]).dropna()[:2]
    zscore_ranked=zscore_ranked.append(latest.T.sort_values(by=latest.T.columns[0]).dropna()[-2:])
    return serialize(zscore_ranked, kind="bar",render_to=div, title="Noteable market moves")
