import json
# from albumentations.augmentations.functional import bbox_center_crop 
import cv2
import matplotlib.pyplot as plt
from preprocessing.zy_utils import instance_to_json, json_to_instance
import albumentations as A
import random
import os 
from glob import glob
import numpy as np 
from atools.tools import *

def random_vertical_flip(img, bboxs=[]):
    p = random.random()
    if p < 0.5:
        img = cv2.flip(img, 0)
        if bboxs != []:
            bboxs[:, 1] = img.shape[0] - bboxs[:, 1]
            bboxs[:, 3] = img.shape[0] - bboxs[:, 3]
            return img, bboxs
        else:
            return img
    else:
        return img, bboxs

def random_horizontal_flip(img, bboxs=[]):
    p = random.random()
    if p < 0.5:
        img = cv2.flip(img, 1)
        if bboxs != []:
            bboxs[:, 0] = img.shape[1] - bboxs[:, 0]
            bboxs[:, 2] = img.shape[1] - bboxs[:, 2]
            return img, bboxs
        else:
            return img
    else:
        return img, bboxs


def random_rot90(img, bboxs=[]):
    p = random.random()
    if p < 0.5:
        img = np.rot90(img)
        if bboxs != []:
            bboxs[:, [3, 0, 1, 2]] = bboxs[:, [0, 1, 2, 3]]
            bboxs[:, [1, 3]] = img.shape[0] - bboxs[:, [1, 3]]
            return img, bboxs
        else:
            return img
    else:
        return img 

def transform():
    transform = A.Compose([
                    A.MedianBlur(blur_limit=3, always_apply=False, p=0.5),
                    A.GaussNoise(var_limit=(0,2), p=1),
                    A.RandomBrightnessContrast(brightness_limit=0.05, contrast_limit=0.1, p=0.5),
                    
                    ])
    return transform

def visulization(img, bboxs):
    plt_img = img.copy()
    for bbox in bboxs:
        x1, y1, x2, y2 = bbox
        cv2.rectangle(plt_img, (int(x1), int(y1)), (int(x2), int(y2)), (0,255,0), 2)
    plt.imshow(plt_img, cmap='gray')
    plt.show()

def modify_json_file(bboxs, instance):
    shapes = instance['shapes']
    assert len(bboxs) == len(shapes)
    for bbox, shape in zip(bboxs, shapes):
        x1, y1, x2, y2 = bbox
        shape['points'] = [[x1, y1], [x2, y2]]
    return instance 

def random_data_aug_2(img_dir, save_dir):
    num_arg = 2
    make_dir(save_dir)
    img_path_list = glob(os.path.join(img_dir, '*.jpg'))
    for img_path in img_path_list:
        print(img_path)
        img_name = os.path.basename(img_path) 
        ori_img = cv2.imread(img_path)
        # tra_img = transform()
        for i in range(num_arg):
            image = ori_img.copy()
            trans_form = transform()
            tra_img = trans_form(image=image)['image']
            # tra_img = random_horizontal_flip(tra_img)
            # tra_img = random_vertical_flip(tra_img)
            # tra_img = random_rot90(tra_img)
            out_img_name = 'arg' + str(i) + '_' + img_name
            cv2.imwrite(os.path.join(save_dir, out_img_name), tra_img)

def random_data_aug(img_dir, save_dir):
    num_aug = 2
    make_dir(save_dir)
    img_path_list = glob(os.path.join(img_dir, '*.jpg'))
    for img_path in img_path_list:
        print(img_path)
        json_path = img_path.replace('.jpg', '.json')
        # ori_img = Image.open(img_path)
        ori_img = cv2.imread(img_path)
        img_name = os.path.basename(img_path) 
        instance = json_to_instance(json_path)
        instance['imageData'] = None
        shapes = instance['shapes']

        ori_bboxs = [] 
        for shape in shapes:
            x1, y1 = shape['points'][0]
            x2, y2 = shape['points'][1]
            ori_bboxs.append([x1, y1, x2, y2])
        if ori_bboxs == []:
            continue
        ori_bboxs = np.array(ori_bboxs)
        
        for i in range(num_aug):
            image = ori_img.copy()
            bboxs = ori_bboxs.copy()
            # shapes = 
            inst = instance.copy()
            transform_ = transform()
            tra_image = transform_(image=image)["image"]

            # bboxs = shapes['points']
            # visulization(tra_image, bboxs)
            tra_image, bboxs = random_vertical_flip(tra_image, bboxs)
            tra_image, bboxs = random_horizontal_flip(tra_image, bboxs)
            # tra_image, bboxs = random_rot90(tra_image, bboxs)
            # visulization(tra_image, bboxs)
            out_img_name = 'arg' + str(i) + '_' + img_name
            out_json_name = out_img_name.replace('.jpg', '.json')
            inst = modify_json_file(bboxs, inst)
            inst['imagePath'] = out_img_name
            inst['imageHeight'], inst['imageWidth'] = tra_image.shape[0], tra_image.shape[1]
            # out_img = Image.fromarray(tra_image)
            # out_img.save(os.path.join(save_dir, out_img_name))
            cv2.imwrite(os.path.join(save_dir, out_img_name), tra_image)
            inst = eval(str(inst))
            instance_to_json(inst, os.path.join(save_dir, out_json_name))
            # save_json(os.path.join(save_dir, out_json_name), inst)

if __name__ == '__main__':
    img_dir = '/home/jerry/Desktop/jpg'  # 1.only img  2.img and json
    # save_dir = img_dir.format('')
    save_dir = '/home/jerry/Desktop/jpg_r' # save_path, 1.save img 2. save img and json

    random_data_aug(img_dir, save_dir)  # 1.only img
    # random_data_aug_2(img_dir, save_dir)  # 2.img and json


    


