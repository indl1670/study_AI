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
            # 선택된 카테고리 id값 저장 - category_id
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
