import json
import os

json_path = input("json path: ")
json_list = os.listdir(json_path)
json_list = [file for file in json_list if file.endswith(".json")]
out_path = input("save path: ")

for jl in json_list:
    with open(json_path + jl, "r", encoding="utf8") as f:
        data = json.load(f)
        
        for a in data["annotations"]:
            filename = str(a["image_id"])
            filename = filename.rstrip('.jpg')
            filename = filename + ".txt"
            
            bbox_str = a["bbox"]
            bbox_str[2] = float(bbox_str[2]) / 1920 # w
            bbox_str[3] = float(bbox_str[3]) / 1080 # h
            bbox_str[0] = float(bbox_str[0]) / 1920 + (bbox_str[2] / 2) # x
            bbox_str[1] = float(bbox_str[1]) / 1080 + (bbox_str[3] / 2) # y

            bbox_str = str(bbox_str)
            bbox_str = bbox_str.replace("[", "")
            bbox_str = bbox_str.replace("]", "")
            
            print(bbox_str)
            
            f = open(out_path + filename, 'a')
            data = str(a['category_id']-1) + ' ,' + bbox_str + '\n'
            data = data.replace(',', "")
            f.write(data)