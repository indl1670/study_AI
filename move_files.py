import shutil
import os

file_s = "start_file_path"
file_d = "destination_file_path"

get_files = os.listdir(file_s)
print(get_files)

for g in get_files:
    img_list = os.listdir(file_s + g)
    for i in img_list:
        shutil.move(file_s + g + "//" + i, file_d)

a = os.listdir(file_d)
print(len(a))
