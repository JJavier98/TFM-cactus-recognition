# BIBLIOTECAS
#_______________________________________________________________________________
import timeit
import os
from os.path import join as pj
import argparse
from datetime import datetime

import pandas as pd
import numpy as np
from tqdm import tqdm
from mmdet.apis import init_detector, inference_detector

from count_cacti_UI import UI


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
    "-i",
    "--imgs_path",
    required=False,
    default='src/imgs_prueba/',
    help="Directorio donde se encuentran las imágenes a testear."
)
parser.add_argument(
    "-r",
    "--res_path",
    required=False,
    default='src/results/',
    help="Directorio donde guardar los resultados: imágenes, bboxes, logs"
)
parser.add_argument(
    "-s",
    "--save_imgs",
    required=False,
    action='store_true',
    help="Si se indica, las imágenes resultado serán almacenadas"
)
parser.add_argument(
    "-t",
    "--threshold",
    required=False,
    default=0.5,
    help="Nivel de confianza en la detección y etiquetado de los cactus."
)
parser.add_argument(
    "-co",
    "--config_file",
    required=False,
    default='mmdetection/configs/cactus/faster_rcnn_r50_fpn_1x_saguaro.py',
    help="Si se indica, almacena los resultados en dicho archivo."
)
parser.add_argument(
    "-ch",
    "--checkpoint_file",
    required=False,
    default='mmdetection/work_dirs/faster_rcnn_r50_fpn_1x_saguaro/latest.pth',
    help="Si se indica, almacena los resultados en dicho archivo."
)

args = parser.parse_args()


# VARIABLES GLOBALES
#_______________________________________________________________________________
TXT_TODAY = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")


# FUNCIONES
#_______________________________________________________________________________
def print_save_results(res_list, bbox_file, out_file=None):
    """
    Muestra los resultados y configuraciones por terminal y los escribe en un 
    archivo si se indica.

    Args:
        res_list (list(str)): lista con las líneas a mostrar/escribir
        bbox_file (str): path hacia el archivo donde se guardarán los bbox calculados.
        out_file (str, optional): path hacia el archivo de resultados. Defaults to None.
    """
    print('')
    if out_file:
        out_file = open(out_file, 'a', encoding='utf-8')

    for res in res_list[:-1]:
        print(res)
        out_file.write(res)
        out_file.write('\n')

    print('')
    out_file.write('\n')
    out_file.write('\n')
    out_file.close()

    if bbox_file:
        res_list[-1].to_csv(bbox_file, index=False)


def run(args):
    """
    Función encargada de realizar las principales tareas que ocupa este script:
    detección y conteo de cactus
    Args:
        args (object): argumentos necesarios para la ejecución del programa

    Returns:
        tuple: data frame de bboxes, número de bboxes, número imgs
    """
    # Specify the path to model config and checkpoint file
    config_file = args.config_file
    checkpoint_file = args.checkpoint_file
    img_path = args.imgs_path
    results_path = args.res_path
    threshold = args.threshold
    save_imgs = args.save_imgs

    # build the model from a config file and a checkpoint file
    device = 'cuda:0'
    model = init_detector(config_file, checkpoint_file, device=device)

    n_bbox = 0
    n_imgs = 0
    bbox_pd = pd.DataFrame(
        columns = [
            'Img Name',
            'X_0',
            'Y_0',
            'X_1',
            'Y_1',
            'Confidence',
            'Bbox'
        ]
    )
    imgs_list = os.listdir(img_path)
    for img_name in tqdm(imgs_list):
        img = pj(img_path, img_name)

        if os.path.isfile(img):

            n_imgs += 1
            # result es un vector de 5 componentes
            # contiene los bboxes (4 primeras coords) y el score (la última)
            result = inference_detector(model, img)
            if save_imgs:
                model.show_result(
                    img,
                    result,
                    score_thr = float(threshold),
                    out_file = pj(results_path, 'imgs', TXT_TODAY, 'res_'+img_name)
                )

            bboxes = np.vstack(result)
            bboxes = bboxes[np.where(bboxes[:,-1] >= float(threshold))]
            n_bbox += len(bboxes)

            new_row = pd.DataFrame(
                {
                    'Img Name' : img_name,
                    'X_0' : bboxes[:,0],
                    'Y_0' : bboxes[:,1],
                    'X_1' : bboxes[:,2],
                    'Y_1' : bboxes[:,3],
                    'Confidence' : bboxes[:,4],
                    'Bbox' : bboxes.tolist()
                }
            )
            bbox_pd = pd.concat([bbox_pd, new_row], ignore_index=True)

    return bbox_pd, n_bbox, n_imgs


# FUNCIÓN MAIN
#_______________________________________________________________________________
def main(args):
    """
    Función main del programa que reune todas las operaciones a realizar.

    Args:
        args (object): argumentos necesarios para la ejecución del programa

    Returns:
        list: lista con todos los datos en formato texto para ser mostrados
    """
    secuential_start = timeit.default_timer()
    bbox_list, n_bbox, n_imgs = run(args)
    secuential_stop = timeit.default_timer()

    txt_exe_time = f'Tiempo de ejecución: {secuential_stop - secuential_start:.2f} segundos'
    txt_n_imgs = f'Número de imágenes analizadas: {n_imgs}'
    txt_n_cacti = f'Número de cactus detectados: {n_bbox}'
    txt_config_file = f'Archivo de configuración: {args.config_file}'
    txt_checkpoint_file = f'Archivo de control: {args.checkpoint_file}'
    bbox_file = pj(args.res_path, 'bboxes', 'bbox_'+TXT_TODAY+".csv")
    txt_bbox_file = f'Archivo con todos los bbox detectados: {bbox_file}'

    res_list = [
        TXT_TODAY,
        txt_exe_time,
        txt_n_imgs,
        txt_n_cacti,
        txt_config_file,
        txt_checkpoint_file,
        txt_bbox_file,
        bbox_list
    ]
    print_save_results(
        res_list=res_list,
        bbox_file=bbox_file,
        out_file=pj(args.res_path, 'logs', 'log_'+TXT_TODAY+'.log')
    )

    return res_list


# EJECUCIÓN
#_______________________________________________________________________________
if __name__ == '__main__':
    if args.user_interface:
        app = UI(main)
    else:
        main(args)
