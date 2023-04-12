"""
    Script para realizar el entrenamiento sobre las imágenes
    satelitales correspondientes al Parque Nacional de Saguaro
    en Arizona, EE.UU.

    Returns:
        file: devuelve un compendio de archivos correspondientes al entrenamiento
        del moodelo: fases tras cada época, logs y config.
"""


# BIBLIOTECAS
#_______________________________________________________________________________
import argparse
import os
import warnings

from UI.train_ui import UI


# IGNORE WARNINGS
#_______________________________________________________________________________
warnings.filterwarnings('ignore')


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
    "-train",
    "--train_file",
    required=False,
    help="Script de entrenamiento."
)


parser.add_argument(
    "-conf",
    "--config_file",
    required=False,
    help="Archivo de configuración para el entrenamiento."
)

args = parser.parse_args()


def train_model(train_file, config_file):
    """
    Ejecuta el script de entrenamiento de MMDetection.

    Args:
        train_file (src): script python que contiene el código de entrenamiento.
        config_file (src): script python que contiene la configuración
    """
    os.system(f'python {train_file} {config_file}')


# EJECUCIÓN
#_______________________________________________________________________________
if __name__ == '__main__':
    if args.user_interface:
        UI(train_model)
    else:
        train_model(args.train_file, args.config_file)
