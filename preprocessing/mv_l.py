import os
import shutil
p = '/home/jerry/Documents/yolov5-5.0/runs/detect/exp/labels'
o_p = '/home/jerry/Documents/yolov5-5.0/runs/detect/exp/jsons'
o_p_1 = '/home/jerry/Documents/yolov5-5.0/runs/detect/exp/jsons_select'
for i in os.listdir(p):
    name = i.split('.txt')[0]
    nn = '{}.json'.format(name)

    try:
        shutil.move(os.path.join(o_p,nn),o_p_1)
    except:
        print(nn)
