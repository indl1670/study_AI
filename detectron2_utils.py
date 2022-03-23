from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.utils.visualizer import Visualizer
from detectron2.config import get_cfg
from detectron2 import model_zoo

from detectron2.utils.visualizer import ColorMode

import random
import cv2
import matplotlib.pyplot as plt

def plot_samples(dataset_name, n=1):
    dataset_custom = DatasetCatalog.get(dataset_name)
    dataset_custom_metadata = MetadataCatalog.get(dataset_name)
    
    for s in random.sample(dataset_custom, n):
        img = cv2.imread(s["file_name"])
        v = Visualizer(img[:,:,::-1], metadata=dataset_custom_metadata, scale=0.5)
        v = v.draw_dataset_dict(s)
        plt.figure(figsize=(15, 20))
        plt.imshow(v.get_image())
        plt.show()
        
def get_train_cfg(config_file_path, checkpoint_url, train_dataset_name, test_dataset_name, num_classes, device, output_dir):
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file(config_file_path))
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(checkpoint_url)
    cfg.DATASETS.TRAIN = (train_dataset_name,)
    cfg.DATASETS.TEST = (test_dataset_name,)
    
    cfg.DATALOADER.NUM_WORKERS = 2
    cfg.SOLVER.IMS_PER_BATCH = 16
    cfg.SOLVER.BASE_LR = 0.02
    cfg.SOLVER.MAX_ITER = 5000
    cfg.SOLVER.STEPS = []
    
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = num_classes
    cfg.MODEL.DEVICE = device
    cfg.OUTPUT_DIR = output_dir
    
    return cfg
def on_image(image_path, predictor):
    im = cv2.imread("./Frame/frame0.png")
    outputs = predictor(im)
    v = Visualizer(im[:,:,::-1], metadata={}, scale=0.5, instance_mode=ColorMode.IMAGE_BW)
    v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    
    plt.figure(figsize=(14,10))
    plt.imshow(v.get_image())
    plt.show()
    #return (v.get_image())
    
def on_video(videoPath, predictor):
    cap = cv2.VideoCapture(videoPath)
    if (cap.isOpened()==False):
        print("Error opening files . . .")
        return
    
    (success, image) = cap.read()
    while success:
        predictions = predictor(image)
        v = Visualizer(image[:,:,::-1], metadata={}, scale=0.5, instance_mode=ColorMode.IMAGE_BW)
        output = v.draw_instance_predictions(predictions["instances"].to("cpu"))
        
        cv2.imshow("Result", output.get_image()[:,:,::-1])
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        (success, image) = cap.read()
def cap_video(videoPath):
    vidcap = cv2.VideoCapture(videoPath)
    count = 0
    while(vidcap.isOpened()):
        ret, image = vidcap.read()
        image = cv2.resize(image, (1920, 1080))
        # 30프레임당 하나씩 이미지 추출
        if(int(vidcap.get(1)) % 1 == 0):
            print('Saved frame number : ' + str(int(vidcap.get(1))))
            # 추출된 이미지가 저장되는 경로
            cv2.imwrite("/home/centos/KST/AI_RoadMap/Frame/plate%d.png" % count, image)
            #print('Saved frame%d.jpg' % count)
            count += 1
    vidcap.release()