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


#RQ1_TC1 (Form Density Low)
data = {
    '% Matching Fixation': [
        percentage_matching_fixation_rq1_tobii_form_density_low,
        percentage_matching_fixation_rq1_webgazer_form_density_low
    ],
    'Device/Software (TC1)': [
        r'\textbf{Infrared/Tobii Pro Spark}',  # Texto en negrita en LaTeX
        r'\textbf{Webcam/Webgazer.js}'  # Lo mismo para el segundo texto
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
            ha='center', va='bottom', fontsize=18, color='#555555', weight='bold')  

plt.text(-0.1, 1.20, r'\textbf{a)}', 
         fontsize=26, color='black', ha='left', va='top', transform=ax.transAxes)
plt.ylabel(r'\textbf{STMF (\%)}', fontsize=16, color='#555555')
plt.xticks(rotation=0, ha='center', fontsize=16, color='#555555')
yticks = np.arange(0, 120, 20)
ytick_labels = [rf"{y}\%" for y in yticks]
plt.yticks(yticks, ytick_labels, fontsize=16, color='#555555')
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('output/figs/RQ1_TC1_STMF.jpg', dpi=300)
plt.show()


#RQ1_TC2 (Form Density High)
data = {
    '% Matching Fixation': [percentage_matching_fixation_rq1_tobii_form_density_high,
                          percentage_matching_fixation_rq1_webgazer_form_density_high],
    'Device/Software (TC2)': ['Infrared/Tobii Pro Spark', 'Webcam/Webgazer.js']}
df = pd.DataFrame(data)
fig, ax = plt.subplots(figsize=(9.85, 5.5))
bars = plt.bar(df['Device/Software (TC2)'], df['% Matching Fixation'], 
               color=['#E97132', '#156082'])
for bar, pct in zip(bars, df['% Matching Fixation']):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{pct:.2f}%', 
             ha='center', va='bottom', fontsize=16,  color='#555555', weight='bold')
plt.title('Single Target Matching Fixations (STMF) by Device (TC2)', 
          fontsize=16,  color='#555555')
plt.ylabel('STMF (%)', fontsize=16,  color='#555555')
plt.xticks(rotation=0, ha='center', fontsize=16,  color='#555555')
plt.yticks(yticks, ytick_labels, fontsize=16,  color='#555555')
plt.ylim(0, 110)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('output/figs/RQ1_TC2_STMF.jpg')


# RQ1_TC1 (MAE Form Density Low)
data = {
    'Mean Error Distance': [average_error_distance_rq1_tobii_form_density_low,
                            average_error_distance_rq1_webgazer_form_density_low,],
    'Device/Software (TC1)': ['Infrared/Tobii Pro Spark', 'Webcam/Webgazer.js',],}
df = pd.DataFrame(data)
fig, ax = plt.subplots(figsize=(9.85, 5.5))
bars = plt.bar(df['Device/Software (TC1)'], df['Mean Error Distance'], 
               color=['#E97132', '#156082'])
for bar, pct in zip(bars, df['Mean Error Distance']):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{pct:.2f}px',
             ha='center', va='bottom', fontsize=16,  color='#555555', weight='bold')
plt.title('Mean Absolute Error (MAE) by Device (TC1)', fontsize=16,  color='#555555')
plt.ylabel('MAE (px)', fontsize=16,  color='#555555')
plt.xticks(rotation=0, ha='center', fontsize=16,  color='#555555')
plt.yticks(yticks_mae, ytick_labels_mae, fontsize=16,  color='#555555')
plt.ylim(0, 400)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('output/figs/RQ1_TC1_MAE.jpg')


# RQ1_TC2 (MAE Form Density High)
data = {
    'Mean Error Distance': [average_error_distance_rq1_tobii_form_density_high,
                            average_error_distance_rq1_webgazer_form_density_high,],
    'Device/Software (TC2)': ['Infrared/Tobii Pro Spark', 'Webcam/Webgazer.js',],}
df = pd.DataFrame(data)
fig, ax = plt.subplots(figsize=(9.85, 5.5))
bars = plt.bar(df['Device/Software (TC2)'], df['Mean Error Distance'], 
               color=['#E97132', '#156082'])
for bar, pct in zip(bars, df['Mean Error Distance']):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{pct:.2f}px',
             ha='center', va='bottom', fontsize=16,  color='#555555', weight='bold')
plt.title('Mean Absolute Error (MAE) by Device (TC2)', fontsize=16,  color='#555555')
plt.ylabel('MAE (px)', fontsize=16,  color='#555555')
plt.xticks(rotation=0, ha='center', fontsize=16,  color='#555555')
plt.yticks(yticks_mae, ytick_labels_mae, fontsize=16,  color='#555555')
plt.ylim(0, 400)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('output/figs/RQ1_TC2_MAE.jpg')



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



# TC3_RQ2_Matching fixations (Alternance Buttons)
new_data_rq2 = {
    '% Matching Fixation': [percentage_matching_fixation_rq2_tobii_alternance_buttons,
                            percentage_matching_fixation_rq2_webgazer_alternance_buttons],
    'Device/Software': ['Infrared/Tobii Pro Spark', 'Webcam/Webgazer.js']
}
new_df = pd.DataFrame(new_data_rq2)
fig, ax = plt.subplots(figsize=(9.85, 5.5))
bars = plt.bar(new_df['Device/Software'], new_df['% Matching Fixation'], color=['#E97132', '#156082'])
for bar, pct in zip(bars, new_df['% Matching Fixation']):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{pct:.2f}%', 
            ha='center', va='bottom', fontsize=16,  color='#555555' ,weight='bold')
plt.title('Single Target Matching Fixations (STMF) by Device (TC3)', fontsize=16 , color='#555555')
plt.ylabel('STMF (%)', fontsize=16,  color='#555555')
plt.xticks(rotation=0, ha='center', fontsize=16,  color='#555555')
plt.yticks(yticks, ytick_labels, fontsize=16,  color='#555555')
plt.ylim(0, 110)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('output/figs/RQ2_TC3_STMF.jpg')


#RQ2_TC3 EIF (Alternance Buttons)
tools = [ "Infrared/Tobii Pro Spark","Webcam/Webgazer.js",]
percentages = [percentage_events_including_fixations_rq2_tobii_alternance_buttons,
               percetange_events_including_fixations_rq2_webgazer_alternance_buttons]
fig, ax = plt.subplots(figsize=(9.85, 5.5))
bars = ax.bar(tools, percentages, color=['#E97132', '#156082'])
ax.set_ylabel("% EIF")
ax.set_title("% Events Including Fixation (EIF) by Device/Software (TC3)")
ax.set_ylim(0, 110)  # Limitar el eje Y para espacio adicional
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, 
            height - 5,  
            f'{height:.2f}%',  
            ha='center', va='top', 
            fontsize=16,  color='white', weight='bold')     
plt.title('Events Including Fixations (EIF) by Device (TC3)', fontsize=16 , color='#555555')
plt.ylabel('EIF (%)', fontsize=16,  color='#555555')
plt.xticks(rotation=0, ha='center', fontsize=16,  color='#555555')
plt.yticks(yticks, ytick_labels, fontsize=16,  color='#555555')
plt.ylim(0, 110)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.tight_layout()
plt.savefig('output/figs/RQ2_TC3_EIF.jpg')


#RQ2_TC3 (mean MAE)
data = {
    'Mean Error Distance': [average_error_distance_rq2_tobii_alternance_buttons,
                            average_error_distance_rq2_webgazer_alternance_buttons,],   
    'Device/Software': ['Infrared/Tobii Pro Spark', 'Webcam/Webgazer.js',],}
df = pd.DataFrame(data)
fig, ax = plt.subplots(figsize=(9.85, 5.5))
bars = plt.bar(df['Device/Software'], df['Mean Error Distance'], 
               color=['#E97132', '#156082'])
for bar, pct in zip(bars, df['Mean Error Distance']):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{pct:.2f}px',
             ha='center', va='bottom', fontsize=16,  color='#555555', weight='bold')
plt.title('Mean Absolute Error (MAE) by Device (TC3)', fontsize=16,  color='#555555')
plt.ylabel('MAE (px)', fontsize=16,  color='#555555')
plt.xticks(rotation=0, ha='center', fontsize=16,  color='#555555')
plt.yticks(yticks_mae, ytick_labels_mae, fontsize=16,  color='#555555')
plt.ylim(0, 400)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('output/figs/RQ2_TC3_MAE.jpg')


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
x = np.arange(len(positions))  
width = 0.3
fig, ax = plt.subplots(figsize=(9.85, 5.5))
bars_tobii = ax.bar(x - width / 3, percentages_tobii, width, label="Infrared/Tobii Pro Spark", color='#E97132')
bars_webgazer = ax.bar(x + width, percentages_webgazer, width, label="Webcam/Webgazer.js", color='#156082')
ax.set_xlabel("Test Case (User-Screen/Device distance)", fontsize=16,  color='#555555')
ax.set_ylabel("EIF (%)", fontsize=16,  color='#555555')
ax.set_title("Events Including Fixation (EIF) by Device and Test Case (TC4,TC5,TC6)", 
             fontsize=16,  color='#555555')
ax.set_xticks(x)
ax.set_xticklabels(positions, fontsize=16,  color='#555555')
plt.grid(axis='y', linestyle='--', alpha=0.7)
ax.tick_params(axis='y', labelsize=16, colors='#555555')
ax.set_yticks(np.linspace(0, 100, 6))  
ax.set_ylim(0, 110)  
def percent_formatter(x, pos):
    return f'{x:.2f}%'
ax.yaxis.set_major_formatter(FuncFormatter(percent_formatter))
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height - 5,  
                f'{height:.2f}%', ha='center', va='top', fontsize=16, 
                 color='white', weight='bold')  
add_labels(bars_webgazer)
add_labels(bars_tobii)
ax.legend(fontsize=16, frameon=True)
plt.tight_layout()
plt.savefig('output/figs/RQ3_TC4_TC5_TC6_EIF_bars.jpg')

# Datos grafico linea events_captured_fixations

positions = ["TC4 (50cm)", "TC5 (70cm)", "TC6 (90cm)"]
percentages_tobii = [percentage_events_including_fixations_rq3_tobii_position_50cm,
                     percentage_events_including_fixations_rq3_tobii_position_70cm,
                     percentage_events_including_fixations_rq3_tobii_position_90cm]
percentages_webgazer = [percentage_events_including_fixations_rq3_webgazer_position_50cm,
                        percentage_events_including_fixations_rq3_webgazer_position_70cm,
                        percentage_events_including_fixations_rq3_webgazer_position_90cm]


x = np.arange(len(positions))  
fig, ax = plt.subplots(figsize=(9.85, 5.5))

ax.plot(x, percentages_tobii, marker='o', linestyle='-', linewidth=3, markersize=10, 
        label="Infrared/Tobii Pro Spark", color='#E97132')
ax.plot(x, percentages_webgazer, marker='s', linestyle='-', linewidth=3, markersize=10, 
        label="Webcam/Webgazer.js", color='#156082')

ax.set_xlabel("Test Case (User-Screen/Device distance)", fontsize=16,  color='#555555')
ax.set_ylabel("EIF (%)", fontsize=16,  color='#555555')
ax.set_title("Events Including Fixation (EIF) by Device and Test Case (TC4,TC5,TC6)", 
             fontsize=16,  color='#555555')

ax.set_xticks(x)
ax.set_xticklabels(positions, fontsize=16,  color='#555555')

plt.grid(axis='y', linestyle='--', alpha=0.7)
ax.tick_params(axis='y', labelsize=16, colors='#555555')
ax.set_yticks(np.linspace(0, 100, 6))
ax.set_ylim(0, 110)

def percent_formatter(x, pos): 
    return f'{x:.2f}%'

ax.yaxis.set_major_formatter(FuncFormatter(percent_formatter))

for i, value in enumerate(percentages_tobii):
    ax.text(x[i], value + 2, f'{value:.1f}%', ha='center', fontsize=16, color='#E97132')

for i, value in enumerate(percentages_webgazer):
    ax.text(x[i], value + 2, f'{value:.1f}%', ha='center', fontsize=16, color='#156082')

ax.legend(fontsize=16, frameon=True) 
plt.tight_layout()
plt.savefig('output/figs/RQ3_TC4_TC5_TC6_EIF_line.jpg')


# RQ3_TC4_TC5_TC6 Matching Fixations (STMF)
percentage_matching_fixation_rq3_tobii_position_50cm = rq3__tobii_position_50cm['%MatchingFixations'].mean()
percentage_matching_fixation_rq3_tobii_position_70cm = rq3__tobii_position_70cm['%MatchingFixations'].mean()
percentage_matching_fixation_rq3_tobii_position_90cm = rq3__tobii_position_90cm['%MatchingFixations'].mean()
percentage_matching_fixation_rq3_webgazer_position_50cm = rq3__webgazer_position_50cm['%MatchingFixations'].mean()
percentage_matching_fixation_rq3_webgazer_position_70cm = rq3__webgazer_position_70cm['%MatchingFixations'].mean()
percentage_matching_fixation_rq3_webgazer_position_90cm = rq3__webgazer_position_90cm['%MatchingFixations'].mean()

tools = ["Infrared/Tobii Pro Spark","Webcam/Webgazer.js"]
positions = ["TC4 (50cm)", "TC5 (70cm)", "TC6 (90cm)"]
percentages_tobii = [percentage_matching_fixation_rq3_tobii_position_50cm,
                     percentage_matching_fixation_rq3_tobii_position_70cm,
                     percentage_matching_fixation_rq3_tobii_position_90cm]
percentages_webgazer = [percentage_matching_fixation_rq3_webgazer_position_50cm,
                        percentage_matching_fixation_rq3_webgazer_position_70cm,
                        percentage_matching_fixation_rq3_webgazer_position_90cm]

x = np.arange(len(positions))  
width = 0.3
fig, ax = plt.subplots(figsize=(9.85, 5.5))
bars_tobii = ax.bar(x - width / 3, percentages_tobii, width, label="Infrared/Tobii Pro Spark", color='#E97132')
bars_webgazer = ax.bar(x + width, percentages_webgazer, width, label="Webcam/Webgazer.js", color='#156082')
ax.set_xlabel("Test Case (User-Screen/Device distance)", fontsize=16,  color='#555555')
ax.set_ylabel("STMF (%)", fontsize=16,  color='#555555')
ax.set_title("Single Target Matching Fixations (STMF) by Device and Test Case (TC4,TC5,TC6)", 
             fontsize=16,  color='#555555')
ax.set_xticks(x)
ax.set_xticklabels(positions, fontsize=16,  color='#555555')
plt.grid(axis='y', linestyle='--', alpha=0.7)
ax.tick_params(axis='y', labelsize=16, colors='#555555')
ax.set_yticks(np.linspace(0, 100, 6))  
ax.set_ylim(0, 110)  
def percent_formatter(x, pos):
    return f'{x:.2f}%'
ax.yaxis.set_major_formatter(FuncFormatter(percent_formatter))
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height - 5,  
                f'{height:.2f}%', ha='center', va='top', fontsize=16, 
                 color='white', weight='bold')  
add_labels(bars_tobii)
add_labels(bars_webgazer)
ax.legend(fontsize=16, frameon=True)
plt.tight_layout()
plt.savefig('output/figs/RQ3_TC4_TC5_TC6_STMF_bars.jpg')


# Datos Matching fixations linea
positions = ["TC4 (50cm)", "TC5 (70cm)", "TC6 (90cm)"]
percentages_tobii = [percentage_matching_fixation_rq3_tobii_position_50cm,
                     percentage_matching_fixation_rq3_tobii_position_70cm,
                     percentage_matching_fixation_rq3_tobii_position_90cm]
percentages_webgazer = [percentage_matching_fixation_rq3_webgazer_position_50cm,
                        percentage_matching_fixation_rq3_webgazer_position_70cm,
                        percentage_matching_fixation_rq3_webgazer_position_90cm]

x = np.arange(len(positions))  
fig, ax = plt.subplots(figsize=(9.85, 5.5))

ax.plot(x, percentages_tobii, marker='o', linestyle='-', linewidth=3, markersize=10, 
        label="Infrared/Tobii Pro Spark", color='#E97132')
ax.plot(x, percentages_webgazer, marker='s', linestyle='-', linewidth=3, markersize=10, 
        label="Webcam/Webgazer.js", color='#156082')

ax.set_xlabel("Test Case (User-Screen/Device distance)", fontsize=16,  color='#555555')
ax.set_ylabel("STMF (%)", fontsize=16,  color='#555555')
ax.set_title("Single Target Matching Fixations (STMF) by Device and Test Case (TC4,TC5,TC6)", 
             fontsize=16,  color='#555555')

ax.set_xticks(x)
ax.set_xticklabels(positions, fontsize=16,  color='#555555')

plt.grid(axis='y', linestyle='--', alpha=0.7)
ax.tick_params(axis='y', labelsize=16, colors='#555555')
ax.set_yticks(np.linspace(0, 100, 6))
ax.set_ylim(0, 110)

def percent_formatter(x, pos): 
    return f'{x:.2f}%'

ax.yaxis.set_major_formatter(FuncFormatter(percent_formatter))

for i, value in enumerate(percentages_tobii):
    ax.text(x[i], value + 2, f'{value:.1f}%', ha='center', fontsize=16, color='#E97132')

for i, value in enumerate(percentages_webgazer):
    ax.text(x[i], value + 2, f'{value:.1f}%', ha='center', fontsize=16, color='#156082')

ax.legend(fontsize=16, frameon=True) 
plt.tight_layout()
plt.savefig('output/figs/RQ3_TC4_TC5_TC6_STMF_line.jpg')


# Datos mean MAE RQ3
average_error_distance_rq3_tobii_position_50cm = rq3__tobii_position_50cm['MAE'].mean()
average_error_distance_rq3_tobii_position_70cm = rq3__tobii_position_70cm['MAE'].mean()
average_error_distance_rq3_tobii_position_90cm = rq3__tobii_position_90cm['MAE'].mean()
average_error_distance_rq3_webgazer_position_50cm = rq3__webgazer_position_50cm['MAE'].mean()
average_error_distance_rq3_webgazer_position_70cm = rq3__webgazer_position_70cm['MAE'].mean()
average_error_distance_rq3_webgazer_position_90cm = rq3__webgazer_position_90cm['MAE'].mean()

positions = ["TC4 (50cm)", "TC5 (70cm)", "TC6 (90cm)"]
med_tobii = [average_error_distance_rq3_tobii_position_50cm,
             average_error_distance_rq3_tobii_position_70cm,
             average_error_distance_rq3_tobii_position_90cm]
med_webgazer = [average_error_distance_rq3_webgazer_position_50cm,
                average_error_distance_rq3_webgazer_position_70cm,
                average_error_distance_rq3_webgazer_position_90cm]

x = np.arange(len(positions))  
width = 0.3
fig, ax = plt.subplots(figsize=(9.85, 5.5))
bars_tobii = ax.bar(x - width / 3, med_tobii, width, label="Infrared/Tobii Pro Spark", color='#E97132')
bars_webgazer = ax.bar(x + width, med_webgazer, width, label="Webcam/Webgazer.js", color='#156082')
ax.set_xlabel("Test Case (User-Screen/Device distance)", fontsize=16,  color='#555555')
ax.set_ylabel("MAE (px)", fontsize=16,  color='#555555')
ax.set_title("Mean Absolute Error (MAE) by Device and Test Case (TC4,TC5,TC6)", 
             fontsize=16,  color='#555555')
ax.set_xticks(x)
ax.set_xticklabels(positions, fontsize=16,  color='#555555')
plt.grid(axis='y', linestyle='--', alpha=0.7)
ax.tick_params(axis='y', labelsize=16, colors='#555555')
ax.set_yticks(np.linspace(0, 400, 5))  
ax.set_ylim(0, 400)  
def percent_formatter(x, pos):
    return f'{x:.2f}'
ax.yaxis.set_major_formatter(FuncFormatter(percent_formatter))
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height - 5,  
                f'{height:.2f}px', ha='center', va='top', fontsize=16, 
                 color='white', weight='bold')  
add_labels(bars_tobii)
add_labels(bars_webgazer)
ax.legend(fontsize=16, frameon=True)
plt.tight_layout()
plt.savefig('output/figs/RQ3_TC4_TC5_TC6_MAE.jpg')
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
# plt.savefig('output/figs/RQ4_EITOF_TC7.jpg')
# Mostrar gráfico
# plt.show()

# Datos %Matching_test_object_fixations
percentage_matching_test_object_fixations_rq4_tobii_rpm = rq4_tobii_rpm['%RelevantFixations'].mean()
percentage_matching_test_object_fixations_rq4_webgazer_rpm = rq4_webgazer_rpm['%RelevantFixations'].mean()


new_data_rq4 = {
    '% Matching Fixation': [percentage_matching_test_object_fixations_rq4_tobii_rpm,
                            percentage_matching_test_object_fixations_rq4_webgazer_rpm],
    'Device/Software': ['Infrared/Tobii Pro Spark', 'Webcam/Webgazer.js']
}
new_df = pd.DataFrame(new_data_rq4)
fig, ax = plt.subplots(figsize=(9.85, 5.5))
bars = plt.bar(new_df['Device/Software'], new_df['% Matching Fixation'], color=['#E97132', '#156082'])
for bar, pct in zip(bars, new_df['% Matching Fixation']):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{pct:.2f}%', 
            ha='center', va='bottom', fontsize=16,  color='#555555' ,weight='bold')
plt.title('Multiple Target Matching Fixations (MTMF) by Device (TC7)', fontsize=16 , color='#555555')
plt.ylabel('MTMF (%)', fontsize=16,  color='#555555')
plt.xticks(rotation=0, ha='center', fontsize=16,  color='#555555')
plt.yticks(yticks, ytick_labels, fontsize=16,  color='#555555')
plt.ylim(0, 110)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('output/figs/RQ4_TC7_MTMF.jpg')
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


