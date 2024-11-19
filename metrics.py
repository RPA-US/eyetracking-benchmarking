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

def name_group_containing_point(coordX, coordY, polygons):
    point = Point(coordX, coordY)
    for group, poly_list in polygons.items():
        for polygon in poly_list:
            if polygon.contains(point):
                return group
    return None

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
    return None

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
    
    return df

def process_RQ1_df(df, polygons, threshold):
    fixation_index = 1
    for i in range(len(df)):
        if df.loc[i, "category"] == "GazeFixation":
            df.loc[i, "Gaze_Fixation_Index"] = fixation_index
            for j in range(i + 1, len(df)):
                next_event = df.loc[j]
                if next_event["category"] in ["Keyboard", "MouseClick", "DoubleMouseClick"]:
                    group = name_group_containing_point(next_event["coordX"], next_event["coordY"], polygons)
                    if group:
                        for k in range(i, j):
                            if df.loc[k, "category"] == "GazeFixation":
                                df.loc[k, "Gaze_Fixation_Baseline"] = is_gaze_fixation_baseline(df.loc[k, "coordX"], df.loc[k, "coordY"], {group: polygons[group]}, threshold)
                    break
        elif df.loc[i, "category"] in ["Keyboard", "MouseClick", "DoubleMouseClick"]:
            fixation_index += 1

    df["Gaze_Fixation_Baseline"] = df["Gaze_Fixation_Baseline"].astype(object)
    df["Gaze_Fixation_Index"] = df["Gaze_Fixation_Index"].astype(object)

    # Establecer las celdas de Gaze_Fixation_target como vacías para filas con category Keyboard o MouseClick
    df.loc[df["category"].isin(["Keyboard", "MouseClick", "DoubleMouseClick"]), "Gaze_Fixation_Baseline"] = "BaselineComponentClick"
    df.loc[df["category"].isin(["Keyboard", "MouseClick", "DoubleMouseClick"]), "Gaze_Fixation_Index"] = ""

    return df


def execute_RQ1(json_path):
    # Cargar los polígonos de las AOIs
    polygons_json = load_polygons(json_path)
    # Calcular el umbral de distancia
    threshold = get_distance_threshold_by_resolution()
    # Procesar cada archivo CSV en el directorio de entrada
    # for filename in os.listdir(input_dir):
    #     input_file_path = os.path.join(input_dir, filename)
    #     df = pd.read_csv(input_file_path)
    #     preprocessed_df = preprocess_df(df)
    #     if filename == 'RQ1_tobii_form_density_low' or filename == 'RQ1_webgazer_form_density_low':
    #         preprocessed_df = process_RQ1_df(preprocessed_df, polygons, threshold)
    #         output_file_path = os.path.join(output_dir, filename.replace('.csv', '_postprocessed.csv'))
    #         preprocessed_df.to_csv(output_file_path, index=False)
    #         print(f"Preprocessed DataFrame saved to {output_file_path}")
    #     else:
    #         logging.error("No CSV files found in the specified directory.")
    #         raise FileNotFoundError("No CSV files found in the specified directory. Please, save the preprocessed CSV files in 'tests\\tx\\preprocessed' root.")
    for filename in os.listdir(input_dir):
        if filename in ['RQ1_tobii_form_density_low.csv', 'RQ1_webgazer_form_density_low.csv']:
            input_file_path = os.path.join(input_dir, filename)
            df = pd.read_csv(input_file_path)
            preprocessed_df = preprocess_df(df)
            preprocessed_df = process_RQ1_df(preprocessed_df, polygons_json, threshold)
            output_file_path = os.path.join(output_dir, filename.replace('.csv', '_postprocessed.csv'))
            preprocessed_df.to_csv(output_file_path, index=False)
            print(f"Preprocessed DataFrame saved to {output_file_path}")
# Directorios de entrada y salida. Elegir tests correspondiente al suejeto
input_dir = os.path.join('tests', 't1', 'preprocessed')
output_dir = os.path.join('tests', 't1', 'postprocessed')

# Crear el directorio de salida si no existe
os.makedirs(output_dir, exist_ok=True)

execute_RQ1("configuration/01_01_static_form_density_low.json")

