# @Description:
# @Author     : zhangyan
# @Time       : 2020/12/30 2:20 下午


import os
import random
import time
import cv2
import shutil


path = '/Users/zhangyan/Desktop/crop'
filelist = os.listdir(path)
for file in filelist:
    if file.endswith('jpg'):
        img = cv2.imread(os.path.join(path, file))
        h, w, c =  img.shape
        print(h ,w, c)