# @Description:
# @Author     : zhangyan
# @Time       : 2020/12/30 2:20 下午

from preprocessing.zy_utils import *
import pandas as pd
from tqdm import tqdm
import glob
from collections import Counter

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

# # 如果json为空，移除json和对应jpg
# input_dir = '/home/jerry/Documents/Micro_ADR/R78/daowen'
# output_path = '/home/jerry/Documents/Micro_ADR/R78/garbage'  # Automatically create output folders
# json_list = glob.glob('{}/*.json'.format(input_dir))
# make_dir(output_path)
# for json in json_list:
#     # print(json)
#     instance = json_to_instance(json)
#     shapes = instance.get('shapes')
#     if shapes == [] or shapes[0]['points']:
#         shutil.move(json, output_path)
#         jpg_name = os.path.basename(json).split('.')[0] + '.jpg'
#         jpg_path = os.path.join(os.path.dirname(json), jpg_name)
#         try:
#             shutil.move(jpg_path, output_path)
#         except:
#             print('there is no {}'.format(jpg_name))



# delete image_data
# json_path = '/home/jerry/Documents/yolov5-5.0/runs/detect/exp24/PR'
# save_path = '/home/jerry/data/kesen/labelme_31490_jbl/labelme_aug_train'
# json_list = glob.glob('{}/*.json'.format(json_path))
# for json in json_list:
#     base_name = os.path.basename(json)
#     instance = json_to_instance(json)
#     if instance['imageData'] != None:
#         instance['imageData'] = None
#     instance_to_json(instance, os.path.join(save_path, base_name))

import openpyxl as xl

excel_path = '/home/jerry/Desktop/Book.xlsx'
sheet1 = read_excel(excel_path, 'Sheet1')
k = 0
excel_list = []
for i in range(2, sheet1.max_row+1):
    k+=1
    img_name = sheet1.cell(i, 3).value
    excel_list.append(img_name)
print(excel_list)

a = Counter(excel_list)
print(a)
# img_path = '/home/jerry/Desktop/filtered_image'
# img_list = os.listdir(img_path)
# # print(img_list)
#
# inter = [i for i in excel_list if i not in img_list]
# print(inter)
# print(len(inter))


