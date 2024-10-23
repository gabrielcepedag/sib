import yfinance as yf
import pandas as pd
from extract_info_banks_stocks_tasks.save_to_db import save_to_db


def get_holders_info(engine, data):
    holders_dfs = []
    df = pd.read_json(data, orient='records')

    for symbol in df['symbol']:
        stock = yf.Ticker(symbol)
        holders_dfs.append( get_shares_holders_info(stock) )

    all_holders_data = pd.concat(holders_dfs, ignore_index=True)
    save_to_db(engine, all_holders_data, table_name="stock_holders", if_exists='append')

def get_shares_holders_info(ticker):

    try:
        holders = ticker.institutional_holders[['Date Reported', 'Holder', 'Shares', 'Value']]
        holders['symbol'] = ticker.ticker
        return holders
    except Exception as e:
        print(f"Error getting holders for {ticker.ticker}: {str(e)}")\
       
    
    