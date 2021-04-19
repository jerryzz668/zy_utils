import os
import shutil
p = r'C:\Users\Administrator\Desktop\imgs\outputs'
o_p = r'C:\Users\Administrator\Desktop\imgs'
o_p_1 = r'C:\Users\Administrator\Desktop\img'
for i in os.listdir(p):
    name = i.split('.xml')[0]
    nn = '{}.jpg'.format(name)

    try:
        shutil.move(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)