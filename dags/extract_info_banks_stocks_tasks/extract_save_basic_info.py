import yfinance as yf
from datetime import datetime
import pandas as pd
from extract_info_banks_stocks_tasks.save_to_db import save_to_db

def get_basic_info(engine, data):
    basic_info_list = []
    df = pd.read_json(data, orient='records')

    for symbol in df['symbol']:
        stock = yf.Ticker(symbol)
        basic_info_list.append( get_banks_info(stock) )

    basic_info_df = pd.DataFrame(basic_info_list)
    save_to_db(engine, basic_info_df, table_name="bank_basic_info", if_exists='replace')

def get_banks_info(ticker):
    info = ticker.info
    return {
        'symbol': ticker.ticker,
        'company_name': info.get('longName'),
        'industry': info.get('industry'),
        'sector': info.get('sector'),
        'employee_count': info.get('fullTimeEmployees'),
        'city': info.get('city'),
        'phone': info.get('phone'),
        'state': info.get('state'),
        'country': info.get('country'),
        'website': info.get('website'),
        'address': info.get('address1')
    }