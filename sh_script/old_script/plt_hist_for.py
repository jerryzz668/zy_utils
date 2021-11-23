import glob
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np

input_dir = '/home/jerry/Desktop/yinlihen_valset'
output_dir = '/Users/zhangyan/Desktop/ball'
filelist = glob.glob('{}/*.jpg'.format(input_dir))

for file in filelist:
    img = cv2.imread(file, 0)
    a = plt.hist(img.ravel())  # 直方图
    b = a[0].tolist()
    index = b.index(max(b))  # 获取像素数量最多的数量值索引
    avg_pixel = a[1][index]  # 获取数量最多的像素值
    print(avg_pixel)

    # img = img - avg_pixel-5
    img = img - 150
    # img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    img = img.astype(np.uint8)

    cv2.namedWindow('img', 0)
    cv2.imshow('img', img)
    cv2.waitKey(2000)
    # cv2.imwrite(os.path.join(output_dir, os.path.basename(input_dir)), img)
