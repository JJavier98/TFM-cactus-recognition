import cv2 as cv
import os
from tqdm import tqdm

WRONG_VALUES = [[192, 192, 192], ]

# POI: Pixels of Interest
def _go_through_POI(img_path):
    """
    Elimina las imágenes que tengan menos de la mitad de la matriz
    con píxeles válidos.

    Args:
        img_path (str): path to img
    """    
    if os.path.isfile(img_path):
        img = cv.imread(img_path)

        wrong_POIs = 0
        for i, j in [
                    [img.shape[0]//2,0],  # mid top
                    [img.shape[0]-1, img.shape[1]//2],  # mid right
                    [img.shape[0]//2,img.shape[1]-1],  # mid bottom
                    [0, img.shape[1]//2],  # mid left
                    ]:
            if list(img[i, j]) in WRONG_VALUES:
                wrong_POIs += 1

        if wrong_POIs > 2:
            # print(f'{img_path} eliminada. Poca información relevante')
            os.remove(img_path)

def clean_imgs(path):
    """
    Recorre las imágenes del directorio path y elimina las imágenes inválidas.

    Args:
        path (str): folder with images
    """    
    for img_name in tqdm(os.listdir(path)):
        img_path = os.path.join(path, img_name)
        _go_through_POI(img_path)

if __name__ == '__main__':
    img_to_clean_path = os.path.join('data','imgs','google_maps','bing_saguaro_z21_clean')
    clean_imgs(img_to_clean_path)
