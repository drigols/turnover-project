###################################################################
# Rodrigo Leite - drigols                                         #
# Last update: 27/12/2021                                         #
###################################################################

from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.models import Variable
from airflow import DAG

from datetime import datetime,date, timedelta
from io import BytesIO

from sqlalchemy.engine import create_engine
from minio import Minio

import pandas as pd
import math


DEFAULT_ARGS = {
  'owner': 'Airflow',
  'depends_on_past': False,
  'start_date': datetime(2021, 1, 13),
}

dag = DAG(
  'etl_time_in_company_att', 
  default_args = DEFAULT_ARGS,
  schedule_interval = "@once"
)

data_lake_server = Variable.get("data_lake_server")
data_lake_login = Variable.get("data_lake_login")
data_lake_password = Variable.get("data_lake_password")

database_server = Variable.get("database_server")
database_login = Variable.get("database_login")
database_password = Variable.get("database_password")
database_name = Variable.get("database_name")


url_connection = "mysql+pymysql://{}:{}@{}/{}".format(
  str(database_login),
  str(database_password),
  str(database_server),
  str(database_name)
)

engine = create_engine(url_connection)

client = Minio(
  data_lake_server,
  access_key = data_lake_login,
  secret_key = data_lake_password,
  secure = False
)

def extract():

  # Query para consultar os dados.
  query = """SELECT hire_date
  FROM employees;"""

  df_ = pd.read_sql_query(query, engine)
  
  # Persiste os arquivos na Staging Area.
  df_.to_csv(
    "/tmp/time_in_company.csv",
    index=False
  )

def transform():

  # Carrega os dados a partir da área de staging.
  df_ = pd.read_csv("/tmp/time_in_company.csv")

  # Converte os dados para o formato datetime.
  df_["hire_date"] = pd.to_datetime(df_["hire_date"])

  # Define a data de referencia.
  date_referencia = date(2021, 1, 1)

  # Calcula a diferença de dias entre a data de contratação e a data de referencia.
  days_diff = []
  for d in df_["hire_date"]:
    diff = date_referencia - d.date()
    days_diff.append(diff.days)

  # Converte para o formato inteiro.
  nyears = []
  for ndays in days_diff:
    nyears.append(int(math.ceil(ndays / 365)))
  
  # Atribui os dados ao dataframe temporário.
  df_["time_in_company"] = nyears

  # Persiste os arquivos na área de Staging.
  df_["time_in_company"].to_csv(
    "/tmp/time_in_company.csv",
    index = False
  )
    
def load():

  # Carrega os dados a partir da área de staging.
  df_ = pd.read_csv("/tmp/time_in_company.csv")

  # Converte os dados para o formato parquet.    
  df_.to_parquet(
    "/tmp/time_in_company.parquet"
    ,index = False
  )

  # Carrega os dados para o Data Lake.
  client.fput_object(
    "processing",
    "time_in_company.parquet",
    "/tmp/time_in_company.parquet"
  )


extract_task = PythonOperator(
  task_id = 'extract_data_from_database',
  provide_context = True,
  python_callable = extract,
  dag = dag
)

transform_task = PythonOperator(
  task_id = 'transform_data',
  provide_context = True,
  python_callable = transform,
  dag = dag
)

load_task = PythonOperator(
  task_id = 'load_file_to_data_lake',
  provide_context = True,
  python_callable = load,
  dag = dag
)

clean_task = BashOperator(
  task_id = "clean_files_on_staging",
  bash_command = "rm -f /tmp/*.csv;rm -f /tmp/*.json;rm -f /tmp/*.parquet;",
  dag = dag
)

extract_task >> transform_task >> load_task >> clean_task
