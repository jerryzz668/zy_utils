"""
@Description:
@Author     : zhangyan
@Time       : 2021/9/26 下午3:39
"""
import os
import cv2
from preprocessing.zy_utils import instance_to_json

img_dic = {}
id = 10000
coco_images = []
input_dir = '/home/jerry/Desktop/jpg_r'
save_coco_path = '/home/jerry/Desktop/empty_img.json'
imglist = os.listdir(input_dir)
for img_file in imglist:
    img = cv2.imread(os.path.join(input_dir, img_file))
    w, h, c = img.shape
    img_dic['height'] = w
    img_dic['width'] = h
    img_dic['id'] = id
    img_dic['file_name'] = img_file
    id += 1
    coco_images.append(img_dic)

instance_to_json(coco_images, save_coco_path)

