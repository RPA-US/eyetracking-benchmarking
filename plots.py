import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd
import numpy as np
import os
import datetime

# font = {'family': 'serif', 'serif': ['Times New Roman'], 'weight': 'normal', 'size': 16}

os.makedirs('output/figs', exist_ok=True)

# Especificar la ruta base del proyecto y la salida deseada
base_path = "data/data_collection"


def configure_plot_style():

    """Configure matplotlib to use LaTeX fonts and styling"""

    plt.rcParams.update({

        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Computer Modern Roman"],
        "mathtext.fontset": "cm",
        "axes.labelsize": 16,
        "font.size": 16,
        "legend.fontsize": 16,
        "xtick.labelsize": 16,
        "ytick.labelsize": 16

    })
configure_plot_style()
print("LaTeX está activado:", plt.rcParams["text.usetex"])

yticks = np.linspace(0, 100, 5)
ytick_labels = [f"{y:.2f}%" for y in yticks]  
yticks_mae = np.linspace(0, 400, 5)
ytick_labels_mae = [f"{y:.2f}" for y in yticks_mae]

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


#READING RQ1 Datasets
rq1_tobii_form_density_high = data_collection_csv[data_collection_csv['Filename'] == 'RQ1_tobii_form_density_high_postprocessed.csv']
rq1_tobii_form_density_low = data_collection_csv[data_collection_csv['Filename'] == 'RQ1_tobii_form_density_low_postprocessed.csv']
rq1_webgazer_form_density_high = data_collection_csv[data_collection_csv['Filename'] == 'RQ1_webgazer_form_density_high_postprocessed.csv']
rq1_webgazer_form_density_low = data_collection_csv[data_collection_csv['Filename'] == 'RQ1_webgazer_form_density_low_postprocessed.csv']
# Calcular la media de la columna %MatchingFixations
percentage_matching_fixation_rq1_tobii_form_density_low = rq1_tobii_form_density_low['%MatchingFixations'].mean()
percentage_matching_fixation_rq1_webgazer_form_density_low = rq1_webgazer_form_density_low['%MatchingFixations'].mean()
percentage_matching_fixation_rq1_tobii_form_density_high = rq1_tobii_form_density_high['%MatchingFixations'].mean()
percentage_matching_fixation_rq1_webgazer_form_density_high = rq1_webgazer_form_density_high['%MatchingFixations'].mean()
# Calcular la media de la columna MAE
average_error_distance_rq1_tobii_form_density_high = rq1_tobii_form_density_high['MAE'].mean()
average_error_distance_rq1_webgazer_form_density_high = rq1_webgazer_form_density_high['MAE'].mean()
average_error_distance_rq1_tobii_form_density_low = rq1_tobii_form_density_low['MAE'].mean()
average_error_distance_rq1_webgazer_form_density_low = rq1_webgazer_form_density_low['MAE'].mean()


#RQ1_TC1 STMF (Form Density Low)
data = {
    '% Matching Fixation': [
        percentage_matching_fixation_rq1_tobii_form_density_low,
        percentage_matching_fixation_rq1_webgazer_form_density_low
    ],
    'Device/Software (TC1)': [
        r'\textbf{Infrared/Tobii Pro Spark}',  
        r'\textbf{Webcam/Webgazer.js}'  
    ]
}

df = pd.DataFrame(data)

fig, ax = plt.subplots(figsize=(9.85, 5.5))

bar_colors = ['#B0B0B0', '#555555']  
edge_colors = ['#4D4D4D', '#333333']  

bars = ax.bar(df['Device/Software (TC1)'], df['% Matching Fixation'], 
              color=bar_colors, edgecolor=edge_colors, linewidth=2,  hatch=["//", "\\\\"])

for bar, pct in zip(bars, df['% Matching Fixation']):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2.0, height + 2, rf'$\textbf{{{pct:.2f}\%}}$', 
            ha='center', va='bottom', fontsize=32, color='#555555', weight='bold')  

plt.text(-0.1, 1.20, r'\textbf{a)}', 
         fontsize=32, color='black', ha='left', va='top', transform=ax.transAxes)
plt.ylabel(r'\textbf{STMF (\%)}', fontsize=26, color='#555555')
plt.xticks(rotation=0, ha='center', fontsize=22, color='#555555')
yticks = np.arange(0, 120, 20)
ytick_labels = [rf"{y}\%" for y in yticks]
plt.yticks(yticks, ytick_labels, fontsize=26, color='#555555')
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('output/figs/RQ1_TC1_STMF.jpg', dpi=300)
# plt.show()


#RQ1_TC2 STMF (Form Density High)
data = {
    '% Matching Fixation': [percentage_matching_fixation_rq1_tobii_form_density_high,
                          percentage_matching_fixation_rq1_webgazer_form_density_high],
    'Device/Software (TC2)': 
        [
        r'\textbf{Infrared/Tobii Pro Spark}',  
        r'\textbf{Webcam/Webgazer.js}' 
        ]}
df = pd.DataFrame(data)
fig, ax = plt.subplots(figsize=(9.85, 5.5))
bar_colors = ['#B0B0B0', '#555555']  
edge_colors = ['#4D4D4D', '#333333']  
bars = ax.bar(df['Device/Software (TC2)'], df['% Matching Fixation'], 
              color=bar_colors, edgecolor=edge_colors, linewidth=2, hatch=["//", "\\\\"])

for bar, pct in zip(bars, df['% Matching Fixation']):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2.0, height, rf'$\textbf{{{pct:.2f}\%}}$', 
             ha='center', va='bottom', fontsize=32,  color='#555555', weight='bold')
plt.text(-0.1, 1.20, r'\textbf{a)}', 
         fontsize=32, color='black', ha='left', va='top', transform=ax.transAxes)
plt.ylabel(r'\textbf{STMF (\%)}', fontsize=26, color='#555555')
plt.xticks(rotation=0, ha='center', fontsize=22, color='#555555')
yticks = np.arange(0, 120, 20)
ytick_labels = [rf"{y}\%" for y in yticks]
plt.yticks(yticks, ytick_labels, fontsize=22, color='#555555')
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('output/figs/RQ1_TC2_STMF.jpg')
# plt.show()


# RQ1_TC1 MAE (Form Density Low)
data = {
    'Mean Error Distance': [average_error_distance_rq1_tobii_form_density_low,
                            average_error_distance_rq1_webgazer_form_density_low,],
    'Device/Software (TC1)': [
        r'\textbf{Infrared/Tobii Pro Spark}',  
        r'\textbf{Webcam/Webgazer.js}' 
        ],}
df = pd.DataFrame(data)
fig, ax = plt.subplots(figsize=(9.85, 5.5))
bar_colors = ['#B0B0B0', '#555555']  
edge_colors = ['#4D4D4D', '#333333']  

bars = plt.bar(df['Device/Software (TC1)'], df['Mean Error Distance'], 
               color=bar_colors, edgecolor=edge_colors, linewidth=2,  hatch=["//", "\\\\"])
for bar, pct in zip(bars, df['Mean Error Distance']):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2.0, height, rf'$\textbf{{{pct:.2f}px}}$', 
             ha='center', va='bottom', fontsize=32,  color='#555555', weight='bold')
plt.text(-0.1, 1.20, r'\textbf{b)}', 
         fontsize=32, color='black', ha='left', va='top', transform=ax.transAxes)
plt.ylabel(r'\textbf{MAE (px)}', fontsize=26,  color='#555555')
plt.xticks(rotation=0, ha='center', fontsize=22,  color='#555555')
plt.yticks(yticks_mae, ytick_labels_mae, fontsize=22,  color='#555555')
plt.ylim(0, 400)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('output/figs/RQ1_TC1_MAE.jpg')
# plt.show()


# RQ1_TC2 MAE (Form Density High)
data = {
    'Mean Error Distance': [average_error_distance_rq1_tobii_form_density_high,
                            average_error_distance_rq1_webgazer_form_density_high,],
    'Device/Software (TC2)': [
        r'\textbf{Infrared/Tobii Pro Spark}',  
        r'\textbf{Webcam/Webgazer.js}' 
        ],}
df = pd.DataFrame(data)
fig, ax = plt.subplots(figsize=(9.85, 5.5))
bar_colors = ['#B0B0B0', '#555555']  
edge_colors = ['#4D4D4D', '#333333']  

bars = plt.bar(df['Device/Software (TC2)'], df['Mean Error Distance'], 
               color=bar_colors, edgecolor=edge_colors, linewidth=2,  hatch=["//", "\\\\"])
for bar, pct in zip(bars, df['Mean Error Distance']):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2.0, height, rf'$\textbf{{{pct:.2f}px}}$', 
             ha='center', va='bottom', fontsize=32,  color='#555555', weight='bold')
plt.text(-0.1, 1.20, r'\textbf{b)}', 
         fontsize=32, color='black', ha='left', va='top', transform=ax.transAxes)
plt.ylabel(r'\textbf{MAE (px)}', fontsize=26,  color='#555555')
plt.xticks(rotation=0, ha='center', fontsize=22,  color='#555555')
plt.yticks(yticks_mae, ytick_labels_mae, fontsize=22,  color='#555555')
plt.ylim(0, 400)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('output/figs/RQ1_TC2_MAE.jpg')
# plt.show()



####RQ2####
#Reading RQ2 Datasets
rq2_tobii_alternance_buttons = data_collection_csv[data_collection_csv['Filename'] == 'RQ2_tobii_alternance_buttons_postprocessed.csv']
rq2_webgazer_alternance_buttons = data_collection_csv[data_collection_csv['Filename'] == 'RQ2_webgazer_alternance_buttons_postprocessed.csv']
#Matching fixation RQ2
percentage_matching_fixation_rq2_tobii_alternance_buttons = rq2_tobii_alternance_buttons['%MatchingFixations'].mean()
percentage_matching_fixation_rq2_webgazer_alternance_buttons = rq2_webgazer_alternance_buttons['%MatchingFixations'].mean()
#Events Including Fixations RQ2
percentage_events_including_fixations_rq2_tobii_alternance_buttons = rq2_tobii_alternance_buttons['%EventsWithFixations'].mean()
percetange_events_including_fixations_rq2_webgazer_alternance_buttons = rq2_webgazer_alternance_buttons['%EventsWithFixations'].mean()
#Mean Absolute Error RQ2
average_error_distance_rq2_tobii_alternance_buttons = rq2_tobii_alternance_buttons['MAE'].mean()
average_error_distance_rq2_webgazer_alternance_buttons = rq2_webgazer_alternance_buttons['MAE'].mean()



# TC3_RQ2 STMF (Alternance Buttons)
new_data_rq2 = {
    '% Matching Fixation': [percentage_matching_fixation_rq2_tobii_alternance_buttons,
                            percentage_matching_fixation_rq2_webgazer_alternance_buttons],
    'Device/Software': [
        r'\textbf{Infrared/Tobii Pro Spark}',  
        r'\textbf{Webcam/Webgazer.js}' 
        ]
}
bar_colors = ['#B0B0B0', '#555555']  
edge_colors = ['#4D4D4D', '#333333']  

df = pd.DataFrame(new_data_rq2)
fig, ax = plt.subplots(figsize=(9.85, 5.5))
bars = plt.bar(df['Device/Software'], df['% Matching Fixation'], 
               color=bar_colors, edgecolor=edge_colors, linewidth=2,  hatch=["//", "\\\\"])
for bar, pct in zip(bars, df['% Matching Fixation']):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2.0, height, rf'$\textbf{{{pct:.2f}\%}}$', 
             ha='center', va='bottom', fontsize=32,  color='#555555', weight='bold')
plt.text(-0.1, 1.20, r'\textbf{a)}', 
         fontsize=32, color='black', ha='left', va='top', transform=ax.transAxes)
plt.ylabel(r'\textbf{STMF (\%)}', fontsize=26, color='#555555')
plt.xticks(rotation=0, ha='center', fontsize=22, color='#555555')
yticks = np.arange(0, 120, 20)
ytick_labels = [rf"{y}\%" for y in yticks]
plt.yticks(yticks, ytick_labels, fontsize=22, color='#555555')
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('output/figs/RQ2_TC3_STMF.jpg')
# plt.show()


#RQ2_TC3 EIF (Alternance Buttons)

new_data_rq2 = {
    '% EIF': [percentage_events_including_fixations_rq2_tobii_alternance_buttons,
                            percetange_events_including_fixations_rq2_webgazer_alternance_buttons],
    'Device/Software': [
        r'\textbf{Infrared/Tobii Pro Spark}',  
        r'\textbf{Webcam/Webgazer.js}' 
        ]
}
bar_colors = ['#B0B0B0', '#555555']  
edge_colors = ['#4D4D4D', '#333333']  
df = pd.DataFrame(new_data_rq2)
fig, ax = plt.subplots(figsize=(9.85, 5.5))
bars = plt.bar(df['Device/Software'], df['% EIF'], 
               color=bar_colors, edgecolor=edge_colors, linewidth=2,  hatch=["//", "\\\\"])
for bar, pct in zip(bars, df['% EIF']):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height - 12, rf'$\textbf{{{pct:.2f}\%}}$', 
             ha='center', va='bottom', fontsize=32,  color='#555555', weight='bold', bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.3'))

plt.ylabel(r'\textbf{EIF (\%)}', fontsize=32, color='#555555')
plt.xticks(rotation=0, ha='center', fontsize=22, color='#555555')
yticks = np.arange(0, 120, 20)
ytick_labels = [rf"{y}\%" for y in yticks]
plt.yticks(yticks, ytick_labels, fontsize=22, color='#555555')
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('output/figs/RQ2_TC3_EIF.jpg')
# plt.show()


#RQ2_TC3 (mean MAE)
data = {
    'Mean Error Distance': [average_error_distance_rq2_tobii_alternance_buttons,
                            average_error_distance_rq2_webgazer_alternance_buttons,],   
    'Device/Software': [ 
        r'\textbf{Infrared/Tobii Pro Spark}',  
        r'\textbf{Webcam/Webgazer.js}' 
        ]}
df = pd.DataFrame(data)
bar_colors = ['#B0B0B0', '#555555']  
edge_colors = ['#4D4D4D', '#333333']  
fig, ax = plt.subplots(figsize=(9.85, 5.5))
bars = plt.bar(df['Device/Software'], df['Mean Error Distance'], 
               color=bar_colors, edgecolor=edge_colors, linewidth=2,  hatch=["//", "\\\\"])
for bar, pct in zip(bars, df['Mean Error Distance']):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, rf'$\textbf{{{pct:.2f}px}}$',
             ha='center', va='bottom', fontsize=30,  color='#555555', weight='bold')
plt.text(-0.1, 1.20, r'\textbf{b)}', 
         fontsize=30, color='black', ha='left', va='top', transform=ax.transAxes)
plt.ylabel(r'\textbf{MAE (px)}', fontsize=26,  color='#555555')
plt.xticks(rotation=0, ha='center', fontsize=22,  color='#555555')
plt.yticks(yticks_mae, ytick_labels_mae, fontsize=26,  color='#555555')
plt.ylim(0, 400)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('output/figs/RQ2_TC3_MAE.jpg')
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

# Datos grafico linea events_captured_fixations

positions = ["TC4 (50cm)", "TC5 (70cm)", "TC6 (90cm)"]
percentages_tobii = [percentage_events_including_fixations_rq3_tobii_position_50cm,
                     percentage_events_including_fixations_rq3_tobii_position_70cm,
                     percentage_events_including_fixations_rq3_tobii_position_90cm]
percentages_webgazer = [percentage_events_including_fixations_rq3_webgazer_position_50cm,
                        percentage_events_including_fixations_rq3_webgazer_position_70cm,
                        percentage_events_including_fixations_rq3_webgazer_position_90cm]

x = np.arange(len(positions))
width = 0.3
bar_colors = ['#B0B0B0', '#555555']  # Colores de las barras
edge_colors = ['#4D4D4D', '#333333']  # Bordes
hatch_patterns = ["//", "\\\\"]

# Crear figura
fig, ax = plt.subplots(figsize=(9.85, 5.5))

# Dibujar barras
bars_tobii = ax.bar(x - width / 3, percentages_tobii, width, label=r"\textbf{Infrared/Tobii Pro Spark}",
                     color=bar_colors[0], edgecolor=edge_colors[0], linewidth=2)
bars_webgazer = ax.bar(x + width, percentages_webgazer, width, label=r"\textbf{Webcam/Webgazer.js}",
                        color=bar_colors[1], edgecolor=edge_colors[1], linewidth=2)

# Aplicar hatch a cada conjunto de barras
for bars, hatch in zip([bars_tobii, bars_webgazer], hatch_patterns):
    for bar in bars:
        bar.set_hatch(hatch)

# Etiquetas de barras con formato LaTeX
for bars in [bars_tobii, bars_webgazer]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height - 12,  # Ajuste vertical
                rf'$\mathbf{{{height:.2f}\%}}$', ha='center', va='bottom', fontsize=20, 
                color='#555555', weight='bold' ,  bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.1'))

# Configuración de ejes
ax.set_xlabel(r"\textbf{Test Case (User-Screen/Device distance)}", fontsize=18, color='#555555')
ax.set_ylabel(r"\textbf{EIF (\%)}", fontsize=22, color='#555555')
ax.set_xticks(x)
ax.set_xticklabels(positions, fontsize=20, color='#555555')
ax.set_yticks(np.linspace(0, 100, 6))
ax.set_ylim(0, 110)
ax.tick_params(axis='y', labelsize=20, colors='#555555' )
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Formato de porcentaje en eje Y
def percent_formatter(x, pos):
    return rf'$\mathbf{{{x:.0f}\%}}$'
ax.yaxis.set_major_formatter(FuncFormatter(percent_formatter))

# Etiqueta de subfigura
ax.text(-0.08, 1.15, r'\textbf{a)}', fontsize=26, color='black', ha='left', va='top', transform=ax.transAxes)

# Leyenda con formato LaTeX
ax.legend(fontsize=16, frameon=True)

# Ajuste final y guardado
plt.tight_layout()
plt.savefig('output/figs/RQ3_TC4_TC5_TC6_EIF_bars.jpg', dpi=300)
# plt.show()

#RQ3 TC4 TC5 TC6 EIF (linea)

positions = ["TC4 (50cm)", "TC5 (70cm)", "TC6 (90cm)"]
percentages_tobii = [percentage_events_including_fixations_rq3_tobii_position_50cm,
                     percentage_events_including_fixations_rq3_tobii_position_70cm,
                     percentage_events_including_fixations_rq3_tobii_position_90cm]
percentages_webgazer = [percentage_events_including_fixations_rq3_webgazer_position_50cm,
                        percentage_events_including_fixations_rq3_webgazer_position_70cm,
                        percentage_events_including_fixations_rq3_webgazer_position_90cm]

# Configuración del gráfico
x = np.arange(len(positions))  
width = 0.3
bar_colors = ['#B0B0B0', '#555555']  # Colores de las barras
edge_colors = ['#4D4D4D', '#333333']  # Bordes
hatch_patterns = ["//", "\\\\"]

fig, ax = plt.subplots(figsize=(9.85, 5.5))

# Configuración de líneas con formato
ax.plot(x, percentages_tobii, marker='o', linestyle='-', linewidth=3, markersize=20, 
        label=r"\textbf{Infrared/Tobii Pro Spark}", color='#B0B0B0', markerfacecolor='white', markeredgewidth=2)
ax.plot(x, percentages_webgazer, marker='s', linestyle='-', linewidth=3, markersize=20, 
        label=r"\textbf{Webcam/Webgazer.js}", color='#555555', markerfacecolor='white', markeredgewidth=2)


# Etiquetas de los ejes
ax.set_xlabel(r"\textbf{Test Case (User-Screen/Device distance)}", fontsize=20, color='#555555')
ax.set_ylabel(r"\textbf{EIF (px)}", fontsize=20, color='#555555')

# Configuración del eje X
ax.set_xticks(x)
ax.set_xticklabels(positions, fontsize=20, color='#555555')

# Configuración del eje Y
ax.set_yticks(np.linspace(0, 100, 6))
ax.set_ylim(0, 110)
ax.tick_params(axis='y', labelsize=20, colors='#555555')

# Formato de porcentaje en el eje Y
def percent_formatter(x, pos): 
    return rf'$\mathbf{{{x:.0f}\%}}$'
ax.yaxis.set_major_formatter(FuncFormatter(percent_formatter))

# Etiquetas de los puntos
for i, value in enumerate(percentages_tobii):
    ax.text(x[i] +0.2, value -10, rf'$\mathbf{{{value:.2f}\%}}$', ha='center', va='top', fontsize=18, color='#B0B0B0', bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.1'))

for i, value in enumerate(percentages_webgazer):
    ax.text(x[i] +0.2, value + 7, rf'$\mathbf{{{value:.2f}\%}}$', ha='center', va='bottom', fontsize=18, color='#555555', bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.1'))

# Etiqueta de subfigura
ax.text(-0.08, 1.15, r'\textbf{b)}', fontsize=26, color='black', ha='left', va='top', transform=ax.transAxes)

# Leyenda
ax.legend(fontsize=16, frameon=True)

# Ajuste y guardado
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('output/figs/RQ3_TC4_TC5_TC6_EIF_line.jpg', dpi=300)
# plt.show()



# RQ3_TC4_TC5_TC6 Matching Fixations (STMF)
percentage_matching_fixation_rq3_tobii_position_50cm = rq3__tobii_position_50cm['%MatchingFixations'].mean()
percentage_matching_fixation_rq3_tobii_position_70cm = rq3__tobii_position_70cm['%MatchingFixations'].mean()
percentage_matching_fixation_rq3_tobii_position_90cm = rq3__tobii_position_90cm['%MatchingFixations'].mean()
percentage_matching_fixation_rq3_webgazer_position_50cm = rq3__webgazer_position_50cm['%MatchingFixations'].mean()
percentage_matching_fixation_rq3_webgazer_position_70cm = rq3__webgazer_position_70cm['%MatchingFixations'].mean()
percentage_matching_fixation_rq3_webgazer_position_90cm = rq3__webgazer_position_90cm['%MatchingFixations'].mean()

positions = ["TC4 (50cm)", "TC5 (70cm)", "TC6 (90cm)"]
percentages_tobii = [percentage_matching_fixation_rq3_tobii_position_50cm,
                     percentage_matching_fixation_rq3_tobii_position_70cm,
                     percentage_matching_fixation_rq3_tobii_position_90cm]
percentages_webgazer = [percentage_matching_fixation_rq3_webgazer_position_50cm,
                        percentage_matching_fixation_rq3_webgazer_position_70cm,
                        percentage_matching_fixation_rq3_webgazer_position_90cm]

# Configuración del gráfico
x = np.arange(len(positions))  
width = 0.3
bar_colors = ['#B0B0B0', '#555555']  # Colores de las barras
edge_colors = ['#4D4D4D', '#333333']  # Bordes
hatch_patterns = ["//", "\\\\"]

fig, ax = plt.subplots(figsize=(9.85, 5.5))

# Dibujar barras
bars_tobii = ax.bar(x - width / 3, percentages_tobii, width, label=r"\textbf{Infrared/Tobii Pro Spark}",
                     color=bar_colors[0], edgecolor=edge_colors[0], linewidth=2)
bars_webgazer = ax.bar(x + width, percentages_webgazer, width, label=r"\textbf{Webcam/Webgazer.js}",
                        color=bar_colors[1], edgecolor=edge_colors[1], linewidth=2)

# Aplicar hatch a cada conjunto de barras
for bars, hatch in zip([bars_tobii, bars_webgazer], hatch_patterns):
    for bar in bars:
        bar.set_hatch(hatch)

# Etiquetas de barras con formato LaTeX
for bars in [bars_tobii, bars_webgazer]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height - 5,
                rf'$\mathbf{{{height:.2f}\%}}$', ha='center', va='top', fontsize=20, 
                color='#555555', weight='bold', bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.1'))

# Configuración de ejes
ax.set_xlabel(r"\textbf{Test Case (User-Screen/Device distance)}", fontsize=22, color='#555555')
ax.set_ylabel(r"\textbf{STMF (\%)}", fontsize=22, color='#555555')
ax.set_xticks(x)
ax.set_xticklabels(positions, fontsize=16, color='#555555')
ax.set_yticks(np.linspace(0, 100, 6))
ax.set_ylim(0, 100)
ax.tick_params(axis='y', labelsize=16, colors='#555555')
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Formato de porcentaje en eje Y
def percent_formatter(x, pos):
    return rf'$\mathbf{{{x:.0f}\%}}$'
ax.yaxis.set_major_formatter(FuncFormatter(percent_formatter))

# Etiqueta de subfigura
ax.text(-0.08, 1.15, r'\textbf{1a)}', fontsize=26, color='black', ha='left', va='top', transform=ax.transAxes)

# Leyenda con formato LaTeX
ax.legend(fontsize=16, frameon=True)

# Ajuste final y guardado
plt.tight_layout()
plt.savefig('output/figs/RQ3_TC4_TC5_TC6_STMF_bars.jpg', dpi=300)
# plt.show()



# Datos STMF linea
positions = ["TC4 (50cm)", "TC5 (70cm)", "TC6 (90cm)"]
percentages_tobii = [percentage_matching_fixation_rq3_tobii_position_50cm,
                     percentage_matching_fixation_rq3_tobii_position_70cm,
                     percentage_matching_fixation_rq3_tobii_position_90cm]
percentages_webgazer = [percentage_matching_fixation_rq3_webgazer_position_50cm,
                        percentage_matching_fixation_rq3_webgazer_position_70cm,
                        percentage_matching_fixation_rq3_webgazer_position_90cm]

x = np.arange(len(positions))

# Crear figura
fig, ax = plt.subplots(figsize=(9.85, 5.5))

# Configuración de líneas con formato
ax.plot(x, percentages_tobii, marker='o', linestyle='-', linewidth=3, markersize=20, 
        label=r"\textbf{Infrared/Tobii Pro Spark}", color='#B0B0B0', markerfacecolor='white', markeredgewidth=2)
ax.plot(x, percentages_webgazer, marker='s', linestyle='-', linewidth=3, markersize=20, 
        label=r"\textbf{Webcam/Webgazer.js}", color='#555555', markerfacecolor='white', markeredgewidth=2)

# Etiquetas de los ejes
ax.set_xlabel(r"\textbf{Test Case (User-Screen/Device distance)}", fontsize=20, color='#555555')
ax.set_ylabel(r"\textbf{STMF (\%)}", fontsize=20, color='#555555')

# Configuración del eje X
ax.set_xticks(x)
ax.set_xticklabels(positions, fontsize=16, color='#555555')

# Configuración del eje Y
ax.set_yticks(np.linspace(0, 100, 6))
ax.set_ylim(0, 100)
ax.tick_params(axis='y', labelsize=16, colors='#555555')

# Formato de porcentaje en el eje Y
def percent_formatter(x, pos): 
    return rf'$\mathbf{{{x:.0f}\%}}$'
ax.yaxis.set_major_formatter(FuncFormatter(percent_formatter))

# Etiquetas de los puntos
for i, value in enumerate(percentages_tobii):
    ax.text(x[i] +0.05, value -8, rf'$\mathbf{{{value:.2f}\%}}$', ha='center', va= 'top' , fontsize=20, color='#B0B0B0', bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.1'))

for i, value in enumerate(percentages_webgazer):
    ax.text(x[i] +0.05, value +7, rf'$\mathbf{{{value:.2f}\%}}$', ha='center', va='bottom' , fontsize=20, color='#555555', bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.1'))

# Etiqueta de subfigura
ax.text(-0.08, 1.15, r'\textbf{1b)}', fontsize=26, color='black', ha='left', va='top', transform=ax.transAxes)

# Leyenda
ax.legend(fontsize=16, frameon=True)

# Ajuste y guardado
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('output/figs/RQ3_TC4_TC5_TC6_STMF_line.jpg', dpi=300)
# plt.show()


# Datos mean MAE RQ3
average_error_distance_rq3_tobii_position_50cm = rq3__tobii_position_50cm['MAE'].mean()
average_error_distance_rq3_tobii_position_70cm = rq3__tobii_position_70cm['MAE'].mean()
average_error_distance_rq3_tobii_position_90cm = rq3__tobii_position_90cm['MAE'].mean()
average_error_distance_rq3_webgazer_position_50cm = rq3__webgazer_position_50cm['MAE'].mean()
average_error_distance_rq3_webgazer_position_70cm = rq3__webgazer_position_70cm['MAE'].mean()
average_error_distance_rq3_webgazer_position_90cm = rq3__webgazer_position_90cm['MAE'].mean()

# Datos
positions = ["TC4 (50cm)", "TC5 (70cm)", "TC6 (90cm)"]
med_tobii = [average_error_distance_rq3_tobii_position_50cm,
             average_error_distance_rq3_tobii_position_70cm,
             average_error_distance_rq3_tobii_position_90cm]
med_webgazer = [average_error_distance_rq3_webgazer_position_50cm,
                average_error_distance_rq3_webgazer_position_70cm,
                average_error_distance_rq3_webgazer_position_90cm]

x = np.arange(len(positions))  
width = 0.3

# Crear figura
fig, ax = plt.subplots(figsize=(9.85, 5.5))

# Dibujar barras con formato
bars_tobii = ax.bar(x - width / 3, med_tobii, width, label=r"\textbf{Infrared/Tobii Pro Spark}",
                     color='#B0B0B0', edgecolor='#4D4D4D', linewidth=2)
bars_webgazer = ax.bar(x + width, med_webgazer, width, label=r"\textbf{Webcam/Webgazer.js}",
                        color='#555555', edgecolor='#333333', linewidth=2)

# Aplicar hatch a las barras
hatch_patterns = ["//", "\\\\"]
for bars, hatch in zip([bars_tobii, bars_webgazer], hatch_patterns):
    for bar in bars:
        bar.set_hatch(hatch)

# Etiquetas de los ejes
ax.set_xlabel(r"\textbf{Test Case (User-Screen/Device distance)}", fontsize=22, color='#555555')
ax.set_ylabel(r"\textbf{MAE (px)}", fontsize=22, color='#555555')

# Configuración del eje X
ax.set_xticks(x)
ax.set_xticklabels(positions, fontsize=22, color='#555555')

# Configuración del eje Y
ax.set_yticks(np.linspace(0, 400, 5))
ax.set_ylim(0, 400)
ax.tick_params(axis='y', labelsize=22, colors='#555555')

# Formato de valores en el eje Y
def px_formatter(x, pos): 
    return rf'$\mathbf{{{x:.0f}}}$'
ax.yaxis.set_major_formatter(FuncFormatter(px_formatter))

# Etiquetas de valores en barras
for bars in [bars_tobii, bars_webgazer]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 30,  # Ajuste vertical
                rf'$\mathbf{{{height:.2f}px}}$', ha='center', va='top', fontsize=18, 
                color='#555555', weight='bold', bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.1'))

# Etiqueta de subfigura
ax.text(-0.08, 1.15, r'\textbf{2)}', fontsize=26, color='black', ha='left', va='top', transform=ax.transAxes)

# Leyenda
ax.legend(fontsize=22, frameon=True)

# Ajuste final y guardado
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('output/figs/RQ3_TC4_TC5_TC6_MAE.jpg', dpi=300)
# plt.show()
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
ax.set_ylim(0, 100)  # Limitar el eje Y para espacio adicional

# Mostrar porcentaje en las barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 2,
            f'{height:.2f}%', ha='center', va='bottom')

# Guardar la gráfica
plt.tight_layout()
# plt.savefig('output/figs/RQ4_EITOF_TC7.jpg')
# Mostrar gráfico
# plt.show()

# Datos %Matching_test_object_fixations
percentage_matching_test_object_fixations_rq4_tobii_rpm = rq4_tobii_rpm['%RelevantFixations'].mean()
percentage_matching_test_object_fixations_rq4_webgazer_rpm = rq4_webgazer_rpm['%RelevantFixations'].mean()


# Crear DataFrame con los datos
new_data_rq4 = {
    '% Matching Fixation': [percentage_matching_test_object_fixations_rq4_tobii_rpm,
                            percentage_matching_test_object_fixations_rq4_webgazer_rpm],
    'Device/Software': ['Infrared/Tobii Pro Spark', 'Webcam/Webgazer.js']
}
new_df = pd.DataFrame(new_data_rq4)

# Crear figura
fig, ax = plt.subplots(figsize=(9.85, 5.5))

# Colores y bordes de las barras
bar_colors = ['#B0B0B0', '#555555']
edge_colors = ['#4D4D4D', '#333333']
hatch_patterns = ["//", "\\\\"]

# Dibujar barras
bars = ax.bar(new_df['Device/Software'], new_df['% Matching Fixation'], 
              color=bar_colors, edgecolor=edge_colors, linewidth=2)

# Aplicar hatch a las barras
for bar, hatch in zip(bars, hatch_patterns):
    bar.set_hatch(hatch)

# Etiquetas en las barras con formato LaTeX
for bar, pct in zip(bars, new_df['% Matching Fixation']):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height - 5,  
            rf'$\mathbf{{{pct:.2f}\%}}$', ha='center', va='top', fontsize=22, 
            color='#555555', weight='bold', bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.1'))

# Etiquetas de los ejes
ax.set_ylabel(r"\textbf{MTMF (\%)}", fontsize=22, color='#555555')

# Configuración del eje Y
ax.set_yticks(np.linspace(0, 100, 6))
ax.set_ylim(0, 100)
ax.tick_params(axis='y', labelsize=22, colors='#555555')

# Formato de valores en el eje Y
def percent_formatter(x, pos): 
    return rf'$\mathbf{{{x:.0f}\%}}$'
ax.yaxis.set_major_formatter(FuncFormatter(percent_formatter))

# Ajuste final y guardado
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('output/figs/RQ4_TC7_MTMF.jpg', dpi=300)
# plt.show()
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




############################ Questionnaire Plots ############################

#1a Know and day-to-day use of Infrared Device
labels = ["I know it and I work with it.", "I do not know it." , "I know, but I do not work with it."]
sizes = [10, 40, 50] 
colors = ['#6495ED', '#D2691E', '#B0B0B0'] 
hatches = ['//', '\\\\', '']  

fig, ax = plt.subplots(figsize=(5.5, 3.5))  
wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.2f%%',
                                  colors=colors, startangle=140, pctdistance=0.8,
                                  wedgeprops={'edgecolor': '#4D4D4D', 'linewidth': 2})
i = 0
for wedge in wedges:
    wedge.set_hatch(hatches[i])
    i += 1

total_size = sum(sizes)
for autotext in autotexts:
    autotext.set_color('#333333')
    autotext.set_fontsize(12)  
    autotext.set_weight('bold')
    autotext.set_bbox(dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'))

# ax.set_title(r'a) \textbf{Know and day-to-day use} of a \textbf{Infrared device}',
#              fontsize=11, color='black', pad=1) 
ax.set_title(r'a)', fontsize=20, color='black', pad=1, loc='left')

ax.legend(labels, loc='upper center', bbox_to_anchor=(0.5, 0), fontsize=11, frameon=True, fancybox=True)
plt.tight_layout(pad=0.1)
plt.savefig('output/figs_questionnaire/1a_KnowUse_Infrared.jpg', dpi=300, bbox_inches='tight')


#1b Know and day-to-day use of Webcam Device
labels = ["I know it and I work with it.", "I know, but I do not work with it.", "I do not know it."]
sizes = [80, 20]  
colors = ['#6495ED', '#B0B0B0']  
hatches = ['//', '']  

fig, ax = plt.subplots(figsize=(5.5, 3.5))  
wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.2f%%',
                                  colors=colors, startangle=140, pctdistance=0.8,
                                  wedgeprops={'edgecolor': '#4D4D4D', 'linewidth': 2})
i = 0
for wedge in wedges:
    wedge.set_hatch(hatches[i])
    i += 1

total_size = sum(sizes)
for autotext in autotexts:
    autotext.set_color('#333333')
    autotext.set_fontsize(12)  
    autotext.set_weight('bold')
    autotext.set_bbox(dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'))

# ax.set_title(r'b) \textbf{Know and day-to-day use} of a \textbf{Webcam device}',
#              fontsize=11, color='black', pad=1) 
ax.set_title(r'b)', fontsize=20, color='black', pad=1, loc='left')
ax.legend(labels, loc='upper center', bbox_to_anchor=(0.5, 0), fontsize=11, frameon=True, fancybox=True)
plt.tight_layout(pad=0.1)
plt.savefig('output/figs_questionnaire/1b_KnowUse_Webcam.jpg', dpi=300, bbox_inches='tight')



#2a Fatigue feeling Infrared Device
labels = ["Yes.", "No.", "Do not Know/Maybe."]
sizes = [60, 30, 10] 
colors = ['#6495ED', '#D2691E', '#B0B0B0'] 
hatches = ['//', '\\\\', '']  

fig, ax = plt.subplots(figsize=(5.5, 3.5))  
wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.2f%%',
                                  colors=colors, startangle=140, pctdistance=0.8,
                                  wedgeprops={'edgecolor': '#4D4D4D', 'linewidth': 2})
i = 0
for wedge in wedges:
    wedge.set_hatch(hatches[i])
    i += 1

total_size = sum(sizes)
for autotext in autotexts:
    autotext.set_color('#333333')
    autotext.set_fontsize(12)  
    autotext.set_weight('bold')
    autotext.set_bbox(dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'))

# ax.set_title(r'a) \textbf{Fatigue feeling} after experiment with \textbf{Infrared device}',
#              fontsize=11, color='black', pad=1) 
ax.set_title(r'a)', fontsize=20, color='black', pad=1, loc='left')
ax.legend(labels, loc='upper center', bbox_to_anchor=(0.5, 0), fontsize=11, frameon=True, fancybox=True)
plt.tight_layout(pad=0.1)
plt.savefig('output/figs_questionnaire/2a_Fatigue_Infrared.jpg', dpi=300, bbox_inches='tight')

#2b Fatigue feeling Webcam Device
labels = ["Yes.", "No."]
sizes = [30, 70,] 
colors = ['#6495ED', '#D2691E'] 
hatches = ['//', '\\\\',]  

fig, ax = plt.subplots(figsize=(5.5, 3.5))  
wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.2f%%',
                                  colors=colors, startangle=140, pctdistance=0.8,
                                  wedgeprops={'edgecolor': '#4D4D4D', 'linewidth': 2})
i = 0
for wedge in wedges:
    wedge.set_hatch(hatches[i])
    i += 1

total_size = sum(sizes)
for autotext in autotexts:
    autotext.set_color('#333333')
    autotext.set_fontsize(12)  
    autotext.set_weight('bold')
    autotext.set_bbox(dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'))

# ax.set_title(r'b) \textbf{Fatigue feeling} after experiment with \textbf{Webcam device}',
#              fontsize=11, color='black', pad=1) 
ax.set_title(r'b)', fontsize=20, color='black', pad=1, loc='left')

ax.legend(labels, loc='upper center', bbox_to_anchor=(0.5, 0), fontsize=11, frameon=True, fancybox=True)
plt.tight_layout(pad=0.1)
plt.savefig('output/figs_questionnaire/2b_Fatigue_Webcam.jpg', dpi=300, bbox_inches='tight')



#3a Concentration Level Infrared Device
labels = ["Yes.", "No."]
sizes = [20, 80] 
colors = ['#6495ED', '#D2691E'] 
hatches = ['//', '\\\\',]  

fig, ax = plt.subplots(figsize=(5.5, 3.5))  
wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.2f%%',
                                  colors=colors, startangle=140, pctdistance=0.8,
                                  wedgeprops={'edgecolor': '#4D4D4D', 'linewidth': 2})
i = 0
for wedge in wedges:
    wedge.set_hatch(hatches[i])
    i += 1

total_size = sum(sizes)
for autotext in autotexts:
    autotext.set_color('#333333')
    autotext.set_fontsize(12)  
    autotext.set_weight('bold')
    autotext.set_bbox(dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'))

# ax.set_title(r'a) \textbf{Concentration level} during experiment due to the use of \textbf{Infrared device}',
#              fontsize=11, color='black', pad=1) 
ax.set_title(r'a)', fontsize=20, color='black', pad=1, loc='left')

ax.legend(labels, loc='upper center', bbox_to_anchor=(0.5, 0), fontsize=11, frameon=True, fancybox=True)
plt.tight_layout(pad=0.1)
plt.savefig('output/figs_questionnaire/3a_Concentration_Infrared.jpg', dpi=300, bbox_inches='tight')


#3b Concentration Level Webcam Device
labels = ["Yes.", "No.", "Do not Know/Maybe."]
sizes = [10, 80, 10] 
colors = ['#6495ED', '#D2691E', '#B0B0B0'] 
hatches = ['//', '\\\\', '']  

fig, ax = plt.subplots(figsize=(5.5, 3.5))  
wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.2f%%',
                                  colors=colors, startangle=140, pctdistance=0.8,
                                  wedgeprops={'edgecolor': '#4D4D4D', 'linewidth': 2})
i = 0
for wedge in wedges:
    wedge.set_hatch(hatches[i])
    i += 1

total_size = sum(sizes)
for autotext in autotexts:
    autotext.set_color('#333333')
    autotext.set_fontsize(12)  
    autotext.set_weight('bold')
    autotext.set_bbox(dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'))

# ax.set_title(r'b) \textbf{Concentration level} during experiment due to the use of \textbf{Webcam device}',
#              fontsize=11, color='black', pad=1)
ax.set_title(r'b)', fontsize=20, color='black', pad=1, loc='left')

ax.legend(labels, loc='upper center', bbox_to_anchor=(0.5, 0), fontsize=11, frameon=True, fancybox=True)
plt.tight_layout(pad=0.1)
plt.savefig('output/figs_questionnaire/3b_Concentration_Webcam.jpg', dpi=300, bbox_inches='tight')




#4a Privacy Threat Infrared Device
labels = ["Yes.", "No.", "Do not Know/Maybe."]
sizes = [20, 50, 30] 
colors = ['#6495ED', '#D2691E', '#B0B0B0'] 
hatches = ['//', '\\\\', '']  

fig, ax = plt.subplots(figsize=(5.5, 3.5))  
wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.2f%%',
                                  colors=colors, startangle=140, pctdistance=0.8,
                                  wedgeprops={'edgecolor': '#4D4D4D', 'linewidth': 2})
i = 0
for wedge in wedges:
    wedge.set_hatch(hatches[i])
    i += 1

total_size = sum(sizes)
for autotext in autotexts:
    autotext.set_color('#333333')
    autotext.set_fontsize(12)  
    autotext.set_weight('bold')
    autotext.set_bbox(dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'))

# ax.set_title(r'a) \textbf{Potential feeling of privacy threat} in the daily use of \textbf{Infrared device}',
#              fontsize=11, color='black', pad=1) 
ax.set_title(r'a)', fontsize=20, color='black', pad=1, loc='left')

ax.legend(labels, loc='upper center', bbox_to_anchor=(0.5, 0), fontsize=11, frameon=True, fancybox=True)
plt.tight_layout(pad=0.1)
plt.savefig('output/figs_questionnaire/4a_Privacy_Infrared.jpg', dpi=300, bbox_inches='tight')

#4b Privacy Threat Infrared Device
labels = ["Yes.", "No.", "Do not Know/Maybe."]
sizes = [20, 40, 40] 
colors = ['#6495ED', '#D2691E', '#B0B0B0'] 
hatches = ['//', '\\\\', '']  

fig, ax = plt.subplots(figsize=(5.5, 3.5))  
wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.2f%%',
                                  colors=colors, startangle=140, pctdistance=0.8,
                                  wedgeprops={'edgecolor': '#4D4D4D', 'linewidth': 2})
i = 0
for wedge in wedges:
    wedge.set_hatch(hatches[i])
    i += 1

total_size = sum(sizes)
for autotext in autotexts:
    autotext.set_color('#333333')
    autotext.set_fontsize(12)  
    autotext.set_weight('bold')
    autotext.set_bbox(dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'))

# ax.set_title(r'b) \textbf{Potential feeling of privacy threat} in the daily use of \textbf{Webcam device}',
#              fontsize=11, color='black', pad=1) 

ax.set_title(r'b)', fontsize=20, color='black', pad=1, loc='left')
ax.legend(labels, loc='upper center', bbox_to_anchor=(0.5, 0), fontsize=11, frameon=True, fancybox=True)
plt.tight_layout(pad=0.1)
plt.savefig('output/figs_questionnaire/4b_Privacy_Webcam.jpg', dpi=300, bbox_inches='tight')


#5 Intrusiveness Sense after Experiment
labels = ["Infrared Device was perceived as more intrusive.", "Webcam Device was perceived as more intrusive.", "Both were perceived equally intrusive.", "Neither were perceived intrusive."]
sizes = [40, 30, 20, 10] 
sizes = [40, 30, 20, 10] 
colors = ['#6495ED', '#D2691E', '#B0B0B0', '#32CD32'] 
hatches = ['//', '\\\\', '..', 'xx']

fig, ax = plt.subplots(figsize=(5.5, 3.5))  
wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.2f%%',
                                  colors=colors, startangle=140, pctdistance=0.8,
                                  wedgeprops={'edgecolor': '#4D4D4D', 'linewidth': 2})
i = 0
for wedge in wedges:
    wedge.set_hatch(hatches[i])
    i += 1

total_size = sum(sizes)
for autotext in autotexts:
    autotext.set_color('#333333')
    autotext.set_fontsize(12)  
    autotext.set_weight('bold')
    autotext.set_bbox(dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'))

# ax.set_title(r'\textbf{Intrusiveness sense} after experiment',
#              fontsize=11, color='black', pad=1) 

ax.legend(labels, loc='upper center', bbox_to_anchor=(0.5, 0), fontsize=12, frameon=True, fancybox=True)
plt.tight_layout(pad=0.1)
plt.savefig('output/figs_questionnaire/5_Intrusiveness_Sense.jpg', dpi=300, bbox_inches='tight')


#6a Symtoms Infrared Device

labels = ["No symptoms reported", "Tearing", "Burning Eyes", "Dryness", "Irritation", "Tiredness of eyes"]
sizes = [3, 1, 1, 1, 3, 2]
colors = ['#B0B0B0', '#555555', '#555555', '#555555', '#555555', '#555555']
hatches = ['//', '', '', '', '', '', '']

fig, ax = plt.subplots(figsize=(7, 3.5))
y_pos = np.arange(len(labels))

bars = ax.barh(y_pos, sizes, color=colors, edgecolor='#4D4D4D', linewidth=2)

# Apply hatches
for bar, hatch in zip(bars, hatches):
    bar.set_hatch(hatch)

ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.set_xlabel("Number of Participants", fontsize=16)
ax.set_xticks(np.arange(0, max(sizes) + 1, 1))
ax.set_title(r'a) Symptoms after experiment with \textbf{Infrared device}', fontsize=16, pad=8)
# ax.set_title(r'a)', fontsize=20, color='black', pad=1, loc='left')

plt.tight_layout(pad=0.5)
plt.savefig('output/figs_questionnaire/6a_symptoms_infrared.jpg', dpi=300, bbox_inches='tight')

#6b Symtoms Webcam Device

labels = ["No symptoms reported", "Tearing", "Burning Eyes", "Dryness", "Irritation", "Tiredness of eyes"]
sizes = [7, 0, 0, 2, 0, 1]
colors = ['#B0B0B0', '#555555', '#555555', '#555555', '#555555', '#555555']
hatches = ['//', '', '', '', '', '', '']

fig, ax = plt.subplots(figsize=(7, 3.5))
y_pos = np.arange(len(labels))

bars = ax.barh(y_pos, sizes, color=colors, edgecolor='#4D4D4D', linewidth=2)

# Apply hatches
for bar, hatch in zip(bars, hatches):
    bar.set_hatch(hatch)

ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.set_xlabel("Number of Participants", fontsize=16)
ax.set_xticks(np.arange(0, max(sizes) + 1, 1))
ax.set_title(r'b) Symptoms after experiment with \textbf{Webcam device}', fontsize=16, pad=8)
plt.tight_layout(pad=0.5)
plt.savefig('output/figs_questionnaire/6b_symptoms_webcam.jpg', dpi=300, bbox_inches='tight')