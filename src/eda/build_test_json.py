import json
import os
from tqdm import tqdm

test_dict = {
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

test_folder = os.path.join('data','imgs','google_maps','gm_saguaro_z21_test')
imgs_list = os.listdir(test_folder)

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

    test_dict['images'].append(new_dict)

json_file = os.path.join('data','coco_annotations','saguaro','test.json')
with open(json_file, 'w') as outfile:
    json.dump(test_dict, outfile)
