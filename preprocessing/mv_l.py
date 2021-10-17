import os
import shutil
p = '/home/jerry/data/Micro_A/A_loushi/combined/psbj/22'
o_p = '/home/jerry/data/Micro_A/A_loushi/combined/psbj/qj'
o_p_1 = '/home/jerry/data/Micro_A/A_loushi/combined/psbj/22'
for i in os.listdir(p):
    name = i.split('.jpg')[0]
    nn = '{}.json'.format(name)

    try:
        shutil.copy(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)
