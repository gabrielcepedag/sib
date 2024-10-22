from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from extract_info_banks_stocks_tasks.scraping_banks_info import extract_bank_and_financial_services_stocks
from extract_info_banks_stocks_tasks.save_banks_info_db import save_bank_stocks_to_db
# from extract_info_banks_stocks_tasks.scraping_banks_stocks import get_banks_stocks
# from extract_info_banks_stocks_tasks.save_stocks_info import save_stocks_info_to_db
from extract_info_banks_stocks_tasks.extract_save_basic_info import get_basic_info
from extract_info_banks_stocks_tasks.extract_save_fundamentals_info import get_fundamentals_info
from extract_info_banks_stocks_tasks.extract_save_price_stock import get_price_info
from extract_info_banks_stocks_tasks.extract_save_holders_info import get_holders_info
from extract_info_banks_stocks_tasks.extract_save_calificadores_info import get_calificadores_info
import os

host = os.getenv("DB_HOST", "postgres-db")         
database = os.getenv("POSTGRES_DB2", "landing_zone")      
user = os.getenv("POSTGRES_USER", "sib_user")        
password = os.getenv("POSTGRES_PASSWORD", "sib_user") 
port = os.getenv("POSTGRES_PORT", "5432")        
ENGINE_DB = f'postgresql://{user}:{password}@{host}:{port}/{database}'

# Definir el DAG
with DAG(
    'extract_info_banks_stocks',
    description='DAG para buscar la información de los stocks de los bancos que cotizan en la bolsa de USA',
    schedule_interval=None,
    start_date=datetime(2024, 10, 1),
    catchup=False,
) as dag:

    # Tarea 1: Extraer información de los bancos
    extract_banks_task = PythonOperator(
        task_id='extract_bank_stocks',
        python_callable=extract_bank_and_financial_services_stocks,
        op_kwargs={
            'engine': ENGINE_DB
        },
        provide_context=True,
    )

    # Tarea 2: Recopilar y guardar las informaciones básicas de los stocks de los bancos
    extract_save_basic_stocks_info = PythonOperator(
        task_id='extract_save_stocks_info',
        python_callable=get_basic_info,
        op_kwargs={
            'engine': ENGINE_DB,
            'data': "{{ ti.xcom_pull(task_ids='extract_bank_stocks') }}"
        },
        provide_context=True,
    )

    # Tarea 3: Recopilar y guardar las informaciones de fundamentales de los stocks de los bancos
    extract_save_fundamentals_stocks_info = PythonOperator(
        task_id='extract_save_fundamentals_info',
        python_callable=get_fundamentals_info,
        op_kwargs={
            'engine': ENGINE_DB,
            'data': "{{ ti.xcom_pull(task_ids='extract_bank_stocks') }}"
        },
        provide_context=True,
    )

    # Tarea 4: Recopilar y guardar las informaciones de fundamentales de los stocks de los bancos
    extract_save_price_stocks_info = PythonOperator(
        task_id='extract_save_price_info',
        python_callable=get_price_info,
        op_kwargs={
            'engine': ENGINE_DB,
            'data': "{{ ti.xcom_pull(task_ids='extract_bank_stocks') }}"
        },
        provide_context=True,
    )

    # Tarea 5: Recopilar y guardar las informaciones de holders de los stocks de los bancos
    extract_save_holders_info = PythonOperator(
        task_id='extract_save_holders_info',
        python_callable=get_holders_info,
        op_kwargs={
            'engine': ENGINE_DB,
            'data': "{{ ti.xcom_pull(task_ids='extract_bank_stocks') }}"
        },
        provide_context=True,
    )

    # Tarea 6: Recopilar y guardar las informaciones de calificadores de los stocks de los bancos
    extract_save_calificadores_info = PythonOperator(
        task_id='extract_save_calificadores_info',
        python_callable=get_calificadores_info,
        op_kwargs={
            'engine': ENGINE_DB,
            'data': "{{ ti.xcom_pull(task_ids='extract_bank_stocks') }}"
        },
        provide_context=True,
    )

    extract_banks_task >> [extract_save_basic_stocks_info, extract_save_fundamentals_stocks_info, extract_save_price_stocks_info, extract_save_holders_info, extract_save_calificadores_info]
