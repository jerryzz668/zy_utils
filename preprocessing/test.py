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
# from zy_utils import *
import pandas as pd

def json_to_instance(json_file_path):
    '''
    :param json_file_path: json文件路径
    :return: json instance
    '''
    with open(json_file_path, 'r', encoding='utf-8') as f:
        instance = json.load(f)
    return instance


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


input_dir = '/home/adt/Desktop/A_daowen_select/daowen_jiao_modify'
output_path = '/home/adt/Desktop/A_daowen_select/empty_jsons'
json_list = os.listdir(input_dir)
for json_name in json_list:
    print(json_name)
    instance = json_to_instance(os.path.join(input_dir,json_name))
    shapes = instance.get('shapes')
    if shapes == []:
        shutil.move(os.path.join(input_dir,json_name), output_path)

    # print(instance)
