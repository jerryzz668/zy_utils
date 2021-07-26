# @Description:
# @Author     : zhangyan
# @Time       : 2020/12/30 2:20 下午


import os
import random
import time
import cv2
import shutil
import glob
import json

import numpy as np

from preprocessing.zy_utils import *
import pandas as pd
from tqdm import tqdm


# def search(array, num):
#     low, high = 0, len(array)-1
#     while low < high:
#         mid = (low+high)//2
#         if num > array[mid]:
#             low = mid + 1
#         elif num < array[mid]:
#             high = mid - 1
#         else:
#             return mid
#     return -1
#
# array = [i for i in range(1,1000,5)]
# print(array)
# print(search(array, 46))


# a = '阿姨那种'
# b = pypinyin(a)

# # 如果json为空，移除
# input_dir = '/home/adt/Desktop/A_daowen_select/daowen_jiao_modify'
# output_path = '/home/adt/Desktop/A_daowen_select/empty_jsons'
# json_list = os.listdir(input_dir)
# for json_name in json_list:
#     print(json_name)
#     instance = json_to_instance(os.path.join(input_dir,json_name))
#     shapes = instance.get('shapes')
#     if shapes == []:
#         shutil.move(os.path.join(input_dir,json_name), output_path)
#
#     # print(instance)

# delete image_data
json_path = '/home/jerry/Documents/yolov5-5.0/runs/detect/exp24/PR'
save_path = '/home/jerry/data/kesen/labelme_31490_jbl/labelme_aug_train'
json_list = glob.glob('{}/*.json'.format(json_path))
for json in json_list:
    base_name = os.path.basename(json)
    instance = json_to_instance(json)
    if instance['imageData'] != None:
        instance['imageData'] = None
    instance_to_json(instance, os.path.join(save_path, base_name))