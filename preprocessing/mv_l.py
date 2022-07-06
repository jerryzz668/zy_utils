import os
import shutil
p = '/home/jerry/Desktop/garbage/2022-05-15_143047/loushi'
o_p = '/home/jerry/data/Micro_R/R/gs/05-15-gs-loushi/05-15-gs-loushi-z-almost_ori_data/05-15-gs-loushi-labelme-filter'
o_p_1 = '/home/jerry/Desktop/garbage/2022-05-15_143047/loushi'
for i in os.listdir(p):
    name = i.split('.csv')[0]
    nn = '{}.jpg'.format(name)

    try:
        shutil.copy(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)
