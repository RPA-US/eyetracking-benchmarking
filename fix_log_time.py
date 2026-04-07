import os
import pandas as pd
from datetime import timedelta

def ajustar_timestamp(input_file: str):
    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv(input_file)
    
    # Convertir la columna 'time:timestamp' a formato datetime
    df["time:timestamp"] = pd.to_datetime(df["time:timestamp"])
    
    # Restar 600 ms
    df["time:timestamp"] = df["time:timestamp"] - timedelta(milliseconds=600)
    
    # Convertir de nuevo a formato de texto ISO 8601 con milisegundos
    df["time:timestamp"] = df["time:timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S.%f").str[:-3]
    
    # Guardar el DataFrame ajustado en el mismo archivo CSV
    df.to_csv(input_file, index=False)
    print(f"Archivo corregido guardado como: {input_file}")

def process_all_logs(directory: str):
    for root, _, files in os.walk(directory):
        for file in files:
            if file == "log.csv":
                input_file = os.path.join(root, file)
                ajustar_timestamp(input_file)

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))
    process_all_logs(current_directory)