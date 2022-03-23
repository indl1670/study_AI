import os
import json
from collections import OrderedDict
json_path = input("json path: ")
out_path = input("out path: ")
image_path = input("image path: ")
image_list = os.listdir(image_path)

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
        "id": object_id,
        "name": "object_name",
        "subcategory": ""
    }
]

images = "{}"
annotations = "{}"

coco_group["info"] = info
coco_group["licenses"] = [licenses]
coco_group["categories"] = categories
coco_group["images"] = [images]
coco_group["annotations"] = [annotations]

json_list = os.listdir(json_path)
img_list = []
ann_list = []

for jl in json_list:
    with open(json_path + "1.json", 'r', encoding='utf8') as f:
        data = json.load(f)
        
        for a in data["images"]:
            for b in image_list:
                if a["file_name"] == b:
                    print("find")
                    img_list.append(a)
                    for c in data["annotations"]:
                        if a["id"] == c["image_id"]:
                            ann_list.append(c)
                
images=list({img_list['id']: img_list for img_list in img_list}.values())
annotations=ann_list

coco_group["images"] = images
coco_group["annotations"] = annotations 

with open(out_path + "result.json", 'w+', encoding='utf8') as make_file:
        json.dump(coco_group, make_file, ensure_ascii=False, indent="\t")

