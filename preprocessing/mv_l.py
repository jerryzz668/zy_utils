import os
import shutil
p = '/home/jerry/data/Micro_AD/A_loushi/labeled/Ajian-2021-11-11-loushi_r/labelme_yin'
o_p = '/home/jerry/data/Micro_AD/A_loushi/labeled/Ajian-2021-11-11-loushi_r/labelme'
o_p_1 = '/home/jerry/data/Micro_AD/A_loushi/labeled/Ajian-2021-11-11-loushi_r/labelme_yin'
for i in os.listdir(p):
    name = i.split('.jpg')[0]
    nn = '{}.json'.format(name)

    try:
        shutil.copy(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)
