"""
@Description:
@Author     : zhangyan
@Time       : 2021/9/29 上午11:20
"""
import glob
import os
import cv2 as cv
import random
from preprocessing.zy_utils import make_dir, instance_to_json, json_to_instance

def erode_demo(image):
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))  # 定义结构元素的形状和大小  内核形状：{矩形：MORPH_RECT，交叉形：MORPH_CROSS，椭圆形：MORPH_ELLIPSE}
    dst = cv.erode(image, kernel)  # 腐蚀操作
    return dst

def dilate_demo(image):
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))  # 定义结构元素的形状和大小  内核形状：{矩形：MORPH_RECT，交叉形：MORPH_CROSS，椭圆形：MORPH_ELLIPSE}
    dst = cv.dilate(image, kernel)  # 膨胀操作
    return dst

def modify_json_name(file, output_dir):
    json_file = file.split('.')[0] + '.json'
    instance = json_to_instance(json_file)
    modify_img_path = 'erode_' + os.path.basename(json_file)
    instance['imagePath'] = 'erode_' + os.path.basename(file)
    instance_to_json(instance, os.path.join(output_dir, modify_img_path))


def erode_img(input_dir, output_dir):
    make_dir(output_dir)
    file_list = glob.glob('{}/*.jpg'.format(input_dir))

    for file in file_list:
        p = random.random()
        if p < 1000/8500:
            img_name = os.path.basename(file)
            print('正在处理：', img_name)
            img = cv.imread(file)
            erode_img = erode_demo(img)
            cv.imwrite(os.path.join(output_dir, 'erode_' + img_name), erode_img)
            modify_json_name(file, output_dir)

if __name__ == '__main__':
    input_dir = '/home/jerry/Desktop/erode_test'
    output_dir = '/home/jerry/Desktop/erode_test_r'
    erode_img(input_dir, output_dir)