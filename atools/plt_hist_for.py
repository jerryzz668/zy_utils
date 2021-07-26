import cv2
import os
import matplotlib.pyplot as plt
import numpy as np

path = '/Users/zhangyan/Desktop/huanxingdaowen50'
path_save = '/Users/zhangyan/Desktop/ball/'
filelist = os.listdir(path)
for file in filelist:
    img = cv2.imread(path + '/' + file, 0)
    img = img[1000:5000, 800:3500]

    a = plt.hist(img.ravel())  # 直方图
    b = a[0].tolist()
    index = b.index(max(b))  # 获取像素数量最多的数量值索引
    avg_piexl = a[1][index]  # 获取数量最多的像素值
    # print(avg_piexl)

    img = img - avg_piexl-5
    # img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    img = img.astype(np.uint8)
    img = cv2.resize(img, (128, 128))
    cv2.imwrite(path_save + file, img)
