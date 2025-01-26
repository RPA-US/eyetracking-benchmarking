import os
import pandas as pd

def collect_csv_files(base_path, output_file):
    """
    Función para recopilar y combinar todos los archivos CSV de un proyecto en un solo archivo.

    Args:
        base_path (str): Ruta principal del proyecto donde buscar los CSV.
        output_file (str): Ruta del archivo combinado de salida.
    """
    # Lista para almacenar los DataFrames
    combined_data = []

    # Recorrer todas las subcarpetas y archivos
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.csv'):  # Identificar archivos CSV
                file_path = os.path.join(root, file)
                try:
                    # Leer cada CSV y añadirlo a la lista
                    df = pd.read_csv(file_path)
                    combined_data.append(df)
                    print(f"Archivo leído: {file_path}")
                except Exception as e:
                    print(f"Error al leer {file_path}: {e}")

    if combined_data:
        # Combinar todos los DataFrames
        combined_df = pd.concat(combined_data, ignore_index=True)

        # Guardar en el archivo de salida
        try:
            combined_df.to_csv(output_file, index=False)
            print(f"Archivo combinado guardado en: {output_file}")
        except Exception as e:
            print(f"Error al guardar el archivo combinado: {e}")
    else:
        print("No se encontraron archivos CSV para combinar.")

# Especificar la ruta base del proyecto y la salida deseada
base_path = "data/data_collection"
output_file = "data/combined_data.csv"

collect_csv_files(base_path, output_file)


