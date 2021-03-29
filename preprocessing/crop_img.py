# @Description:
# @Author     : zhangyan
# @Time       : 2021/2/27 12:24 PM

import os
import time
import cv2
import numpy as np

def crop_image(src, rownum, colnum, dstpath):
    img = cv2.imread(src)
    w, h = img.shape[1], img.shape[0]
    if rownum <= h and colnum <= w:

        s = os.path.split(src)
        print('Original image info: %s, %sx%s' % (s[-1], w, h))
        # print(s)
        if dstpath == '':
            dstpath = s[0]
        fn = s[1].split('.')
        basename = fn[0]
        ext = fn[-1]

        num = 0
        rowheight = h // rownum
        colwidth = w // colnum
        for r in range(rownum):
            for c in range(colnum):
                cv2.imwrite(os.path.join(dstpath, basename + '_' + str(num) + '.' + ext), img[r * rowheight:(r + 1) * rowheight, c * colwidth:(c + 1) * colwidth])
                num = num + 1
    else:
        print('不合法的行列切割参数！')

def crop_images(img_path, rownum, colnum, dstpath):
    if not os.path.exists(dstpath): os.mkdir(dstpath)
    img_list = os.listdir(img_path)
    t0 = time.time()
    for img in img_list:
        crop_image(os.path.join(img_path, img), rownum, colnum, dstpath)
    t1 = time.time()
    print('time:', t1-t0)

def jigsaw(jig_img_path, rownum, colnum, save_path):
    img_jig_list = os.listdir(save_path)
    img_jig_len = len(img_jig_list)
    # img_num = rownum*colnum
    for i in range(img_jig_len):
        img_jig_list[i] = img_jig_list[i].split('_')[0] + '.' + img_jig_list[i].split('.')[-1]
    img_jig_list = list(set(img_jig_list))
    # print(img_jig_list)
    for img_jig in img_jig_list:
        img_row = []
        img_col = []
        num = rownum * colnum
        img_first = img_jig.split('.')[0] + '_0.' + img_jig.split('.')[-1]
        # print(img_name)
        img1 = cv2.imread(os.path.join(save_path, img_first))
        h, w, c = img1.shape

        img_vertical_white = np.zeros((h,5,3))
        img_horizontal_white = np.zeros((5, rownum*w+5, 3))
        img_vertical_white = np.uint8(np.asarray(img_vertical_white))
        img_horizontal_white = np.uint8(np.asarray(img_horizontal_white))

        img1 = np.hstack((img1, img_vertical_white))
        # cv2.imshow('img',img)
        # cv2.waitKey()

        for i in range(rownum):
            for j in range(colnum):
                img_name = img_jig.split('.')[0] + '_{}.'.format(i+j) + img_jig.split('.')[-1]
                # print(img_name)
                img = cv2.imread(os.path.join(save_path, img_name))
                img_row.append(img)
            img_col.append(img_row)
        # print(np.array(img_col).shape)



if __name__ == '__main__':
    img_path = r'C:\Users\Administrator\Desktop\1'  # img文件夹路径
    save_path = r'C:\Users\Administrator\Desktop\crop_result'  # 保存路径
    # crop_images(img_path, 2, 2, save_path)
    jigsaw(jig_img_path=None, rownum=2, colnum=2, save_path=save_path)
