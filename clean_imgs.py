import cv2 as cv
import os
from tqdm import tqdm

IMG_TO_CLEAN_PATH = os.path.join('imgs','bing_saguaro_z21_clean')
WRONG_VALUES = [[192, 192, 192], ]

# POI: Pixels of Interest
def go_through_POI(img_path):
    if os.path.isfile(img_path):
        img = cv.imread(img_path)

        wrong_corners = 0
        for i, j in [
                    [img.shape[0]//2,0],  # mid top
                    [img.shape[0]-1, img.shape[1]//2],  # mid right
                    [img.shape[0]//2,img.shape[1]-1],  # mid bottom
                    [0, img.shape[1]//2],  # mid left
                    ]:
            if list(img[i, j]) in WRONG_VALUES:
                wrong_corners += 1

        if wrong_corners > 2:
            # print(f'{img_path} eliminada. Poca información relevante')
            os.remove(img_path)

def main():
    for img_name in tqdm(os.listdir(IMG_TO_CLEAN_PATH)):
        img_path = os.path.join(IMG_TO_CLEAN_PATH, img_name)
        go_through_POI(img_path)

if __name__ == '__main__':
    main()