from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime


# Crear el DAG
with DAG(
    dag_id='test_dbt_bash_operator',
    schedule_interval='@daily',
    catchup=False,
    start_date= datetime(2024, 10, 23),
    tags=['dbt', 'bash_operator'],
) as dag:


    # Tarea que ejecuta dbt run para ejecutar el modelo
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='dbt run --profiles-dir /home/airflow/.dbt --project-dir /opt/airflow',
    )

    # Definir el flujo de las tareas
    dbt_run
