# Test
from detectron2.engine import DefaultPredictor
import os
import pickle
from utils import *
cfg_save_path = "OD_cfg.pickle"

with open(cfg_save_path, 'rb') as f:
    cfg = pickle.load(f)
    
cfg.MODEL.WEIGHTS = os.path.join("./dataset/output/", "model_final.pth")
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5

predictor = DefaultPredictor(cfg)

test_dataset_name = "test_"
test_images_path = "/home/centos/KST/AI_RoadMap/dataset/test/"
test_json_annot_path = "/home/centos/KST/AI_RoadMap/dataset/test.json"

image_list = os.listdir(test_images_path)
image_path = test_images_path + image_list[100]
result = on_image(image_path, predictor)