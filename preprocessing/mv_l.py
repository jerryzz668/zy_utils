import os
import shutil
p = r'C:\Users\Administrator\Desktop\all\pre_new1\dm'
o_p = r'C:\Users\Administrator\Desktop\all\pre_yolo\dm\jsons'
o_p_1 = r'C:\Users\Administrator\Desktop\zy_all\pre_yolo\dm'
for i in os.listdir(p):
    name = i.split('.json')[0]
    nn = '{}.json'.format(name)

    try:
        shutil.move(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)