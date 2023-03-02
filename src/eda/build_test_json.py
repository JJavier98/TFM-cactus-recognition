import json
import os
from tqdm import tqdm

TEST_DICT_GOOGLE = {
    "info": {
        "year":2022,
        "version":"0.1.0",
        "description":"Detect and count the number of cacti at National Park of Saguaro",
        "url":"",
        "date_created":1671539383183
    },
    "categories": [
        {
            "id": 1,
            "datatorch_id": "fcec8862-d1e6-46a1-9c39-0ba30cf7810e",
            "name": "Cactus",
            "supercategory": None
        },
        {
            "id": 2,
            "datatorch_id": "25dd88b3-6c0b-4cbd-97a8-841ac1722b93",
            "name": "cactus 1 brazo",
            "supercategory": "fcec8862-d1e6-46a1-9c39-0ba30cf7810e"
        },
        {
            "id": 3,
            "datatorch_id": "149b9edb-c4e9-4b14-a606-35194608b0f9",
            "name": "Cactus 2 brazos",
            "supercategory": "fcec8862-d1e6-46a1-9c39-0ba30cf7810e"
        },
        {
            "id": 4,
            "datatorch_id": "dcbdcaee-d1b5-4bfa-80ad-20c058669e04",
            "name": "cactus 3+ brazos",
            "supercategory": "fcec8862-d1e6-46a1-9c39-0ba30cf7810e"
        }
    ],
    "images": []
}

TEST_DICT_BING = {
    "info": {
        "year":2022,
        "version":"0.1.0",
        "description":"Detect and count the number of cacti at National Park of Saguaro",
        "url":"",
        "date_created":1671539383183
    },
    "categories": [
        {
            "id": 1,
            "datatorch_id": "1ea2d20e-36e7-4b7f-96b7-abc5e5402530",
            "name": "cactus 3+ brazos",
            "supercategory": "d3267cd8-cd89-4ad9-959c-44bd1f15104a"
        },
        {
            "id": 2,
            "datatorch_id": "51890e00-25e7-4c0c-903a-920fa209efd7",
            "name": "cactus 2 brazos",
            "supercategory": "d3267cd8-cd89-4ad9-959c-44bd1f15104a"
        },
        {
            "id": 3,
            "datatorch_id": "ef651b08-5816-4840-9024-9403204fccd7",
            "name": "cactus 1 brazo",
            "supercategory": "d3267cd8-cd89-4ad9-959c-44bd1f15104a"
        },
        {
            "id": 4,
            "datatorch_id": "d3267cd8-cd89-4ad9-959c-44bd1f15104a",
            "name": "Cactus",
            "supercategory": None
        }
    ],
    "images": []
}

TEST_FOLDER_GOOGLE = os.path.join('data','imgs','google_maps','gm_saguaro_z21_clean')
TEST_FOLDER_BING = os.path.join('data','imgs','bing_maps','bing_saguaro_z21_clean')

OUT_FILE_GOOGLE = os.path.join('data','coco_annotations','google_saguaro','test.json')
OUT_FILE_BING = os.path.join('data','coco_annotations','bing_saguaro','test.json')

TEST_DICT = TEST_DICT_GOOGLE
TEST_FOLDER = TEST_FOLDER_GOOGLE
OUT_FILE = OUT_FILE_GOOGLE


def main():
    imgs_list = os.listdir(TEST_FOLDER)

    for i, img_name in enumerate(tqdm(imgs_list)):
        new_dict = {
            "id": i+1,
            "path": img_name,
            "width": 255,
            "height": 255,
            "file_name": img_name,
            "metadata": {},
            "date_captured": "2022-12-20T11:44:47.142Z"
        }

        TEST_DICT['images'].append(new_dict)

    with open(OUT_FILE, 'w',encoding='utf-8') as outfile:
        json.dump(TEST_DICT, outfile)

if __name__=="__main__":
    main()
