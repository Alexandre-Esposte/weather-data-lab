from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from pathlib import Path
from station_historical_data_collector import get_historical_data
from station_historical_data_process import process_weather_data
from schemas.database_schema import Base, Stations
import logging
import shutil

logging.basicConfig(level=logging.INFO)

load_dotenv()

def main():

    # carregando dados do .env
    source = os.getenv('hist_source')
    start_year = int(os.getenv('start_year'))
    end_year = int(os.getenv('end_year'))
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    database = os.getenv('POSTGRES_DATABASE')

    #definindo e criando diretório temporário
    download_dir = Path('.temp_data')
    download_dir.mkdir(exist_ok=True, parents=True)
    
    # Fazendo download dos dados
    for year in range(start_year, end_year+1):
        logging.info(f'Download data for: {year}')
        url = source + f"{year}.zip"
        get_historical_data(url, year, download_dir)
        logging.info('Done')


    # Processando dados
    for arq in download_dir.rglob('*.CSV'):
        metadados, df = process_weather_data(arq)
        logging.info(metadados)

    # Criando tabelas e inputando dados no banco de dados
    engine = create_engine(f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}")
    with engine.connect() as conn:
        print('Connected to database')
    Base.metadata.create_all(engine)


    with Session(engine) as session:
        pass


    
    # Removendo diretorio e arquivos temporarios
    shutil.rmtree(download_dir)
    if not download_dir.exists():
        logging.info('Temp. directory removed')

if __name__ == "__main__":
    main()