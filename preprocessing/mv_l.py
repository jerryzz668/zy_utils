import os
import shutil
p = '/Users/zhangyan/Desktop/xml'
o_p = '/Users/zhangyan/Desktop/img'
o_p_1 ='/Users/zhangyan/Desktop/xmlxx'
for i in os.listdir(p):
    name = i.split('.xml')[0]
    nn = '{}.jpg'.format(name)

    try:
        shutil.move(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)