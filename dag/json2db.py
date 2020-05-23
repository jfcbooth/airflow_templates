"""
Takes json file and exports it to DB
"""

import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
#import sys
#sys.path.insert(0, '../dag_dependencies')
#for p in sys.path:
#    print(p)
#from dag_dependencies.file_transforms import json2csv
from file_transforms import json2csv

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,  # stops task from triggering if previous schedule for the task hasn't succeeded
    'start_date': days_ago(2),  # how many days in the past the DAG should run when first uploaded
    'email': ['boothjmail@gmail.com'],
    'email_on_failure': True,  # emails after failing 'retries' time
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': datetime.timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime.datetime(2016, 1, 1),  # last day the DAG can execute
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

dag = DAG(
    'json2db',  # name of the DAG
    default_args=default_args,
    #catchup=False,
    description='Takes .json file and exports it to DB',
    schedule_interval=datetime.timedelta(days=1),  # How often the DAG should run.
)

# Define tasks in the DAG below


t1 = PythonOperator(
    task_id='convert_json_to_csv',  # task name
    python_callable=json2csv,
    op_kwargs={'input': '/home/boothm/airflow/dag_dependencies/data.nljson', 'output': '/home/boothm/airflow/dag_dependencies/data.csv'},
    dag=dag
)

t2 = DummyOperator(task_id='dummy_task', dag=dag)

t2 >> t1
