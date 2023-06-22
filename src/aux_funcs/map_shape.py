"""
    Muestra por pantalla el número de fila y columna máximo y mínimo de todo el
    conjunto de imágenes para saber el tamaño del área muestreada del
    Parque Nacional de Saguaro, Arizona, EE.UU.
"""


# BIBLIOTECAS
#_______________________________________________________________________________
import os


# VARIABLES GLOBALES
#_______________________________________________________________________________
IMG_PATH = os.path.join('data', 'imgs', 'google_maps', 'gm_saguaro_z21_clean')


# FUNCIONES
#_______________________________________________________________________________
def get_min_max_row_col(img_path):
    """
    número de fila y columna máximo y mínimo de todo el conjunto de imágenes

    Args:
        img_path (str): path hasta el directorio con todas las imágenes muestreadas
    """
    imgs_list = os.listdir(img_path)

    max_col = 0
    min_col = 9999
    max_col_img = ''
    min_col_img = ''

    max_row = 0
    min_row = 9999
    max_row_img = ''
    min_row_img = ''
    for img in imgs_list:
        col = img.split('-')[1]
        col = col.split('.')[0]
        col = int(col)

        row = img.split('-')[0]
        row = row.split('_')[1]
        row = int(row)

        if col > max_col:
            max_col = col
            max_col_img = img
        if col < min_col:
            min_col = col
            min_col_img = img

        if row > max_row:
            max_row = row
            max_row_img = img
        if row < min_row:
            min_row = row
            min_row_img = img

    # return min_row, min_col, max_row, max_col

    print(f'Max col: {max_col_img}')
    print(f'Min col: {min_col_img}')
    print(f'Max row: {max_row_img}')
    print(f'Min row: {min_row_img}')


# EJECUCIÓN
#_______________________________________________________________________________
if __name__ == '__main__':
    get_min_max_row_col(IMG_PATH)
