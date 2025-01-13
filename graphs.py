import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# Crear la carpeta si no existe
os.makedirs('tests/figs', exist_ok=True)

# Datos actualizados RQ1
data = {
    '% Matching Fixation True': [61.97, 51.00, 18.40, 27.39],
    'Tool/Software': ['Infrared/Tobii', 'Infrared/Tobii', 'Webcam/Webgazer.js', 'Webcam/Webgazer.js'],
    'Scenario': ['Form High Density', 'Form Low Density', 'Form High Density', 'Form Low Density']
}

df = pd.DataFrame(data)
df['Tool/Software (Scenario)'] = df['Tool/Software'] + ' (' + df['Scenario'] + ')'

# Crear la gráfica
fig, ax = plt.subplots(figsize=(10, 6))
bars = plt.bar(df['Tool/Software (Scenario)'], df['% Matching Fixation True'], 
               color=['orange', 'green', 'red', 'blue'])

# Etiquetas de porcentaje en las barras
for bar, pct in zip(bars, df['% Matching Fixation True']):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{pct:.2f}%', ha='center', va='bottom', fontsize=10)

# Personalización del gráfico
plt.title('% Matching Fixation True by Tool/Software and Scenario', fontsize=14)
plt.ylabel('% Matching Fixation True', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.ylim(0, 100)
plt.tight_layout()

# Guardar la gráfica
plt.savefig('tests/figs/RQ1_matching_fixations.jpg')
# Mostrar la gráfica
# plt.show()


############## RQ2 ##############
# Matching Fixation True by Tool/Software
new_data_rq2 = {
    '% Matching Fixation True': [80.95, 41.15],
    'Tool/Software': ['Infrared/Tobii', 'Webcam/Webgazer.js']
}

new_df = pd.DataFrame(new_data_rq2)

# Crear la gráfica
fig, ax = plt.subplots(figsize=(8, 5))
bars = plt.bar(new_df['Tool/Software'], new_df['% Matching Fixation True'], color=['orange', 'skyblue'])

# Etiquetas de porcentaje en las barras
for bar, pct in zip(bars, new_df['% Matching Fixation True']):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{pct:.2f}%', ha='center', va='bottom', fontsize=10)

# Personalización del gráfico
plt.title('% Matching Fixation True by Tool/Software', fontsize=14)
plt.ylabel('% Matching Fixation True', fontsize=12)
plt.xticks(rotation=0, ha='center', fontsize=10)
plt.ylim(0, 100)
plt.tight_layout()

# Guardar la gráfica
plt.savefig('tests/figs/RQ2_Matching_fixation.jpg')
# Mostrar la gráfica
# 00


# Datos %Event Including Captured Fixations
tools = [ "Infrared/Tobii","Webcam/Webgazer.js",]
percentages = [84.70,100.00]

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