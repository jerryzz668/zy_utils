import os
import shutil
p = '/Users/zhangyan/Desktop/defects/guashang1'
o_p = '/Users/zhangyan/Desktop/a件_0830damian/0830damian_yolo/labels/train'
o_p_1 ='/Users/zhangyan/Desktop/defects/guashang1'
for i in os.listdir(p):
    name = i.split('.json')[0]
    nn = '{}.txt'.format(name)

    try:
        shutil.copy(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)