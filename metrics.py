import logging
import pandas as pd
import os
import numpy as np
import json
from shapely.geometry import Point, Polygon
from settings import get_distance_threshold_by_resolution


def load_polygons(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    polygons_dict = {}
    for element in data["form"]["elements"]:
        group = element["group"]
        dimensions = [tuple(map(int, point.split(','))) for point in element["dimensions"]]
        if group not in polygons_dict:
            polygons_dict[group] = []
        polygons_dict[group].append(Polygon(dimensions))
    return polygons_dict

def filter_polygons_by_point(coordX, coordY, polygons):
    point = Point(coordX, coordY)
    filtered_polygons = {}
    for group, poly_list in polygons.items():
        for polygon in poly_list:
            if polygon.contains(point):
                filtered_polygons[group] = poly_list
                break  # Salir del bucle interno si se encuentra un polígono que contiene el punto
    return filtered_polygons
    
    

def polygons_group_containing_point(coordX, coordY, polygons):
    point = Point(coordX, coordY)
    polygons_group = set()
    for poly_list in polygons.values():
        for polygon in poly_list:
            if polygon.contains(point):
                polygons_group.add(poly_list)
    return polygons_group

def is_gaze_fixation_baseline(x, y, polygons, threshold):
    point = Point(x, y)
    for poly_list in polygons.values():
        for polygon in poly_list:
            if polygon.distance(point) <= threshold:
                return "True"
    return "False"

def get_polygon_group(x, y, polygons, threshold):
    point = Point(x, y)
    for group, poly_list in polygons.items():
        for polygon in poly_list:
            if polygon.distance(point) <= threshold:
                return group
   

def preprocess_df(df):
    df = df.iloc[1:] # Eliminar la primera fila del DataFrame
    # Seleccionar solo las columnas especificadas y la primera columna que indica el rowindex
    columns_to_keep = ["time:timestamp", "category", "application", "coordX", "coordY", "typed_word", "screenshot", "concept:name"]
    df = df.reset_index()[["index"] + columns_to_keep]
    # Redondear las columnas coordX y coordY a dos decimales
    df["coordX"] = df["coordX"].round(2)
    df["coordY"] = df["coordY"].round(2)
    # Añadir la columna Gaze_Fixation_target y Gaze_Fixation_id
    df["Gaze_Fixation_Baseline"] = False
    df["Gaze_Fixation_Index"] = 1
    df["Gaze_Fixation_Baseline"] = df["Gaze_Fixation_Baseline"].astype(object)
    df["Gaze_Fixation_Index"] = df["Gaze_Fixation_Index"].astype(object)

    # Encontrar el índice del último evento de MouseClick, Keyboard o DoubleMouseClick
    last_event_index = df[df["category"].isin(["MouseClick", "Keyboard", "DoubleMouseClick"])].index.max()

    # Eliminar todas las filas cuya categoría sea GazeFixation después del último evento
    if not pd.isna(last_event_index):
        df = df.drop(df[(df.index > last_event_index) & (df["category"] == "GazeFixation")].index)

    return df

def postprocess_df(df):
    df["Gaze_Fixation_Baseline"] = df["Gaze_Fixation_Baseline"].astype(object)
    df["Gaze_Fixation_Index"] = df["Gaze_Fixation_Index"].astype(object)

    df.loc[df["category"].isin(["Keyboard", "MouseClick", "DoubleMouseClick"]), "Gaze_Fixation_Index"] = ""
    df.loc[df["category"].isin(["Keyboard", "MouseClick", "DoubleMouseClick"]), "Gaze_Fixation_Baseline"] = "BaselineComponentClick"

    # Eliminar las filas que no tengan "Group" vacío
    df = df[df["Group"].notna()]

    if 'index' in df.columns:
        df = df.drop(columns=["index"])

    # Restablecer el índice
    df["index"] = 1+np.arange(len(df))
    # Mover la columna "index" a la primera posición
    cols = ['index'] + [col for col in df.columns if col != 'index']
    df = df[cols]
    
    return df

def process_RQ1_RQ2_df(df, polygons, threshold):
    fixation_index = 1
    for i in range(len(df)):
        if df.loc[i, "category"] == "GazeFixation":
            df.loc[i, "Gaze_Fixation_Index"] = fixation_index
            for j in range(i + 1, len(df)):
                next_event = df.loc[j]
                if next_event["category"] in ["Keyboard", "MouseClick", "DoubleMouseClick"]:
                    filtered_groups = filter_polygons_by_point(next_event["coordX"], next_event["coordY"], polygons)
                    group = next(iter(filtered_groups), None)  # Obtener el primer grupo del diccionario filtrado
                    # print(f"Checking point ({next_event['coordX']}, {next_event['coordY']})")
                    # print(f"Filtered groups: {filtered_groups}")
                    df.at[j, "Group"] = group
                    # print(f"Assigned group: {group}")
                    if group:
                        for k in range(i, j):
                            if df.loc[k, "category"] == "GazeFixation":
                                df.at[k, "Gaze_Fixation_Baseline"] = is_gaze_fixation_baseline(df.loc[k, "coordX"], df.loc[k, "coordY"], filtered_groups, threshold)
                                df.at[k, "Group"] = group
                    break
        elif df.loc[i, "category"] in ["Keyboard", "MouseClick", "DoubleMouseClick"]:
            fixation_index += 1

    return postprocess_df(df)


def execute_RQ1_RQ2(json_path):
    # Cargar los polígonos de las AOIs
    polygons_json = load_polygons(json_path)
    # Calcular el umbral de distancia
    threshold = get_distance_threshold_by_resolution()
    # Procesar los archivos CSV
    for filename in os.listdir(input_dir):
        if filename in ['RQ1_tobii_form_density_low.csv', 'RQ1_webgazer_form_density_low.csv']:
            input_file_path = os.path.join(input_dir, filename)
            df = pd.read_csv(input_file_path)
            preprocessed_df = preprocess_df(df)
            preprocessed_df = process_RQ1_RQ2_df(preprocessed_df, polygons_json, threshold)
            output_file_path = os.path.join(output_dir, filename.replace('.csv', '_postprocessed.csv'))
            preprocessed_df.to_csv(output_file_path, index=False)
            print(f"Preprocessed DataFrame saved to {output_file_path}")



# Directorios de entrada y salida. Elegir tests correspondiente al suejeto
input_dir = os.path.join('tests', 't1', 'preprocessed')
output_dir = os.path.join('tests', 't1', 'postprocessed')

# Crear el directorio de salida si no existe
os.makedirs(output_dir, exist_ok=True)


###Ejecuciones###
execute_RQ1_RQ2("configuration/01_01_static_form_density_low.json",)

