import yfinance as yf
import pandas as pd
from extract_info_banks_stocks_tasks.save_to_db import save_to_db

def get_calificadores_info(engine, data):
    calificadores_dfs = []
    df = pd.read_json(data, orient='records')

    for symbol in df['symbol']:
        stock = yf.Ticker(symbol)
        calificadores_dfs.append(get_calificadores(stock))

    calificadores_df = pd.concat(calificadores_dfs, ignore_index=True)
    save_to_db(engine, calificadores_df, table_name="stocks_calificadores", if_exists='append')

def get_calificadores(ticker,  start_year=2023, end_year=2024):
    data = ticker.upgrades_downgrades
    
    data.reset_index(inplace=True)

    data['GradeDate'] = pd.to_datetime(data['GradeDate'])
    data_filtered = data[
        (data['GradeDate'].dt.year >= start_year) &
        (data['GradeDate'].dt.year <= end_year)
    ].copy()
    
    data_filtered['symbol'] = ticker.ticker

    return data_filtered