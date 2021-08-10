import os
import shutil
p = '/home/jerry/Documents/Micro_ADR/R78/daowen'
o_p = '/home/jerry/Documents/Micro_ADR/R78/physical_check'
o_p_1 = '/home/jerry/Documents/Micro_ADR/R78/daowen'
for i in os.listdir(p):
    name = i.split('.json')[0]
    nn = '{}.jpg'.format(name)

    try:
        shutil.copy(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)
