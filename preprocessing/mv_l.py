import os
import shutil
p = r'/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/Anew/all/outputcm'
o_p = r'/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/Anew/all/origin'
o_p_1 = r'/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/Anew/all/origincm'
for i in os.listdir(p):
    name = i.split('.xml')[0]
    nn = '{}.jpg'.format(name)

    try:
        shutil.copy(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)