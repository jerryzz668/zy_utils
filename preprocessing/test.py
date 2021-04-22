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
import pypinyin
import xlwt

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

import os
import openpyxl

gt_cate: [['aokeng', 'baidian', 'guashang-baiduan', 'guashang-baizhang', 'guashang-heiduan', 'guashang-heizhang',
          'heidian', 'maoxu', 'pengshang-bian', 'pengshang-zhang', 'shahenyin', 'tabian-an', 'tabian-liang', 'yise-bai', 'yise-hei', 'yise-liang', 'z_lou_or_guo']]
