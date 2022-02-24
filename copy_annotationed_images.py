def num5(json_path, img_path, out_path):
    json_list = os.listdir(json_path)
    trn_img = []

    for jl in json_list:
        img_name = []
        with open(json_path + jl, 'r', encoding='UTF-8') as f:
            data = json.load(f)
            
            
            # 라벨링이 있는 이미지 파일 명 저장
            for a in data['images']:
                for b in data['annotations']:
                    if a['id'] == b['image_id']:
                        img_name.append(a['file_name'])
            img_name = set(img_name)
            
        trn_img.extend(img_name)
     
    print("Labelled images number: ", len(trn_img))


    img_list = os.listdir(img_path)

    for i in range(len(trn_img)):
        if trn_img[i] in img_list:
            src = img_path + trn_img[i]
            shutil.copy2(src, out_path)
    print("Done!")