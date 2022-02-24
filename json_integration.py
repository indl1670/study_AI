def num3_1(json_path, out_path):
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
    num3_2(json_path, out_path)
    
    for jl in json_list:
        with open(json_path + jl, 'r', encoding='utf8') as f:
            data = json.load(f)

            for a in data["images"]:
                for b in data["annotations"]:
                    if b["image_id"] == a["file_name"]:
                        b["image_id"] = a["id"]
                            
        with open(json_path + jl, 'w+', encoding='utf8') as make_file:
            json.dump(data, make_file, ensure_ascii=False, indent="\t")
    
    
def num3_2(json_path, out_path):
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

    images = "{}"
    annotations = "{}"
    categories = "{}"
    
    coco_group["info"] = info
    coco_group["licenses"] = [licenses]
    coco_group["categories"] = [categories]
    coco_group["images"] = [images]
    coco_group["annotations"] = [annotations]

    json_list = os.listdir(json_path)
    img_list = []
    ann_list = []
    cat_list = []
    cat_result = []
    image_index = 1

    for jl in json_list:
        ann_id_index = 1
        print(jl)
        with open(json_path + jl, 'r', encoding='utf8') as f:
            data = json.load(f)
            
            for cl in data["categories"]:
                cat_list.append(cl)
                
            for a in data["images"]:
                a["id"] = image_index
                image_index = image_index + 1
            
            for b in data["images"]:
                for c in data["annotations"]:
                    if b["file_name"] == c["image_id"]:
                        c["image_id"] = b["id"]
                        
            for c in data['images']:
                img_list.append(c)        
                
            for d in data['annotations']:
                ann_list.append(d)
    
    cat_result = list(map(dict, collections.OrderedDict.fromkeys(tuple(sorted(d.items())) for d in cat_list)))
    categories=sorted(cat_result, key=lambda k: k['id'])
    images=img_list
    annotations=ann_list

    coco_group["categories"] = categories
    print("coco categories part complete.")
    
    coco_group["images"] = images
    print("coco images part complete.")

    coco_group["annotations"] = annotations 
    for e in coco_group["annotations"]:
        e["id"] = ann_id_index
        ann_id_index = ann_id_index + 1
        
    print("coco annotations part complete.")              

    with open(out_path + "result.json", 'w+', encoding='utf8') as make_file:
            json.dump(coco_group, make_file, ensure_ascii=False, indent="\t")