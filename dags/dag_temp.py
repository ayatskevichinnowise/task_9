import pandas as pd
import pendulum
from airflow.decorators import dag, task, task_group
from airflow.utils.edgemodifier import Label
from airflow.sensors.filesystem import FileSensor
from airflow.operators.email_operator import EmailOperator
from dotenv import load_dotenv
import os
import json
# import logging
# import logging.config

load_dotenv()
# logging.config.fileConfig(fname=os.getenv('CONFIG_PATH'))

default_args = {
    'email': os.getenv('EMAIL2'),
    'email_on_failure': True,
}


@dag(schedule=None, start_date=pendulum.now(), catchup=False, default_args=default_args)
def checking_logs2():
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
        minutes = str(int(errors_in_1_minute(file)))
        bundle = str(int(errors_in_1_bundle(file)))
        return minutes + bundle

    @task
    def move_file(error_string: str) -> None:
        if error_string != '00':
            os.replace(raw_file, file_path_bad + 
                    file_name[:-4] + str(pendulum.now().int_timestamp) + '.csv')
            raise Exception(error_decoder[error_string])
        else:
            # logging.info(error_decoder[error_string])
            os.replace(raw_file, file_path_good + 
                        file_name[:-4] + str(pendulum.now().int_timestamp) + '.csv')
    
    @task
    def alert():
        raise Exception(f'FILE: {raw_file}. ERROR:' + str(error_decoder['10']))


    file_name = os.getenv('FILE_NAME')
    file_path = os.getenv('FILE_PATH')
    file_path_bad = os.getenv('FILE_PATH_BAD')
    file_path_good = os.getenv('FILE_PATH_GOOD')
    config_path = os.getenv('CONFIG_PATH')
    raw_file = file_path + file_name
    with open(os.getenv('ERROR_LIST', 'r')) as f:
        error_decoder = json.load(f)

    wait_for_file = FileSensor(task_id='wait_for_file',
                               poke_interval=10,
                               filepath=raw_file
                               )
    alert()
    # file = wait_for_file >> read_data(raw_file)
    # prep_file = data_preparation(file)
    # move_file(errors(prep_file))

    
checking_logs2()
