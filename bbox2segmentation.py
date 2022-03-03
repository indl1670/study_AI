import json
import os

json_path = input("json path: ")
json_list = os.listdir(json_path)
out_path = input("out path: ")

for jl in json_list:
    with open(json_path + jl, "r", encoding="utf8") as f:
        data = json.load(f)
        
        for a in data["annotations"]:
            if a["category_id"] == 2:
                a["bbox"] = a["segmentation"][0]

                x1 = a["segmentation"][0][0]
                y1 = a["segmentation"][0][1]
                x2 = a["segmentation"][0][2]
                y2 = a["segmentation"][0][3]
                
                a["segmentation"] = [[x1,y1,x1,(y1 + y2), (x1 + x2), (y1 + y2), (x1 + x2), y1]]

    with open(out_path + jl, 'w+', encoding='utf8') as make_file:
            json.dump(data, make_file, ensure_ascii=False, indent="\t")
    print(jl, "completed")