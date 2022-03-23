import cv2
import numpy as np
import glob
 
img_array = []
for filename in glob.glob('/home/centos/KST/AI_RoadMap/video_result/*.png'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
 
 
out = cv2.VideoWriter('plate_night.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()