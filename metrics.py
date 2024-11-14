import logging
import pandas as pd
import os
import numpy as np
from settings import target_radio_tobii, target_radio_webgazer




def ellipses_intersect(x1, y1, x2, y2, threshold):
    # Check if the distance between the centers of the ellipses is less than or equal to the threshold
    distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distance <= 2 * threshold

def preprocess_df(df,target_radio):
    # Eliminar la primera fila del DataFrame
    df = df.iloc[1:]
    
    # Seleccionar solo las columnas especificadas y la primera columna que indica el rowindex
    columns_to_keep = ["time:timestamp", "category", "application", "coordX", "coordY", "typed_word", "screenshot", "concept:name"]
    df = df.reset_index()[["index"] + columns_to_keep]
    
    # Redondear las columnas coordX y coordY a dos decimales
    df["coordX"] = df["coordX"].round(2)
    df["coordY"] = df["coordY"].round(2)
    
    # Añadir la columna Gaze_Fixation_target y Gaze_Fixation_id
    df["Gaze_Fixation_Baseline"] = False
    df["Gaze_Fixation_Index"] = 1
    
    # Inicializar el índice de fijación
    fixation_index = 1
    
    # Iterar sobre el DataFrame para encontrar fijaciones y eventos de Keyboard o MouseClick
    for i in range(len(df)):
        if df.loc[i, "category"] == "GazeFixation":
            df.loc[i, "Gaze_Fixation_Index"] = fixation_index
            for j in range(i + 1, len(df)):
                next_event = df.loc[j]
                if next_event["category"] in ["Keyboard", "MouseClick", "DoubleMouseClick"]:
                    if ellipses_intersect(df.loc[i, "coordX"], df.loc[i, "coordY"], next_event["coordX"], next_event["coordY"], target_radio):
                        df.loc[i, "Gaze_Fixation_Baseline"] = True
                    break
        elif df.loc[i, "category"] in ["Keyboard", "MouseClick", "DoubleMouseClick"]:
            fixation_index += 1
    
    df["Gaze_Fixation_Baseline"] = df["Gaze_Fixation_Baseline"].astype(object)
    df["Gaze_Fixation_Index"] = df["Gaze_Fixation_Index"].astype(object)
    
    # Establecer las celdas de Gaze_Fixation_target como vacías para filas con category Keyboard o MouseClick
    df.loc[df["category"].isin(["Keyboard", "MouseClick", "DoubleMouseClick"]), "Gaze_Fixation_Baseline"] = "BaselineComponentClick"
    df.loc[df["category"].isin(["Keyboard", "MouseClick", "DoubleMouseClick"]), "Gaze_Fixation_Index"] = ""
    
    return df

def preprocess_notification_popup(df,target_radio):
    #popup abajo derecha
    for i in range(len(df)):
        if df.loc[i, "category"] == "GazeFixation":
             if ellipses_intersect(df.loc[i, "coordX"], df.loc[i, "coordY"], 216, 929, target_radio):
                 df.loc[i, "Gaze_Fixation_Baseline"] = "PopUp_True"
                
    return df

def preprocess_notification_popup__p1_tobii(df,target_radio):
    #popup arriba izquierda
    #centroide del popup (210,185)
    for i in range(len(df)):
        if df.loc[i, "category"] == "GazeFixation":
             if ellipses_intersect(df.loc[i, "coordX"], df.loc[i, "coordY"], 210, 185, target_radio):
                 df.loc[i, "Gaze_Fixation_Baseline"] = "PopUp_True"
                
    return df

def preprocess_notification_popup__p1_webgazer(df,target_radio):
    #popup arriba derecha
    #centroide del popup (1700, 185)

    for i in range(len(df)):
        if df.loc[i, "category"] == "GazeFixation":
             if ellipses_intersect(df.loc[i, "coordX"], df.loc[i, "coordY"], 1704, 185, target_radio):
                 df.loc[i, "Gaze_Fixation_Baseline"] = "PopUp_True"
                
    return df

def preprocess_multiscreen_aoi_name(df,target_radio):
    # Nombre del paciente a introducir en el input text
    # centroide del nombre del paciente (350, 390)
    for i in range(len(df)):
        if df.loc[i, "category"] == "GazeFixation":
            for j in range(i + 1, len(df)):
                if df.loc[j, "category"] == "Keyboard":
                    if ellipses_intersect(df.loc[i, "coordX"], df.loc[i, "coordY"], 350, 390, target_radio):
                        df.loc[i, "Gaze_Fixation_Baseline"] = "AOI_Name_True"
                    break
                elif df.loc[j, "category"] != "GazeFixation":
                    break
    return df
    

# Directorios de entrada y salida. Elegir tests correspondiente al suejeto
input_dir = os.path.join('tests', 't1', 'preprocessed')
output_dir = os.path.join('tests', 't1', 'postprocessed')

# Crear el directorio de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Procesar cada archivo CSV en el directorio de entrada
for filename in os.listdir(input_dir):
    if "tobii" in filename:
        TARGET_RADIO = target_radio_tobii()
        # TARGET_RADIO = 35*2
    elif "webgazer" in filename:
        TARGET_RADIO = target_radio_webgazer()
        # TARGET_RADIO = 35*2
    
    if filename.endswith('.csv'):
        input_file_path = os.path.join(input_dir, filename)
        df = pd.read_csv(input_file_path)
        preprocessed_df= preprocess_df(df,TARGET_RADIO)
        

        if filename.endswith('_multiscreen.csv'):
            preprocess_multiscreen_aoi_name(preprocessed_df,TARGET_RADIO)
        if  filename.endswith('_notification.csv'):
            preprocess_notification_popup(preprocessed_df,TARGET_RADIO)
        #Si existe el archivo RQ3_tobii_notification.csv en la ruta tests/t1/preprocessed, se ejecuta la función preprocess_notification_popup__p1_tobii
        if filename == 'RQ3_tobii_notification.csv':
            preprocess_notification_popup__p1_tobii(preprocessed_df,TARGET_RADIO)
        #Si existe el archivo RQ3_tobii_notification.csv en la ruta tests/t1/preprocessed, se ejecuta la función preprocess_notification_popup__p1_tobii
        if filename == 'RQ3_webgazer_notification.csv':
            preprocess_notification_popup__p1_webgazer(preprocessed_df,TARGET_RADIO)
        # Guardar el DataFrame preprocesado en el directorio de salida
        output_file_path = os.path.join(output_dir, filename.replace('.csv', '_postprocessed.csv'))
        preprocessed_df.to_csv(output_file_path, index=False)
        print(f"Preprocessed DataFrame saved to {output_file_path}")
    else    :
        logging.error("No CSV files found in the specified directory.")
        raise FileNotFoundError("No CSV files found in the specified directory. Please, save the preprocessed CSV files in 'tests\tx\preprocessed' root.")
