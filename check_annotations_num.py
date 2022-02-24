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