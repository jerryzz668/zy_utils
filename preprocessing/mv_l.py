import os
import shutil
p = '/home/jerry/data/kesen/31490/31490-guojian-0725/guosha-hy_empty_json'
o_p = '/home/jerry/data/kesen/31490/31490-guojian-0725/guosha-hy_crop'
o_p_1 = '/home/jerry/data/kesen/31490/31490-guojian-0725/guosha-hy_empty_json'
for i in os.listdir(p):
    name = i.split('.json')[0]
    nn = '{}.jpg'.format(name)

    try:
        shutil.move(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)
