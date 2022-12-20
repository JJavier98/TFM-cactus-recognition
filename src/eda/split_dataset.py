import os
from tqdm import tqdm
import random
import shutil

def split_dataset(source_folder, train_folder, val_folder, test_folder, train_size=80, validation_size=20):
    """
    Divide las imágenes localizadas en 'source_folder' en conjuntos de entrenamiento,
    validación y test.

    Args:
        source_folder (str): Carpeta con las imágenes a separar.
        train_folder (str): carpeta donde se guardarán las imágenes de entrenamiento
        val_folder (str): carpeta donde se guardarán las imágenes de validación
        test_folder (str): carpeta donde se guardarán las imágenes de test
        train_size (int, optional): número de imágenes para el conjunto de entrenamiento. Defaults to 80.
        validation_size (int, optional): número de imágenes para el conjunto de validación. Defaults to 20.
    """     
    imgs_list = os.listdir(source_folder)
    random.shuffle(imgs_list)

    assert(train_size + validation_size < len(imgs_list))

    for folder in [train_folder, val_folder, test_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Copy train imgs
    top_limit = train_size
    for file in tqdm(imgs_list[:top_limit]):
        source_file_path = os.path.join(source_folder, file)
        destiny_file_path = os.path.join(train_folder, file)
        shutil.copyfile(source_file_path, destiny_file_path)

    # Copy val imgs
    bot_limit = train_size
    top_limit = train_size+validation_size
    for file in tqdm(imgs_list[bot_limit:top_limit]):
        source_file_path = os.path.join(source_folder, file)
        destiny_file_path = os.path.join(val_folder, file)
        shutil.copyfile(source_file_path, destiny_file_path)

    # Copy train imgs
    bot_limit = train_size+validation_size
    for file in tqdm(imgs_list[bot_limit:]):
        source_file_path = os.path.join(source_folder, file)
        destiny_file_path = os.path.join(test_folder, file)
        shutil.copyfile(source_file_path, destiny_file_path)

if __name__ == '__main__':
    source_imgs_folder = os.path.join('data','imgs','google_maps','gm_saguaro_z21_clean')
    train_imgs_folder = os.path.join('data','imgs','google_maps','gm_saguaro_z21_train')
    val_imgs_folder = os.path.join('data','imgs','google_maps','gm_saguaro_z21_val')
    test_imgs_folder = os.path.join('data','imgs','google_maps','gm_saguaro_z21_test')
    
    split_dataset(source_imgs_folder, train_imgs_folder, val_imgs_folder, test_imgs_folder)
