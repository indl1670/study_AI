import shutil

#Phase 1
img_path = "./person_dataset/eval2/images"
img_list = os.listdir(img_path)
img_list = [file for file in img_list if file.endswith(".jpg")]

for il in img_list:
    os.makedirs("./person_dataset/eval1/images/" + il.rstrip(".jpg"))

# Phase2
img_path = "./person_dataset/eval2/images/"
img_list = os.listdir(img_path)
img_list = [file for file in img_list if file.endswith(".jpg")]
folder_path = "./person_dataset/eval1/images/"
folder_list = os.listdir(folder_path)

for fl in folder_list:
    for il in img_list:
        if fl == il.rstrip(".jpg"):
            print(il)
            shutil.copy2(img_path + il, folder_path + fl)