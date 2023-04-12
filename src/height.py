"""
    Script para calcular la altura de los cactus detectados en las imágenes
    satelitales de Google Maps correspondientes al Parque Nacional de Saguaro
    en Arizona, EE.UU.

    Returns:
        file: devuelve el .CSV de "count_cacti.py" o "geoloc_cacti.py" con el
        que trabaja completado con las alturas (en cm) correspondientes a cada bbox.
"""


# BIBLIOTECAS
#_______________________________________________________________________________
from os.path import join as pj
import argparse
from datetime import datetime

import pandas as pd
import numpy as np

from UI.height_ui import UI


# ARGUMENTOS
#_______________________________________________________________________________
parser = argparse.ArgumentParser()

# INTERFAZ GRÁFICA
parser.add_argument(
    "-ui",
    "--user_interface",
    required=False,
    action='store_true',
    help="Muestra una interfaz gráfica"
)

# LÍNEA DE COMANDOS
parser.add_argument(
    "-bbox",
    "--bbox_file",
    required=False,
    default='src/results/bboxes/bbox_file.csv',
    help="Archivo con los bbox a transformar en coordenadas"
)
parser.add_argument(
    "-r",
    "--res_path",
    required=False,
    default='src/results/heights/',
    help="Directorio donde guardar el .csv actualizado con la altura de los cactus"
)
parser.add_argument(
    "-over",
    "--overwrite",
    required=False,
    default=False,
    help="Ignorar height_folder y sobrescribir bboxes_file"
)

args = parser.parse_args()


# VARIABLES GLOBALES
#_______________________________________________________________________________
TXT_TODAY = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
# En SAS Planet la resolución a la que se hizo el cálculo era 0.02m/pixel
PIXEL_TO_CM_FACTOR = 20
SHADOW_TO_HEIGHT_FACTOR = 0.5


# FUNCIONES
#_______________________________________________________________________________
def get_cacti_height(bboxes_file, height_folder, overwrite=False):
    """
    Calcula la altura de los cactus a partir de las dimensiones de su bbox.

    Args:
        bboxes_file (str): arvhico csv con los bboxes de los cactus.
        height_folder (str): carpeta destino donde se guardará el csv resultado.
        overwrite (bool, optional): Ignorar height_folder y sobrescribir
            bboxes_file. Defaults to False.
    """
    print(f'\n\n» Leyendo archivo: {bboxes_file}...')
    bbox_df = pd.read_csv(bboxes_file, encoding='utf-8')

    print(f'\n» Calculando la altura de {len(bbox_df.index)} cactus.')
    bbox_height = np.abs(bbox_df['Y_1'] - bbox_df['Y_0'])
    bbox_width = np.abs(bbox_df['X_1'] - bbox_df['X_0'])
    bbox_diagonal = np.sqrt(bbox_height**2 + bbox_width**2)

    cacti_shadow_height = bbox_diagonal * PIXEL_TO_CM_FACTOR
    real_shadow_height = cacti_shadow_height * SHADOW_TO_HEIGHT_FACTOR

    bbox_df['Height (cm)'] = real_shadow_height

    res_file_path = pj(height_folder,'height_'+TXT_TODAY+'.csv')
    if overwrite:
        res_file_path = bboxes_file

    print(f'\n» COMPLETADO.\n» Resultado guardado en {res_file_path}.\n')

    bbox_df.to_csv(
        res_file_path,
        quoting=None,
        index=False,
        encoding='utf-8'
    )


# EJECUCIÓN
#_______________________________________________________________________________
if __name__ == '__main__':
    if args.user_interface:
        UI(get_cacti_height)
    else:
        get_cacti_height(args.bbox_file, args.res_path)
