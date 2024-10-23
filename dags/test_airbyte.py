
from datetime import datetime
from airflow import DAG
from cosmos import DbtDag, ProjectConfig, ProfileConfig
from cosmos.profiles import ClickhouseUserPasswordProfileMapping

import os
password = os.getenv("CLICKHOUSE_PASSWORD", "password") 
port = int(os.getenv("CLICKHOUSE_TCP_PORT", 8000))
# Definir el DAG
with DAG(
    'test_airbyte',
    description='Dag de prueba',
    schedule_interval=None,
    start_date=datetime(2024, 10, 1),
    catchup=False,
) as dag:
    
    dbt_run = DbtDag(
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
                    "port": port,
                    "password" : password,
                    "clickhouse": True
                }
            ),
        ),
        operator_args={
            "install_deps": True,  
            "full_refresh": True, 
        },
        # normal dag parameters
        start_date=datetime(2024, 1, 1),
        catchup=False,
        dag_id="dbt_run",
        default_args={"retries": 2},
    )