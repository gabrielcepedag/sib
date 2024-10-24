from datetime import datetime
from airflow.operators.python import PythonOperator
from extract_info_banks_stocks_tasks.scraping_banks_info import extract_bank_and_financial_services_stocks
from extract_info_banks_stocks_tasks.extract_save_basic_info import get_basic_info
from extract_info_banks_stocks_tasks.extract_save_fundamentals_info import get_fundamentals_info
from extract_info_banks_stocks_tasks.extract_save_price_stock import get_price_info
from extract_info_banks_stocks_tasks.extract_save_holders_info import get_holders_info
from extract_info_banks_stocks_tasks.extract_save_calificadores_info import get_calificadores_info
import os
from airflow.decorators import dag
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from cosmos import DbtDag, ProjectConfig, ProfileConfig
from cosmos.profiles import ClickhouseUserPasswordProfileMapping

# Obtener las variables de entorno
password_ch = os.getenv("CLICKHOUSE_PASSWORD", "default") 
port_ch = int(os.getenv("CLICKHOUSE_TCP_PORT", 9000))
host = os.getenv("DB_HOST", "postgres-db")         
database = os.getenv("POSTGRES_DB", "landing_zone")      
user = os.getenv("POSTGRES_USER", "sib_user")        
password_pg = os.getenv("POSTGRES_PASSWORD", "sib_user") 
port = os.getenv("POSTGRES_PORT", 5432)        
AIRBYTE_CONN_ID=os.getenv("AIRBYTE_CONNECTION_ID", "8bf4a1bc-7071-4b67-8d55-4b5be1484508")
ENGINE_DB = f'postgresql://{user}:{password_pg}@{host}:{port}/{database}'

# Definir el DAG
@dag(
    'extract_info_banks_stocks',
    description='DAG para buscar la información de los stocks de los bancos que cotizan en la bolsa de USA',
    schedule_interval=None,
    start_date=datetime(2024, 10, 1),
    catchup=False,
)
def extract_info_banks_stocks():

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

    # Tarea 7: Ejecutar JOB de Airbyte que envia lo cargado en postgresql a clickhouse
    send_to_datawarehouse = AirbyteTriggerSyncOperator(
        task_id='send_to_datawarehouse',
        airbyte_conn_id='airbyte_conn_id',
        connection_id=AIRBYTE_CONN_ID,
        asynchronous=False,
        timeout=900,
        wait_seconds=3
    )

    trigger_execute_dbt_jobs = TriggerDagRunOperator(
        task_id='trigger_execute_dbt_jobs',
        trigger_dag_id='execute_dbt_jobs',
        trigger_rule='all_success',
        wait_for_completion=True,
    )

    extract_banks_task >> [
                        extract_save_basic_stocks_info, 
                        extract_save_fundamentals_stocks_info,
                        extract_save_price_stocks_info,
                        extract_save_holders_info,
                        extract_save_calificadores_info
    ] >> send_to_datawarehouse >> trigger_execute_dbt_jobs

extract = extract_info_banks_stocks()

execute_dbt_jobs = DbtDag(
    dag_id="execute_dbt_jobs",
    project_config=ProjectConfig(
        "/home/dbt"
    ),
    profile_config=ProfileConfig(
        profile_name="dbt_project",
        target_name="dev",
        profile_mapping=ClickhouseUserPasswordProfileMapping(
            conn_id="clickhouse_conn_id",
            profile_args={
                "host": "clickhouse",
                "user": "default",
                "port": port_ch,
                "password" : password_ch,
                "clickhouse": True
            }
        ),
    ),
    operator_args={
        "install_deps": True,  
        "full_refresh": True, 
    },
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={"retries": 2},
)

execute_dbt_jobs