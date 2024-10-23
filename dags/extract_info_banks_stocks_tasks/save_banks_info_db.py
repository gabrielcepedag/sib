import pandas as pd
from sqlalchemy import create_engine

def save_bank_stocks_to_db(engine, data):
    # Deserializar el JSON a DataFrame
    df = pd.read_json(data, orient='records')
    engine = create_engine(engine)

    # Guardar los datos en PostgreSQL
    df.to_sql('banks_stocks', con=engine, if_exists='replace', index=False)
