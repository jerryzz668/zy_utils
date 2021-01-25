import os
import shutil
p = '/Users/zhangyan/Desktop/a件_0830damian/0830img/train/imgs'
o_p = '/Users/zhangyan/Desktop/label'
o_p_1 ='/Users/zhangyan/Desktop/labels'
for i in os.listdir(p):
    name = i.split('.jpg')[0]
    nn = '{}.txt'.format(name)

    try:
        shutil.move(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)