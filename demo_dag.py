from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'lhogeshwaran',
    'depends_on_past': False,
    'email': ['lhogeshwaran@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'kpmg',
    default_args=default_args,
    description='An oversimplified replica of project for UTS PQU',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(0),
    tags=['example']
)

prepare_csvs_script = '/Users/loki/UTS_MDSI/code_practices/loki_kpmg/data_check.sh'
t1 = BashOperator(
    task_id='prepare_csvs',
    bash_command=prepare_csvs_script,
    dag=dag
)
