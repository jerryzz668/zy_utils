import os
import shutil
p = r'/home/adt/data/data/Djian/yolo_gs_shy/images/train'
o_p = r'/home/adt/data/data/Djian/cemian_crop_qingxi/train_cemian_crop/select/crop'
o_p_1 = r'/home/adt/data/data/Djian/yolo_gs_shy/images/train'
for i in os.listdir(p):
    name = i.split('.jpg')[0]
    nn = '{}.json'.format(name)

    try:
        shutil.copy(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)