from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd

def save_to_db(engine, data, table_name, if_exists='append'):
    engine = create_engine(engine)
    
    data['created_at'] = datetime.now()
    data['updated_at'] = datetime.now()
    data.columns = data.columns.str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

    data.to_sql(table_name, con=engine, if_exists=if_exists, index=False)