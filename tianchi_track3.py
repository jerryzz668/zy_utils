"""
@Description:  input: test_csv  txt
output: [{
	"image_id": int,
	"category_id": int,
	"bbox": [xmin,ymin,xmax,ymax],
	"score": float
}]

ground     0    ->     ...
offground  1    ->    3 offgroundperson
safebelt   2    ->    2 safebeltperson
badge      3    ->    1 guarder

@return: instance

@Author     : zhangyan
@Time       : 2021/6/8 下午1:59
"""

import os
import pandas as pd
import numpy as np
from preprocessing.zy_utils import *

test_csv_dir = '/home/jerry/Desktop/tianchi/Track3_helmet/3_testa_user.csv'
txt_dir = '/home/jerry/Documents/yolov5-5.0/runs/detect/exp/jsons'
save_path = ''

dataframe = pd.read_csv(test_csv_dir)
test_csv = np.array(dataframe)
# print(test_csv)

# image_id字典
image_id_dict = {}
for i, path in enumerate(test_csv):
    image_id_dict[os.path.basename(path[0])] = i
print(image_id_dict)

# category_id字典
category_id_dict = {'guarder':1, 'safebeltperson':2, 'offgroundperson':3}

annotations = []
for key, value in image_id_dict.items():
    img_name = key.split(".")[0] + ".json"
    instance = json_to_instance(os.path.join(txt_dir, img_name))
    shapes = instance['shapes']

    for i in range(len(shapes)):
        if shapes[i] == 'offground':
            anno = {}
            anno['image_id'] = value
            anno['category_id'] = 3
            anno['bbox'] = shapes[i]['points'].flatten().tolist()
            anno['score'] = shapes[i]['score']  # yolo_to_labelme加入score
            annotations.append(anno)

        if shapes[i] == 'safebelt':
            anno = {}
            anno['image_id'] = value
            anno['category_id'] = 2
            safebelt_box = shapes[i]['points'].flatten().tolist()
            for j in range(len(shapes)):
                if shapes[j]['label'] == 'ground':
                    ground_box = shapes[j]['points'].flatten().tolist()
                    iou = compute_iou(safebelt_box, ground_box)
                    if iou > 0.3:
                        anno['bbox'] = ground_box
                        anno['score'] = shapes[j]['score']
                elif shapes[j]['label'] == 'offground':
                    offground_box = shapes[j]['points'].flatten().tolist()
                    iou = compute_iou(safebelt_box, offground_box)
                    if iou > 0.3:
                        anno['bbox'] = offground_box
                        anno['score'] = shapes[j]['score']
                else:
                    anno['bbox'] = []
                    anno['score'] = []
            annotations.append(anno)

        if shapes[i] == 'badge':
            anno = {}
            anno['image_id'] = value
            anno['category_id'] = 1
            badge_box = shapes[i]['points'].flatten().tolist()
            for j in range(len(shapes)):
                if shapes[j]['label'] == 'ground':
                    ground_box = shapes[j]['points'].flatten().tolist()
                    iou = compute_iou(badge_box, ground_box)
                    if iou > 0.3:
                        anno['bbox'] = ground_box
                        anno['score'] = shapes[j]['score']
                elif shapes[j]['label'] == 'offground':
                    offground_box = shapes[j]['points'].flatten().tolist()
                    iou = compute_iou(badge_box, offground_box)
                    if iou > 0.3:
                        anno['bbox'] = offground_box
                        anno['score'] = shapes[j]['score']
                else:
                    anno['bbox'] = []
                    anno['score'] = []
            annotations.append(anno)

print(annotations)

# instance_to_json(annotations, save_path)













