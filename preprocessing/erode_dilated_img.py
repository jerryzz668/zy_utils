"""
@Description:
@Author     : zhangyan
@Time       : 2021/9/29 上午11:20
"""
import glob
import os
import cv2 as cv
from pathlib import Path
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

# 图像亮度自适应增强(图像自动调亮)
def compute(img, min_percentile, max_percentile):
    """计算分位点，目的是去掉图1的直方图两头的异常情况"""
    max_percentile_pixel = np.percentile(img, max_percentile)
    min_percentile_pixel = np.percentile(img, min_percentile)
    return max_percentile_pixel, min_percentile_pixel

def get_lightness(src):
    # 计算亮度
    hsv_image = cv.cvtColor(src, cv.COLOR_BGR2HSV)
    lightness = hsv_image[:, :, 2].mean()
    return lightness

def adaptive_brightness(src):
    """图像亮度增强"""
    if get_lightness(src) > 130:
        print("图片亮度足够，不做增强")
    # 先计算分位点，去掉像素值中少数异常值，这个分位点可以自己配置。
    # 比如1中直方图的红色在0到255上都有值，但是实际上像素值主要在0到20内。
    max_percentile_pixel, min_percentile_pixel = compute(src, 1, 99)

    # 去掉分位值区间之外的值
    src[src >= max_percentile_pixel] = max_percentile_pixel
    src[src <= min_percentile_pixel] = min_percentile_pixel

    # 将分位值区间拉伸到0到255，这里取了255*0.1与255*0.9是因为可能会出现像素值溢出的情况，所以最好不要设置为0到255。
    out = np.zeros(src.shape, src.dtype)
    cv.normalize(src, out, 255 * 0.1, 255 * 0.9, cv.NORM_MINMAX)
    return out

def modify_json_name(file, write_img_name, output_dir):
    json_basename = os.path.basename(file)
    json_dirname = os.path.dirname(file)
    json_file = json_basename.split('.')[0] + '.json'
    instance = json_to_instance(os.path.join(json_dirname, json_file))
    modify_img_path = '{}'.format(write_img_name) + json_file
    instance['imagePath'] = '{}'.format(write_img_name) + os.path.basename(file)
    instance_to_json(instance, os.path.join(output_dir, modify_img_path))

def get_output_dir(input_dir, filter):
    output_dirname = os.path.dirname(input_dir)
    output_basename = os.path.basename(input_dir)
    write_img_name = str(filter).split('_')[-1].split(' ')[0] + '_'
    output_dir = os.path.join(output_dirname, '{}'.format(write_img_name) + output_basename)
    return output_dir

def erode_img(input_dir, filter, probability, rename):
    output_dir = get_output_dir(input_dir, filter)
    make_dir(output_dir)
    file_list = glob.glob('{}/*.jpg'.format(input_dir))

    for file in file_list:
        p = random.random()
        if p < probability:
            json_path = Path(file.split('.jpg')[0] + '.json')
            img_name = os.path.basename(file)
            if rename:
                write_img_name = str(filter).split('_')[-1].split(' ')[0] + '_'
            else:
                write_img_name = ''
            if json_path.exists():
                print('正在处理：{} and {}'.format(img_name, os.path.basename(json_path)))
                modify_json_name(file, write_img_name, output_dir)
            else:
                print('正在处理：', img_name)
            img = cv.imread(file)
            processed_img = filter(img)
            cv.imwrite(os.path.join(output_dir, '{}'.format(write_img_name) + img_name), processed_img, [int(cv.IMWRITE_JPEG_QUALITY), 95])

if __name__ == '__main__':
    input_dir = '/home/jerry/Desktop/garbage/111'  # 输入img和json // or only img // or img和部分json
    filter = adaptive_brightness  # 模式选择-----> demo_erode, demo_dilate, MORPH_OPEN, MORPH_CLOSE, MORPH_GRADIENT, MORPH_TOPHAT, MORPH_BLACKHAT, adaptive_brightness
    probability = 1  # 0.8----->即随机处理80%的输入图像
    erode_img(input_dir, filter, probability, rename=False)  # Automatically create output folders under the same path as input_dir