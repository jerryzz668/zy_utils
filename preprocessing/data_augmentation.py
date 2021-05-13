import json
from albumentations.augmentations.functional import bbox_center_crop 
import cv2
import matplotlib.pyplot as plt   
from PIL import Image
import utils
import albumentations as A
import random
import os 
from glob import glob
import numpy as np 

def random_vertical_flip(img, bboxs):
    p = random.random()
    if p < 0.5:
        img = cv2.flip(img, 0)
        bboxs[:, 1] = img.shape[0] - bboxs[:, 1]
        bboxs[:, 3] = img.shape[0] - bboxs[:, 3]
    return img, bboxs


def random_horizontal_flip(img, bboxs):
    p = random.random()
    if p < 0.5:
        img = cv2.flip(img, 1)
        
        bboxs[:, 0] = img.shape[1] - bboxs[:, 0]
        bboxs[:, 2] = img.shape[1] - bboxs[:, 2]
    return img, bboxs


def random_rot90(img, bboxs):
    p = random.random()
    if p < 0.5:
        img = np.rot90(img)
       
        bboxs[:, [3, 0, 1, 2]] = bboxs[:, [0, 1, 2, 3]]
        bboxs[:, [1, 3]] = img.shape[0] - bboxs[:, [1, 3]]
    return img, bboxs

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
    # print(instance['shapes'])
    # instance['']
    return instance 

def random_data_aug(img_dir, save_dir):
    num_aug = 3
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    img_path_list = glob(os.path.join(img_dir, '*.jpg'))
    for img_path in img_path_list:
        # print(img_path)

        # img_path = '/home/xiaozhiheng/Documents/cemian_clear/0385-0022-11.jpg'
        print(img_path)
        json_path = img_path.replace('.jpg', '.json')
        # ori_img = Image.open(img_path)
        ori_img = cv2.imread(img_path)
        img_name = os.path.basename(img_path) 
        instance = utils.json_to_instance(json_path)
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
            # image = Image.fromarray(img)
            # image = np.asarray(img)
            transform = A.Compose([
                A.MedianBlur(blur_limit=7, always_apply=False, p=0.5),
                A.GaussNoise(var_limit=(5,10), p=0.5),
                A.RandomBrightnessContrast(brightness_limit=0.1, contrast_limit=0.1, p=0.5),
                ])
            tra_image = transform(image=image)["image"]

            # bboxs = shapes['points']
            # visulization(tra_image, bboxs)
            tra_image, bboxs = random_vertical_flip(tra_image, bboxs)
            tra_image, bboxs = random_horizontal_flip(tra_image, bboxs)
            tra_image, bboxs = random_rot90(tra_image, bboxs)
            # visulization(tra_image, bboxs)
            out_img_name = 'arg' + str(i) + '_' + img_name
            out_json_name = out_img_name.replace('.jpg', '.json')
            inst = modify_json_file(bboxs, inst)
            inst['imagePath'] = out_img_name
            inst['imageHeight'], inst['imageWidth'] = tra_image.shape[0], tra_image.shape[1]
            # out_img = Image.fromarray(tra_image)
            # out_img.save(os.path.join(save_dir, out_img_name))
            cv2.imwrite(os.path.join(save_dir, out_img_name), tra_image)
            utils.instance_to_json(inst, os.path.join(save_dir, out_json_name))

if __name__ == '__main__':
    img_dir = '/home/xiaozhiheng/Documents/cemian_clear'
    save_dir = '//home/xiaozhiheng/Documents/cemian_clear_aug'

    random_data_aug(img_dir, save_dir)


    


