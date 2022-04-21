import os
import json
from collections import OrderedDict

coco_group = OrderedDict()
info = OrderedDict()
licenses = OrderedDict()
categories = OrderedDict()
images = OrderedDict()
annotations = OrderedDict()

info["year"] = None
info["version"] = None
info["description"] = None
info["contributor"] = None
info["url"] = None
info["date_created"] = None

licenses["id"] = 1
licenses["url"] = None
licenses["name"] = None
categories=[
    {
        "id": 1,
        "name": "plate_c",
        "supercategory": ""
    },
    {
        "id": 2,
        "name": "plate_e",
        "supercategory": ""
    },
    {
        "id": 3,
        "name": "plate_b",
        "supercategory": ""
    },
    {
        "id": 4,
        "name": "plate_o",
        "supercategory": ""
    },
    {
        "id": 5,
        "name": "plate_n",
        "supercategory": ""
    },
    {
        "id": 6,
        "name": "no_mask",
        "supercategory": ""
    },
    {
        "id": 7,
        "name": "mask",
        "supercategory": ""
    }
    ]

images = "{}"
annotations = "{}"

coco_group["info"] = info
coco_group["licenses"] = [licenses]
coco_group["categories"] = categories
coco_group["images"] = [images]
coco_group["annotations"] = [annotations]

json_path = "./person_dataset/"
out_path = "./person_dataset/annotations/"
json_list = os.listdir(json_path)
json_list = [file for file in json_list if file.endswith(".json")]

img_list = []
images_list = []
ann_list = []
annotations_list = []


with open(json_path + "result.json", 'r', encoding='utf8') as f:
    data = json.load(f)

    for a in data["images"]:
        coco_group["images"] = [images]
        coco_group["annotations"] = [annotations]
        for b in data["annotations"]:
            if a["id"] == b["image_id"]:
                print(a["file_name"])
                coco_group["images"] = [a]
                coco_group["annotations"].append(b)

                with open(out_path + "/" + a["file_name"].rstrip('.jpg') + ".json", 'w+', encoding='utf8') as make_file:
                    json.dump(coco_group, make_file, ensure_ascii=False, indent="\t")       