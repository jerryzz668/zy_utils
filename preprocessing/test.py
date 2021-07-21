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


def grid_search(a, b):
    x, y = np.meshgrid(np.linspace(a[0], a[1], a[2]), np.linspace(b[0], b[1], b[2]))
    cartesian_arr = np.array([x.ravel(),y.ravel().T])
    return cartesian_arr.T

a = [0.1, 0.8, 3]
b = [0.3, 0.7, 3]

c = grid_search(a, b)
print(c)