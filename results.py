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
    #Actualizar el valor de "Match_Fixation" en función de los segundos. Aplicable solo para el escenario de notifications
    # Calcular el tiempo total de fijaciones
    total_duration_intersecting = df[(df["Match_Fixation"] == "True") & (df["category"] == "GazeFixation")]["duration"].sum()
    # Calcular el tiempo total de no fijaciones
    total_duration_non_intersecting = total_time - total_duration_intersecting
    # Calcular la duración promedio de fijaciones que intersectan con eventos de Keyboard o MouseClick
    avg_duration_intersecting = df[(df["Match_Fixation"] == "True") & (df["category"] == "GazeFixation")]["duration"].mean().total_seconds()
    avg_duration_intersecting = round(avg_duration_intersecting, 2)
    # Calcular la duración promedio de fijaciones que no intersectan con eventos de Keyboard o MouseClick
    avg_duration_non_intersecting = df[(df["Match_Fixation"] == "False") & (df["category"] == "GazeFixation")]["duration"].mean().total_seconds()
    avg_duration_non_intersecting = round(avg_duration_non_intersecting, 2)
    
    # Number of events of Keyboard or MouseClick taken (Number of ["Match_Fixation"] == "MatchingComponentClick")
    num_total_events =  int(df["TotalEvents"].iloc[0])
    num_events_with_fixations = len(df[df["Match_Fixation"] == "BaselineComponentClick"])

    # Total Number of Fixations (["category"] == "GazeFixation")
    total_fixations = len(df[df["category"] == "GazeFixation"])
    # Total Number of Match Fixations (["Match_Fixation"] == True)
    total_match_fixations = len(pd.concat([df[df["Match_Fixation"] == "True"]]))
    # Total Number of non-Match Fixations (["Match_Fixation"] == False)
    total_non_match_fixations = len(df[df["Match_Fixation"] == "False"])
    # Mean number of fixations captured per Keyboard or MouseClick event
    avg_fixations_per_event = round(total_fixations / num_total_events, 2) if num_total_events > 0 else 0
    # Mean number of fixations match captured per Keyboard or MouseClick event (Match Fixations)
    avg_fixations_match_per_event = round(total_match_fixations / num_total_events, 2) if num_total_events > 0 else 0
    # Mean number of fixations non-match captured per Keyboard or MouseClick event (Non-Match Fixations)
    avg_fixations_non_match_per_event = round(total_non_match_fixations / num_total_events, 2) if num_total_events > 0 else 0
    # %Match Fixations: % ["Match_Fixation"] == True
    percentage_match_fixations = round(total_match_fixations / total_fixations * 100, 2) if total_fixations > 0 else 0
    # %Non-Match Fixations: % ["Match_Fixation"] == False
    percentage_non_match_fixations = round(total_non_match_fixations / total_fixations * 100, 2) if total_fixations > 0 else 0
    
    # Calcular el porcentaje de eventos que incluyen "GazeFixation" entre filas de eventos
    baseline_events = df[df["Match_Fixation"] == "BaselineComponentClick"]
    count_events_with_fixations = 1 #El ultimo evento no se cuenta, ya que es un submit y no tiene fijaciones sucesivas.
    for i in baseline_events.index:
        if i + 1 < len(df) and df.loc[i + 1, "category"] == "GazeFixation":
            count_events_with_fixations += 1
    percentage_events_with_fixations = (count_events_with_fixations / num_total_events) * 100 if len(baseline_events) > 0 else 0
    percentage_events_with_fixations = round(percentage_events_with_fixations, 2)   
    
        
    
    # Mostrar los resultados por consola
    print(f"Number of total events: {num_total_events}")
    print(f"Number of events of Keyboard or MouseClick With Fixations: {num_events_with_fixations}")
    print("\n")
    print(f"Total Number of Fixations: {total_fixations}")
    print(f"Total Number of Matching Fixations: {total_match_fixations}")
    print(f"Total Number of non-Matching Fixations: {total_non_match_fixations}")
    print(f"Mean number of fixations captured per Keyboard or MouseClick event: {avg_fixations_per_event:.2f}")
    print(f"Mean number of fixations match captured per Keyboard or MouseClick event: {avg_fixations_match_per_event:.2f}")
    print(f"Mean number of fixations non-match captured per Keyboard or MouseClick event: {avg_fixations_non_match_per_event:.2f}")
    print(f"%Matching Fixations: {percentage_match_fixations:.2f}%")
    print(f"%Non-Matching Fixations: {percentage_non_match_fixations:.2f}%")
    print(f"% of events with fixations: {percentage_events_with_fixations:.2f}%")
    print("\n")
    print(f"Total time of the test: {format_timedelta(total_time)}")
    print(f"Total duration of fixations that intersect with Keyboard or MouseClick events: {format_timedelta(total_duration_intersecting)}")
    print(f"Total duration of fixations that do not intersect with Keyboard or MouseClick events: {format_timedelta(total_duration_non_intersecting)}")
    print(f"Average duration of fixations that intersect with Keyboard or MouseClick events: {format_timedelta(avg_duration_intersecting)}")
    print(f"Average duration of fixations that do not intersect with Keyboard or MouseClick events: {format_timedelta(avg_duration_non_intersecting)}")
    print("\n")

    results = {
        "Events": num_total_events,  # "Number of events of Keyboard or MouseClick"
        "EventsIncludingFixations": num_events_with_fixations,  # "Number of events of Keyboard or MouseClick With Fixations"   
        "TotalFixations": total_fixations,  # "Total Number of Fixations"
        "TotalMatchingFixations": total_match_fixations,  # "Total Number of Matching Fixations"
        "TotalNonMatchingFixations": total_non_match_fixations,  # "Total Number of non-Matching Fixations"
        "AvgFixationsPerEvent": avg_fixations_per_event,  # "Mean number of fixations captured per Keyboard or MouseClick event"
        "%MatchingFixations": percentage_match_fixations,  # "%Matching Fixations"
        "%NonMatchingFixations": percentage_non_match_fixations,  # "%Non-Matching Fixations"
        "TotalTestTime": format_timedelta(total_time),  # "Total time of the test"
        "TotalDurationIntersecting": format_timedelta(total_duration_intersecting),  # "Total duration of fixations that intersect with Keyboard or MouseClick events"
        "TotalDurationNonIntersecting": format_timedelta(total_duration_non_intersecting),  # "Total duration of fixations that do not intersect with Keyboard or MouseClick events"
        "AvgDurationIntersecting": format_timedelta(avg_duration_intersecting),  # "Average duration of fixations that intersect with Keyboard or MouseClick events"
        "AvgDurationNonIntersecting": format_timedelta(avg_duration_non_intersecting),  # "Average duration of fixations that do not intersect with Keyboard or MouseClick events"
        "%EventsWithFixations": percentage_events_with_fixations,  # "%Events with at least one GazeFixation"
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
        print(f"Sacando métricas para tests/t1/postprocessed/{csv_test}'")
        df = pd.read_csv(f'tests/t1/postprocessed/{csv_test}')
        df.head()
        print("-----")
        metrics=calculate_metrics(df)
        metrics["Subject"] = "T1"
        metrics["Filename"] = csv_test
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
        

