import pandas as pd
import os
from Quandl import Quandl
import time


auth_tok = "fTx5CNFXPPxrBePMiz7k"

##data = Quandl.get("WIKI/KO", trim_start = "2000-12-12",trim_end = "2014-12-30", authtoken= auth_tok)
##
##print(data)

path = "C:\\intraQuarter"

def Stock_Prices():
    df = pd.DataFrame()
    statspath = path+'\\_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    

    for each_dir in stock_list[1:]:
        try:
            ticker = each_dir.split("\\")[-1]
            print(ticker)
            name = "WIKI/"+ ticker.upper()
            data = Quandl.get(name, trim_start = "2000-12-12",trim_end = "2014-12-30", authtoken= auth_tok)
            data[ticker.upper()] = data["Adj. Close"]
            df= pd.concat([df, data[ticker.upper()]], axis = 1)
        except Exception as e:
            print(str(e))
            time.sleep(10)
            try:
                ticker = each_dir.split("\\")[-1]
                print(ticker)
                name = "WIKI/"+ ticker.upper()
                data = Quandl.get(name, trim_start = "2000-12-12",trim_end = "2014-12-30", authtoken= auth_tok)
                data[ticker.upper()] = data["Adj. Close"]
                df= pd.concat([df, data[ticker.upper()]], axis = 1)
            except Exception as e:
                print(str(e))

    df.to_csv("stock_prices.csv")
            
Stock_Prices()
