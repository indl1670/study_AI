# polygon
import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt

# Root directory 경로 저장
ROOT_DIR = os.path.abspath("/content/drive/MyDrive/kst_project/oneCycle/Mask_RCNN2/")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils

# MS-COCO 기반으로 Pretrained 된 모델을 로딩
import mrcnn.model as modellib
from mrcnn import visualize

# Import COCO config
sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))  # To find local version
import coco

%matplotlib inline 

# MRCNN 모델 경로 저장
MODEL_DIR = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

# 자체 데이터셋 trained weight file 경로 저장
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "logs/mask_rcnn_kst_case2_0006.h5")

# 이미지 경로 저장
IMG_DIR = os.path.abspath("/content/drive/Shareddrives/KST_Project/final_img/")

# 테스트 이미지폴더 경로 저장
IMAGE_DIR = os.path.join(IMG_DIR, "dataset/test2021/")

class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

# config 세부사항 출력
config = InferenceConfig()
config.display()

# inference 모드에서 모델 객체 생성
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

# MS-COCO에서 trained weights 로드
model.load_weights(
    COCO_MODEL_PATH, by_name=True)

# test2021(이미지 폴더)에서 무작위 이미지 선정
file_names = next(os.walk(IMAGE_DIR))[2]
image = skimage.io.imread(os.path.join(IMAGE_DIR, random.choice(file_names)))

# class명 저장(0: 'border_stone', 1: 'side_sphere', 2: 'Manhole', 3: 'center_separato', 4: 'PE_barrier', 5: 'temporary_safety_barrier')
class_names = ['BG', 'border_stone', 'side_sphere', 'Manhole', 'center_separato', 'PE_barrier', 'temporary_safety_barrier']

# Detection
results = model.detect([image], verbose=1)

# 발견된 객체 개수 확인
print(results[0]['class_ids'].shape) 

# Visualize 결과
r = results[0]
visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])