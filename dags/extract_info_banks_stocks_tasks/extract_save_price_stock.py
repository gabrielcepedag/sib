import yfinance as yf
import pandas as pd
from extract_info_banks_stocks_tasks.save_to_db import save_to_db

def get_price_info(engine, data):
    price_dfs = []
    df = pd.read_json(data, orient='records')

    for symbol in df['symbol']:
        stock = yf.Ticker(symbol)
        price_dfs.append(get_price_stock(stock))

    all_price_data = pd.concat(price_dfs, ignore_index=True)
    save_to_db(engine, all_price_data, table_name="daily_stocks_prices", if_exists='append')

def get_price_stock(ticker, interval='1d'):
    
    historical_data = ticker.history(period=interval)
    historical_data.reset_index(inplace=True)
    historical_data['symbol'] = ticker.ticker

    return historical_data