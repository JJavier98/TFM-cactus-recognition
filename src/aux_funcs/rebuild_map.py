"""
    Toma las imágenes fragmentadas del parque y las une completando el mosaico
     del parque nacional de Saguaro completo.
"""


# BIBLIOTECAS
#_______________________________________________________________________________
import os
import numpy as np

from tqdm import tqdm
from PIL import Image


# VARIABLES GLOBALES
#_______________________________________________________________________________
GM_IMG_PATH = os.path.join('data', 'imgs', 'google_maps', 'gm_saguaro_z21_clean')
BM_IMG_PATH = os.path.join('data', 'imgs', 'bing_maps', 'bing_saguaro_z21_clean')
RES_IMG_PATH = os.path.join('results','google-over-google_01032023_200627','imgs_01-03-2023_20-06-27')
RES_IMG_PATH_2 = os.path.join('src', 'results', 'imgs', '10-02-2023_11-18-48')

IMG_WIDTH = 255
IMG_HEIGHT = 255

MIN_ROW, MIN_COL, MAX_ROW, MAX_COL = (1, 1, 502, 361)

BACKGROUND = np.zeros((IMG_WIDTH, IMG_HEIGHT, 3))


# FUNCIONES
#_______________________________________________________________________________
def get_col(img_name):
    """
    Devuelve el número de la columna que corresponde a la imagen pasada como 
    argumento.

    Args:
        img_name (str): nombre de la imagen

    Returns:
        int: número de la columna que ocupa la imagen
    """
    col = img_name.split('img_')[1]
    col = col.split('-')[0]
    return int(col)


def get_row(img_name):
    """
    Devuelve el número de la fila que corresponde a la imagen pasada como 
    argumento.

    Args:
        img_name (str): nombre de la imagen

    Returns:
        int: número de la fila que ocupa la imagen
    """
    row = img_name.split('-')[1]
    row = row.split('.')[0]
    return int(row)


def rename_results(path):
    """
    Cambia el nombre de archivo de las imágenes para que sean ordenadas de manera
    correcta y sobreescribe los nombres originales

    Args:
        path (str): directorio que contiene las imágenes
    """
    imgs_list = os.listdir(path)
    for img_name in tqdm(imgs_list):
        col = str(get_col(img_name))
        row = str(get_row(img_name))
        new_name = 'res_img_0' + '0'*(3-len(col)) + f'{col}-0' + '0'*(3-len(row)) + f'{row}.jpg'
        os.rename(os.path.join(path,img_name), os.path.join(path,new_name))


def rename_results_v2(path):
    """
    Cambia el nombre de archivo de las imágenes para que sean ordenadas de manera
    correcta. NO sobreescribe los nombres originales sino que devuelve en una variable
    los nuevos nombres para trabajar con ellos en memoria.

    Args:
        path (str): directorio que contiene las imágenes
    """
    imgs_list = os.listdir(path)
    new_imgs_list = {}
    for img_name in tqdm(imgs_list):
        col = str(get_col(img_name))
        row = str(get_row(img_name))
        new_name = 'res_img_0' + '0'*(3-len(col)) + f'{col}-0' + '0'*(3-len(row)) + f'{row}.jpg'
        new_imgs_list[new_name] = img_name

    return new_imgs_list


def main():
    """
    Función principal en la que se realiza la reconstrucción del mapa.
    """    
    imgs_list = rename_results_v2(RES_IMG_PATH)

    old_col = 0
    old_row = 0
    row_img = None  # Full image
    col_img = None
    for key in tqdm(sorted(imgs_list.keys())[:300]):
        img_name = imgs_list[key]
        current_col = get_col(img_name)
        current_row = get_row(img_name)
        nueva_columna = old_col != current_col

        with Image.open(os.path.join(RES_IMG_PATH, img_name)) as img_pil:
            # img_pil = img_pil.resize((IMG_WIDTH,IMG_HEIGHT), Image.ANTIALIAS)
            img = np.asarray(img_pil, dtype=np.uint8)

        if nueva_columna:
            # rellena por el final si no se ha llegado a la última fila
            if old_row != 361 and old_col > 0:
                #fill = np.repeat(BACKGROUND, 361-old_row, axis=0)
                fill = np.zeros((IMG_WIDTH*(361-old_row), IMG_HEIGHT, 3))
                col_img = np.append(col_img, fill, axis=0)

            if old_col==1:
                row_img = col_img
            if old_col>1:
                row_img = np.append(row_img, col_img, axis=1)
                img_to_save = Image.fromarray(np.uint8(row_img))
                img_to_save.save('MapComplete.png')

            col_img = img

            # Si se empieza una nueva columna y la primera fila leida no es la 1
            if current_row != 1:
                col_img = BACKGROUND
                fill = np.repeat(BACKGROUND, current_row-(1+1), axis=0)
                # fill = np.zeros((IMG_WIDTH*(current_row-(1+1)), IMG_HEIGHT, 3))
                col_img = np.append(col_img, fill, axis=0)
                col_img = np.append(col_img, img, axis=0)
        else:
            # Si la siguiente imagen leida no es consecutiva a la anterior
            # se rellena con background
            if current_row > old_row+1:
                fill = np.repeat(BACKGROUND, current_row-(old_row+1), axis=0)
                # fill = np.zeros((IMG_WIDTH*(current_row-(old_row+1)), IMG_HEIGHT, 3))
                col_img = np.append(col_img, fill, axis=0)

            col_img = np.append(col_img, img, axis=0)        

        old_col = current_col
        old_row = current_row

    img = Image.fromarray(np.uint8(row_img))
    img.save('MapComplete.png')


# EJECUCIÓN
#_______________________________________________________________________________
if __name__ == '__main__':
    main()