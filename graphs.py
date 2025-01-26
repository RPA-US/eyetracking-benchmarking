import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# Crear la carpeta si no existe
os.makedirs('tests/figs', exist_ok=True)

# Especificar la ruta base del proyecto y la salida deseada
base_path = "data/data_collection"
output_file = "data/combined_data.csv"


def collect_csv_files(base_path, output_file):
    """
    Función para recopilar y combinar todos los archivos CSV de un proyecto en un solo archivo.

    Args:
        base_path (str): Ruta principal del proyecto donde buscar los CSV.
        output_file (str): Ruta del archivo combinado de salida.
    """
    # Lista para almacenar los DataFrames
    combined_data = []

    # Recorrer todas las subcarpetas y archivos
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.csv'):  # Identificar archivos CSV
                file_path = os.path.join(root, file)
                try:
                    # Leer cada CSV y añadirlo a la lista
                    df = pd.read_csv(file_path)
                    combined_data.append(df)
                    print(f"Archivo leído: {file_path}")
                except Exception as e:
                    print(f"Error al leer {file_path}: {e}")

    if combined_data:
        # Combinar todos los DataFrames
        combined_df = pd.concat(combined_data, ignore_index=True)

        # Guardar en el archivo de salida
        try:
            combined_df.to_csv(output_file, index=False)
            print(f"Archivo combinado guardado en: {output_file}")
        except Exception as e:
            print(f"Error al guardar el archivo combinado: {e}")
    else:
        print("No se encontraron archivos CSV para combinar.")

#GRÁFICAS
collect_csv_files(base_path, output_file)
data_collection_csv = pd.read_csv(output_file)

# Filtrar las filas que corresponden al Filename "RQ1_tobii_form_density_high_postprocessed.csv"
rq1_tobii_form_density_high = data_collection_csv[data_collection_csv['Filename'] == 'RQ1_tobii_form_density_high_postprocessed.csv']
rq1_tobii_form_density_low = data_collection_csv[data_collection_csv['Filename'] == 'RQ1_tobii_form_density_low_postprocessed.csv']
rq1_webgazer_form_density_high = data_collection_csv[data_collection_csv['Filename'] == 'RQ1_webgazer_form_density_high_postprocessed.csv']
rq1_webgazer_form_density_low = data_collection_csv[data_collection_csv['Filename'] == 'RQ1_webgazer_form_density_low_postprocessed.csv']

# Calcular la media de la columna %MatchingFixations
percentage_matching_fixation_rq1_webgazer_form_density_low = rq1_webgazer_form_density_low['%MatchingFixations'].mean()
percentage_matching_fixation_rq1_tobii_form_density_high = rq1_tobii_form_density_high['%MatchingFixations'].mean()
percentage_matching_fixation_rq1_tobii_form_density_low = rq1_tobii_form_density_low['%MatchingFixations'].mean()
percentage_matching_fixation_rq1_webgazer_form_density_high = rq1_webgazer_form_density_high['%MatchingFixations'].mean()

# Datos actualizados RQ1
data = {
    '% Matching Fixation': [percentage_matching_fixation_rq1_tobii_form_density_high,
                            percentage_matching_fixation_rq1_tobii_form_density_low,
                            percentage_matching_fixation_rq1_webgazer_form_density_high,
                            percentage_matching_fixation_rq1_webgazer_form_density_low],
    
    'Tool/Software': ['Infrared/Tobii', 'Infrared/Tobii', 'Webcam/Webgazer.js', 'Webcam/Webgazer.js'],
    'Scenario': ['Form High Density', 'Form Low Density', 'Form High Density', 'Form Low Density']
}

df = pd.DataFrame(data)
df['Tool/Software (Scenario)'] = df['Tool/Software'] + ' (' + df['Scenario'] + ')'

# Crear la gráfica
fig, ax = plt.subplots(figsize=(10, 6))
bars = plt.bar(df['Tool/Software (Scenario)'], df['% Matching Fixation'], 
               color=['orange', 'green', 'red', 'blue'])

# Etiquetas de porcentaje en las barras
for bar, pct in zip(bars, df['% Matching Fixation']):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{pct:.2f}%', ha='center', va='bottom', fontsize=10)

# Personalización del gráfico
plt.title('% Matching Fixation by Tool/Software and Scenario', fontsize=14)
plt.ylabel('% Matching Fixation', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.ylim(0, 100)
plt.tight_layout()

# Guardar la gráfica
plt.savefig('tests/figs/RQ1_matching_fixations.jpg')
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
    'Tool/Software': ['Infrared/Tobii', 'Webcam/Webgazer.js']
}

new_df = pd.DataFrame(new_data_rq2)

# Crear la gráfica
fig, ax = plt.subplots(figsize=(8, 5))
bars = plt.bar(new_df['Tool/Software'], new_df['% Matching Fixation'], color=['orange', 'skyblue'])

# Etiquetas de porcentaje en las barras
for bar, pct in zip(bars, new_df['% Matching Fixation']):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{pct:.2f}%', ha='center', va='bottom', fontsize=10)

# Personalización del gráfico
plt.title('% Matching Fixation by Tool/Software', fontsize=14)
plt.ylabel('% Matching Fixation', fontsize=12)
plt.xticks(rotation=0, ha='center', fontsize=10)
plt.ylim(0, 100)
plt.tight_layout()

# Guardar la gráfica
plt.savefig('tests/figs/RQ2_Matching_fixation.jpg')
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
ax.set_ylabel("% Event Including Captured Fixations")
ax.set_title("Comparison of Tools: %Event Including Captured Fixations")
ax.set_ylim(0, 110)  # Limitar el eje Y para espacio adicional

# Mostrar porcentaje en las barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 2,
            f'{height:.2f}%', ha='center', va='bottom')

# Guardar la gráfica
plt.tight_layout()
plt.savefig('tests/figs/RQ2_events_including_fixations.jpg')
# Mostrar gráfico
# plt.show()


############## RQ3 ##############
# Datos grafica barras events_captured_fixations
tools = ["Infrared/Tobii","Webcam/Webgazer.js"]
positions = ["50cm", "70cm", "90cm"]
percentages_tobii = [100.00, 100.00, 40.00]
percentages_webgazer = [100.00, 100.00, 100.00]

x = np.arange(len(positions))  # Posiciones para las etiquetas del eje X
width = 0.35  # Ancho de las barras

# Crear figura y ejes
fig, ax = plt.subplots(figsize=(8, 5))
bars_tobii = ax.bar(x + width/2, percentages_tobii, width, label="Infrared/Tobii", color='orange')
bars_webgazer = ax.bar(x - width/2, percentages_webgazer, width, label="Webcam/Webgazer.js", color='skyblue')

# Añadir etiquetas y título
ax.set_xlabel("Position")
ax.set_ylabel("% Event Including Captured Fixations")
ax.set_title("Comparison of Tools by Distance")
ax.set_xticks(x)
ax.set_xticklabels(positions)
ax.legend()

# Mostrar porcentaje en las barras
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{height:.2f}%', ha='center', va='bottom')

add_labels(bars_tobii)
add_labels(bars_webgazer)

# Guardar la gráfica
plt.tight_layout()
plt.savefig('tests/figs/RQ3_events_captured_fixations_bars.jpg')
# Mostrar gráfico
# plt.show()

# Datos grafico linea events_captured_fixations
positions = ["50cm", "70cm", "90cm"]
percentages_tobii = [100.00, 100.00, 40.00]
percentages_webgazer = [100.00, 100.00, 100.00]

# Crear la gráfica
plt.figure(figsize=(8, 5))
plt.plot(positions, percentages_tobii, marker='o', label="Infrared/Tobii", color='orange')
plt.plot(positions, percentages_webgazer, marker='o', label="Webcam/Webgazer.js", color='skyblue')

# Añadir etiquetas, título y leyenda
plt.xlabel("Position")
plt.ylabel("% Event Including Captured Fixations")
plt.title("Comparison of Tools by Distance")
plt.ylim(0, 110)  # Limitar el eje Y al rango de 0 a 110
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

# Guardar la gráfica
plt.tight_layout()
plt.savefig('tests/figs/RQ3_events_captured_fixations_line.jpg')
# Mostrar la gráfica 
# plt.show()

# Datos grafica matching fixations barras
tools = ["Infrared/Tobii","Webcam/Webgazer.js"]
positions = ["50cm", "70cm", "90cm"]
percentages_tobii = [81.79, 79.74, 0.00]
percentages_webgazer = [22.79, 61.95, 17.92]

x = np.arange(len(positions))  # Posiciones para las etiquetas del eje X
width = 0.35  # Ancho de las barras

# Crear figura y ejes
fig, ax = plt.subplots(figsize=(8, 5))
bars_tobii = ax.bar(x - width/2, percentages_tobii, width, label="Infrared/Tobii", color='orange')
bars_webgazer = ax.bar(x + width/2, percentages_webgazer, width, label="Webcam/Webgazer.js", color='skyblue')

# Añadir etiquetas y título
ax.set_xlabel("Position")
ax.set_ylabel("% Matching Fixation")
ax.set_title("Matching Fixation by Tool and Distance")
ax.set_xticks(x)
ax.set_xticklabels(positions)
ax.set_ylim(0, 100)
ax.legend()

# Mostrar porcentaje en las barras
add_labels(bars_tobii)
add_labels(bars_webgazer)

# Guardar la gráfica
plt.tight_layout()
plt.savefig('tests/figs/RQ3_matching_fixations_bars.jpg')
# Mostrar gráfico
# plt.show()


# Datos Matching fixations linea
positions = ["50cm", "70cm", "90cm"]
percentages_tobii = [81.79, 79.74, 0.00]
percentages_webgazer = [22.79, 61.95, 17.92]

# Crear la gráfica
plt.figure(figsize=(8, 5))
plt.plot(positions, percentages_tobii, marker='o', label="Infrared/Tobii", color='orange')
plt.plot(positions, percentages_webgazer, marker='o', label="Webcam/Webgazer.js", color='skyblue')

# Añadir etiquetas, título y leyenda
plt.xlabel("Position")
plt.ylabel("% Matching Fixation")
plt.title("Matching Fixation by Tool and Distance")
plt.ylim(0, 100)  # Limitar el eje Y al rango de 0 a 100
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

# Guardar la gráfica
plt.tight_layout()
plt.savefig('tests/figs/RQ3_matching_fixations_line.jpg')
# Mostrar la gráfica
# plt.show()


############## RQ4 ##############

# Datos %Event Including Relevant Fixations
tools = [ "Infrared/Tobii","Webcam/Webgazer.js"]
percentages = [100.00, 100.00]

# Crear la gráfica
fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(tools, percentages, color=[ 'orange','skyblue',])

# Añadir etiquetas y título
ax.set_ylabel("% Event Including Test Object Fixations")
ax.set_title("Comparison of Tools: Test Object Fixations")
ax.set_ylim(0, 110)  # Limitar el eje Y para espacio adicional

# Mostrar porcentaje en las barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 2,
            f'{height:.2f}%', ha='center', va='bottom')

# Guardar la gráfica
plt.tight_layout()
plt.savefig('tests/figs/RQ4_event_including_test_object_fixations.jpg')
# Mostrar gráfico
# plt.show()

# Datos %Matching_test_object_fixations
tools = ["Infrared/Tobii", "Webcam/Webgazer.js"]
percentages = [99.36,70.34]

# Crear la gráfica
fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(tools, percentages, color=[ 'orange','skyblue',])

# Añadir etiquetas y título
ax.set_ylabel("% Matching Test Object Fixations")
ax.set_title("Comparison of Tools: Matching Test Object Fixations")
ax.set_ylim(0, 110)  # Limitar el eje Y para espacio adicional

# Mostrar porcentaje en las barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 2,
            f'{height:.2f}%', ha='center', va='bottom')

# Guardar la gráfica
plt.tight_layout()
plt.savefig('tests/figs/RQ4_matching_test_object_fixations.jpg')
# Mostrar gráfico
# plt.show()