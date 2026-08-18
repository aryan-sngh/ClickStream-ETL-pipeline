# import os
# import sys
# from datetime import datetime, timedelta
# from airflow import DAG
# from airflow.operators.python import PythonOperator

# # Ensure the root project folder is on Python's path
# PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# if PROJECT_DIR not in sys.path:
#     sys.path.insert(0, PROJECT_DIR)

# from api_ingestion import run_stream_ingestion

# default_args = {
#     "owner": "airflow",
#     "depends_on_past": False,
#     "start_date": datetime(2026, 1, 1),
#     "email_on_failure": False,
#     "email_on_retry": False,
#     "retries": 2,
#     "retry_delay": timedelta(minutes=1),
# }

# def stream_task(**kwargs):
#     """
#     Airflow task callable: runs a bounded batch ingestion
#     of 50 events per scheduled run.
#     """
#     batch_size = 50
#     print(f"Starting clickstream stream ingestion batch (size={batch_size})...")
#     run_stream_ingestion(max_events=batch_size)
#     print("Clickstream stream ingestion batch completed successfully.")

# with DAG(
#     dag_id="clickstream_wikimedia_pipeline",
#     default_args=default_args,
#     description="Batch-stream ingestion of Wikimedia clickstream events into MySQL",
#     schedule_interval=timedelta(minutes=5),
#     catchup=False,
#     max_active_runs=1,
# ) as dag:

#     ingest_task = PythonOperator(
#         task_id="ingest_and_load_wikimedia_stream",
#         python_callable=stream_task,
#         provide_context=True,
#     )

#     ingest_task


# import os
# import sys
# from datetime import datetime, timedelta
# from airflow import DAG
# from airflow.providers.standard.operators.python import PythonOperator

# # Ensure project root is in sys.path
# PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# if PROJECT_DIR not in sys.path:
#     sys.path.insert(0, PROJECT_DIR)

# from api_ingestion import run_stream_ingestion

# default_args = {
#     "owner": "airflow",
#     "depends_on_past": False,
#     "start_date": datetime(2026, 1, 1),
#     "email_on_failure": False,
#     "email_on_retry": False,
#     "retries": 1,
#     "retry_delay": timedelta(minutes=1),
# }

# def stream_task(**kwargs):
#     print("Starting clickstream ingestion batch (50 events)...")
#     run_stream_ingestion(max_events=50)
#     print("Ingestion batch completed successfully.")

# with DAG(
#     dag_id="clickstream_wikimedia_pipeline",
#     default_args=default_args,
#     description="Wikimedia clickstream ingestion into MySQL",
#     schedule=timedelta(minutes=5),  # 'schedule' replaces 'schedule_interval' in Airflow 3
#     catchup=False,
#     max_active_runs=1,
# ) as dag:

#     ingest_task = PythonOperator(
#         task_id="ingest_and_load_wikimedia_stream",
#         python_callable=stream_task,
#     )

#     ingest_task



import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------
# 1. Resolve & add Project Root to sys.path
# ---------------------------------------------------------
PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ---------------------------------------------------------
# 2. Imports after path configuration
# ---------------------------------------------------------
from airflow import DAG

# Airflow 3 uses standard provider for PythonOperator; fallback to core if needed
try:
    from airflow.providers.standard.operators.python import PythonOperator
except ImportError:
    from airflow.operators.python import PythonOperator

from api_ingestion import run_stream_ingestion


# ---------------------------------------------------------
# 3. Default DAG Arguments
# ---------------------------------------------------------
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}


# ---------------------------------------------------------
# 4. Task Callable
# ---------------------------------------------------------
def execute_stream_ingestion(**kwargs):
    """
    Airflow task execution: streams a bounded batch of 50
    Wikimedia clickstream events and commits them into MySQL.
    """
    batch_size = 50
    print(f"Starting clickstream ingestion batch (limit={batch_size} events)...")
    run_stream_ingestion(max_events=batch_size)
    print("Clickstream ingestion batch processed and committed successfully.")


# ---------------------------------------------------------
# 5. DAG Definition
# ---------------------------------------------------------
with DAG(
    dag_id="clickstream_wikimedia_pipeline",
    default_args=default_args,
    description="Stream Wikimedia clickstream edits into MySQL via scheduled micro-batches",
    schedule=timedelta(minutes=5),
    catchup=False,
    max_active_runs=1,
    tags=["clickstream", "wikimedia", "etl"],
) as dag:

    ingest_clickstream_events = PythonOperator(
        task_id="ingest_and_load_wikimedia_stream",
        python_callable=execute_stream_ingestion,
    )

    ingest_clickstream_events