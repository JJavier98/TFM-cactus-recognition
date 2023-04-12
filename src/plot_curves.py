"""
    Script para realizar las gráficas de evolución de algunas métricas
    obtenidas durante el entrenamiento.

    Returns:
        files: crea tres imágenes con las curvas de evolución de mAP, mAP_50 y mAP_75
"""


# BIBLIOTECAS
#_______________________________________________________________________________
import argparse
import os

from UI.plot_curve_ui import UI


# ARGUMENTOS
#_______________________________________________________________________________
parser = argparse.ArgumentParser()

# INTERFAZ GRÁFICA
parser.add_argument(
    "-ui",
    "--user_interface",
    required=False,
    action='store_true',
    help="Muestra una interfaz gráfica."
)

# LÍNEA DE COMANDOS
parser.add_argument(
    "-wd",
    "--workdir",
    required=False,
    help="Script de entrenamiento."
)

args = parser.parse_args()


def plot_curve(log_file, metric, out):
    """
    Ejecuta el script de entrenamiento de MMDetection.

    Args:
        train_file (src): script python que contiene el código de entrenamiento.
        config_file (src): script python que contiene la configuración
    """
    os.system(f'python mmdetection/tools/analysis_tools/analyze_logs.py \
        plot_curve {log_file} --keys {metric} --legend {metric} --out {out}')


def save_mAP_curves(workdir):
    """
    Guarda las gráficas con las curvas de las métricas mAP, mAP_50 y
    mAP_75

    Args:
        workdir (str): directorio de trabajo de donde leer las métricas.
    """    
    complete_workdir = os.path.abspath(workdir)
    file_list = os.listdir(complete_workdir)
    json_file = [file for file in file_list if file.endswith('.json')][0]

    out_dir = os.path.join(complete_workdir,'mAP')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    metrics = ['bbox_mAP', 'bbox_mAP_50', 'bbox_mAP_75']
    for metric in metrics:
        in_file = os.path.join(complete_workdir, json_file)
        output_file = os.path.join(out_dir, metric+'.png')
        plot_curve(in_file, metric, output_file)


# EJECUCIÓN
#_______________________________________________________________________________
if __name__ == '__main__':
    if args.user_interface:
        UI(save_mAP_curves)
    else:
        save_mAP_curves(args.workdir)
