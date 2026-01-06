import pandas as pd
from pathlib import Path
import numpy as np

def process_weather_data(arquivo: Path) -> tuple[dict, pd.DataFrame]:
    # metadados
    metadados = {}
    with open(arquivo, encoding="latin-1") as f:
        for i in range(8):  # primeiras linhas
            linha = f.readline().strip()

            if ":" in linha:
                chave, valor = linha.split(":", 1)
                valor = valor.split(';')[-1]
                valor= valor.replace(',','.')
                metadados[chave.strip().lower()] = valor.strip()

    # Dados tabulares / medidas
    df = pd.read_csv(
        arquivo,
        sep=";",
        encoding="latin-1",
        skiprows=8
    )
    df.iloc[:, 2:-1] = df.iloc[:, 2:].replace(',', '.', regex=True)

    df = df.drop(columns=['Unnamed: 19'])
    df.replace(-9999, pd.NA, inplace=True)

    for col in df.iloc[:,2:19].columns:
        df[col] = pd.to_numeric(df[col])
    
    return metadados, df[['DATA (YYYY-MM-DD)',
                          'HORA (UTC)',
                          'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)',
                          'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)',
                          'RADIACAO GLOBAL (KJ/m²)',
                          'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)',
                          'TEMPERATURA DO PONTO DE ORVALHO (°C)',
                          'UMIDADE RELATIVA DO AR, HORARIA (%)',
                          'VENTO, DIREÇÃO HORARIA (gr) (° (gr))',
                          'VENTO, RAJADA MAXIMA (m/s)',
                          'VENTO, VELOCIDADE HORARIA (m/s)']]
