import os
import shutil
p = '/Users/zhangyan/Desktop/tmp/xml'
o_p = '/Users/zhangyan/Desktop/tmp/origin'
o_p_1 ='/Users/zhangyan/Desktop/tmp/img'
for i in os.listdir(p):
    name = i.split('.xml')[0]
    nn = '{}.jpg'.format(name)

    try:
        shutil.move(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)