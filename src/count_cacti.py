import numpy as np
import timeit
import os
import argparse
from tqdm import tqdm
from mmdet.apis import init_detector, inference_detector
from datetime import datetime


parser = argparse.ArgumentParser()
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
    default='src/results/imgs/',
    help="Directorio donde guardar las imágenes resultado. \
        Si no se indica, no se almacenarán las imágenes con bbox."
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
parser.add_argument(
    "-o",
    "--out_file",
    required=False,
    default='src/results/results.txt',
    help="Si se indica, almacena los resultados en dicho archivo."
)
parser.add_argument(
    "-bbox",
    "--bbox_file",
    required=False,
    default='src/results/bboxes/bbox_',
    help="Si se indica, almacena los resultados en dicho archivo."
)
args = parser.parse_args()


TXT_TODAY = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")


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
        with open(bbox_file, 'a', encoding='utf-8') as file:
            for line in res_list[-1]:
                file.writelines(str(line)+'\n')


def main(args):
    # Specify the path to model config and checkpoint file
    config_file = args.config_file
    checkpoint_file = args.checkpoint_file
    img_path = args.imgs_path
    results_path = args.res_path
    threshold = args.threshold

    # build the model from a config file and a checkpoint file
    device = 'cuda:0'
    model = init_detector(config_file, checkpoint_file, device=device)

    n_bbox = 0
    n_imgs = 0
    bbox_list = np.array(['#','#','#','#','#'])
    bbox_list = bbox_list[np.newaxis, :]
    imgs_list = os.listdir(img_path)
    for img_name in tqdm(imgs_list):
        img = os.path.join(img_path, img_name)

        if os.path.isfile(img):
            
            n_imgs += 1
            # result es un vector de 5 componentes
            # contiene los bboxes (4 primeras coords) y el score (la última)
            result = inference_detector(model, img)
            if results_path:
                model.show_result(
                    img,
                    result,
                    score_thr = float(threshold),
                    out_file = os.path.join(results_path, TXT_TODAY, 'res_'+img_name)
                )
            
            bboxes = np.vstack(result)
            bboxes = bboxes[np.where(bboxes[:,-1] >= float(threshold))]
            n_bbox += len(bboxes)
            
            aux_bbox_list = np.array(['#','#','#','#',img_name])
            aux_bbox_list = aux_bbox_list[np.newaxis, :]
            aux_bbox_list = np.append(aux_bbox_list, bboxes, axis=0)
            bbox_list = np.append(bbox_list, aux_bbox_list, axis=0)

    return bbox_list, n_bbox, n_imgs


if __name__ == '__main__':
    secuential_start = timeit.default_timer()
    bbox_list, n_bbox, n_imgs = main(args)
    secuential_stop = timeit.default_timer()

    txt_exe_time = f'Tiempo de ejecución: {secuential_stop - secuential_start:.2f}'
    txt_n_imgs = f'Número de imágenes analizadas: {n_imgs}'
    txt_n_cacti = f'Número de cactus detectados: {n_bbox}'
    txt_config_file = f'Archivo de configuración: {args.config_file}'
    txt_checkpoint_file = f'Archivo de control: {args.checkpoint_file}'
    txt_bbox_file = f'Archivo con todos los bbox detectados: {args.bbox_file+TXT_TODAY+".txt"}'

    print_save_results(
        res_list=[
            TXT_TODAY,
            txt_exe_time,
            txt_n_imgs,
            txt_n_cacti,
            txt_config_file,
            txt_checkpoint_file,
            txt_bbox_file,
            bbox_list[1:,:]
        ],
        bbox_file=args.bbox_file+TXT_TODAY+".txt",
        out_file=args.out_file
    )
