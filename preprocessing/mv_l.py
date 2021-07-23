import os
import shutil
p = '/home/jerry/data/kesen/labelme_31490_hy/labelme_aug_train'
o_p = '/home/jerry/data/kesen/labelme_31490_hy/labelme_train'
o_p_1 = '/home/jerry/data/kesen/labelme_31490_hy/labelme_aug_train'
for i in os.listdir(p):
    name = i.split('.json')[0]
    nn = '{}.jpg'.format(name)

    try:
        shutil.copy(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)
