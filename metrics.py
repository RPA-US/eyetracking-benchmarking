import pandas as pd
import os
import numpy as np
from settings import I_DT_THRESHOLD_DISPERSION

def ellipses_intersect(x1, y1, x2, y2, threshold):
    # Check if the distance between the centers of the ellipses is less than or equal to the threshold
    distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distance <= 2 * threshold

def preprocess_df(df):
    # Eliminar la primera fila del DataFrame
    df = df.iloc[1:]
    
    # Seleccionar solo las columnas especificadas y la primera columna que indica el rowindex
    columns_to_keep = ["time:timestamp", "category", "application", "coordX", "coordY", "typed_word", "screenshot", "concept:name"]
    df = df.reset_index()[["index"] + columns_to_keep]
    
    # Redondear las columnas coordX y coordY a dos decimales
    df["coordX"] = df["coordX"].round(2)
    df["coordY"] = df["coordY"].round(2)
    
    # Añadir la columna Gaze_Fixation_target
    df["Gaze_Fixation_target"] = False
    
    # Iterar sobre el DataFrame para encontrar fijaciones y eventos de Keyboard o MouseClick
    for i in range(len(df) - 1):
        if df.loc[i, "category"] == "GazeFixation":
            for j in range(i + 1, len(df)):
                next_event = df.loc[j]
                if next_event["category"] in ["Keyboard", "MouseClick"]:
                    if ellipses_intersect(df.loc[i, "coordX"], df.loc[i, "coordY"], next_event["coordX"], next_event["coordY"], I_DT_THRESHOLD_DISPERSION):
                        df.loc[i, "Gaze_Fixation_target"] = True
                    break
    
    # Cambiar el tipo de datos de la columna Gaze_Fixation_target a object
    df["Gaze_Fixation_target"] = df["Gaze_Fixation_target"].astype(object)
    
    # Establecer las celdas de Gaze_Fixation_target como vacías para filas con category Keyboard o MouseClick
    df.loc[df["category"].isin(["Keyboard", "MouseClick"]), "Gaze_Fixation_target"] = ""
    
    return df

# Directorios de entrada y salida
input_dir = os.path.join('media', 'p1', 'preprocessed')
output_dir = os.path.join('media', 'p1', 'postprocessed')

# Crear el directorio de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Procesar cada archivo CSV en el directorio de entrada
for filename in os.listdir(input_dir):
    if filename.endswith('.csv'):
        input_file_path = os.path.join(input_dir, filename)
        df = pd.read_csv(input_file_path)
        
        # Preprocesar el DataFrame
        preprocessed_df = preprocess_df(df)
        
        # Guardar el DataFrame preprocesado en el directorio de salida
        output_file_path = os.path.join(output_dir, filename.replace('.csv', '_postprocessed.csv'))
        preprocessed_df.to_csv(output_file_path, index=False)
        
        print(f"Preprocessed DataFrame saved to {output_file_path}")
        
        
