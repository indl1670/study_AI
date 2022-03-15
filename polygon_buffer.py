import os
import json
import datetime


import numpy as np

from matplotlib import pyplot
from shapely.geometry import Polygon
from descartes import PolygonPatch
from functools import reduce


from math import sqrt
# from shapely.figures import BLUE

import pycocotools.mask as _mask
frPyObjects = _mask.frPyObjects

GM = (sqrt(5)-1.0)/2.0
W = 8.0
H = W*GM


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

class line2segment:
    def __init__(self):
        self.path = input('json path: ')
        self.output = input('save path: ')
        self.buf_value = round(float(input("Enter buffer size: ")), 1)
        self.item_dict = dict(
            item =[]
        )
        self.polyline = dict(
            info=dict(
                description=None,
                url=None,
                version=None,
                year=datetime.datetime.now().year,
                contributor=None,
                date_created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            ),
            licenses=[dict(url=None, id=1, name=None, )],
            images=[
                # license, url, file_name, height, width, date_captured, id
            ],
            type="instances",
            annotations=[
                # segmentation, area, iscrowd, image_id, bbox, category_id, id
            ],
            categories=[
                # supercategory, id, name
                {
                    "id": 1,
                    "name": "mask",
                    "supercategory": ""
                },
                {
                    "id": 2,
                    "name": "no_mask",
                    "supercategory": ""
                },
                {
                    "id": 3,
                    "name": "n_plate",
                    "supercategory": ""
                },
                {
                    "id": 4,
                    "name": "o_plate",
                    "supercategory": ""
                },
                {
                    "id": 5,
                    "name": "b_plate",
                    "supercategory": ""
                },
                {
                    "id": 6,
                    "name": "e_plate",
                    "supercategory": ""
                },
                {
                    "id": 7,
                    "name": "c_plate",
                    "supercategory": ""
                }
            ],
        )

        self.polygon_obj =[]
        self.getJson_f(self.path)
        self.writeDict()
        self.writeJson()

    #경로 안 json 파일 읽기
    def getJson_f(self, path):
        file_list = [os.path.join(path, i) for i in os.listdir(path)]
        for file_ in file_list:
            if os.path.isdir(file_):
                self.getJson_f(file_)
            elif '.json' in file_:
                print(file_)
                self.readJson(file_)


    def readJson(self, j_file):
        area =_mask.area
        with open(j_file, 'r', encoding='UTF8') as f:
            json_data = json.load(f)
        items = [i for i in json_data['annotations']]
        file_name =json_data['images'][0]['file_name']
        cat_id = json_data['annotations'][0]['category_id']
        for i in items:
            point = self.getPolygon(i['segmentation'][0], self.buf_value)
            if type(point) == list:
                for multi in point:
                    coord = list(reduce(lambda x, y: x + y, multi))
                    rs = frPyObjects(np.array([coord]), 1080, 1920)
                    self.item_dict['item'].append(
                        dict(
                            id =file_name,
                            segment = coord,
                            bbox = self.getBbox(coord),
                            area = area(rs),
                            category_id = cat_id
                        )
                    )
            else:
                coord = list(reduce(lambda x, y: x + y, list(point.exterior.coords)))
                rs = frPyObjects(np.array([coord]), 1080, 1920)
                self.item_dict['item'].append(
                    dict(
                        id =file_name,
                        segment = coord,
                        bbox = self.getBbox(coord),
                        area = float(area(rs)),
                        category_id = cat_id
                    )
                )

    def getPolygon(self, coordinates, buf_value):
        #polyline 좌표값 (x,y)로 변환
        coor = []
        length = [i*2 for i in range(len(coordinates)//2)]
        for i in length:
            coor.append((coordinates[i],coordinates[i+1]))
        line = Polygon(coor)
        dilated = line.buffer(buf_value, cap_style=2)
        if dilated.type == 'MultiPolygon':
            self.polygon_obj = [x.exterior.coords for x in dilated.geoms]
        else:
            self.polygon_obj = dilated
        return self.polygon_obj


    #bbox 값
    def getBbox(self, list_):
        x = [i for i in list_ if list_.index(i) % 2 == 0]
        y = [i for i in list_ if list_.index(i) % 2 == 1]
        return [min(x), min(y), max(x) - min(x), max(y) - min(y)]

    def writeDict(self):
        img_dict ={}
        img = [i['id'] for i in self.item_dict['item']]
        img = list(set(img))
        #coco data images write
        for i in img:
            img_dict[i] = img.index(i)+1
            self.polyline['images'].append(
                dict(
                    license=0,
                    url=None,
                    # file_name=i+'.jpg',
                    file_name=i,
                    height=1080,
                    width=1920,
                    date_captured=None,
                    id=len(self.polyline['images']) + 1
                    # id=img.index(i)+1
                )
            )
        #coco data annotations write
        for i in self.item_dict['item']:
            print(i)
            self.polyline["annotations"].append(
                dict(
                    id=len(self.polyline["annotations"]) + 1,
                    image_id=img_dict[i['id']],
                    category_id= i['category_id'],
                    segmentation=[i['segment']],
                    area=i['area'],
                    bbox=i['bbox'],
                    iscrowd=0,
                )
            )
    #수정완료 json파일 write
    def writeJson(self):
        # file_name = 'self.output\\annotations.json'
        file_name = os.path.join(self.output, 'result.json')
        print('write file: ' + file_name)
        with open(file_name, "w", encoding='UTF8') as f:
            json.dump(self.polyline, f, ensure_ascii=False, indent="\t", cls=NumpyEncoder)



if __name__ == "__main__":
    line2segment()


