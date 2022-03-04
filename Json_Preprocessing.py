import os
import json
import shutil
from collections import OrderedDict

def num1(json_path, out_path):
    json_list = os.listdir(json_path)
    cat_num = []
    while True:
        cat_id = int(input("Enter the category_ids in order(-1 to quit): "))
        if cat_id == -1:
            break
        else:
            cat_num.append(cat_id)
    in_name = []
    print("Enter the category_name that you want!")
    for i in range(len(cat_num)):
        print(i+1, ": ", end="\t")
        in_name.append(input())
        
    for jl in json_list:
        with open(json_path + jl, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            for i in range(len(in_name)):
                for c in data["categories"]:
                    if c["id"] == i+1:
                        if c["name"] != in_name[i]:
                            c["name"] = in_name[i]
                            
            for d in data['categories']:
                for e in data['annotations']:
                    if e['category_id'] == d['name']:
                        e['category_id'] = d['id']
            
        with open(out_path + jl, 'w', encoding='utf-8') as make_file:
                json.dump(data, make_file, indent="\t", ensure_ascii=False)
    print("Done!")

def num2(json_path, out_path):
    json_list = os.listdir(json_path)
    
    for jl in json_list:
        with open(json_path + jl, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            cat_num = []
            cat_name = []
            for a in data["categories"]:                        
                cat_num.append(a["id"])
                cat_name.append(a["name"])
                
            print("\n[Current categories]")
            for i in range(len(cat_name)):
                print(cat_num[i], ": ", cat_name[i], " | ", end="")
            print("")
            
            del_cat = []
            while True:
                in_num = int(input("Select the category_id that you want to delete(-1 to quit): "))
                if in_num == -1:
                    break
                elif in_num not in cat_num:
                    print("You entered wrong number.\n")
                else:
                    del_cat.append(in_num)
            del_cat.reverse()
            
            del_ann = []
            for b in data["annotations"]:
                for i in range(len(del_cat)):
                    if b["category_id"] == del_cat[i]:
                        del_ann.append(b["id"]-1)
            del_ann.reverse()
            for c in data["annotations"]:
                if c["category_id"] in del_cat:
                    for d in del_ann:
                        del data["annotations"][d]
                    for f in del_cat:
                        del data["categories"][f-1]
                del_ann = []
                del_cat = []
                
        with open(out_path + jl, 'w', encoding='utf-8') as make_file:
            json.dump(data, make_file, indent="\t", ensure_ascii=False)
    print("Done!")     
        
def num3_1(json_path, out_path):
    print("Preprocessing start . . .")
    json_list = os.listdir(json_path)
    for jl in json_list:
        with open(json_path + jl, 'r', encoding='utf8') as f:
            data = json.load(f)

            for a in data["images"]:
                for b in data["annotations"]:
                    if b["image_id"] == a["id"]:
                        b["image_id"] = a["file_name"]
                            
        with open(json_path + jl, 'w+', encoding='utf8') as make_file:
            json.dump(data, make_file, ensure_ascii=False, indent="\t")
    print("Done!")
    num3_2(json_path, out_path)
    
def num3_2(json_path, out_path):
    print("Integrating start . . .")
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
            "name": "경계석",
            "subcategory": ""
        },
        {
            "id": 2,
            "name": "측구",
            "subcategory": ""
        },
        {
            "id": 3,
            "name": "맨홀",
            "subcategory": ""
        },
        {
            "id": 4,
            "name": "임시 안전방호벽",
            "subcategory": ""
        },
        {
            "id": 5,
            "name": "점자 블럭",
            "subcategory": ""
        },
        {
            "id": 6,
            "name": "보도블럭 파손",
            "subcategory": ""
        },
        {
            "id": 7,
            "name": "간이 부분 경사로",
            "subcategory": ""
        },
        {
            "id": 8,
            "name": "도로 홀",
            "subcategory": ""
        },
        {
            "id": 9,
            "name": "도로 균열",
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
        
        print(jl)
        with open(json_path + jl, 'r', encoding='utf8') as f:
            data = json.load(f)
                        
            for c in data['images']:
                img_list.append(c)        
                
            for d in data['annotations']:
                ann_list.append(d)

    print("coco categories part complete.")
    images=img_list
    annotations=ann_list
    
    image_index = 1
    ann_id_index = 1
    
    coco_group["images"] = images
    for g in coco_group["images"]:
        g["id"] = image_index
        image_index = image_index + 1
    print("coco images part complete.")

    coco_group["annotations"] = annotations 
    for e in coco_group["annotations"]:
        e["id"] = ann_id_index
        ann_id_index = ann_id_index + 1        
    print("coco annotations part complete.")              

    for a in coco_group["images"]:
        for b in coco_group["annotations"]:
            if a["file_name"] == b["image_id"]:
                b["image_id"] = a["id"]
                
    with open(out_path + "result.json", 'w+', encoding='utf8') as make_file:
            json.dump(coco_group, make_file, ensure_ascii=False, indent="\t")
    print("Done!")
    
def num4(json_path, out_path):
    coco_group = OrderedDict()
    info = OrderedDict()
    licenses = OrderedDict()
    categories = OrderedDict()
    images = OrderedDict()
    annotations = OrderedDict()

    info["year"] = ""
    info["version"] = ""
    info["description"] = ""
    info["contributor"] = ""
    info["url"] = ""
    info["date_created"] = ""

    licenses["id"] = 1
    licenses["url"] = ""
    licenses["name"] = ""

    images = "{}"
    categories = "{}"
    annotations = "{}"

    coco_group["info"] = info
    coco_group["licenses"] = [licenses]
    coco_group["categories"] = [categories]
    coco_group["images"] = [images]
    coco_group["annotations"] = [annotations]
    
    json_list = os.listdir(json_path)
    
    rem_num = int(input("\nSelect category's id: "))

    for jl in json_list:
        image_list = []
        annot_list = []
        category_id = []
        print("Information Part complete.") 

        image_id = []
        with open(json_path + jl, 'r', encoding='utf8') as f:
            data = json.load(f)
            for a in data['categories']:
                if a['id'] == rem_num:
                    print("Selected category_name:  ", a['name'])
            
            categories = data['categories'][rem_num - 1]
            coco_group["categories"] = categories
            print("Category part complete.")
            
            for b in data['annotations']:
                if b['category_id'] == rem_num:
                    image_id.append(b['image_id'])
            image_id = sorted(list(set(image_id)))
            
            for e in image_id:
                image_list.append(data['images'][e-1])
                
            images = image_list
            coco_group["images"] = images
            print("Images Part complete.")
            
            for f in data['annotations']:
                if f['category_id'] == rem_num:
                    category_id.append(f['id'])
            for g in category_id:
                annot_list.append(data['annotations'][g-1])
            
            annotations = annot_list
            coco_group["annotations"] = annotations
            print("Annotations Part complete.")
            
        if coco_group["images"] == [] or coco_group["annotations"] == []:
            print("", end='')
        else:
            with open(out_path + jl, 'w+', encoding='utf8') as make_file:
                json.dump(coco_group, make_file, ensure_ascii=False, indent="\t")
    print("Done!")

def num5(json_path, img_path, out_path):
    json_list = os.listdir(json_path)
    img_list = os.listdir(img_path)
    img_list = os.listdir(img_path)
    all_img = []
    use_img = []

    for jl in json_list:
        with open(json_path + jl, encoding="utf8") as f:
            data = json.load(f)
            
            for a in data["images"]:
                all_img.append(a["file_name"])
            
    use_img = list(set(all_img) & set(img_list))
    print("Total labelled images number: ", len(use_img))

    file_list = os.listdir(img_path)

    for i in range(len(use_img)):
        if use_img[i] in file_list:
            src = img_path + use_img[i]
            shutil.copy2(src, out_path)
    print("Done!")
    
def num6(json_path):
    json_list = os.listdir(json_path)

    ann_len = []
    tot_len = 0
    for jl in json_list:
        with open(json_path + jl, 'r', encoding='utf8') as f:
            data = json.load(f)

            ann_len.append(len(data['annotations']))
                
    for an in range(len(ann_len)):
        tot_len = tot_len + ann_len[an] 
    print("The number of labels: ", tot_len)
    print("Done!")
    
def num7(json_path, out_path):
    json_list = os.listdir(json_path)
    for jl in json_list:
        with open(json_path + jl, "r", encoding="utf8") as f:
            data = json.load(f)

            for a in data["annotations"]:
                if a["segmentation"] == []:
                    x1 = a["bbox"][0]
                    y1 = a["bbox"][1]
                    x2 = a["bbox"][2]
                    y2 = a["bbox"][3]
                    a["segmentation"] = [[x1,y1,x1,(y1 + y2), (x1 + x2), (y1 + y2), (x1 + x2), y1]]
                    
                elif a["bbox"] == []:
                    a["bbox"] = a["segmentation"][0]
                    x1 = a["segmentation"][0][0]
                    y1 = a["segmentation"][0][1]
                    x2 = a["segmentation"][0][2]
                    y2 = a["segmentation"][0][3]
                    a["segmentation"] = [[x1,y1,x1,(y1 + y2), (x1 + x2), (y1 + y2), (x1 + x2), y1]]
                    
        with open(out_path + jl, 'w+', encoding='utf8') as make_file:
                json.dump(data, make_file, ensure_ascii=False, indent="\t")
        print(jl, "completed")
        
    print("Done!")
    
def main():
    print("[2022 KST Json Preprocessing]")
    while True:
        sel_num = int(input("""\n--------------Select number--------------\n1. Match categories\n2. Delete all information in that category\n3. Json Integration\n4. Split object\n5. Split images\n6. Check the number of labels\n(-1 to quit)\n\n Input: """))
        if sel_num == -1:
            print("Thank you for using!")
            break
        elif sel_num == 1:
            json_path = input("\nJson path: ")
            out_path = input("Out json path: ")
            num1(json_path, out_path)
        elif sel_num == 2:
            json_path = input("\nJson path: ")
            out_path = input("Out json path: ")
            num2(json_path, out_path)
        elif sel_num == 3:
            json_path = input("\nJson path: ")
            out_path = input("Out json path: ")
            num3_1(json_path, out_path)
        elif sel_num == 4:
            json_path = input("\nJson path: ")
            out_path = input("Out json path: ")
            num4(json_path, out_path)
        elif sel_num == 5:
            json_path = input("\nJson path: ")
            img_path = input("All images path: ")
            out_path = input("Out images path: ")
            num5(json_path, img_path, out_path)
        elif sel_num == 6:
            json_path = input("\nJson path: ")
            num6(json_path)
        elif sel_num == 7:
            json_path = input("\nJson path: ")
            out_path = input("Out json path: ")
            num7(json_path, out_path)
        else:
            print("\nInvalid input! Select correct number.")
                
if __name__ == "__main__":
    main()
