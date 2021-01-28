import os
import shutil
p = '/Users/zhangyan/Desktop/yichang'
o_p = '/Users/zhangyan/Desktop/a件_0830damian/0830damian_yolo/images/train/PR'
o_p_1 ='/Users/zhangyan/Desktop/yichang1'
for i in os.listdir(p):
    name = i.split('.jpg')[0]
    nn = '{}.json'.format(name)

    try:
        shutil.copy(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)