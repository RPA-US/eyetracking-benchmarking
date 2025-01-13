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

def count_consecutive_baseline_clicks(df):
    # Filtrar las filas donde Match_Fixation es 'BaselineComponentClick'
    baseline_df = df[df['Match_Fixation'] == 'BaselineComponentClick']
    
    # Variable para contar las ocurrencias
    count = 0
    
    # Iterar sobre las filas del DataFrame filtrado
    for i in range(1, len(baseline_df)):
        # Comprobar si las filas son consecutivas en el índice
        if baseline_df.iloc[i-1]['index'] + 1 == baseline_df.iloc[i]['index']:
            prev_index = baseline_df.iloc[i-1]['index']
            next_index = baseline_df.iloc[i]['index']
            
            # Comprobar si no hay una fila 'GazeFixation' entre las dos
            intermediate_rows = df[(df['index'] > prev_index) & (df['index'] < next_index) & (df['category'] == 'GazeFixation')]
            
            # Si no hay filas 'GazeFixation' intermedias, incrementar el contador
            if intermediate_rows.empty:
                count += 1
    
    return count

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
    
    #Quiero calcular el numero de veces que en hay dos filas o más consecutivas con Match_Fixation BaselineCompomentClick en el df
    num_events_without_fixations = count_consecutive_baseline_clicks(df)

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
    count_events_with_fixations = num_total_events - num_events_without_fixations
    percentage_events_with_fixations = (count_events_with_fixations / num_total_events) * 100 if num_total_events > 0 else 0
    percentage_events_with_fixations = round(percentage_events_with_fixations, 2)
    
    
    #RQ4
    #TEST OBJECT y RelevantFixations   
    if "Relevant_Fixation" in df.columns:
        # Filtrar las filas donde Relevant_Fixation es "True" o "False"
        print(df.head())
        # Contar el número de filas con "True" en la columna "Relevant_Fixation"
        true_count = (df["Relevant_Fixation"] == "True").sum()
        # Contar el número de filas con "False" en la columna "Relevant_Fixation"
        false_count = (df["Relevant_Fixation"] == "False").sum()
        # Mostrar los resultados
        print(f"Número de filas con 'True': {true_count}")
        print(f"Número de filas con 'False': {false_count}")
        
        total_relevant_fixations = len(df[df["Relevant_Fixation"].isin(["True", "False"])])
        total_relevant_fixations_true = len(df[df["Relevant_Fixation"] == "True"])
        total_relevant_fixations_false = len(df[df["Relevant_Fixation"] == "False"])
    
        # Porcentaje de Relevant Fixations que son True
        percentage_relevant_fixations = round(total_relevant_fixations_true / total_relevant_fixations * 100, 2) if total_relevant_fixations > 0 else 0
    else:
        total_relevant_fixations = 0
        total_relevant_fixations_true = 0
        total_relevant_fixations_false = 0
        percentage_relevant_fixations = 0
    
    if all(col in df.columns for col in ["Target_Object", "Match_Fixation"]):
        # Filtrar las filas donde Target_Object es "True", "False" o "NA" y Match_Fixation es "BaselineComponentClick"
        events_with_target_object = len(df[(df["Target_Object"].isin(["True", "False", "NA"])) & (df["Match_Fixation"] == "BaselineComponentClick")])
    
        # Filtrar las filas donde Target_Object es "True" y Match_Fixation es "BaselineComponentClick"
        all_events_with_target_object_true = len(df[(df["Target_Object"] == "True") & (df["Match_Fixation"] == "BaselineComponentClick")])
    
        # Porcentaje de eventos con Test Object True
        percentage_events_with_target_object_true = (all_events_with_target_object_true / events_with_target_object) * 100 if events_with_target_object > 0 else 0
    else:
        events_with_target_object = 0
        all_events_with_target_object_true = 0
        percentage_events_with_target_object_true = 0

        
    
    #RESULTADOS FINALES
    results = {
        "Events": num_total_events,  # "Number of events of Keyboard or MouseClick"
        "EventsIncludingFixations": count_events_with_fixations,  # "Number of events of Keyboard or MouseClick With Fixations"   
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
        "EventsWithTestObject": events_with_target_object,  # "Total Number of events with Test Object"
        "AllEventsWithTestObjectTrue": all_events_with_target_object_true,  # "Number of events with Test Object equals True"
        "PercentageEventsWithTestObjectTrue": percentage_events_with_target_object_true,  # "% of events with Test Object equals True"
        "TotalRelevantFixations": total_relevant_fixations,  # "Total Number of Relevant Fixations"
        "TotalRelevantFixationsTrue": total_relevant_fixations_true,  # "Total Number of Relevant Fixations equals True"
        "TotalRelevantFixationsFalse": total_relevant_fixations_false,  # "Total Number of Relevant Fixations equals False"
        "%RelevantFixations": percentage_relevant_fixations  # "% of Relevant Fixations equals True"
    }
    
    # Mostrar los resultados por consola
    print(f"Number of total events: {num_total_events}")
    print(f"Number of events of Keyboard or MouseClick With Fixations: {count_events_with_fixations}")
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
    print(f"Total duration of fixations that intersect with Keyboard or MouseClick events (tMATCH_FIXATIONS): {format_timedelta(total_duration_intersecting)}")
    print(f"Total duration of fixations that do not intersect with Keyboard or MouseClick events (tNonMATCHING_FIXATIONS) : {format_timedelta(total_duration_non_intersecting)}")
    print(f"Average duration of fixations that intersect with Keyboard or MouseClick events (tMATCH_FIXATIONS): {format_timedelta(avg_duration_intersecting)}")
    print(f"Average duration of fixations that do not intersect with Keyboard or MouseClick event (tNonMATCHING_FIXATIONS): {format_timedelta(avg_duration_non_intersecting)}")
    print("\n")
    print("Only for RQ4")
    print(f"Total Number of events with Test Object: {events_with_target_object}")
    print(f"Number of events with Test Object equals True: {all_events_with_target_object_true}")
    print(f"% of events with Test Object equals True: {percentage_events_with_target_object_true:.2f}%")
    print(f"Total Number of Relevant Fixations: {total_relevant_fixations}")
    print(f"Total Number of Relevant Fixations equals True: {total_relevant_fixations_true}")
    print(f"Total Number of Relevant Fixations equals False: {total_relevant_fixations_false}")
    print(f"% of Relevant Fixations equals True: {percentage_relevant_fixations:.2f}%")
    


    return results

    
    
# Directorios de entrada y salida. Elegir tests correspondiente al suejeto
test= "t2"
input_dir = os.path.join('tests', test, 'preprocessed')
output_dir = os.path.join('tests', test, 'postprocessed')
results_dir = os.path.join('tests', test, 'results')

# Crear el directorio de resultados si no existe
os.makedirs(results_dir, exist_ok=True)

# Lista para almacenar todos los resultados
all_results = []

for csv_test in os.listdir(f'tests/{test}/postprocessed'):
    if csv_test.endswith('.csv'):
        print("\n" + "#" * 75)
        print(f"EXTRACTING RESULTS FROM {csv_test.upper()}...")
        print("#" * 75 + "\n")
        print(f"Sacando métricas para tests/{test}/postprocessed/{csv_test}'")
        df = pd.read_csv(f'tests/{test}/postprocessed/{csv_test}')
        df.head()
        print("-----")
        metrics=calculate_metrics(df)
        metrics["Subject"] = test
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
        

