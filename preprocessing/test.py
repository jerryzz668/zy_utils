# @Description:
# @Author     : zhangyan
# @Time       : 2020/12/30 2:20 下午


import os
import random
import time
import cv2
import shutil
import glob

save_path = '/Users/zhangyan/Desktop/new_ja'
path = '/Users/zhangyan/Desktop/jalama'
filelist = os.listdir(path)
for file in filelist:
    if file.endswith('jpg'):
        img = cv2.imread(os.path.join(path, file))
        # h, w, c =  img.shape
        # if h > w:
        #     img = cv2.transpose(img)
        #     img = cv2.flip(img, 1)
        #     cv2.imwrite(os.path.join(save_path, file), img, 95.)
        # else:
        #     shutil.copy(os.path.join(path, file), save_path)
        # print(h ,w, c)
        a = random.randint()
