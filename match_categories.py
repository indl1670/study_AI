def num1(json_path, out_path):
    json_list = os.listdir(json_path)
    
    for jl in json_list:
        with open(json_path + jl, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            cat_num = []
            cat_name = []
            for a in data["categories"]:
                for b in data["annotations"]:
                    if b["category_id"] == a["id"]:
                        b["category_id"] = a["name"]
                        
                cat_num.append(a["id"])
                cat_name.append(a["name"])
                
            print("\n[Current categories]")
            for i in range(len(cat_name)):
                print(cat_num[i], ": ", cat_name[i], " | ", end="")
            print("")
                
            in_name = []
            print("Enter the category_name that you want!")
            for i in range(len(cat_name)):
                print(i+1, ": ", end="\t")
                in_name.append(input())
            
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