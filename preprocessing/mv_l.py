import os
import shutil
p = '/Users/zhangyan/Desktop/exp'
o_p = '/Users/zhangyan/Desktop/a件_0830damian/crop'
o_p_1 ='/Users/zhangyan/Desktop/exp'
for i in os.listdir(p):
    name = i.split('.jpg')[0]
    nn = '{}.json'.format(name)

    try:
        shutil.copy(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)