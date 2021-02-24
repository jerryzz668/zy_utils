# @Description:
# @Author     : zhangyan
# @Time       : 2020/12/30 2:20 下午


import os
import random
import time
import cv2
import shutil

a = random.randint(3,10)
# print(a)
#
# print('\033[1;45m 字体不变色，有背景色 \033[0m')  # 有高亮

save_path = '/Users/zhangyan/Desktop/img/'
img_path = '/Users/zhangyan/Desktop/crop'
# cemian = '/Users/zhangyan/Desktop/cemian'
filelist = os.listdir(img_path)
print(filelist)
for file in filelist:
    img = cv2.imread(os.path.join(img_path, file))
    h,w = img.shape[0],img.shape[1]
    if h ==8500 and w == 500:
        shutil.copy(os.path.join(img_path, file), save_path)

    # width = int(w/2)
    # height = int(h/2)
    # img1 = img[0:width, 0:height]
    # img2 = img[width:w, 0:height]
    # img3 = img[0:width, height:h]
    # img4 = img[width:w, height:h]
    # name = file.split('.')[0]
    # cv2.imwrite(save_path+name+'_1.jpg', img1)
    # cv2.imwrite(save_path+name+'_2.jpg', img2)
    # cv2.imwrite(save_path+name+'_3.jpg', img3)
    # cv2.imwrite(save_path+name+'_4.jpg', img4)

    print(file + 'has been cropped!')