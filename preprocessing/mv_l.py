import os
import shutil
p = r'C:\Users\Administrator\Desktop\heidian_crop_split(1)\heidian_crop_split\val\黑点-不确定'
o_p = r'C:\Users\Administrator\Desktop\heidian_crop_split\images\val'
o_p_1 = r'C:\Users\Administrator\Desktop\heidian_crop_split(1)\heidian_crop_split\val\黑点-不确定'
for i in os.listdir(p):
    name = i.split('.jpg')[0]
    nn = '{}.json'.format(name)

    try:
        shutil.copy(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)