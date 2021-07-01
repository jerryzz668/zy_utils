"""
description: 把现场给的csv文件中bbox和cate画到img上
author: zhangyan
date: 2021-03-31 17:36
"""

import pandas as pd
import numpy as np
import os
import cv2
from preprocessing.zy_utils import make_dir

def draw_rec_text(csv_path, imgs_path, img_save_path):
    make_dir(img_save_path)
    data = pd.read_csv(csv_path)
    data = data.iloc[:,[1,3,4,5,6,7,8,9]]
    data = np.array(data)
    class_mapper = {
        '0': 'guashang','1': 'yise','2': 'shuiyin','3': 'pengshang','4': 'aokeng','5': 'cashang','6': 'daowen','7':'heidian',
        '8': 'baisezaodian', '9': 'yiwu', '10': 'shahenyin', '11': 'penshaobujun', '12': 'mianhua', '13':'aotuhen', '14': 'tabian', '15':'huanxingdaowen'
    }
    color_mapper = {
        '0': (152, 0, 0),'1': (255, 0, 0),'2': (255, 153, 0),'3': (255, 255, 0),'4': (0, 255, 0),'5': (0, 255, 255),'6': (74, 134, 232),'7':(0, 0, 255),
        '8': (153, 0, 255), '9': (255, 0, 255), '10': (241, 194, 50), '11': (69, 129, 142), '12': (61, 133, 198), '13': (166, 77, 121), '14': (102, 0, 0), '15': (127, 96, 0),
        '16': (39, 78, 19), '17': (12, 52, 61), '18': (28, 69, 135), '19': (7, 55, 99), '20': (32, 18, 77), '21': (76, 17, 48)
    }

    for i in range(len(data)):
        a1, a2, a3, cate = "%04d" % data[i][0], "%04d" % data[i][1], "%02d" % data[i][2], data[i][3]
        x, y, w, h = data[i][4], data[i][5], data[i][6],data[i][7]
        # print(a1, a2, a3, cate,x,y,w,h)
        img_name = a1 + '-' + a2 + '-' + a3 + '.jpg'
        img_path = os.path.join(imgs_path, img_name)
        img = cv2.imread(img_path)

        ptlefttop = (x,y)
        ptrightbottom = (x+w, y+h)
        point_color = color_mapper.get(str(cate))
        # point_color = cate
        thickness = 2
        lineType = 4
        cv2.rectangle(img, ptlefttop, ptrightbottom, point_color, thickness, lineType)

        text = class_mapper.get(str(cate))
        img = cv2.putText(img, text, (x,y), cv2.FONT_ITALIC, 2, (100,200,200), 2)

        cv2.imwrite(os.path.join(img_save_path, img_name), img)
        print(img_path + ' has been drawn(｡ì_í｡)')

if __name__ == '__main__':
    csv_path = r'C:\Users\Administrator\Desktop\ProductGradeMaterialChecks.csv'  # path to csv
    imgs_path = r'C:\Users\Administrator\Desktop\aa'  # path to imgs
    img_save_path = r'C:\Users\Administrator\Desktop\aaa'  # automatically create a saved folder
    draw_rec_text(csv_path, imgs_path, img_save_path)