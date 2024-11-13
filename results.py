#Elegir a continuación la carpeta de tests correspondiente al sujeto

import logging
import os
import pandas as pd
import time

def format_timedelta(td):
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
    avg_duration_intersecting = df[(df["Gaze_Fixation_Baseline"] == "True") & (df["category"] == "GazeFixation")]["duration"].mean()
    # Calcular la duración promedio de fijaciones que no intersectan con eventos de Keyboard o MouseClick
    avg_duration_non_intersecting = df[(df["Gaze_Fixation_Baseline"] == "False") & (df["category"] == "GazeFixation")]["duration"].mean()
    
    #Number of events of Keyboard or MouseClick taken (Number of ["Gaze_Fixation_Baseline"] == "BaselineComponentClick")
    num_events = len(df[df["Gaze_Fixation_Baseline"] == "BaselineComponentClick"])
    #Number of screenshots taken (Number of unique ["screenshot"])
    num_screenshots = df["screenshot"].nunique()
    #Total Number of Fixations (["category"] == "GazeFixation")
    total_fixations = len(df[df["category"] == "GazeFixation"])
    #Total Number of Baseline Fixations (["Gaze_Fixation_Baseline"] == True)
    total_baseline_fixations = len(df[df["Gaze_Fixation_Baseline"] == "True"])
    #Total Number of non-Baseline Fixations (["Gaze_Fixation_Baseline"] == False)
    total_non_baseline_fixations = len(df[df["Gaze_Fixation_Baseline"] == "False"])  
    #Mean number of fixations captured per Keyboard or MouseClick event 
    avg_fixations_per_event = total_fixations / num_events if num_events > 0 else 0
    #Mean number of fixations baseline captured per Keyboard or MouseClick event (Baseline Fixations)
    avg_fixations_baseline_per_event = total_baseline_fixations / num_events if num_events > 0 else 0
    #Mean number of fixations non-baseline captured per Keyboard or MouseClick event (Non-Baseline Fixations)
    avg_fixations_non_baseline_per_event = total_non_baseline_fixations / num_events if num_events > 0 else 0
    
    #%Baseline Fixations: % ["Gaze_Fixation_Baseline"] == True
    percentage_baseline_fixations = total_baseline_fixations / total_fixations * 100 if total_fixations > 0 else 0
    #%Non-Baseline Fixations: % ["Gaze_Fixation_Baseline"] == False
    percentage_non_baseline_fixations = total_non_baseline_fixations / total_fixations * 100 if total_fixations > 0 else 0
    #% de screenshots que contienen al menos algun GazeFixation (["category"] == "GazeFixation" / ["screenshot"].nunique())
    screenshots_with_fixations = df[df["category"] == "GazeFixation"]["screenshot"].nunique()
    percentage_screenshots_with_fixations = screenshots_with_fixations / num_screenshots * 100 if num_screenshots > 0 else 0
    #% de screenshots que contienen al menos algun GazeFixation Baseline (["Gaze_Fixation_Baseline"] == True / ["screenshot"].nunique())
    percentage_screenshots_with_fixations_baseline = df[(df["Gaze_Fixation_Baseline"] == "True") & (df["category"] == "GazeFixation")]["screenshot"].nunique() / num_screenshots * 100 if num_screenshots > 0 else 0
    #% de screenshots que contienen al menos algun GazeFixation no Baseline (["Gaze_Fixation_Baseline"] == False / ["screenshot"].nunique())
    percentage_screenshots_with_fixations_non_baseline = df[(df["Gaze_Fixation_Baseline"] == "False") & (df["category"] == "GazeFixation")]["screenshot"].nunique() / num_screenshots * 100 if num_screenshots > 0 else 0
    
    # Mostrar los resultados por consola
    print(f"Number of events of Keyboard or MouseClick: {num_events}")
    print(f"Number of screenshots taken: {num_screenshots}")
    print(f"Total Number of Fixations: {total_fixations}")
    print(f"Total Number of Baseline Fixations: {total_baseline_fixations}")
    print(f"Total Number of non-Baseline Fixations: {total_non_baseline_fixations}")
    print(f"Mean number of fixations captured per Keyboard or MouseClick event: {avg_fixations_per_event:.2f}")
    print(f"Mean number of fixations baseline captured per Keyboard or MouseClick event: {avg_fixations_baseline_per_event:.2f}")
    print(f"Mean number of fixations non-baseline captured per Keyboard or MouseClick event: {avg_fixations_non_baseline_per_event:.2f}")
    print(f"%Baseline Fixations: {percentage_baseline_fixations:.2f}%")
    print(f"%Non-Baseline Fixations: {percentage_non_baseline_fixations:.2f}%")
    print(f"Percentage (%) of screenshots that contain at least one GazeFixation: {percentage_screenshots_with_fixations:.2f}%")
    print(f"Percentage (%) of screenshots that contain at least one GazeFixation Baseline: {percentage_screenshots_with_fixations_baseline:.2f}%")
    print(f"Percentage (%) of screenshots that contain at least one GazeFixation non-Baseline: {percentage_screenshots_with_fixations_non_baseline:.2f}%")
    print(f"Total time of the test: {format_timedelta(total_time)}")
    print(f"Total duration of fixations that intersect with Keyboard or MouseClick events: {format_timedelta(total_duration_intersecting)}")
    print(f"Total duration of fixations that do not intersect with Keyboard or MouseClick events: {format_timedelta(total_duration_non_intersecting)}")
    print(f"Average duration of fixations that intersect with Keyboard or MouseClick events: {format_timedelta(avg_duration_intersecting)}")
    print(f"Average duration of fixations that do not intersect with Keyboard or MouseClick events: {format_timedelta(avg_duration_non_intersecting)}")
    
    results = {
        "Number of events of Keyboard or MouseClick": num_events,
        "Number of screenshots taken": num_screenshots,
        "Total Number of Fixations": total_fixations,
        "Total Number of Baseline Fixations": total_baseline_fixations,
        "Total Number of non-Baseline Fixations": total_non_baseline_fixations,
        "Mean number of fixations captured per Keyboard or MouseClick event": avg_fixations_per_event,
        "%Baseline Fixations": percentage_baseline_fixations,
        "%Non-Baseline Fixations": percentage_non_baseline_fixations,
        "Percentage of screenshots that contain at least one GazeFixation": percentage_screenshots_with_fixations,
        "Percentage of screenshots that contain at least one GazeFixation Baseline": percentage_screenshots_with_fixations_baseline,
        "Percentage of screenshots that contain at least one GazeFixation non-Baseline": percentage_screenshots_with_fixations_non_baseline,
        "Total time of the test": format_timedelta(total_time),
        "Total duration of fixations that intersect with Keyboard or MouseClick events": format_timedelta(total_duration_intersecting),
        "Total duration of fixations that do not intersect with Keyboard or MouseClick events": format_timedelta(total_duration_non_intersecting),
        "Average duration of fixations that intersect with Keyboard or MouseClick events": format_timedelta(avg_duration_intersecting),
        "Average duration of fixations that do not intersect with Keyboard or MouseClick events": format_timedelta(avg_duration_non_intersecting)
    }
    
    return results
    
    
def calculate_rq3_notification_popup(df):
    # Especificar el formato de fecha y hora
    df["time:timestamp"] = pd.to_datetime(df["time:timestamp"], format='%H:%M:%S') 
    # Ordenar el DataFrame por tiempo
    df = df.sort_values(by="time:timestamp").reset_index(drop=True)
    # Calcular el tiempo total del test
    total_time = df["time:timestamp"].max() - df["time:timestamp"].min()
    # Calcular la duración de cada evento
    df["duration"] = df["time:timestamp"].diff().shift(-1).fillna(pd.Timedelta(seconds=0))
    num_events = len(df[df["Gaze_Fixation_Baseline"] == "BaselineComponentClick"])
    total_fixations = len(df[df["category"] == "GazeFixation"])
    
    
    #Total number of fixations that intersect with the notification popup
    total_fixations_intersecting = len(df[(df["Gaze_Fixation_Baseline"] == "PopUp_True") & (df["category"] == "GazeFixation")])
    #Mean number of fixations that intersect with the notification popup per Keyboard or MouseClick event
    avg_fixations_intersecting_per_event = total_fixations_intersecting / num_events if num_events > 0 else 0
    #Percentage of fixations that intersect with the notification popup
    percentage_fixations_intersecting = total_fixations_intersecting / total_fixations * 100 if total_fixations > 0 else 0
    #Total duration of fixations that intersect with the notification popup
    total_duration_intersecting = df[(df["Gaze_Fixation_Baseline"] == "PopUp_True") & (df["category"] == "GazeFixation")]["duration"].sum()
    #Mean duration of fixations that intersect with the notification popup
    avg_duration_intersecting = df[(df["Gaze_Fixation_Baseline"] == "PopUp_True") & (df["category"] == "GazeFixation")]["duration"].mean()
    
    print(f"Total number of fixations that intersect with the notification popup: {total_fixations_intersecting}")
    print(f"Mean number of fixations that intersect with the notification popup per Keyboard or MouseClick event: {avg_fixations_intersecting_per_event:.2f}")
    print(f"Percentage (%) of fixations that intersect with the notification popup: {percentage_fixations_intersecting:.2f}%")
    print(f"Total duration of fixations that intersect with the notification popup: {format_timedelta(total_duration_intersecting)}")
    print(f"Mean duration of fixations that intersect with the notification popup: {format_timedelta(avg_duration_intersecting)}")
    
    results = {
        "Total number of fixations that intersect with the notification popup": total_fixations_intersecting,
        "Mean number of fixations that intersect with the notification popup per Keyboard or MouseClick event": avg_fixations_intersecting_per_event,
        "Percentage of fixations that intersect with the notification popup": percentage_fixations_intersecting,
        "Total duration of fixations that intersect with the notification popup": format_timedelta(total_duration_intersecting),
        "Mean duration of fixations that intersect with the notification popup": format_timedelta(avg_duration_intersecting)
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
    
for csv_test in os.listdir('tests/t1/postprocessed'):
    if csv_test.endswith('.csv'):
        print("\n" + "#" * 75)
        print(f"EXTRACTING RESULTS FROM {csv_test.upper()}...")
        print("#" * 75 + "\n")
        df = pd.read_csv(f'tests/t1/postprocessed/{csv_test}')
        metrics=calculate_metrics(df)
        metrics["Filename"] = csv_test
        all_results.append(metrics)
        
        if csv_test.endswith('_notification_postprocessed.csv'):
            print("-------------------------------------------------------------------------------")
            print("RQ3_notification extra metrics:")
            rq3_metrics = calculate_rq3_notification_popup(df)
            for key, value in rq3_metrics.items():
                metrics[key] = value
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
        

