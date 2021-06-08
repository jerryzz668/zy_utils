"""
@Description:  input: test_csv  txt
output: [{
	"image_id": int,
	"category_id": int,
	"bbox": [xmin,ymin,xmax,ymax],
	"score": float
}]

offground      ->     offgroundperson
badge          ->     guarder
safebelt       ->     safebeltperson
ground         ->     ...

@return: instance

@Author     : zhangyan
@Time       : 2021/6/8 下午1:59
"""

import os
import pandas as pd
import numpy as np
from preprocessing.zy_utils import *

test_csv_dir = '/home/jerry/Desktop/tianchi/Track3_helmet/3_testa_user.csv'
txt_dir = '/home/jerry/Documents/yolov5-5.0/runs/detect/exp3/labels'

dataframe = pd.read_csv(test_csv_dir)
test_csv = np.array(dataframe)
print(test_csv)

# image_id字典
image_id_dict = {}
for i, path in enumerate(test_csv):
    image_id_dict[os.path.basename(path[0])] = i
print(image_id_dict)

# category_id字典
category_id_dict = {'guarder':1, 'safebeltperson':2, 'offgroundperson':3}

instance = []
for key, value in image_id_dict:
    anno = {}
    txt = read_txt(os.path.join(txt_dir, key))