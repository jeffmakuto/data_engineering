"""Airflow DAG example to run scheduled extract from a library system API and load into ODS.
Replace connection IDs and endpoints with real values before deploying.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import requests
import psycopg2
import json

DEFAULT_ARGS = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

DAG_ID = 'library_api_to_ods'

def extract_library():
    # placeholder for API call
    resp = requests.get('https://library.example.edu/api/checkouts', params={'since': '2025-01-01'})
    resp.raise_for_status()
    return resp.json()


def load_to_ods(records_json):
    conn = psycopg2.connect(host='localhost', dbname='ods', user='ods_user', password='REPLACE')
    cur = conn.cursor()
    for r in records_json:
        cur.execute('''
        INSERT INTO canonical.library_record (record_id, borrower_id, borrower_type, item_id, checkout_date, due_date, returned_date, fines, source_systems)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (record_id) DO UPDATE SET
          borrower_id = EXCLUDED.borrower_id,
          borrower_type = EXCLUDED.borrower_type,
          item_id = EXCLUDED.item_id,
          checkout_date = EXCLUDED.checkout_date,
          due_date = EXCLUDED.due_date,
          returned_date = EXCLUDED.returned_date,
          fines = EXCLUDED.fines,
          source_systems = EXCLUDED.source_systems;
        ''', (
            r.get('record_id'), r.get('borrower_id'), r.get('borrower_type'), r.get('item_id'), r.get('checkout_date'), r.get('due_date'), r.get('returned_date'), r.get('fines'), json.dumps({'source': 'library_api'})
        ))
    conn.commit()
    cur.close()
    conn.close()

with DAG(DAG_ID, default_args=DEFAULT_ARGS, schedule_interval='@hourly', catchup=False) as dag:
    t1 = PythonOperator(task_id='extract_library', python_callable=extract_library)
    t2 = PythonOperator(task_id='load_to_ods', python_callable=lambda **ctx: load_to_ods(ctx['ti'].xcom_pull(task_ids='extract_library')))

    t1 >> t2
