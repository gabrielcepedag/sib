import yfinance as yf
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
from sqlalchemy import create_engine
from extract_info_banks_stocks_tasks.save_to_db import save_to_db

def extract_bank_and_financial_services_stocks(engine):

    urlBankStocks = 'https://finance.yahoo.com/u/yahoo-finance/watchlists/bank-and-financial-services-stocks/'
    headersRequest = {
        'User-Agent': 'Safari'
    }

    response = requests.get(urlBankStocks, headers=headersRequest)
    response.raise_for_status() 

    soup = BeautifulSoup(response.content, 'html.parser')
    section = soup.find('section', {'data-test': 'cwl-symbols'})
    table = section.find('table')

    headers = [th.get_text() for th in table.find_all('th')]
    rows = []
    for tr in table.find_all('tr')[1:]: 
        cells = tr.find_all('td')
        row = [cell.get_text(strip=True) for cell in cells]
        rows.append(row)

    df = pd.DataFrame(rows, columns=headers)
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

    save_to_db(engine, df, "bank_basic_info", if_exists="replace")

    return df.to_json(orient='records')