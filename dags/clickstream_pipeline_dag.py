from datetime import datetime, timedelta
import sys
import os
from airflow import DAG
from airflow.operators.python import PythonOperator

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from api_ingestion import run_stream_ingestion

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

def stream_task():
    # Ingests 50 records per batch run
    run_stream_ingestion(max_events=50)

with DAG(
    dag_id="clickstream_wikimedia_pipeline",
    default_args=default_args,
    description="Wikimedia clickstream ETL pipeline",
    schedule_interval=timedelta(minutes=5),
    catchup=False,
) as dag:

    run_etl = PythonOperator(
        task_id="ingest_and_transform_stream",
        python_callable=stream_task,
    )

    run_etl