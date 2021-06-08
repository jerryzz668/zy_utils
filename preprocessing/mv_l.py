import os
import shutil
p = r'/home/jerry/Documents/yolov5-5.0/runs/detect/exp'
o_p = r'/home/jerry/Desktop/tianchi/Track3_helmet/labelme/labelme_json'
o_p_1 = r'/home/jerry/Documents/yolov5-5.0/runs/detect/exp'
for i in os.listdir(p):
    name = i.split('.jpg')[0]
    nn = '{}.json'.format(name)

    try:
        shutil.copy(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)
