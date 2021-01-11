import os
import shutil
p = '/Users/zhangyan/Desktop/val'
o_p = '/Users/zhangyan/Desktop/a件_0830damian/0830img/imgs'
o_p_1 ='/Users/zhangyan/Desktop/val_imgs'
for i in os.listdir(p):
    name = i.split('.json')[0]
    nn = '{}.jpg'.format(name)

    try:
        shutil.move(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)