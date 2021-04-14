# @Description:
# @Author     : zhangyan
# @Time       : 2020/12/30 2:20 下午


import os
import random
import time
import cv2
import shutil
import glob
import numpy as np

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

import os
import shutil
p = '/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/Anew/all/outputs'
o_p = '/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/Anew/all/outputcm'

img_list = os.listdir(p)
for img in img_list:
    file_path = os.path.join(p, img)
    if not os.path.isfile(file_path) or img[img.rindex('.') + 1:] not in ['xml']: continue
    suffix_img = img.split('-')[2].split('.')[0]
    # print(suffix_img)
    # if suffix_img in ['13','14']:
    if 5 <= int(suffix_img) <= 12:
        # print(file_path)
        try:
            shutil.copy(file_path,o_p)
        except:
            print(file_path)