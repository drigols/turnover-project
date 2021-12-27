###################################################################
# Rodrigo Leite - drigols                                         #
# Last update: 27/12/2021                                         #
###################################################################

from datetime import datetime,date, timedelta
from io import BytesIO

from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.models import Variable
from airflow import DAG

from sqlalchemy.engine import create_engine

from minio import Minio
import pandas as pd

# Argumentos padrão (default) da nossa DAGs:
# - Dono da DAG (owner);
# - Se a DAG tem dependência;
# - A data de início da DAG (Você pode definir um agendamento para ficar sempre consultando)
DEFAULT_ARGS = {
  'owner': 'Airflow',
  'depends_on_past': False,
  'start_date': datetime(2021, 1, 13),
}

# Instancia nossa DAG e passa como argumento:
# - Nosso dicionário de argumentos default;
# - Intervelo de execução "@once" = Vai ser executado só uma vez.
dag = DAG(
  'etl_department_salary_left_att', 
  default_args=DEFAULT_ARGS,
  schedule_interval="@once"
)

# [Datalake connection]
# Pega os dados de conexão do Datalake armazenados nas variáveis do Airflow.
data_lake_server = Variable.get("data_lake_server")
data_lake_login = Variable.get("data_lake_login")
data_lake_password = Variable.get("data_lake_password")

# [Database connection]
# Pega os dados de conexão do Banco de Dados armazenados nas variáveis do Airflow.
database_server = Variable.get("database_server")
database_login = Variable.get("database_login")
database_password = Variable.get("database_password")
database_name = Variable.get("database_name")

# [Cria uma variável que vai representar conexão com o Banco de Dados]
# Se você prestar bem atenção vai ver que nossa variável é do tipo String.
# Com isso nós utilizamos o método format() da classe String para fazer um tipo
# de concatenação ou adição de palavras na nossa String, representando login, senha
# e etc do Banco de Dados.
url_connection = "mysql+pymysql://{}:{}@{}/{}".format(
  str(database_login),
  str(database_password),
  str(database_server),
  str(database_name)
)

# Cria uma instânciada classe Engine, ou seja, conexão com o Banco de Dados.
engine = create_engine(url_connection)

# Cria uma instância do MinIO com os dados das variáveis de acesso armazenadas no Airflow.
client = Minio(
  data_lake_server,
  access_key = data_lake_login,
  secret_key = data_lake_password,
  secure=False
)

# ETL de extração dos dados.
def extract():

  # Query para consultar os dados.
  query = """SELECT emp.department as department,sal.salary as salary, emp.left
    FROM employees emp
    INNER JOIN salaries sal
    ON emp.emp_no = sal.emp_id;"""

  # Passa a query e conexão com o Banco de Dados.
  df_ = pd.read_sql_query(query, engine)
    
  # Persiste os arquivos na Staging Area.
  df_.to_csv(
    "/tmp/department_salary_left.csv",
    index=False
  )

# ETL de carregamento dos dados.
def load():

  # Carrega os dados a partir da área de staging.
  df_ = pd.read_csv("/tmp/department_salary_left.csv")

  # Converte os dados para o formato parquet.
  # Formato parquet é um formato orientado por coluna.
  df_.to_parquet(
    "/tmp/department_salary_left.parquet"
    ,index=False
  )

  # Carrega os dados para o Data Lake.
  client.fput_object(
    "processing", # Passa para a zona (butcket) processing.
    "department_salary_left.parquet",
    "/tmp/department_salary_left.parquet"
  )

extract_task = PythonOperator(
  task_id = 'extract_data_from_database',
  provide_context = True,
  python_callable = extract, # Chama a função extract().
  dag = dag
)

load_task = PythonOperator(
  task_id = 'load_file_to_data_lake',
  provide_context = True,
  python_callable = load,  # Chama a função load().
  dag = dag
)

clean_task = BashOperator(
  task_id = "clean_files_on_staging",
  # Remove os arquivos temporários da Stanging Area.
  bash_command = "rm -f /tmp/*.csv;rm -f /tmp/*.json;rm -f /tmp/*.parquet;",
  dag = dag
)

# Executa ETL > Sequência de tarefas.
extract_task >> load_task >> clean_task
