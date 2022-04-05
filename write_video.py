import cv2
import numpy as np
import glob
import os 

img_array = []
file_path = input("image path: ")
file_list = os.listdir(file_path)

# 현재 경로에 vlog.avi 생성
for fl in file_list:
    img = cv2.imread(file_path + fl)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
 
 
out = cv2.VideoWriter('vlog.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()