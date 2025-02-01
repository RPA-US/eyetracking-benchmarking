import logging
import pandas as pd
import os
import numpy as np
import json
from shapely.geometry import Point, Polygon
from settings import get_distance_threshold_by_resolution
import sys
import math

def load_polygons(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    polygons_dict = {}
    for element in data["elements"]:
        group = element["group"]
        name = element["name"]
        dimensions = [tuple(map(int, point.split(','))) for point in element["dimensions"]]
        if group not in polygons_dict:
            polygons_dict[group] = []
        polygons_dict[group].append({"polygon": Polygon(dimensions), "name": name})
    return polygons_dict

def filter_polygons_by_point(coordX, coordY, polygons):
    point = Point(coordX, coordY)
    filtered_polygons = {}
    for group, poly_list in polygons.items():
        for poly_info in poly_list:
            polygon = poly_info["polygon"]
            if polygon.contains(point):
                filtered_polygons[group] = poly_list
                break  # Salir del bucle interno si se encuentra un polígono que contiene el punto
    return filtered_polygons

def get_polygon_group_by_containing_point(coordX, coordY, polygons):
    point = Point(coordX, coordY)
    polygons_group = set()
    for poly_list in polygons.values():
        for poly_info in poly_list:
            polygon = poly_info["polygon"]
            if polygon.contains(point):
                polygons_group.add(poly_list)
    return polygons_group

def is_gaze_fixation_baseline(x, y, polygons, threshold):
    point = Point(x, y)
    for poly_list in polygons.values():
        for poly_info in poly_list:
            polygon = poly_info["polygon"]
            if polygon.distance(point) <= threshold:
                return "True"
    return "False"

def get_polygon_group_by_threshold(x, y, polygons, threshold):
    point = Point(x, y)
    for group, poly_list in polygons.items():
        for poly_info in poly_list:
            polygon = poly_info["polygon"]
            if polygon.distance(point) <= threshold:
                return group
    return "None" 

def get_polygon_test_object_list_by_threshold(x, y, polygons, threshold):
    point = Point(x, y)
    names_within_threshold = []
    for name, poly_list in polygons.items():
        for poly_info in poly_list:
            polygon = poly_info["polygon"]
            if polygon.distance(point) <= threshold:
                names_within_threshold.append(poly_info["name"])
    return names_within_threshold

def preprocess_df(df):
    df = df.iloc[1:] # Eliminar la primera fila del DataFrame
    # Seleccionar solo las columnas especificadas y la primera columna que indica el rowindex
    columns_to_keep = ["time:timestamp", "category", "application", "coordX", "coordY", "typed_word", "screenshot", "concept:name"]
    df = df.reset_index()[["index"] + columns_to_keep]
    df["TotalEvents"] = len(df[df["category"].isin(["MouseClick", "DoubleMouseClick", "Keyboard"])])
    # Redondear las columnas coordX y coordY a dos decimales
    df["coordX"] = df["coordX"].round(2)
    df["coordY"] = df["coordY"].round(2)
    # Añadir la columna Gaze_Fixation_target y Gaze_Fixation_id
    df["Match_Fixation"] = False
    df["Gaze_Fixation_Index"] = 1
    df["Match_Fixation"] = df["Match_Fixation"].astype(object)
    df["Gaze_Fixation_Index"] = df["Gaze_Fixation_Index"].astype(object)

    # Encontrar el índice del último evento de MouseClick, Keyboard o DoubleMouseClick
    last_event_index = df[df["category"].isin(["MouseClick", "Keyboard", "DoubleMouseClick"])].index.max()

    # Eliminar todas las filas cuya categoría sea GazeFixation después del último evento
    if not pd.isna(last_event_index):
        df = df.drop(df[(df.index > last_event_index) & (df["category"] == "GazeFixation")].index)

    return df

def postprocess_df(df):
    df["Match_Fixation"] = df["Match_Fixation"].astype(object)
    df["Gaze_Fixation_Index"] = df["Gaze_Fixation_Index"].astype(object)

    df.loc[df["category"].isin(["Keyboard", "MouseClick", "DoubleMouseClick"]), "Gaze_Fixation_Index"] = ""
    df.loc[df["category"].isin(["Keyboard", "MouseClick", "DoubleMouseClick"]), "Match_Fixation"] = "BaselineComponentClick"

    #Eliminar las filas que  tengan "Group" vacío
    # df = df[df["Group"].notna()]

    if 'index' in df.columns:
        df = df.drop(columns=["index"])

    # Restablecer el índice
    df["index"] = 1+np.arange(len(df))
    # Mover la columna "index" a la primera posición
    cols = ['index'] + [col for col in df.columns if col != 'index']
    df = df[cols]
    
    return df

def process_RQ_df(df, polygons, threshold):
    fixation_index = 1

    for i in range(len(df)):
        if df.loc[i, "category"] == "GazeFixation":
            df.loc[i, "Gaze_Fixation_Index"] = fixation_index
            # Buscar el primer evento de tipo "Keyboard", "MouseClick" o "DoubleMouseClick" después de la fijación
            for j in range(i + 1, len(df)):
                next_event = df.loc[j]
                if next_event["category"] in ["Keyboard", "MouseClick", "DoubleMouseClick"]:
                    filtered_groups = filter_polygons_by_point(float(next_event["coordX"]), float(next_event["coordY"]), polygons)
                    group = next(iter(filtered_groups), None)
                    df.at[j, "Group"] = group

                    if group:
                        total_distance_error = 0
                        fixation_count = 0
                        for k in range(i, j):
                            if df.loc[k, "category"] == "GazeFixation":
                                # Verificar si la fijación está dentro del grupo del clic
                                df.at[k, "Match_Fixation"] = is_gaze_fixation_baseline(float(df.loc[k, "coordX"]), float(df.loc[k, "coordY"]), filtered_groups, threshold)
                                # Asignar el grupo de la fijación
                                if df.at[k, "Match_Fixation"] == "False":
                                    distance_error = math.sqrt((float(df.loc[k, "coordX"]) - float(df.loc[j, "coordX"]))**2 + (float(df.loc[k, "coordY"]) - float(df.loc[j, "coordY"]))**2)
                                    total_distance_error += distance_error
                                    fixation_count += 1
                                df.at[k, "Group"] = get_polygon_group_by_threshold(float(df.loc[k, "coordX"]), float(df.loc[k, "coordY"]), polygons, threshold)
                                
                                name_list = get_polygon_test_object_list_by_threshold(float(df.loc[k, "coordX"]), float(df.loc[k, "coordY"]), polygons, threshold)
                                # Asegurarse de que la columna Target_Object_List existe
                                if "Target_Object_List" not in df.columns:
                                    df["Target_Object_List"] = None
                                df.at[k, "Target_Object_List"] = name_list
                                assign_target_object(df, k, j, name_list)

                                # Lógica para asignar RelevantFixation
                                assign_relevant_fixation(df, k, j, name_list)
                        
                        average_distance_error = total_distance_error / fixation_count if fixation_count > 0 else 0
                        df.at[j, "Average_Distance_Error"] = average_distance_error
                    break
        elif df.loc[i, "category"] in ["Keyboard", "MouseClick", "DoubleMouseClick"]:
            fixation_index += 1

    return postprocess_df(df)

# Función auxiliar para asignar el "Target_Object"
def assign_target_object(df, k, j, name_list):
    group_j = df.loc[j, "Group"]
    
    for name in name_list:
        if (name == "excel_name" and group_j == "name") or \
            (name == "excel_position" and group_j == "position") or \
           (name == "excel_email" and group_j == "email") or  (name == "excel_car_need" and group_j == "car_need"):
            df.at[k, "Target_Object"] = "Target_Object"
            df.at[j, "Target_Object"] = "True"

# Función auxiliar para asignar el "RelevantFixation"
def assign_relevant_fixation(df, k, j, name_list):
    group_j = df.loc[j, "Group"]
    
    for name in name_list:
        if ((name == "excel_name" or "excel_position" or "excel_email" or "excel_car_need" or "exce") and (group_j == "submit" or group_j == "name" or group_j == "position" or group_j == "email" or group_j == "car_need")):
            df.at[k, "Relevant_Fixation"] = "True"

def postprocess_RQ3_df(df):
    df["Number_True_Fixation_In_This_Event"] = ""
    df["Number_False_Fixation_In_This_Event"] = ""
    df["Percentage_Fixation_Matching_In_This_Event"] = ""

    true_cont = 0
    false_cont = 0

    for i in range(len(df)):
        if df.loc[i, "category"] == "GazeFixation":
            if df.loc[i, "Match_Fixation"] == "True":
                true_cont += 1
            elif df.loc[i, "Match_Fixation"] == "False":
                false_cont += 1
        elif df.loc[i, "category"] in ["Keyboard", "MouseClick", "DoubleMouseClick"]:
            df.at[i, "Number_True_Fixation_In_This_Event"] = true_cont
            df.at[i, "Number_False_Fixation_In_This_Event"] = false_cont
            df.at[i, "Percentage_Fixation_Matching_In_This_Event"] = round(((true_cont / (true_cont + false_cont))*100),2)  if (true_cont + false_cont) > 0 else 0
            true_cont = 0
            false_cont = 0

    return df

def postprocess_RQ4_df(df, filename):
    # Procesamientos importantes para RQ4
    if filename == "RQ4_tobii_rpm.csv" or filename == "RQ4_webgazer_rpm.csv":
        if "Target_Object" not in df.columns:
            df["Target_Object"] = ""
        # Las que tengan Target_Object vacío porque no haya gazefixation con el group en cuestión dependiendo del BaselineComponentClick, como puede ser "name", "position", "email" o "car_need", añadir un False 
        condition_baseline = (df["Match_Fixation"] == "BaselineComponentClick") & (df["Target_Object"] == "")
        df.loc[condition_baseline, "Target_Object"] = "False"        
                
        # Todas las gazeFixation que no tengan un Relevant_Fixation=True, se les asigna False
        condition_relevant = (df["Relevant_Fixation"] != "True") & (df["category"] == "GazeFixation")
        df.loc[condition_relevant, "Relevant_Fixation"] = "False"
        
        # Las filas que tengan como match_fixation el BaselineComponentClick y no tengan un Target_Object asignado, se les asigna False
        condition_target_object_false = (df["Match_Fixation"] == "BaselineComponentClick") & (df["Target_Object"] != "True")
        df.loc[condition_target_object_false, "Target_Object"] = "False"
        
        # El submit no tiene Target_Object. Se deja como NA
        condition_submit = df["Group"] == "submit"
        df.loc[condition_submit, "Target_Object"] = "NA"
        
        condition_component = df["Match_Fixation"] == "BaselineComponentClick"
        df.loc[condition_component, "Relevant_Fixation"] = "BaselineComponentClick"
    
    return df

def execute(json_path, filename):
    # Cargar los polígonos de las AOIs
    polygons_json = load_polygons(json_path)
    # Calcular el umbral de distancia
    threshold = get_distance_threshold_by_resolution()
    # Procesar los archivos CSV
    for file in os.listdir(input_dir):
        if file == filename:
            input_file_path = os.path.join(input_dir, filename)
            df = pd.read_csv(input_file_path)
            preprocessed_df = preprocess_df(df)
            processed_df = process_RQ_df(preprocessed_df, polygons_json, threshold)
            postprocessed_df_1 = postprocess_RQ3_df(processed_df)
            postprocessed_df_2 = postprocess_RQ4_df(postprocessed_df_1, filename)
            output_file_path = os.path.join(output_dir, filename.replace('.csv', '_postprocessed.csv'))
            postprocessed_df_2.to_csv(output_file_path, index=False)
            print(f"Preprocessed DataFrame saved to {output_file_path}")

tests = ["s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9"]

for i, test in enumerate(tests, start=1):
    # DEFINIR Directorios de entrada y salida. Elegir tests correspondiente al suejeto
    input_dir = os.path.join('tests', f'{test}', 'preprocessed')
    output_dir = os.path.join('tests', f'{test}', 'postprocessed')

    # Crear el directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Barra de progreso
    progress = (i / len(tests)) * 100
    sys.stdout.write(f"\Postprocessing UB Log Progress: [{i}/{len(tests)}] {progress:.2f}%")
    sys.stdout.flush()

    ### Ejecuciones ###
    # RQ1 - Static UI elements - %Matching Fixations . Familiy Form Scenario (High and Low density)
    execute("configuration/01_01_static_form_density_low.json", "RQ1_tobii_form_density_low.csv")
    execute("configuration/01_01_static_form_density_low.json", "RQ1_webgazer_form_density_low.csv")
    # execute("configuration/01_02_static_form_density_medium.json", "RQ1_tobii_form_density_medium.csv")
    # execute("configuration/01_02_static_form_density_medium.json", "RQ1_webgazer_form_density_medium.csv")
    execute("configuration/01_02_static_form_density_high.json", "RQ1_tobii_form_density_high.csv")
    execute("configuration/01_02_static_form_density_high.json", "RQ1_webgazer_form_density_high.csv")

    # RQ2 - Alternance UI Element - %Events captured - Buttons click Scenario
    execute("configuration/02_alternance_buttons.json", "RQ2_tobii_alternance_buttons.csv")
    execute("configuration/02_alternance_buttons.json", "RQ2_webgazer_alternance_buttons.csv")

    # RQ3 - Position - %Matching Fixations - Medium Density form scenario
    execute("configuration/03_position.json", "RQ3_tobii_position_50cm.csv")
    execute("configuration/03_position.json", "RQ3_tobii_position_70cm.csv")
    execute("configuration/03_position.json", "RQ3_tobii_position_90cm.csv")
    execute("configuration/03_position.json", "RQ3_webgazer_position_50cm.csv")
    execute("configuration/03_position.json", "RQ3_webgazer_position_70cm.csv")
    execute("configuration/03_position.json", "RQ3_webgazer_position_90cm.csv")

    # RQ4 - RPM - Time Matching Intersection - RPM Scenario
    execute("configuration/04_rpm.json", "RQ4_tobii_rpm.csv")
    execute("configuration/04_rpm.json", "RQ4_webgazer_rpm.csv")

    # RQX (DISCARDED) - Notification - Pop-up Noise Detection - Notification Scenario
    # Only questions
    # execute("configuration/03_notification.json", "RQ3_tobii_notification.csv")
    # execute("configuration/03_notification.json", "RQ3_webgazer_notification.csv")
    # All container
    # execute("configuration/03_02_notification_all.json", "RQ3_tobii_notification.csv")
    # execute("configuration/03_02_notification_all.json", "RQ3_webgazer_notification.csv")


print("\nCompleted!")