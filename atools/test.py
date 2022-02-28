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
from preprocessing.zy_utils import json_to_instance

img_path = '/home/jerry/Desktop/garbage/yuantu/NG'
output_path = '/home/jerry/Desktop/garbage/new/NG'
for file in tqdm(os.listdir(img_path)):
    img = cv2.imread(os.path.join(img_path,file))
    img = cv2.resize(img, (1024,1024))
    cv2.imwrite(os.path.join(output_path, file), img)


# input_dir = '/home/jerry/data/Micro_R/R/R_lp/05_lp'
# output_dir = '/home/jerry/data/Micro_R/R/02-10-yinglihen/yinglihen-enhanced-dataset0224/OK'
# img_path = glob.glob('{}/*.jpg'.format(input_dir))
# val_num = 250  # int(len(img_path) * ratio)  # 按照rate比例从文件夹中取一定数量图片
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

