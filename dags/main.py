from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from api.movies_stats import get_movies_stats, save_to_json
from datawarehouse.datawarehouse import transform_and_load_data

local_tz = pendulum.timezone("Europe/Madrid")

default_args = {
    "owner": "dataengineers",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "data@engineers.com",
    "max_active_runs": 1,
    "dagrun_timeout": timedelta(minutes=60),
    "start_date": datetime(2025, 1, 1, tzinfo=local_tz)
}

with DAG(
    dag_id="movies_stats_dag",
    default_args=default_args,
    description="A DAG to extract and save movies stats from TMDB API",
    schedule='0 14 * * *',
    catchup=False,
) as dag:
    movies_stats = get_movies_stats()
    json_file = save_to_json(movies_stats)
    tl_task = transform_and_load_data()

    # Define dependencies between tasks
    movies_stats >> json_file >> tl_task


with DAG(
    dag_id="update_movies_stats_dag",
    default_args=default_args,
    description="A DAG to update movies stats in the data warehouse",
    schedule='0 15 * * *',
    catchup=False,
) as dag:
    tl_task = transform_and_load_data()