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

from zy_utils import *
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
#

# 挑选不同面 dm/cm/gj
# import os
# import shutil
# p = r'G:\BaiduNetdiskDownload\微软D件\D件-0413\D2-2021-04-12\大面\outputs'
# o_p = r'C:\Users\Administrator\Desktop\dm1314'
#
# img_list = os.listdir(p)
# for img in img_list:
#     file_path = os.path.join(p, img)
#     if not os.path.isfile(file_path) or img[img.rindex('.') + 1:] not in ['xml']: continue
#     suffix_img = img.split('-')[2].split('.')[0]
#     # print(suffix_img)
#     if suffix_img in ['13','14']:
#     # if 5 <= int(suffix_img) <= 12:
#         # print(file_path)
#         try:
#             shutil.move(file_path,o_p)
#         except:
#             print(file_path)

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

# rename
# input_dir = r'G:\BaiduNetdiskDownload\Rain100H\target'
# file_list = os.listdir(input_dir)
# for file in file_list:
#     # new_name = file.split('-')[-1].split('x')[0] + '.png'
#     new_name = file.split('-')[-1]
#     # print(new_name)
#     os.renames(os.path.join(input_dir, file), os.path.join(input_dir, new_name))

# t1 = np.arange(12)
# t2 = t1.reshape(3,4)
#
# print(t2)
# t3 = t2.flatten()
#
# print(t3)
# print(type(t3))
# t4 = t3.tolist()
# print(t4)
# print(type(t4))


# import numpy as np
# import matplotlib.pyplot as plt
# import pywt.data


# # 中文显示工具函数
# def set_ch():
#     from pylab import mpl
#     mpl.rcParams['font.sans-serif'] = ['FangSong']
#     mpl.rcParams['axes.unicode_minus'] = False


# set_ch()
# # original = pywt.data.camera()
# original = '/Users/zhangyan/Desktop/IMG_3951.JPG'
# original = cv2.imread(original, 0)
# # cv2.imshow('ori', original)
# # cv2.waitKey()
# # Wavelet transform of image, and plot approximation and details
# titles = ['近似图像', '水平细节', '垂直细节', '对角线细节']
# coeffs2 = pywt.dwt2(original, 'haar')
# LL, (LH, HL, HH) = coeffs2
# fig = plt.figure(figsize=(12, 3))
# for i, a in enumerate([LL, LH, HL, HH]):
#     ax = fig.add_subplot(1, 4, i + 1)
#     ax.imshow(a, interpolation="nearest", cmap=plt.cm.gray)
#     ax.set_title(titles[i], fontsize=10)
#     ax.set_xticks([])
#     ax.set_yticks([])
# fig.tight_layout()
# plt.show()

