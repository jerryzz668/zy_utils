"""
@Description:
@Author     : zhangyan
@Time       : 2021/11/22 下午3:53
"""
import os
import shutil

from tqdm import tqdm
import cv2
import glob
import random
from preprocessing.zy_utils import json_to_instance, make_dir

# img_path = '/home/jerry/Documents/code/mask2json/static/multi_objs_json/label.png'
# img = cv2.imread(img_path)
# cv2.namedWindow('img',0)
# cv2.imshow('img',img)
# cv2.waitKey()


img_path = '/home/jerry/data/Micro_R/R/yinglihen/03-18-ylh/0318-all-ylh'
output_path = '/home/jerry/data/Micro_R/R/yinglihen/03-18-ylh/0318-all-ylh_1024'
make_dir(output_path)
for file in tqdm(os.listdir(img_path)):
    if file.endswith('.jpg'):
        img = cv2.imread(os.path.join(img_path,file))
        img = cv2.resize(img, (1024,1024))
        cv2.imwrite(os.path.join(output_path, file), img)


# input_dir = '/home/jerry/data/Micro_R/R/R_lp/05_lp_1024'
# output_dir = '/home/jerry/data/Micro_R/R/R_lp/05_lp_1024_random_150'
# make_dir(output_dir)
# img_path = glob.glob('{}/*.jpg'.format(input_dir))
# val_num = 150  # int(len(img_path) * ratio)  # 按照rate比例从文件夹中取一定数量图片
# val_sample = random.sample(img_path, val_num)  # 从img_path中随机选取val_num数量的样本图片
# for sample in val_sample:
#     shutil.copy(sample, output_dir)
#     print('processing {}'.format(sample))

# input_dir = '/home/jerry/data/Micro_R/R/02-10-yinglihen/R-yinglihen'
# ok_dir = '/home/jerry/data/Micro_R/R/02-10-yinglihen/zhoupeng_r_yinglihen/OK'
# ng_dir = '/home/jerry/data/Micro_R/R/02-10-yinglihen/zhoupeng_r_yinglihen/NG'
# jsons = glob.glob('{}/*.json'.format(input_dir))
# for json in jsons:
#     instance = json_to_instance(json)
#     json_name = os.path.basename(json)
#     jpg_name = json_name.replace('.json', '.jpg')
#     if instance['label'] == 'ok':
#         shutil.copy(os.path.join(input_dir, jpg_name), os.path.join(ok_dir, jpg_name))
#     elif instance['label'] == 'yinglihen':
#         shutil.copy(os.path.join(input_dir, jpg_name), os.path.join(ng_dir, jpg_name))
#     print(instance['label'])

# input_dir = '/home/jerry/Desktop/garbage/yuantu/OK'
# output_dir = '/home/jerry/Desktop/garbage/crop/OK'
# file_list = glob.glob('{}/*.jpg'.format(input_dir))
# for file in file_list:
#     file_name = os.path.basename(file)
#     img = cv2.imread(file)
#     img = img[410:2260, 1700:4200]
#     cv2.imwrite(os.path.join(output_dir, file_name), img)
#     print('processing:', file_name)

# n = int(input())
# mail_list = []
# for i in range(n):
#     mail_list.append(input())
#
# for i in range(n):
#     for j in range(n-i-1):
#         if mail_list[j].split('@')[-1] > mail_list[j+1].split('@')[-1]:
#             mail_list[j], mail_list[j+1] = mail_list[j+1], mail_list[j]
# # print(mail_list)############
# break_p = [0]
# for i in range(n-1):
#     if mail_list[i].split('@')[-1] != mail_list[i+1].split('@')[-1]:
#         break_p.append(i+1)
# if break_p[-1] != n:
#     break_p.append(n)
# # print(break_p)###########
# list_all = []
# for i in range(len(break_p)-1):
#     list_a = mail_list[break_p[i]:break_p[i+1]]
#     # print(list_a)
#     for j in range(len(list_a)):
#         for k in range(len(list_a)-j-1):
#             if list_a[j].split('@')[0] < list_a[j+1].split('@')[0]:
#                 list_a[j], list_a[j+1] = list_a[j+1], list_a[j]
#     list_all.extend(list_a)
#
# for i in list_all:
#     print(i)
