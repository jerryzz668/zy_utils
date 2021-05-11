import json
import os
from labelme import utils
# label_dic = {'diaoqi': 1, 'pengshang': 2, 'guashang': 3, 'yise': 4, 'guoqie': 5, 'yiwu': 6, 'keli': 7, 'heidian': 8}
label_dic = {'a':1, 'aotuhen':2, 'aotuhen1':3, 'aotuhen2':4, 'baidian':5, 'bianxing':6, 'daowen':7, 'diaoqi':8, 'guashang':9, 'guoqie':10,
                 'heidian':11, 'jiaxi':12, 'keli':13, 'maoxu':14, 'pengshang':15, 'tabian':16, 'xianhen':17, 'yashang':18, 'yinglihen':19, 'yise':20, 'yiwu':21}

def ljq(input):
    json_file,r_label = input
    data = json.load(open(json_file,encoding='utf8'))
    img_shape = (data['imageWidth'],data['imageHeight'],data['imageDepth'])
    label_name_to_value = {"_background_": 0}  # 存储类别和索引的字典，这里添加了一个背景类
    for shape in sorted(data["shapes"], key=lambda x: x["label"]):
        label_name = shape["label"]
        label_name_to_value[label_name]=label_dic[label_name]
    try:
        lbl, _ = utils.shapes_to_label(
            img_shape, data["shapes"], label_name_to_value
        )
    except:
        print(json_file)

    label_names = [None] * (max(label_name_to_value.values()) + 1)
    for name, value in label_name_to_value.items():
        label_names[value] = name
    utils.lblsave(r_label, lbl)
    print('正在处理：',r_label,json_file)

import time
import multiprocessing
if __name__ == '__main__':
    jsonf1 = r"/Users/zhangyan/Desktop/crop/jsons"
    labelf1 = r"/Users/zhangyan/Desktop/train_mask"
    s = time.time()
    input_ts = []
    for i in os.listdir(jsonf1):
        json_p = os.path.join(jsonf1,i)
        if i.endswith('.json'):
            k = i.split('.json')[0]
            r_label = os.path.join(labelf1,k)
            input_ts.append((json_p,r_label))
    pool = multiprocessing.Pool(processes=16) # 创建进程个数
    start_time = time.time()
    pool.map(ljq,input_ts)
    print('run time:',time.time()-start_time)
    pool.close()
    pool.join()
