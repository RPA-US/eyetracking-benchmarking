import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import datetime

# Crear la carpeta si no existe
os.makedirs('output/figs', exist_ok=True)

# Especificar la ruta base del proyecto y la salida deseada
base_path = "data/data_collection"



def collect_csv_files(base_path, output_file):
    """
    Función para recopilar y combinar todos los archivos CSV de un proyecto en un solo archivo.

    Args:
        base_path (str): Ruta principal del proyecto donde buscar los CSV.
        output_file (str): Ruta del archivo combinado de salida.
    """

#GRÁFICAS
output_file = "data/combined_data.csv"
data_collection_csv = pd.read_csv(output_file)

# Filtrar las filas que corresponden al Filename "RQ1_tobii_form_density_high_postprocessed.csv"
rq1_tobii_form_density_high = data_collection_csv[data_collection_csv['Filename'] == 'RQ1_tobii_form_density_high_postprocessed.csv']
rq1_tobii_form_density_low = data_collection_csv[data_collection_csv['Filename'] == 'RQ1_tobii_form_density_low_postprocessed.csv']
rq1_webgazer_form_density_high = data_collection_csv[data_collection_csv['Filename'] == 'RQ1_webgazer_form_density_high_postprocessed.csv']
rq1_webgazer_form_density_low = data_collection_csv[data_collection_csv['Filename'] == 'RQ1_webgazer_form_density_low_postprocessed.csv']

# Calcular la media de la columna %MatchingFixations
percentage_matching_fixation_rq1_tobii_form_density_low = rq1_tobii_form_density_low['%MatchingFixations'].mean()
percentage_matching_fixation_rq1_webgazer_form_density_low = rq1_webgazer_form_density_low['%MatchingFixations'].mean()
percentage_matching_fixation_rq1_tobii_form_density_high = rq1_tobii_form_density_high['%MatchingFixations'].mean()
percentage_matching_fixation_rq1_webgazer_form_density_high = rq1_webgazer_form_density_high['%MatchingFixations'].mean()

# Calcular la media de la columna MeanErrorDistance
average_error_distance_rq1_tobii_form_density_high = rq1_tobii_form_density_high['MeanErrorDistance'].mean()
average_error_distance_rq1_webgazer_form_density_high = rq1_webgazer_form_density_high['MeanErrorDistance'].mean()
average_error_distance_rq1_tobii_form_density_low = rq1_tobii_form_density_low['MeanErrorDistance'].mean()
average_error_distance_rq1_webgazer_form_density_low = rq1_webgazer_form_density_low['MeanErrorDistance'].mean()

# Datos actualizados RQ1_TC1 (Form Density Low)
data = {
    '% Matching Fixation': [percentage_matching_fixation_rq1_tobii_form_density_low,
                            percentage_matching_fixation_rq1_webgazer_form_density_low,],
    
    'Device/Software (TC1)': ['Infrared/Tobii', 'Webcam/Webgazer.js',],}

df = pd.DataFrame(data)


# Crear la gráfica
fig, ax = plt.subplots(figsize=(10, 6))
bars = plt.bar(df['Device/Software (TC1)'], df['% Matching Fixation'], 
               color=['orange', 'skyblue'])

# Etiquetas de porcentaje en las barras
for bar, pct in zip(bars, df['% Matching Fixation']):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{pct:.2f}%', ha='center', va='bottom', fontsize=10)

# Personalización del gráfico
plt.title('% Matching Fixation (%MF) by Device/Software (TC1)', fontsize=12)
plt.ylabel('% MF', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.ylim(0, 100)
plt.tight_layout()

# Guardar la gráfica
plt.savefig('output/figs/RQ1_MF_TC1.jpg')
# Mostrar la gráfica
# plt.show()

# Datos actualizados RQ1_TC1 (Form Density Low)
data = {
    '% Matching Fixation': [percentage_matching_fixation_rq1_tobii_form_density_high,
                            percentage_matching_fixation_rq1_webgazer_form_density_high,],
    
    'Device/Software (TC2)': ['Infrared/Tobii', 'Webcam/Webgazer.js',],}

df = pd.DataFrame(data)


# Crear la gráfica
fig, ax = plt.subplots(figsize=(10, 6))
bars = plt.bar(df['Device/Software (TC2)'], df['% Matching Fixation'], 
               color=['orange', 'skyblue'])

# Etiquetas de porcentaje en las barras
for bar, pct in zip(bars, df['% Matching Fixation']):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{pct:.2f}%', ha='center', va='bottom', fontsize=10)

# Personalización del gráfico
plt.title('% Matching Fixation (%MF) by Device/Software (TC2)', fontsize=12)
plt.ylabel('% MF', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.ylim(0, 100)
plt.tight_layout()

# Guardar la gráfica
plt.savefig('output/figs/RQ1_MF_TC2.jpg')
# Mostrar la gráfica
# plt.show()

# Datos actualizados RQ1_TC1 (mean MeanErrorDistance)
data = {
    'Mean Error Distance': [average_error_distance_rq1_tobii_form_density_low,
                            average_error_distance_rq1_webgazer_form_density_low,],
    
    'Device/Software (TC1)': ['Infrared/Tobii', 'Webcam/Webgazer.js',],}

df = pd.DataFrame(data)


# Crear la gráfica
fig, ax = plt.subplots(figsize=(10, 6))
bars = plt.bar(df['Device/Software (TC1)'], df['Mean Error Distance'], 
               color=['orange', 'skyblue'])

# Etiquetas de porcentaje en las barras
for bar, pct in zip(bars, df['Mean Error Distance']):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{pct:.2f}', ha='center', va='bottom', fontsize=10)

# Personalización del gráfico
plt.title('Mean Error Distance (MED) by Device/Software (TC1)', fontsize=12)
plt.ylabel('MED (px)', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.ylim(0, 60)
plt.tight_layout()

# Guardar la gráfica
plt.savefig('output/figs/RQ1_MED_TC1.jpg')
# Mostrar la gráfica
# plt.show()


# Datos actualizados RQ1_TC2 (mean MeanErrorDistance)
data = {
    'Mean Error Distance': [average_error_distance_rq1_tobii_form_density_high,
                            average_error_distance_rq1_webgazer_form_density_high,],
    
    'Device/Software (TC2)': ['Infrared/Tobii', 'Webcam/Webgazer.js',],}

df = pd.DataFrame(data)


# Crear la gráfica
fig, ax = plt.subplots(figsize=(10, 6))
bars = plt.bar(df['Device/Software (TC2)'], df['Mean Error Distance'], 
               color=['orange', 'skyblue'])

# Etiquetas de porcentaje en las barras
for bar, pct in zip(bars, df['Mean Error Distance']):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{pct:.2f}', ha='center', va='bottom', fontsize=10)

# Personalización del gráfico
plt.title('Mean Error Distance (MED) by Device/Software (TC1)', fontsize=12)
plt.ylabel('MED (px)', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.ylim(0, 60)
plt.tight_layout()

# Guardar la gráfica
plt.savefig('output/figs/RQ1_MED_TC2.jpg')
# Mostrar la gráfica
# plt.show()



############## RQ2 ##############
# Matching Fixation True by Tool/Software

rq2_tobii_alternance_buttons = data_collection_csv[data_collection_csv['Filename'] == 'RQ2_tobii_alternance_buttons_postprocessed.csv']
rq2_webgazer_alternance_buttons = data_collection_csv[data_collection_csv['Filename'] == 'RQ2_webgazer_alternance_buttons_postprocessed.csv']

percentage_matching_fixation_rq2_tobii_alternance_buttons = rq2_tobii_alternance_buttons['%MatchingFixations'].mean()
percentage_matching_fixation_rq2_webgazer_alternance_buttons = rq2_webgazer_alternance_buttons['%MatchingFixations'].mean()



new_data_rq2 = {
    '% Matching Fixation': [percentage_matching_fixation_rq2_tobii_alternance_buttons,
                            percentage_matching_fixation_rq2_webgazer_alternance_buttons],
    'Device/Software': ['Infrared/Tobii', 'Webcam/Webgazer.js']
}

new_df = pd.DataFrame(new_data_rq2)

# Crear la gráfica
fig, ax = plt.subplots(figsize=(8, 5))
bars = plt.bar(new_df['Device/Software'], new_df['% Matching Fixation'], color=['orange', 'skyblue'])

# Etiquetas de porcentaje en las barras
for bar, pct in zip(bars, new_df['% Matching Fixation']):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{pct:.2f}%', ha='center', va='bottom', fontsize=10)

# Personalización del gráfico
plt.title('% Matching Fixations (%MF) by Device/Software (TC3)', fontsize=14)
plt.ylabel('% MF', fontsize=12)
plt.xticks(rotation=0, ha='center', fontsize=10)
plt.ylim(0, 100)
plt.tight_layout()

# Guardar la gráfica
plt.savefig('output/figs/RQ2_MF_TC3.jpg')
# Mostrar la gráfica


percentage_events_including_fixations_rq2_tobii_alternance_buttons = rq2_tobii_alternance_buttons['%EventsWithFixations'].mean()
percetange_events_including_fixations_rq2_webgazer_alternance_buttons = rq2_webgazer_alternance_buttons['%EventsWithFixations'].mean()

# Datos %Event Including Captured Fixations
tools = [ "Infrared/Tobii","Webcam/Webgazer.js",]
percentages = [percentage_events_including_fixations_rq2_tobii_alternance_buttons,
               percetange_events_including_fixations_rq2_webgazer_alternance_buttons]

# Crear la gráfica
fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(tools, percentages, color=['orange','skyblue'])

# Añadir etiquetas y título
ax.set_ylabel("% EIF")
ax.set_title("% Events Including Fixation (EIF) by Device/Software (TC3)")
ax.set_ylim(0, 110)  # Limitar el eje Y para espacio adicional

# Mostrar porcentaje en las barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 2,
            f'{height:.2f}%', ha='center', va='bottom')

# Guardar la gráfica
plt.tight_layout()
plt.savefig('output/figs/RQ2_EIF_TC3.jpg')
# Mostrar gráfico
# plt.show()


average_error_distance_rq2_tobii_alternance_buttons = rq2_tobii_alternance_buttons['MeanErrorDistance'].mean()
average_error_distance_rq2_webgazer_alternance_buttons = rq2_webgazer_alternance_buttons['MeanErrorDistance'].mean()

# Datos actualizados RQ1_TC2 (mean MeanErrorDistance)
data = {
    'Mean Error Distance': [average_error_distance_rq2_tobii_alternance_buttons,
                            average_error_distance_rq2_webgazer_alternance_buttons,],
    
    'Device/Software': ['Infrared/Tobii', 'Webcam/Webgazer.js',],}

df = pd.DataFrame(data)


# Crear la gráfica
fig, ax = plt.subplots(figsize=(10, 6))
bars = plt.bar(df['Device/Software'], df['Mean Error Distance'], 
               color=['orange', 'skyblue'])

# Etiquetas de porcentaje en las barras
for bar, pct in zip(bars, df['Mean Error Distance']):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{pct:.2f}', ha='center', va='bottom', fontsize=10)

# Personalización del gráfico
plt.title('Mean Error Distance (MED) by Device/Software (TC3)', fontsize=12)
plt.ylabel('MED (px)', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.ylim(0, 100)
plt.tight_layout()

# Guardar la gráfica
plt.savefig('output/figs/RQ2_MED_TC3.jpg')
# Mostrar la gráfica
# plt.show()


############## RQ3 ##############
# Datos grafica barras events_captured_fixations

rq3__tobii_position_50cm = data_collection_csv[data_collection_csv['Filename'] == 'RQ3_tobii_position_50cm_postprocessed.csv']
rq3__tobii_position_70cm = data_collection_csv[data_collection_csv['Filename'] == 'RQ3_tobii_position_70cm_postprocessed.csv']
rq3__tobii_position_90cm = data_collection_csv[data_collection_csv['Filename'] == 'RQ3_tobii_position_90cm_postprocessed.csv']
rq3__webgazer_position_50cm = data_collection_csv[data_collection_csv['Filename'] == 'RQ3_webgazer_position_50cm_postprocessed.csv']
rq3__webgazer_position_70cm = data_collection_csv[data_collection_csv['Filename'] == 'RQ3_webgazer_position_70cm_postprocessed.csv']
rq3__webgazer_position_90cm = data_collection_csv[data_collection_csv['Filename'] == 'RQ3_webgazer_position_90cm_postprocessed.csv']

percentage_events_including_fixations_rq3_tobii_position_50cm = rq3__tobii_position_50cm['%EventsWithFixations'].mean()
percentage_events_including_fixations_rq3_tobii_position_70cm = rq3__tobii_position_70cm['%EventsWithFixations'].mean()
percentage_events_including_fixations_rq3_tobii_position_90cm = rq3__tobii_position_90cm['%EventsWithFixations'].mean()

percentage_events_including_fixations_rq3_webgazer_position_50cm = rq3__webgazer_position_50cm['%EventsWithFixations'].mean()
percentage_events_including_fixations_rq3_webgazer_position_70cm = rq3__webgazer_position_70cm['%EventsWithFixations'].mean()
percentage_events_including_fixations_rq3_webgazer_position_90cm = rq3__webgazer_position_90cm['%EventsWithFixations'].mean()

positions = ["TC4 (50cm)", "TC5 (70cm)", "TC6 (90cm)"]
percentages_tobii = [percentage_events_including_fixations_rq3_tobii_position_50cm,
                     percentage_events_including_fixations_rq3_tobii_position_70cm,
                     percentage_events_including_fixations_rq3_tobii_position_90cm]

percentages_webgazer = [percentage_events_including_fixations_rq3_webgazer_position_50cm,
                        percentage_events_including_fixations_rq3_webgazer_position_70cm,
                        percentage_events_including_fixations_rq3_webgazer_position_90cm]

x = np.arange(len(positions))  # Posiciones para las etiquetas del eje X
width = 0.35  # Ancho de las barras

# Crear figura y ejes
fig, ax = plt.subplots(figsize=(8, 5))
bars_tobii = ax.bar(x + width/2, percentages_tobii, width, label="Infrared/Tobii", color='orange')
bars_webgazer = ax.bar(x - width/2, percentages_webgazer, width, label="Webcam/Webgazer.js", color='skyblue')

# Añadir etiquetas y título
ax.set_xlabel("Test Case (Distance from subject to screen)")
ax.set_ylabel("% EIF")
ax.set_title("% Events Including Fixation (%EIF) by Device/Software and Distance (TC4,TC5,TC6)")
ax.set_xticks(x)
ax.set_xticklabels(positions)
ax.legend()

# Mostrar porcentaje en las barras
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{height:.2f}%', ha='center', va='bottom')

add_labels(bars_webgazer)
add_labels(bars_tobii)

# Guardar la gráfica
plt.tight_layout()
plt.savefig('output/figs/RQ3_EIF_TC4_TC5_TC6_bars.jpg')
# Mostrar gráfico
# plt.show()

# Datos grafico linea events_captured_fixations

percentage_events_including_fixations_rq3_tobii_position_50cm = rq3__tobii_position_50cm['%EventsWithFixations'].mean()
percentage_events_including_fixations_rq3_tobii_position_70cm = rq3__tobii_position_70cm['%EventsWithFixations'].mean()
percentage_events_including_fixations_rq3_tobii_position_90cm = rq3__tobii_position_90cm['%EventsWithFixations'].mean()

percentage_events_including_fixations_rq3_webgazer_position_50cm = rq3__webgazer_position_50cm['%EventsWithFixations'].mean()
percentage_events_including_fixations_rq3_webgazer_position_70cm = rq3__webgazer_position_70cm['%EventsWithFixations'].mean()
percentage_events_including_fixations_rq3_webgazer_position_90cm = rq3__webgazer_position_90cm['%EventsWithFixations'].mean()

positions = ["TC4 (50cm)", "TC5 (70cm)", "TC6 (90cm)"]
percentages_tobii = [percentage_events_including_fixations_rq3_tobii_position_50cm,
                     percentage_events_including_fixations_rq3_tobii_position_70cm,
                     percentage_events_including_fixations_rq3_tobii_position_90cm]

percentages_webgazer = [percentage_events_including_fixations_rq3_webgazer_position_50cm,
                        percentage_events_including_fixations_rq3_webgazer_position_70cm,
                        percentage_events_including_fixations_rq3_webgazer_position_90cm]

# Crear la gráfica
plt.figure(figsize=(8, 5))
plt.plot(positions, percentages_tobii, marker='o', label="Infrared/Tobii", color='orange')
plt.plot(positions, percentages_webgazer, marker='o', label="Webcam/Webgazer.js", color='skyblue')

# Añadir etiquetas, título y leyenda
plt.xlabel("Test Case (Distance from subject to screen)")
plt.ylabel("% EIF")
plt.title("% Events Including Fixation (%EIF) by Device/Software and Distance (TC4,TC5,TC6)")
plt.ylim(0, 110)  # Limitar el eje Y al rango de 0 a 110
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

# Guardar la gráfica
plt.tight_layout()
plt.savefig('output/figs/RQ3_EIF_TC4_TC5_TC6_line.jpg')
# Mostrar la gráfica 
# plt.show()

# Datos grafica matching fixations barras

percentage_matching_fixation_rq3_tobii_position_50cm = rq3__tobii_position_50cm['%MatchingFixations'].mean()
percentage_matching_fixation_rq3_tobii_position_70cm = rq3__tobii_position_70cm['%MatchingFixations'].mean()
percentage_matching_fixation_rq3_tobii_position_90cm = rq3__tobii_position_90cm['%MatchingFixations'].mean()
percentage_matching_fixation_rq3_webgazer_position_50cm = rq3__webgazer_position_50cm['%MatchingFixations'].mean()
percentage_matching_fixation_rq3_webgazer_position_70cm = rq3__webgazer_position_70cm['%MatchingFixations'].mean()
percentage_matching_fixation_rq3_webgazer_position_90cm = rq3__webgazer_position_90cm['%MatchingFixations'].mean()

tools = ["Infrared/Tobii","Webcam/Webgazer.js"]
positions = ["TC4 (50cm)", "TC5 (70cm)", "TC6 (90cm)"]
percentages_tobii = [percentage_matching_fixation_rq3_tobii_position_50cm,
                     percentage_matching_fixation_rq3_tobii_position_70cm,
                     percentage_matching_fixation_rq3_tobii_position_90cm]
percentages_webgazer = [percentage_matching_fixation_rq3_webgazer_position_50cm,
                        percentage_matching_fixation_rq3_webgazer_position_70cm,
                        percentage_matching_fixation_rq3_webgazer_position_90cm]

x = np.arange(len(positions))  # Posiciones para las etiquetas del eje X
width = 0.35  # Ancho de las barras

# Crear figura y ejes
fig, ax = plt.subplots(figsize=(8, 5))
bars_tobii = ax.bar(x - width/2, percentages_tobii, width, label="Infrared/Tobii", color='orange')
bars_webgazer = ax.bar(x + width/2, percentages_webgazer, width, label="Webcam/Webgazer.js", color='skyblue')

# Añadir etiquetas y título
ax.set_xlabel("Position")
ax.set_ylabel("% MF")
ax.set_title("% Matching Fixation (%MF) by Device/Software and Distance (TC4,TC5,TC6)")
ax.set_xticks(x)
ax.set_xticklabels(positions)
ax.set_ylim(0, 100)
ax.legend()

# Mostrar porcentaje en las barras
add_labels(bars_tobii)
add_labels(bars_webgazer)

# Guardar la gráfica
plt.tight_layout()
plt.savefig('output/figs/RQ3_MF_TC4_TC5_TC6_bar.jpg')
# Mostrar gráfico
# plt.show()


# Datos Matching fixations linea
positions = ["TC4 (50cm)", "TC5 (70cm)", "TC6 (90cm)"]
percentages_tobii = [percentage_matching_fixation_rq3_tobii_position_50cm,
                     percentage_matching_fixation_rq3_tobii_position_70cm,
                     percentage_matching_fixation_rq3_tobii_position_90cm]
percentages_webgazer = [percentage_matching_fixation_rq3_webgazer_position_50cm,
                        percentage_matching_fixation_rq3_webgazer_position_70cm,
                        percentage_matching_fixation_rq3_webgazer_position_90cm]

# Crear la gráfica
plt.figure(figsize=(8, 5))
plt.plot(positions, percentages_tobii, marker='o', label="Infrared/Tobii", color='orange')
plt.plot(positions, percentages_webgazer, marker='o', label="Webcam/Webgazer.js", color='skyblue')

# Añadir etiquetas, título y leyenda
plt.xlabel("Position")
plt.ylabel("% MF")
plt.title("% Matching Fixations (%MF) by Device/Software and Distance (TC4,TC5,TC6)")
plt.ylim(0, 100)  # Limitar el eje Y al rango de 0 a 100
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

# Guardar la gráfica
plt.tight_layout()
plt.savefig('output/figs/RQ3_MF_TC4_TC5_TC6_line.jpg')
# Mostrar la gráfica
# plt.show()


# Datos mean MeanErrorDistance RQ3
average_error_distance_rq3_tobii_position_50cm = rq3__tobii_position_50cm['MeanErrorDistance'].mean()
average_error_distance_rq3_tobii_position_70cm = rq3__tobii_position_70cm['MeanErrorDistance'].mean()
average_error_distance_rq3_tobii_position_90cm = rq3__tobii_position_90cm['MeanErrorDistance'].mean()
average_error_distance_rq3_webgazer_position_50cm = rq3__webgazer_position_50cm['MeanErrorDistance'].mean()
average_error_distance_rq3_webgazer_position_70cm = rq3__webgazer_position_70cm['MeanErrorDistance'].mean()
average_error_distance_rq3_webgazer_position_90cm = rq3__webgazer_position_90cm['MeanErrorDistance'].mean()

positions = ["TC4 (50cm)", "TC5 (70cm)", "TC6 (90cm)"]
med_tobii = [average_error_distance_rq3_tobii_position_50cm,
             average_error_distance_rq3_tobii_position_70cm,
             average_error_distance_rq3_tobii_position_90cm]
med_webgazer = [average_error_distance_rq3_webgazer_position_50cm,
                average_error_distance_rq3_webgazer_position_70cm,
                average_error_distance_rq3_webgazer_position_90cm]

x = np.arange(len(positions))  # Posiciones para las etiquetas del eje X
width = 0.35  # Ancho de las barras

# Crear figura y ejes
fig, ax = plt.subplots(figsize=(8, 5))
bars_tobii = ax.bar(x - width/2, med_tobii, width, label="Infrared/Tobii", color='orange')
bars_webgazer = ax.bar(x + width/2, med_webgazer, width, label="Webcam/Webgazer.js", color='skyblue')

# Añadir etiquetas y título
ax.set_xlabel("Position")
ax.set_ylabel("MED (px)")
ax.set_title("Mean Error Distance (MED) by Device/Software and Distance (TC4,TC5,TC6)")
ax.set_xticks(x)
ax.set_xticklabels(positions)
ax.set_ylim(0, max(max(med_tobii), max(med_webgazer)) + 10)
ax.legend()

# Mostrar valores en las barras
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.2f}', ha='center', va='bottom')

add_labels(bars_tobii)
add_labels(bars_webgazer)

# Guardar la gráfica
plt.tight_layout()
plt.savefig('output/figs/RQ3_MED_TC4_TC5_TC6.jpg')
# Mostrar la gráfica
# plt.show()


############## RQ4 ##############

rq4_tobii_rpm = data_collection_csv[data_collection_csv['Filename'] == 'RQ4_tobii_rpm_postprocessed.csv']
rq4_webgazer_rpm = data_collection_csv[data_collection_csv['Filename'] == 'RQ4_webgazer_rpm_postprocessed.csv']

percentage_events_including_test_object_fixations_rq4_tobii_rpm = rq4_tobii_rpm['PercentageEventsWithTestObjectTrue'].mean()
percentage_events_including_test_object_fixations_rq4_webgazer_rpm = rq4_webgazer_rpm['PercentageEventsWithTestObjectTrue'].mean()

# Datos %Event Including Relevant Fixations
tools = [ "Infrared/Tobii","Webcam/Webgazer.js"]
percentages = [percentage_events_including_test_object_fixations_rq4_tobii_rpm, 
               percentage_events_including_test_object_fixations_rq4_webgazer_rpm]

# Crear la gráfica
fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(tools, percentages, color=[ 'orange','skyblue',])

# Añadir etiquetas y título
ax.set_ylabel("% EITOF")
ax.set_title("%Events Including Test Object Fixations (%EITOF) by Device/Software (TC7)")
ax.set_ylim(0, 110)  # Limitar el eje Y para espacio adicional

# Mostrar porcentaje en las barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 2,
            f'{height:.2f}%', ha='center', va='bottom')

# Guardar la gráfica
plt.tight_layout()
plt.savefig('output/figs/RQ4_EITOF_TC7.jpg')
# Mostrar gráfico
# plt.show()

# Datos %Matching_test_object_fixations
percentage_matching_test_object_fixations_rq4_tobii_rpm = rq4_tobii_rpm['%RelevantFixations'].mean()
percentage_matching_test_object_fixations_rq4_webgazer_rpm = rq4_webgazer_rpm['%RelevantFixations'].mean()


tools = ["Infrared/Tobii", "Webcam/Webgazer.js"]
percentages = [percentage_matching_test_object_fixations_rq4_tobii_rpm,
               percentage_matching_test_object_fixations_rq4_webgazer_rpm]

# Crear la gráfica
fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(tools, percentages, color=[ 'orange','skyblue',])

# Añadir etiquetas y título
ax.set_ylabel("% MTOF")
ax.set_title("% Matching Test Object Fixations (%MTOF) by Device/Software (TC7)")
ax.set_ylim(0, 110)  # Limitar el eje Y para espacio adicional

# Mostrar porcentaje en las barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 2,
            f'{height:.2f}%', ha='center', va='bottom')

# Guardar la gráfica
plt.tight_layout()
plt.savefig('output/figs/RQ4_MTOF_TC7.jpg')
# Mostrar gráfico
# plt.show()


print("Plots correctly generated in folder: output/figs")


# Crear un DataFrame para almacenar todos los resultados
final_results = []

# RQ1 Matching Fixation por Device y Test Case Scenario
rq1_data = [
    ['Infrared/Tobii', 'TC1', round(percentage_matching_fixation_rq1_tobii_form_density_low, 2)],
    ['Infrared/Tobii', 'TC2', round(percentage_matching_fixation_rq1_tobii_form_density_high, 2)],
    ['Webcam/Webgazer.js', 'TC1', round(percentage_matching_fixation_rq1_webgazer_form_density_low, 2)],
    ['Webcam/Webgazer.js', 'TC2', round(percentage_matching_fixation_rq1_webgazer_form_density_high, 2)]
]
df_rq1 = pd.DataFrame(rq1_data, columns=['Device/Software', 'TC', '% MF'])
final_results.append(df_rq1)

rq1_med = [
    ['Infrared/Tobii', 'TC1', round(average_error_distance_rq1_tobii_form_density_low, 2)],
    ['Infrared/Tobii', 'TC2', round(average_error_distance_rq1_tobii_form_density_high, 2)],
    ['Webcam/Webgazer.js', 'TC1', round(average_error_distance_rq1_webgazer_form_density_low, 2)],
    ['Webcam/Webgazer.js', 'TC2', round(average_error_distance_rq1_webgazer_form_density_high, 2)],
]
df_rq1_med = pd.DataFrame(rq1_med, columns=['Device/Software', 'TC', 'MED (px)'])
final_results.append(df_rq1_med)

# RQ2 Matching Fixation True por Tool/Software
rq2_data = [
    ['Infrared/Tobii', 'TC3', round(percentage_matching_fixation_rq2_tobii_alternance_buttons, 2)],
    ['Webcam/Webgazer.js', 'TC3', round(percentage_matching_fixation_rq2_webgazer_alternance_buttons, 2)]
]
df_rq2 = pd.DataFrame(rq2_data, columns=['Device/Software', 'TC', '% MF'])
final_results.append(df_rq2)

# RQ2 Events Including Fixations por Tool/Software
rq2_eif_data = [
    ['Infrared/Tobii', 'TC3', round(percentage_events_including_fixations_rq2_tobii_alternance_buttons, 2)],
    ['Webcam/Webgazer.js', 'TC3', round(percetange_events_including_fixations_rq2_webgazer_alternance_buttons, 2)]
]
df_rq2_eif = pd.DataFrame(rq2_eif_data, columns=['Device/Software', 'TC', '% EIF'])
final_results.append(df_rq2_eif)

rq2_med = [
    ['Infrared/Tobii', 'TC3', round(average_error_distance_rq2_tobii_alternance_buttons, 2)],
    ['Webcam/Webgazer.js', 'TC3', round(average_error_distance_rq2_webgazer_alternance_buttons, 2)]
]
df_rq2_med = pd.DataFrame(rq2_med, columns=['Device/Software', 'TC', 'MED (px)'])
final_results.append(df_rq2_med)

# RQ3 Events Including Fixations por Device y Distance
rq3_eif_data = [
    ['Infrared/Tobii', 'TC4', round(percentage_events_including_fixations_rq3_tobii_position_50cm, 2)],
    ['Infrared/Tobii', 'TC5', round(percentage_events_including_fixations_rq3_tobii_position_70cm, 2)],
    ['Infrared/Tobii', 'TC6', round(percentage_events_including_fixations_rq3_tobii_position_90cm, 2)],
    ['Webcam/Webgazer.js', 'TC4', round(percentage_events_including_fixations_rq3_webgazer_position_50cm, 2)],
    ['Webcam/Webgazer.js', 'TC5', round(percentage_events_including_fixations_rq3_webgazer_position_70cm, 2)],
    ['Webcam/Webgazer.js', 'TC6', round(percentage_events_including_fixations_rq3_webgazer_position_90cm, 2)]
]
df_rq3_eif = pd.DataFrame(rq3_eif_data, columns=['Device/Software', 'TC', '% EIF'])
final_results.append(df_rq3_eif)

# RQ3 Matching Fixation por Device y Distance
rq3_mf_data = [
    ['Infrared/Tobii', 'TC4', round(percentage_matching_fixation_rq3_tobii_position_50cm, 2)],
    ['Infrared/Tobii', 'TC5', round(percentage_matching_fixation_rq3_tobii_position_70cm, 2)],
    ['Infrared/Tobii', 'TC6', round(percentage_matching_fixation_rq3_tobii_position_90cm, 2)],
    ['Webcam/Webgazer.js', 'TC4', round(percentage_matching_fixation_rq3_webgazer_position_50cm, 2)],
    ['Webcam/Webgazer.js', 'TC5', round(percentage_matching_fixation_rq3_webgazer_position_70cm, 2)],
    ['Webcam/Webgazer.js', 'TC6', round(percentage_matching_fixation_rq3_webgazer_position_90cm, 2)]
]
df_rq3_mf = pd.DataFrame(rq3_mf_data, columns=['Device/Software', 'TC', '% MF'])
final_results.append(df_rq3_mf)

rq3_med = [
    ['Infrared/Tobii', 'TC4', round(average_error_distance_rq3_tobii_position_50cm, 2)],
    ['Infrared/Tobii', 'TC5', round(average_error_distance_rq3_tobii_position_70cm, 2)],
    ['Infrared/Tobii', 'TC6', round(average_error_distance_rq3_tobii_position_90cm, 2)],
    ['Webcam/Webgazer.js', 'TC4', round(average_error_distance_rq3_webgazer_position_50cm, 2)],
    ['Webcam/Webgazer.js', 'TC5', round(average_error_distance_rq3_webgazer_position_70cm, 2)],
    ['Webcam/Webgazer.js', 'TC6', round(average_error_distance_rq3_webgazer_position_90cm, 2)]
]
df_rq3_med = pd.DataFrame(rq3_med, columns=['Device/Software', 'TC', 'MED (px)'])
final_results.append(df_rq3_med)

# RQ4 Events Including Test Object Fixations por Device
rq4_eitof_data = [
    ['Infrared/Tobii', 'TC7', round(percentage_events_including_test_object_fixations_rq4_tobii_rpm, 2)],
    ['Webcam/Webgazer.js', 'TC7', round(percentage_events_including_test_object_fixations_rq4_webgazer_rpm, 2)]
]
df_rq4_eitof = pd.DataFrame(rq4_eitof_data, columns=['Device/Software', 'TC', '% EITOF'])
final_results.append(df_rq4_eitof)

# RQ4 Matching Test Object Fixations por Device
rq4_mtof_data = [
    ['Infrared/Tobii', 'TC7', round(percentage_matching_test_object_fixations_rq4_tobii_rpm, 2)],
    ['Webcam/Webgazer.js', 'TC7', round(percentage_matching_test_object_fixations_rq4_webgazer_rpm, 2)]
]
df_rq4_mtof = pd.DataFrame(rq4_mtof_data, columns=['Device/Software', 'TC', '% MTOF'])
final_results.append(df_rq4_mtof)

# Combinar todos los DataFrames en uno solo
final_df = pd.concat(final_results, ignore_index=True)

# Consolidar filas duplicadas combinando valores
final_df = final_df.groupby(["Device/Software", "TC"]).max().reset_index()

# Obtener el timestamp actual
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Crear el nombre del archivo con el timestamp
output_csv_path = f'output/final_results_exp_{timestamp}.csv'

# Guardar el DataFrame en el archivo CSV con el nombre generado
final_df.to_csv(output_csv_path, index=False)

print(f"Datos guardados correctamente en: {output_csv_path}")


