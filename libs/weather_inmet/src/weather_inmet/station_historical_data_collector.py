import requests
import zipfile
from pathlib import Path
import os

def get_historical_data(url: str, year: int, download_dir: Path) -> None:

    zip_path = download_dir / f"{year}.zip"
    
    #Obtendo dados
    response = requests.get(url, timeout=30, stream=True)
    response.raise_for_status()
    with open(zip_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    #Extraindo dados
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(download_dir)
    
    #Removendo arquivo zip após extração
    os.remove(zip_path)
