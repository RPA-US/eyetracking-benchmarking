#Elegir a continuación la carpeta de tests correspondiente al sujeto

import logging
import os
import pandas as pd

def format_timedelta(td):
    if isinstance(td, float):
        # Convertir segundos a Timedelta
        td = pd.to_timedelta(td, unit='s')
    if pd.isna(td):
        return "00:00:00.000"
    
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int(td.microseconds / 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

def calculate_metrics(df):
    # Especificar el formato de fecha y hora
    df["time:timestamp"] = pd.to_datetime(df["time:timestamp"], format='%H:%M:%S')
    # Ordenar el DataFrame por tiempo
    df = df.sort_values(by="time:timestamp").reset_index(drop=True)
    # Calcular el tiempo total del test
    total_time = df["time:timestamp"].max() - df["time:timestamp"].min()
    # Calcular la duración de cada evento
    df["duration"] = df["time:timestamp"].diff().shift(-1).fillna(pd.Timedelta(seconds=0))
    # Calcular el tiempo total de fijaciones
    total_duration_intersecting = df[(df["Gaze_Fixation_Baseline"] == "True") & (df["category"] == "GazeFixation")]["duration"].sum()
    # Calcular el tiempo total de no fijaciones
    total_duration_non_intersecting = total_time - total_duration_intersecting
    # Calcular la duración promedio de fijaciones que intersectan con eventos de Keyboard o MouseClick
    avg_duration_intersecting = df[(df["Gaze_Fixation_Baseline"] == "True") & (df["category"] == "GazeFixation")]["duration"].mean().total_seconds()
    avg_duration_intersecting = round(avg_duration_intersecting, 2)
    # Calcular la duración promedio de fijaciones que no intersectan con eventos de Keyboard o MouseClick
    avg_duration_non_intersecting = df[(df["Gaze_Fixation_Baseline"] == "False") & (df["category"] == "GazeFixation")]["duration"].mean().total_seconds()
    avg_duration_non_intersecting = round(avg_duration_non_intersecting, 2)
    
    # Number of events of Keyboard or MouseClick taken (Number of ["Gaze_Fixation_Baseline"] == "BaselineComponentClick")
    num_events = len(df[df["Gaze_Fixation_Baseline"] == "BaselineComponentClick"])

    # Total Number of Fixations (["category"] == "GazeFixation")
    total_fixations = len(df[df["category"] == "GazeFixation"])
    # Total Number of Baseline Fixations (["Gaze_Fixation_Baseline"] == True)
    total_baseline_fixations = len(pd.concat([
        df[df["Gaze_Fixation_Baseline"] == "True"],
        df[df["Gaze_Fixation_Baseline"] == "AOI_Name_True"]
    ]))
    # Total Number of non-Baseline Fixations (["Gaze_Fixation_Baseline"] == False)
    total_non_baseline_fixations = len(df[df["Gaze_Fixation_Baseline"] == "False"])
    # Mean number of fixations captured per Keyboard or MouseClick event
    avg_fixations_per_event = round(total_fixations / num_events, 2) if num_events > 0 else 0
    # Mean number of fixations baseline captured per Keyboard or MouseClick event (Baseline Fixations)
    avg_fixations_baseline_per_event = round(total_baseline_fixations / num_events, 2) if num_events > 0 else 0
    # Mean number of fixations non-baseline captured per Keyboard or MouseClick event (Non-Baseline Fixations)
    avg_fixations_non_baseline_per_event = round(total_non_baseline_fixations / num_events, 2) if num_events > 0 else 0
    
    # %Baseline Fixations: % ["Gaze_Fixation_Baseline"] == True
    percentage_baseline_fixations = round(total_baseline_fixations / total_fixations * 100, 2) if total_fixations > 0 else 0
    # %Non-Baseline Fixations: % ["Gaze_Fixation_Baseline"] == False
    percentage_non_baseline_fixations = round(total_non_baseline_fixations / total_fixations * 100, 2) if total_fixations > 0 else 0
    
    num_screenshots = len(df["screenshot"].unique())
   
    
    # RQ3_NOTIFICATION POPUP
    total_fixations_intersecting_pop_up = len(df[(df["Gaze_Fixation_Baseline"] == "PopUp_True") & (df["category"] == "GazeFixation")])
    # Mean number of fixations that intersect with the notification popup per Keyboard or MouseClick event
    avg_fixations_intersecting_pop_up_per_event = (total_fixations_intersecting_pop_up / num_events) if num_events > 0 else 0
    if avg_fixations_intersecting_pop_up_per_event > 0:
        avg_fixations_intersecting_pop_up_per_event = round(avg_fixations_intersecting_pop_up_per_event, 2)
    # Percentage of fixations that intersect with the notification popup
    percentage_fixations_intersecting_pop_up = (total_fixations_intersecting_pop_up / total_fixations * 100) if total_fixations > 0 else 0
    if percentage_fixations_intersecting_pop_up > 0:
        percentage_fixations_intersecting_pop_up = round(percentage_fixations_intersecting_pop_up, 2)
    # Total duration of fixations that intersect with the notification popup
    total_duration_intersecting_pop_up = df[(df["Gaze_Fixation_Baseline"] == "PopUp_True") & (df["category"] == "GazeFixation")]["duration"].sum()
    # Mean duration of fixations that intersect with the notification popup
    avg_duration_intersecting_pop_up = df[(df["Gaze_Fixation_Baseline"] == "PopUp_True") & (df["category"] == "GazeFixation")]["duration"].mean().total_seconds()
    if avg_duration_intersecting_pop_up > 0:
        avg_duration_intersecting_pop_up = round(avg_duration_intersecting_pop_up, 2)

    # RQ4_MULTISCREEN_AOI_NAME
    # Total number of fixations that intersect with the AOI_name
    total_fixations_intersecting_aoi = len(df[(df["Gaze_Fixation_Baseline"] == "AOI_Name_True") & (df["category"] == "GazeFixation")])
    avg_fixations_intersecting_aoi_per_event = (total_fixations_intersecting_aoi / num_events) if num_events > 0 else 0
    if avg_fixations_intersecting_aoi_per_event > 0:
        avg_fixations_intersecting_aoi_per_event = round(avg_fixations_intersecting_aoi_per_event, 2)
    # Percentage of fixations that intersect with the AOI_name
    percentage_fixations_intersecting_aoi = (total_fixations_intersecting_aoi / total_fixations * 100) if total_fixations > 0 else 0
    if percentage_fixations_intersecting_aoi > 0:
        percentage_fixations_intersecting_aoi = round(percentage_fixations_intersecting_aoi, 2)
    # Total duration of fixations that intersect with the AOI_name
    total_duration_intersecting_aoi = df[(df["Gaze_Fixation_Baseline"] == "AOI_Name_True") & (df["category"] == "GazeFixation")]["duration"].sum()
    # Mean duration of fixations that intersect with the AOI_name
    avg_duration_intersecting_aoi = df[(df["Gaze_Fixation_Baseline"] == "AOI_Name_True") & (df["category"] == "GazeFixation")]["duration"].mean().total_seconds()
    if avg_duration_intersecting_aoi > 0:
        avg_duration_intersecting_aoi = round(avg_duration_intersecting_aoi, 2)
    
    
    # Mostrar los resultados por consola
    print(f"Number of events of Keyboard or MouseClick: {num_events}")
    print(f"Number of screenshots taken: {num_screenshots}")
    print("\n")
    print(f"Total Number of Fixations: {total_fixations}")
    print(f"Total Number of Baseline Fixations: {total_baseline_fixations}")
    print(f"Total Number of non-Baseline Fixations: {total_non_baseline_fixations}")
    print(f"Mean number of fixations captured per Keyboard or MouseClick event: {avg_fixations_per_event:.2f}")
    print(f"Mean number of fixations baseline captured per Keyboard or MouseClick event: {avg_fixations_baseline_per_event:.2f}")
    print(f"Mean number of fixations non-baseline captured per Keyboard or MouseClick event: {avg_fixations_non_baseline_per_event:.2f}")
    print(f"%Baseline Fixations: {percentage_baseline_fixations:.2f}%")
    print(f"%Non-Baseline Fixations: {percentage_non_baseline_fixations:.2f}%")
    print("\n")
    print(f"Total time of the test: {format_timedelta(total_time)}")
    print(f"Total duration of fixations that intersect with Keyboard or MouseClick events: {format_timedelta(total_duration_intersecting)}")
    print(f"Total duration of fixations that do not intersect with Keyboard or MouseClick events: {format_timedelta(total_duration_non_intersecting)}")
    print(f"Average duration of fixations that intersect with Keyboard or MouseClick events: {format_timedelta(avg_duration_intersecting)}")
    print(f"Average duration of fixations that do not intersect with Keyboard or MouseClick events: {format_timedelta(avg_duration_non_intersecting)}")
    print("\n")
    print("------------------------------------------------------------------------------------------------------------")
    print("METRICS FOR RQ3_NOTIFICATION POPUP:")
    print(f"Total number of fixations that intersect with the notification popup: {total_fixations_intersecting_pop_up}")
    print(f"Mean number of fixations that intersect with the notification popup per Keyboard or MouseClick event: {avg_fixations_intersecting_pop_up_per_event:.2f}")
    print(f"Percentage (%) of fixations that intersect with the notification popup: {percentage_fixations_intersecting_pop_up:.2f}%")
    print(f"Total duration of fixations that intersect with the notification popup: {format_timedelta(total_duration_intersecting_pop_up)}")
    print(f"Mean duration of fixations that intersect with the notification popup: {format_timedelta(avg_duration_intersecting_pop_up)}")
    print("\n")
    print("------------------------------------------------------------------------------------------------------------")
    print("METRICS FOR RQ4_MULTISCREEN_AOI_NAME:")
    print(f"Total number of fixations that intersect with the AOI_name: {total_fixations_intersecting_aoi}")
    print(f"Mean number of fixations that intersect with the AOI_name per Keyboard or MouseClick event: {avg_fixations_intersecting_aoi_per_event:.2f}")
    print(f"Percentage (%) of fixations that intersect with the AOI_name: {percentage_fixations_intersecting_aoi:.2f}%")
    print(f"Total duration of fixations that intersect with the AOI_name: {format_timedelta(total_duration_intersecting_aoi)}")
    print(f"Mean duration of fixations that intersect with the AOI_name: {format_timedelta(avg_duration_intersecting_aoi)}")
    print("\n")

    results = {
        "NumEvents": num_events,  # "Number of events of Keyboard or MouseClick"
        "NumScreenshots": num_screenshots,  # "Number of screenshots taken"
        "TotalFixations": total_fixations,  # "Total Number of Fixations"
        "TotalBaselineFixations": total_baseline_fixations,  # "Total Number of Baseline Fixations"
        "TotalNonBaselineFixations": total_non_baseline_fixations,  # "Total Number of non-Baseline Fixations"
        "AvgFixationsPerEvent": avg_fixations_per_event,  # "Mean number of fixations captured per Keyboard or MouseClick event"
        "%BaselineFixations": percentage_baseline_fixations,  # "%Baseline Fixations"
        "%NonBaselineFixations": percentage_non_baseline_fixations,  # "%Non-Baseline Fixations"
        "TotalTestTime": format_timedelta(total_time),  # "Total time of the test"
        "TotalDurationIntersecting": format_timedelta(total_duration_intersecting),  # "Total duration of fixations that intersect with Keyboard or MouseClick events"
        "TotalDurationNonIntersecting": format_timedelta(total_duration_non_intersecting),  # "Total duration of fixations that do not intersect with Keyboard or MouseClick events"
        "AvgDurationIntersecting": format_timedelta(avg_duration_intersecting),  # "Average duration of fixations that intersect with Keyboard or MouseClick events"
        "AvgDurationNonIntersecting": format_timedelta(avg_duration_non_intersecting),  # "Average duration of fixations that do not intersect with Keyboard or MouseClick events"
        "TotalFixationsIntersectingPopup": total_fixations_intersecting_pop_up,  # "Total number of fixations that intersect with the notification popup"
        "AvgFixationsIntersectingPopupPerEvent": avg_fixations_intersecting_pop_up_per_event,  # "Mean number of fixations that intersect with the notification popup per Keyboard or MouseClick event"
        "%FixationsIntersectingPopup": percentage_fixations_intersecting_pop_up,  # "Percentage of fixations that intersect with the notification popup"
        "TotalDurationIntersectingPopup": format_timedelta(total_duration_intersecting_pop_up),  # "Total duration of fixations that intersect with the notification popup"
        "AvgDurationIntersectingPopup": format_timedelta(avg_duration_intersecting_pop_up),  # "Mean duration of fixations that intersect with the notification popup"
        "TotalFixationsIntersectingAOI": total_fixations_intersecting_aoi,  # "Total number of fixations that intersect with the AOI_name"
        "AvgFixationsIntersectingAOIPerEvent": avg_fixations_intersecting_aoi_per_event,  # "Mean number of fixations that intersect with the AOI_name per Keyboard or MouseClick event"
        "%FixationsIntersectingAOI": percentage_fixations_intersecting_aoi,  # "Percentage of fixations that intersect with the AOI_name"
        "TotalDurationIntersectingAOI": format_timedelta(total_duration_intersecting_aoi),  # "Total duration of fixations that intersect with the AOI_name"
        "AvgDurationIntersectingAOI": format_timedelta(avg_duration_intersecting_aoi)  # "Mean duration of fixations that intersect with the AOI_name"
    }

    return results

    
    
# Directorios de entrada y salida. Elegir tests correspondiente al suejeto
input_dir = os.path.join('tests', 't1', 'preprocessed')
output_dir = os.path.join('tests', 't1', 'postprocessed')
results_dir = os.path.join('tests', 't1', 'results')

# Crear el directorio de resultados si no existe
os.makedirs(results_dir, exist_ok=True)

# Lista para almacenar todos los resultados
all_results = []

columns_to_filter = [
    "TotalFixationsIntersectingPopup",
    "AvgFixationsIntersectingPopupPerEvent",
    "%FixationsIntersectingPopup",
    "TotalDurationIntersectingPopup",
    "AvgDurationIntersectingPopup",
    "TotalFixationsIntersectingAOI",
    "AvgFixationsIntersectingAOIPerEvent",
    "%FixationsIntersectingAOI",
    "TotalDurationIntersectingAOI",
    "AvgDurationIntersectingAOI"
]
    
for csv_test in os.listdir('tests/t1/postprocessed'):
    if csv_test.endswith('.csv'):
        print("\n" + "#" * 75)
        print(f"EXTRACTING RESULTS FROM {csv_test.upper()}...")
        print("#" * 75 + "\n")
        df = pd.read_csv(f'tests/t1/postprocessed/{csv_test}')
        metrics=calculate_metrics(df)
        metrics["Subject"] = "T1"
        metrics["Filename"] = csv_test
        # Eliminar los valores que sean 0 o "00:00:00.000" solo en las columnas especificadas
        metrics = {k: v for k, v in metrics.items() if k not in columns_to_filter or (v != 0 and v != "00:00:00.000")}
        all_results.append(metrics)
        print(f"PROCESSED {csv_test}!")
    else:
        logging.error("No CSV files found in the specified directory.")
        raise FileNotFoundError("No CSV postprocessed files found in the specified directory. Please, execute 'python metrics.py' in the terminal to get the postprocessed CSV files.")

# Crear un DataFrame con todos los resultados
results_df = pd.DataFrame(all_results)

# Guardar el DataFrame en un archivo CSV
results_csv_path = os.path.join(results_dir, 'results_summary.csv')
results_df.to_csv(results_csv_path, index=False)

print(f"All results saved to {results_csv_path}")
        

