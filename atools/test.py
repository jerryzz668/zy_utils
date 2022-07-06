"""
@Description:
@Author     : zhangyan
@Time       : 2021/11/22 下午3:53
"""
import os
import shutil

from tqdm import tqdm
import cv2
import math
import glob
import random
from collections import Counter
import matplotlib.pyplot as plt
from preprocessing.zy_utils import json_to_instance, make_dir, make_dir2, instance_to_json

# img_path = '/home/jerry/data/Micro_R/R/yinglihen/new_form_ylh/tiaozhuang+xinxingtai_all'
# output_path = '/home/jerry/data/Micro_R/R/yinglihen/new_form_ylh/tiaozhuang+xinxingtai_all_1024'
# make_dir(output_path)
# for file in tqdm(os.listdir(img_path)):
#     if file.endswith('.jpg'):
#         img = cv2.imread(os.path.join(img_path,file))
#         img = cv2.resize(img, (1024,1024))
#         cv2.imwrite(os.path.join(output_path, file), img)


# input_dir = '/home/jerry/microsoft/R/Data/original/客认+漏失/keren+loushi_labelme/labelme-filter/dm-heidian'
# output_dir = '/home/jerry/Desktop/garbage/dm-heidian-100'
# make_dir(output_dir)
# img_path = glob.glob('{}/*.jpg'.format(input_dir))
# val_num = 100  # int(len(img_path) * ratio)  # 按照rate比例从文件夹中取一定数量图片
# val_sample = random.sample(img_path, val_num)  # 从img_path中随机选取val_num数量的样本图片
# for sample in val_sample:
#     json_name = os.path.basename(sample).replace('.jpg','.json')
#     json_path = os.path.join(os.path.dirname(sample),json_name)
#     shutil.copy(json_path,output_dir)
#     shutil.copy(sample, output_dir)
#     print('processing {}'.format(sample))


# points_to_rectangle
# def points_to_xywh(obj):
#     '''
#     :param obj: labelme instance中待检测目标obj{}
#     :return: box左上坐标+wh
#     '''
#     points = obj['points']
#     shape_type = obj['shape_type']
#     if shape_type == 'circle':
#         center = [points[0][0], points[0][1]]
#         radius = math.sqrt((points[1][0]-center[0])**2+(points[1][1]-center[1])**2)
#         return [center[0]-radius-1, center[1]-radius-1, 2*radius+3, 2*radius+3]
#     xs = [point[0] for point in points]
#     ys = [point[1] for point in points]
#     min_x, max_x = min(xs), max(xs)
#     min_y, max_y = min(ys), max(ys)
#     return [int(min_x-1), int(min_y-1), int(max_x+3), int(max_y+3)]
# input_dir = '/home/jerry/data/Micro_R/R/line11-12/cate-yise/3_labelme_yise_all_crop512_rec'
# jsons = glob.glob('{}/*.json'.format(input_dir))
# for json in jsons:
#     instance = json_to_instance(json)
#     if instance['shapes'] != '':
#         objs = instance['shapes']
#         for obj in objs:
#             a,b,c,d = points_to_xywh(obj)
#             obj['points'] = [[a,b],[c,d]]
#             obj['shape_type'] = 'rectangle'
#     instance_to_json(instance, json)



# input_dir = '/home/jerry/data/chengtaoyuan/2022_05_31_19_17_37_rename'
# output_dir = '/home/jerry/data/chengtaoyuan/output'
# make_dir2(output_dir, ['ng', 'ok'])
# jsons = glob.glob('{}/*.json'.format(input_dir))
# file_list = os.listdir(input_dir)
# file_list.sort()
# distance = []
# for json in file_list:
#     if json.endswith('.jpg'): continue
#     instance = json_to_instance(os.path.join(input_dir, json))
#     json_name = os.path.basename(json)
#     jpg_name = json_name.replace('.json', '.jpg')
#     print(json_name)
    
#     shapes = instance['shapes']
#     point0 = shapes[0]['points']
#     point1 = shapes[1]['points']
#     # print(point0,point1)
#     a_x = (point0[0][0]+point0[1][0])//2
#     a_y = (point0[0][1]+point0[1][1])//2
#     b_x = (point1[0][0]+point1[1][0])//2
#     b_y = (point1[0][1]+point1[1][1])//2
#     # print(a_x,a_y,b_x,b_y)
#     distance_ab = math.sqrt((math.pow((a_x-b_x),2)+math.pow((a_y-b_y),2)))
#     # if distance_ab <= 91:
#     #     shutil.copy(os.path.join(input_dir, jpg_name), os.path.join(output_dir, 'ng'))
#     # if distance_ab >= 95:
#     #     shutil.copy(os.path.join(input_dir, jpg_name), os.path.join(output_dir, 'ok'))
#     distance.append(int(distance_ab))
# print(distance)
distance = [98, 98, 98, 98, 98, 98, 98, 97, 98, 98, 97, 98, 96, 96, 97, 97, 98, 98, 97, 98, 97, 96, 96, 97, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 97, 97, 97, 97, 97, 98, 98, 98, 97, 98, 98, 97, 97, 96, 98, 98, 98, 98, 98, 97, 97, 97, 97, 97, 97, 98, 97, 97, 97, 98, 97, 97, 98, 98, 97, 98, 97, 98, 97, 98, 98, 97, 98, 98, 98, 98, 98, 97, 98, 98, 97, 96, 97, 98, 97, 98, 98, 98, 96, 92, 90, 89, 88, 89, 88, 88, 86, 86, 85, 85, 84, 84, 84, 83, 83, 83, 83, 82, 84, 87, 85, 83, 83, 83, 82, 83, 83, 82, 83, 83, 83, 83, 86, 88, 87, 87, 87, 89, 88, 87, 86, 85, 85, 87, 86, 84, 97, 87, 86, 86, 85, 85, 84, 85, 82, 88, 86, 85, 83, 90, 90, 88, 87, 85, 83, 86, 85, 85, 83, 82, 83, 83, 85, 86, 87, 86, 86, 86, 86, 87, 86, 86, 87, 85, 84, 89, 87, 86, 88, 86, 84, 86, 85, 82, 82, 83, 84, 84, 86, 88, 87, 87, 87, 94, 98, 97, 90, 90, 97, 91, 88, 97, 86, 88, 88, 89, 87, 86, 86, 86, 85, 85, 86, 98, 98, 93, 96, 99, 86, 96, 85, 85, 85, 84, 84, 87, 87, 85, 86, 85, 84, 84, 85, 84, 86, 86, 85, 84, 84, 83, 84, 83, 84, 89, 91, 87, 100, 100, 100, 100, 100, 100, 98, 95, 86, 85, 84, 84, 83, 87, 84, 84, 83, 83, 82, 83, 82, 82, 84, 85, 84, 83, 84, 83, 83, 85, 84, 82, 83, 84, 85, 82, 83, 83, 83, 83, 83, 82, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106]
# # distance.sort()
# a = Counter(distance)
# print(a)
# a = sorted(a.items(), key=lambda item:item[0])
# print(distance)
a = list(range(1,327))
plt.xlabel('time')
plt.ylabel('distance')
plt.plot(a,distance)
plt.show()
