import yfinance as yf
import pandas as pd
from extract_info_banks_stocks_tasks.save_to_db import save_to_db

def get_fundamentals_info(engine, data):
    fundamentals_dfs = []
    df = pd.read_json(data, orient='records')

    for symbol in df['symbol']:
        stock = yf.Ticker(symbol)
        fundamentals_dfs.append(get_fundamental_stock(stock))

    fundamentals_df = pd.DataFrame(fundamentals_dfs)
    save_to_db(engine, fundamentals_df, table_name="banks_fundamentals", if_exists='append')

def get_fundamental_stock(ticker):
    info = ticker.info

    total_assets = ticker.balance_sheet.loc['Total Assets'].iloc[0] if 'Total Assets' in ticker.balance_sheet.index else None
    invested_capital = ticker.balance_sheet.loc['Invested Capital'].iloc[0] if 'Invested Capital' in ticker.balance_sheet.index else None

    return {
        'symbol': ticker.ticker,
        'assets': total_assets,
        'debt': info.get('totalDebt'),
        'invested_capital': invested_capital,
        'shares_issued': info.get('sharesOutstanding')
    }