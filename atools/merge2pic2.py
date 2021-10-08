'''
* @Description: TODO
* @author: lijianqing
* @date: 2021年09月07日 15:23
'''

# -*- coding:utf-8 -*-
from PIL import Image
import glob
import os
def blend_two_images():
    # path_dt = glob.glob(r'D:\work\data\R\34\3\ga\dt\*.jpg')
    # print('padt',path_dt)
    path_qx=glob.glob(r'D:\work\data\R\34\3\908blend\qx\*.jpg')
    path_dt=glob.glob(r'D:\work\data\R\34\3\908blend\dt\*.jpg')
    path_save = r'D:\work\data\R\34\3\908blend\ga\9'
    if not os.path.exists(path_save):
        os.makedirs(path_save)
    index = 1
    for i in path_qx:
        for j in path_dt:
            img1 = Image.open(i)
            img1 = img1.convert('RGBA')
            img2 = Image.open(j)
            img2 = img2.convert('RGBA')
            route = [Image.ROTATE_90,Image.ROTATE_180,Image.ROTATE_270]
            for k in route:
                index+=1
                dst2 = img2.transpose(k)
                dst1 = img1.transpose(k)
                img = Image.blend(dst2, dst1, 0.9)
                # img.show()
                img.save(os.path.join(path_save,"{}.png".format(index)))
    return
blend_two_images()
