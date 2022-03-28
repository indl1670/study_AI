import json
import os
coco = dict(
        info=dict(
            year=None,
            version=None,
            description=None,
            contributor=None,
            url=None,
            date_created=None
        ),
        licenses=[dict(url=None, id=1, name=None,)],
        categories=[
            {
                "id": 5,
                "name": "braille",
                "subcategory": ""
            },
            {
                "id": 6,
                "name": "side_block",
                "subcategory": ""
            },
            {
                "id": 7,
                "name": "slight_slope",
                "subcategory": ""
            }
        ],
        images=[
            # license, url, file_name, height, width, date_captured, id
        ],
        annotations=[]
    )
json_path = input("json path")
img_path = input("image_path")
img_list = os.listdir(img_path)
images = []
annotations = []
for jl in img_list:
    images.append(jl)

images = list(set(images))   
print(len(images))               
for i in range(len(images)):
    coco["images"].append(
            dict(
                license=0,
                url=None,
                file_name=images[i],
                height=1080,
                width=1920,
                date_captured=None,
                id=i+1
            )
        )
json_list = os.listdir(json_path)
for jl in json_list:
    with open(json_path + jl, "r", encoding="utf8") as f:
        data = json.load(f)
        for a in data["annotations"]:
            annotations.append(a)
coco["annotations"] = annotations 

ann_id_index = 1
for e in coco["annotations"]:
    e["id"] = ann_id_index
    ann_id_index = ann_id_index + 1        
print("coco annotations part complete.")              

for a in coco["images"]:
    for b in coco["annotations"]:
        if a["file_name"] == b["image_id"]:
            b["image_id"] = a["id"]
                
print(len(coco["images"]))
print(len(coco["annotations"]))
with open(json_path + "result.json", 'w+', encoding='utf8') as make_file:
    json.dump(coco, make_file, ensure_ascii=False, indent="\t")