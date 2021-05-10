import os
import shutil
p = r'/home/adt/Desktop/json'
o_p = r'/home/adt/Desktop/16'
o_p_1 = r'/home/adt/Desktop/json'
for i in os.listdir(p):
    name = i.split('.json')[0]
    nn = '{}.jpg'.format(name)

    try:
        shutil.copy(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)