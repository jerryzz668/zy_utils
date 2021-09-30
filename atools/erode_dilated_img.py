"""
@Description:
@Author     : zhangyan
@Time       : 2021/9/29 上午11:20
"""
import glob
import os
import cv2 as cv
from pathlib import Path
import copy
import random
import numpy as np
from preprocessing.zy_utils import make_dir, instance_to_json, json_to_instance

# 腐蚀erode,高亮部分被腐蚀，高亮部分一般为背景
def demo_erode(image):
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))  # 定义结构元素的形状和大小  内核形状：{矩形：MORPH_RECT，交叉形：MORPH_CROSS，椭圆形：MORPH_ELLIPSE}
    dst = cv.erode(image, kernel)  # 腐蚀操作
    return dst

# 腐蚀dilate,高亮部分被膨胀，高亮部分一般为背景
def demo_dilate(image):
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))  # 定义结构元素的形状和大小  内核形状：{矩形：MORPH_RECT，交叉形：MORPH_CROSS，椭圆形：MORPH_ELLIPSE}
    dst = cv.dilate(image, kernel)  # 膨胀操作
    return dst

# 开运算MORPH_OPEN, 先腐蚀后膨胀的操作称之为开操作。它具有消除细小物体, 在纤细处分离物体和平滑较大物体边界的作用
def MORPH_OPEN(image):
    kernel = np.ones((3, 3), np.uint8)
    dst = cv.morphologyEx(image, cv.MORPH_OPEN, kernel)
    return dst

# 闭运算MORPH_CLOSE, 先膨胀后腐蚀的操作称之为闭操作。它具有填充物体内细小空洞, 连接邻近物体和平滑边界的作用
def MORPH_CLOSE(image):
    kernel = np.ones((3, 3), np.uint8)
    dst = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)
    return dst

# 形态学梯度运算, 膨胀以后的图像减去腐蚀以后的图像
def MORPH_GRADIENT(image):
    kernel = np.ones((3, 3), np.uint8)
    dst = cv.morphologyEx(image, cv.MORPH_GRADIENT, kernel)
    return dst

# 图像顶帽（或图像礼帽）运算是原始图像减去图像开运算的结果，得到图像的噪声
def MORPH_TOPHAT(image):
    kernel = np.ones((3, 3), np.uint8)
    dst = cv.morphologyEx(image, cv.MORPH_TOPHAT, kernel)
    return dst

# 图像黑帽运算是图像闭运算操作减去原始图像的结果，得到图像内部的小孔，或者前景色中的小黑点
def MORPH_BLACKHAT(image):
    kernel = np.ones((3, 3), np.uint8)
    dst = cv.morphologyEx(image, cv.MORPH_BLACKHAT, kernel)
    return dst

def modify_json_name(file, write_img_name, output_dir):
    json_file = file.split('.')[0] + '.json'
    instance = json_to_instance(json_file)
    modify_img_path = '{}'.format(write_img_name) + os.path.basename(json_file)
    instance['imagePath'] = '{}'.format(write_img_name) + os.path.basename(file)
    instance_to_json(instance, os.path.join(output_dir, modify_img_path))

def get_output_dir(input_dir, filter):
    output_dirname = os.path.dirname(input_dir)
    output_basename = os.path.basename(input_dir)
    write_img_name = str(filter).split('_')[-1].split(' ')[0] + '_'
    output_dir = os.path.join(output_dirname, '{}'.format(write_img_name) + output_basename)
    return output_dir

def erode_img(input_dir, filter, probability):
    output_dir = get_output_dir(input_dir, filter)
    make_dir(output_dir)
    file_list = glob.glob('{}/*.jpg'.format(input_dir))

    for file in file_list:
        p = random.random()
        if p < probability:
            json_path = Path(file.split('.jpg')[0] + '.json')
            img_name = os.path.basename(file)
            write_img_name = str(filter).split('_')[-1].split(' ')[0] + '_'
            if json_path.exists():
                print('正在处理：{} and {}'.format(img_name, os.path.basename(json_path)))
                modify_json_name(file, write_img_name, output_dir)
            else:
                print('正在处理：', img_name)
            img = cv.imread(file)
            processed_img = filter(img)
            cv.imwrite(os.path.join(output_dir, '{}'.format(write_img_name) + img_name), processed_img, [int(cv.IMWRITE_JPEG_QUALITY), 95])

if __name__ == '__main__':
    input_dir = '/home/jerry/data/zAI_competition/modify/coco_aug/val2017'  # 输入img和json, # Automatically create output folders under the same path
    filter = MORPH_OPEN  # 模式选择-----> demo_erode, demo_dilate, MORPH_OPEN, MORPH_CLOSE, MORPH_GRADIENT, MORPH_TOPHAT, MORPH_BLACKHAT
    probability = 1  # 0.8----->即随机处理80%的输入图像
    erode_img(input_dir, filter, probability)