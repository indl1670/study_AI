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