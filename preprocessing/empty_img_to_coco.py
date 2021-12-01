"""
@Description:
@Author     : zhangyan
@Time       : 2021/9/26 下午3:39
"""
import os
import cv2
from tqdm import tqdm
from preprocessing.zy_utils import instance_to_json

id = 1000
coco_images = []
input_dir = '/home/jerry/data/Micro_D/D_loushi/11-24ceshijieguo/11-25-empty-aug_check68'
save_coco_path = '/home/jerry/Desktop/empty_img.json'
imglist = os.listdir(input_dir)
for img_file in tqdm(imglist):
    img_dic = {}
    img = cv2.imread(os.path.join(input_dir, img_file))
    w, h, c = img.shape
    img_dic['height'] = w
    img_dic['width'] = h
    img_dic['id'] = id
    img_dic['file_name'] = img_file
    id += 1
    coco_images.append(img_dic)

instance_to_json(coco_images, save_coco_path)

