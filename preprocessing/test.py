# @Description:
# @Author     : zhangyan
# @Time       : 2020/12/30 2:20 下午


import os
import random

a = random.randint(3,10)
# print(a)
#
# print('\033[1;45m 字体不变色，有背景色 \033[0m')  # 有高亮

import os
import shutil
p = '/Users/zhangyan/Desktop/yichang'
o_p = '/Users/zhangyan/Desktop/a件_0830damian/0830damian_yolo/images/train/PR'
o_p_1 ='/Users/zhangyan/Desktop/yichang1'
for i in os.listdir(p):


    try:
        shutil.move(os.path.join(o_p,i),o_p_1)
    except:
        print(i)