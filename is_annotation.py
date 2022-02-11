import os
import shutil
import json

def jyun():
    # json 파일 경로 지정
    path = "json_path"

    # json 파일 경로 리스트에 저장
    file_list = os.listdir(path)
    file_list_json = [file for file in file_list if file.endswith(".json")]

    trn_img = []

    # json 파일 전체 탐색
    for i in range(len(file_list_json)):
        img_name = []

        # json 파일 로드
        file_path =  path + "//" + file_list_json[i]
        with open(file_path, 'r', encoding='UTF-8') as f:
            data = json.load(f)
            
            
            # 라벨링이 있는 이미지 파일 명 저장
            for e in data['images']:
                for f in data['annotations']:
                    if e['id'] == f['image_id']:
                        img_name.append(e['file_name'])
            img_name = set(img_name)
            
        trn_img.extend(img_name)
    
    # 해당 이미지 분리: 총 _개   
    print("라벨링 있는 이미지 개수: ", len(trn_img))
    useImg(trn_img)

def useImg(trn_img):
    path = "use_img_path"
    file_list = os.listdir(path)
    
    cnt = 0
    for i in range(len(trn_img)):
        if trn_img[i] in file_list:
            src = path + trn_img[i]
            dst = "result_img_path"
            shutil.move(src, dst)
            
def main():
    jyun()


if __name__ == '__main__':
    main()