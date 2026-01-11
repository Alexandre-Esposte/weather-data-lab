import os
import zipfile
import requests
import pandas as pd


from pathlib import Path
from typing import Optional
from logger import get_logger
from dotenv import load_dotenv
from unidecode import unidecode
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from schemas.metadata_schema import Metadata
from sqlalchemy.dialects.postgresql import insert
from schemas.database_schema import Base, Stations, WeatherData


#TODO genericos:
    # 1.
        # Alguns arquivos estão dando falha devido a duplicidade de primary key
        # Esse problema vem diretamente da maneira como os dados foram organizados na fonte oficial 

    #2.
        # Adicionar descrição no inicio do arquivo

    #3
        # Adicionar docstrings na classe ETL e nos métodos

    #4 
       #Melhorar exceções e tratamento de erros

    #5 
    #   Padronizar diretorio onde arquivos serão salvos

    #6 
        # Tratar error quando o ano não é valido

    #7 
        # Adicionar retry e melhorar tratamento do request


logger = get_logger(__name__)


class ETL():

    def __init__(self, download_dir: Path = Path('temp_data.entrydata')):
        load_dotenv()

        #TO DO:
            # Classe ETL não deveria ter atributos relacionado ao banco de dados
            # Classe ETL não deve saber como se conectar ao banco
            # A função da classe ETL é somente Extrair, Transformar e Carregar
            # Se o gerenciador do banco mudar, a classe quebra
            # As tabelas do banco não devem ser criadas ou verificadas na classe ETL
        self.source = os.getenv('hist_source')
        self.user = os.getenv('POSTGRES_USER')
        self.password = os.getenv('POSTGRES_PASSWORD')
        self.host = os.getenv('POSTGRES_HOST')
        self.port = os.getenv('POSTGRES_PORT')
        self.database = os.getenv('POSTGRES_DATABASE')

        self.engine = create_engine(f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}")
        Base.metadata.create_all(self.engine)


        self.download_dir = download_dir
        self.download_dir.mkdir(exist_ok=True, parents=True)



        self.rename_map_metadados = {"regiao":'region',
                                     "uf":'state_uf',
                                     "estacao":'station_name',
                                     "codigo":'station_code',
                                     "latitude":'latitude',
                                     "longitude":'longitude',
                                     "altitude":'altitude', 
                                     "data de fundacao":'fundation_time'}



    #====================================Public methods===============================================================

    def extract(self, year: int) -> None:

        logger.info("--------------------------New Extract---------------------------")
        logger.info(f"Downloading data from source for {year}")

        zip_path = self.download_dir / f"{year}.zip"
        url = self.source + f"{year}.zip"

        # Data Download
        response = requests.get(url, timeout=30, stream=True)
        response.raise_for_status()
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=64 * 1024):
                f.write(chunk)

        # Data extraction
        logger.info(f"Extracting data for {year}")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(self.download_dir)
        
        # Remove the zip file after extraction
        zip_path.unlink()

        logger.info(f"Data extracted successfully for {year}")

    def transform(self, file: Path)-> Optional[tuple[Metadata, pd.DataFrame]]:

        logger.info(f"------------------------New File: {file.name}-------------------------")
        try:
            # Getting metadata
            logger.info(f'Getting metadata for {file.name}')
            metadata = self._get_metadata(file)
                
            # Getting weather data
            logger.info(f'Getting weather data for {file.name}')
            weather_data_df = self._get_weatherdata(file)
                
            weather_data_df['station_code'] = metadata.station_code

            logger.info(f"Data transformed successfully for {file.name}")
            
            return metadata, weather_data_df[['dt',
                                              'station_code',
                                              'total_precipitation',
                                              'air_pressure',
                                              'global_radiation',
                                              'air_temperature',
                                              'dew_point_temperature',
                                              'relative_humidity',
                                              'wind_direction',
                                              'max_wind_speed',
                                              'wind_speed']]
        except Exception as e:
            logger.warning(f"Transform failed: {e}")
            return None, None




    def load(self, metadata: Metadata, weather_data_df: pd.DataFrame, file: Path) -> None:
        with Session(self.engine) as session:
            
            try:
                
                records = weather_data_df.to_dict(orient='records')

                # Station
                logger.info(f"Loading metadata for {file.name}")
                station = Stations(**metadata.to_dict())
                session.merge(station)
                session.flush()
                logger.info(f"Metadata loaded successfully for {file.name}")

                # WeatherData
                logger.info(f"Loading weather data for {file.name}")
                weather_data_objects = [WeatherData(**record) for record in records]

                session.bulk_save_objects(weather_data_objects)
                session.commit()
                logger.info(f"Weather data loaded successfully for {file.name}")

                file.unlink()
                logger.info(f"File {file.name} removed successfully")


            except IntegrityError as e:
                session.rollback()
                logger.warning("IntegrityError: %s", e.orig)
                

            except Exception as e:
                session.rollback()
                logger.warning("GenericError: %s", e.orig)
                

    
    #=====================Private methods======================================================

    def _process_metadata_keys(self, metadata: dict) -> Metadata:
        
        standard_metadata = {}
        for key, value in metadata.items():

            standard_key = unidecode(key).lower().strip()
            
            if 'codigo' in standard_key:
                standard_key = 'codigo'
            
            # elif 'fundacao' in standard_key:
            #     standard_key = "data de fundacao"
            
            elif standard_key in ['fundacao','data de fundac?o']:
                standard_key = "data de fundacao"

            elif 'regi?o' in standard_key:
                standard_key = 'regiao'

            elif 'estac?o' in standard_key:
                standard_key = "estacao"
                
            standard_key = self.rename_map_metadados[standard_key]        
            standard_metadata[standard_key] = value
        
        # Fixing metadata type
        standard_metadata['region'] = str(standard_metadata['region'])
        standard_metadata['state_uf'] = str(standard_metadata['state_uf'])
        standard_metadata['station_name'] = str(standard_metadata['station_name'])
        standard_metadata['station_code'] = str(standard_metadata['station_code'])
        standard_metadata['latitude'] = float(standard_metadata['latitude'])
        standard_metadata['longitude'] = float(standard_metadata['longitude'])
        standard_metadata['altitude'] = float(standard_metadata['altitude'])
        standard_metadata['fundation_time'] = pd.to_datetime(standard_metadata['fundation_time']).date()
       
        standard_metadata = Metadata(**standard_metadata)

        return standard_metadata
    
    
    def _get_metadata(self,file: Path) -> Metadata:
        
        # Metadata from file
        metadata = {}
        with open(file, encoding="latin-1") as f:
            for i in range(8):  # primeiras linhas
                linha = f.readline().strip()

                if ":" in linha:
                    chave, valor = linha.split(":", 1)
                    valor = valor.split(';')[-1]
                    valor= valor.replace(',','.').lower()
                    metadata[chave.strip().lower()] = valor.strip()
                    
        metadata = self._process_metadata_keys(metadata)
        return metadata
    
    def _get_weatherdata(self,file: Path)-> pd.DataFrame:

        # Tabular data / Weather measurements
        df = pd.read_csv(
            file,
            sep=";",
            encoding="latin-1",
            skiprows=8
        )

        # Replacing comma for dot in some variables
        df.iloc[:, 2:-1] = df.iloc[:, 2:].replace(',', '.', regex=True)

        # Dropping a trash column
        df = df.drop(columns=['Unnamed: 19'])

        # Fixing columns type
        for col in df.iloc[:,2:19].columns:
            df[col] = pd.to_numeric(df[col])

        
        df = df.rename(columns={'DATA (YYYY-MM-DD)':'data',
                                'Data':'data',
                                'HORA (UTC)':'time',
                                'Hora UTC':'time',
                                'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)':'total_precipitation',
                                'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)':'air_pressure',
                                'RADIACAO GLOBAL (KJ/m²)':'global_radiation',
                                'RADIACAO GLOBAL (Kj/m²)': 'global_radiation',
                                'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)':'air_temperature',
                                'TEMPERATURA DO PONTO DE ORVALHO (°C)':'dew_point_temperature',
                                'UMIDADE RELATIVA DO AR, HORARIA (%)':'relative_humidity',
                                'VENTO, DIREÇÃO HORARIA (gr) (° (gr))':'wind_direction',
                                'VENTO, RAJADA MAXIMA (m/s)':'max_wind_speed',
                                'VENTO, VELOCIDADE HORARIA (m/s)':'wind_speed'})
        
        
        # Fixing Nan values
        df.replace(-9999, None, inplace=True)
        df.replace(-9.999, None, inplace=True)
        df.replace(-9999.0, None, inplace=True)

        # Some standardization
        df['dt'] = df['data'] + ' ' + df['time']
        df['dt'] = pd.to_datetime(df['dt'])
        df['total_precipitation'] = df['total_precipitation'].astype(float)
        df['air_pressure'] = df['air_pressure'].astype(float)
        df['global_radiation'] = df['global_radiation'].astype(float)
        df['air_temperature'] = df['air_temperature'].astype(float)
        df['dew_point_temperature'] = df['dew_point_temperature'].astype(float)
        df['relative_humidity'] = df['relative_humidity'].astype(float)
        df['wind_direction'] = df['wind_direction'].astype(float)
        df['max_wind_speed'] = df['max_wind_speed'].astype(float)
        df['wind_speed'] = df['wind_speed'].astype(float)

        return df