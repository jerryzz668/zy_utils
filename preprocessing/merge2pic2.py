'''
* @Description: TODO
* @author: lijianqing
* @date: 2021年09月07日 15:23
'''

# -*- coding:utf-8 -*-
from PIL import Image
import glob
import os
from tqdm import tqdm
from preprocessing.zy_utils import json_to_instance, instance_to_json

def blend_two_images():
    path_qx=glob.glob(r'D:\work\data\R\34\3\908blend\qx\*.jpg')
    path_dt=glob.glob(r'D:\work\data\R\34\3\908blend\dt\*.jpg')
    path_save = r'D:\work\data\R\34\3\908blend\ga\9'
    if not os.path.exists(path_save):
        os.makedirs(path_save)
    index = 1
    for i in path_qx:
        for j in path_dt:
            img1 = Image.open(i)
            img1 = img1.convert('RGBA')
            img2 = Image.open(j)
            img2 = img2.convert('RGBA')
            route = [Image.ROTATE_90,Image.ROTATE_180,Image.ROTATE_270]
            for k in route:
                index+=1
                dst2 = img2.transpose(k)
                dst1 = img1.transpose(k)
                img = Image.blend(dst2, dst1, 0.9)
                # img.show()
                img.save(os.path.join(path_save,"{}.png".format(index)))
    return

def modify_json_name(file, write_img_name, output_dir):
    json_basename = os.path.basename(file)
    json_dirname = os.path.dirname(file)
    json_file = json_basename.split('.')[0] + '.json'
    instance = json_to_instance(os.path.join(json_dirname, json_file))
    modify_img_path = '{}.json'.format(write_img_name)
    instance['imagePath'] = '{}.jpg'.format(write_img_name)
    instance_to_json(instance, os.path.join(output_dir, modify_img_path))

def blend_two_images_with_json():
    path_qx=glob.glob('/home/jerry/data/Micro_D/D_loushi/combined/11-22-dm-dw/qj/*.jpg')
    path_dt=glob.glob('/home/jerry/data/Micro_D/D_loushi/combined/11-22-dm-dw/bg/*.jpg')
    path_save = '/home/jerry/data/Micro_D/D_loushi/combined/11-22-dm-dw/blend'
    if not os.path.exists(path_save):
        os.makedirs(path_save)
    index = 0
    for i in tqdm(path_qx):
        for j in path_dt:
            img1 = Image.open(i)
            img1 = img1.convert('RGBA')
            img2 = Image.open(j)
            img2 = img2.convert('RGBA')
            img = Image.blend(img1, img2, 0.1)
            img = img.convert('RGB')
            # img.show()
            img.save(os.path.join(path_save, "{}.jpg".format(index)))
            modify_json_name(i, index, path_save)
            # print('正在融合:{}.jpg'.format(index))
            index += 1
    return
blend_two_images_with_json()
