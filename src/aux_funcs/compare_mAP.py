"""
    Script para comparar las gráficas referentes a la métrica mAP de distintos workdirs.

    Returns:
        file: devuelve una imagen en la que se comparan las gráficas de mAP.
"""


# BIBLIOTECAS
#_______________________________________________________________________________
import os
import sys
import cv2

# directory reach
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)

# setting path
sys.path.append(parent)

from UI.compare_mAP_ui import UI


# FUNCIONES
#_______________________________________________________________________________
def format_title(workdir1: str, workdir2: str):
    """
    Formatea el título de la limagen a generar a partir de los nombres de los
    directorios donde se encuentran.

    Args:
        workdir1 (str): directorio de trabajo 1
        workdir2 (str): directorio de trabajo 2

    Returns:
        list(str): lista con los dos str describiendo las características de cada
        directorio de trabajo
    """
    str_titles = []
    for workdir in [workdir1, workdir2]:
        sections = workdir.split('/')

        network = sections[3]

        trained = sections[4]

        epochs = sections[5]

        config = sections[6]
        config = config.split('fpn_1x_')[1]
        config = config.split('_saguaro')[0]

        title = f'{network} - {trained} - {epochs} - {config}'
        str_titles.append(title)

    return str_titles


def compare_mAP(workdir1: str, workdir2: str):
    """
    Concatena las gráficas mAP de los directorios de trabajo de manera que
    en una columna aparecen las gráficas del primer directorio y en la otra columna
    los del otro directorio para poder comparar lado a lado los resultados.

    Args:
        workdir1 (str): directorio de trabajo 1
        workdir2 (str): directorio de trabajo 2
    """
    complete_workdir1 = os.path.join(workdir1, 'mAP')
    complete_workdir2 = os.path.join(workdir2, 'mAP')

    map_list1 = os.listdir(complete_workdir1)
    map_list2 = os.listdir(complete_workdir2)

    assert len(map_list1) == len(map_list2)

    final_image = None
    for i, _ in enumerate(map_list1):
        name_img1 = os.path.join(complete_workdir1, map_list1[i])
        name_img2 = os.path.join(complete_workdir2, map_list2[i])
        img1 = cv2.imread(name_img1)
        img2 = cv2.imread(name_img2)

        horizontal = cv2.hconcat([img1, img2])
        if i == 0:
            final_image = horizontal
        else:
            final_image = cv2.vconcat([final_image, horizontal])

    titles = format_title(workdir1, workdir2)

    output_dir = 'doc'
    file_name = f'{titles[0]}   VS   {titles[1]}.png'
    output_file = os.path.join(output_dir,file_name)
    cv2.imwrite(output_file, final_image)


# EJECUCIÓN
#_______________________________________________________________________________
if __name__ == '__main__':
    UI(compare_mAP)
