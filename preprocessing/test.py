# @Description:
# @Author     : zhangyan
# @Time       : 2020/12/30 2:20 下午

from cv2 import PARAM_STRING
from preprocessing.zy_utils import *
import pandas as pd
from tqdm import tqdm
import glob
from collections import Counter


# 如果json为空，移除json和对应jpg
input_dir = '/home/jerry/data/Micro_A/A_loushi/labeled/C_MS_pengshang_20211021'
output_path = '/home/jerry/data/Micro_A/A_loushi/labeled/garbage'  # Automatically create output folders
json_list = glob.glob('{}/*.json'.format(input_dir))
make_dir(output_path)
for json in json_list:
    # print(json)
    instance = json_to_instance(json)
    shapes = instance.get('shapes')
    # if shapes == [] or shapes[0]['points']:
    if shapes == []:
        shutil.move(json, output_path)
        jpg_name = os.path.basename(json).split('.')[0] + '.jpg'
        jpg_path = os.path.join(os.path.dirname(json), jpg_name)
        try:
            shutil.move(jpg_path, output_path)
        except:
            print('there is no {}'.format(jpg_name))



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
# import cv2
# import matplotlib.pyplot as plt
# from atools.erode_dilated_img import MORPH_OPEN, MORPH_GRADIENT

# input_dir = '/home/jerry/data/zAI_competition/modify/coco_aug/val2017'
# output_dir = '/home/jerry/data/zAI_competition/modify/coco_aug/val2017_r'
# make_dir(output_dir)
# img_list = glob.glob('{}/*.jpg'.format(input_dir))
# # img = '/home/jerry/data/zAI_competition/modify/coco_aug/val2017/connected_img_1.jpg'
# # print(img_list)
# for img in img_list:
#     print('processing:', img)
#     img_BGR = cv2.imread(img)
#     img_G = MORPH_OPEN(img_BGR)
#     img_B = MORPH_GRADIENT(img_BGR)

#     img_BGG = np.concatenate([img_BGR[:, :, 2:3], img_B[:, :, 2:3], img_G[:, :, 2:3]], 2)
#     img_BGG = np.array(img_BGG, 'uint8')
#     cv2.imwrite(os.path.join(output_dir, os.path.basename(img)), img_BGG)

# plt.subplot(221)
# plt.imshow(img_BGR)
# plt.subplot(222)
# plt.imshow(img_G)
# plt.subplot(223)
# plt.imshow(img_B)
# plt.subplot(224)
# plt.imshow(img_BGG)
# plt.show()

import datetime
 
# def calc_spend_time(func):
#     def new_func(*args, **kargs):
#         start_time = datetime.datetime.now()
#         result = func(*args, **kargs)
#         end_tiem = datetime.datetime.now()
#         print ("result:", result, "used:", (end_tiem - start_time).microseconds, "μs")
#     return new_func
#
# @calc_spend_time
# def calc_add(a, b):
#     return a + b
#
#
# @calc_spend_time
# def calc_diff(a, b):
#     return a - b
#
# calc_add(a=1, b=2)
# calc_diff(1, 2)


