import pandas as pd
import pendulum
from airflow.decorators import dag, task, task_group
from airflow.utils.edgemodifier import Label
from dotenv import load_dotenv
import os
import json
import logging
import logging.config

# logging.config.fileConfig(fname="config/logging.conf")

logging.basicConfig(
     filename='log_file_name.log',
     level=logging.INFO, 
     format="%(asctime)s %(levelname)s %(message)s",
     datefmt='%H:%M:%S'
 )


load_dotenv()

@dag(schedule=None, start_date=pendulum.now(), catchup=False)
def checking_logs():
    @task
    def read_data(raw_file: str, skip_rows: int=1, names: list=[
            'error_code', 'error_message', 'severity', 'log_location',
            'mode', 'model', 'graphics', 'session_id', 'sdkv', 'test_mode',
            'flow_id', 'flow_type', 'sdk_date', 'publisher_id', 'game_id',
            'bundle_id', 'appv', 'language', 'os', 'adv_id', 'gdpr', 'ccpa',
            'country_code', 'date']) -> pd.DataFrame:
        return pd.read_csv(raw_file, skiprows=skip_rows, names=names)

    @task
    def data_preparation(file: pd.DataFrame) -> pd.DataFrame:
        file['date'] = pd.to_datetime(file['date'], unit='s').dt.strftime('%Y-%m-%d %H:%M')
        file['date_h'] = file['date'].str[:13]
        return file

    
    def errors_in_1_minute(file: pd.DataFrame) -> bool:
        return any(file.loc[file['severity'] == 'Error']
                .groupby('date')['error_code'].agg('count') > 10)

    
    def errors_in_1_bundle(file: pd.DataFrame) -> bool:
        return any(file.loc[file['severity'] == 'Error']
                .groupby(['bundle_id', 'date_h'])['error_code']
                .agg('count') > 10)

    @task
    def errors(file):
        minutes = str(errors_in_1_minute(file))
        bundle = str(errors_in_1_bundle(file))
        return minutes + bundle

    @task
    def move_file(error_string: str) -> None:
        if error_string != '00':
            folder = file_path_bad
            logging.error(error_decoder[error_string])
        else:
            folder = file_path_good
            logging.info(error_decoder[error_string])
        os.replace(raw_file, folder + 
                    file_name[:-4] + str(pendulum.now().int_timestamp) + '.csv')


    file_name = os.getenv('FILE_NAME')
    file_path = os.getenv('FILE_PATH')
    file_path_bad = os.getenv('FILE_PATH_BAD')
    file_path_good = os.getenv('FILE_PATH_GOOD')
    raw_file = file_path + file_name
    with open(os.getenv('ERROR_LIST', 'r')) as f:
        error_decoder = json.load(f)

    file = data_preparation(read_data(raw_file))
    move_file(errors(file))

    


checking_logs()
