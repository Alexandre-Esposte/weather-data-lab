from etl import ETL
from pathlib import Path
from logger import setup_logging, get_logger

logger = get_logger(__name__)

setup_logging()


def main():
    
    years = [i for i in range(2017,2026)]

    download_dir = Path(r'temporary_data.entrydata')
    etl = ETL(download_dir)

    for year in years:
        #etl.extract(year)
        for file in download_dir.rglob(f"*.CSV"):
            metadata , weather_data_df = etl.transform(file)
            if metadata is None or weather_data_df is None:
                continue

            etl.load(metadata, weather_data_df, file)


if __name__ == "__main__":
    logger.info('Starting ETL process')
    main()
    logger.info('ETL process finished')