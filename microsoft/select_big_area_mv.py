import json
def count_guashang_size(points):
    x,y = zip(*points)
    #max_x,max_y,min_x,min_y = max(x),max(y),min(x),min(y)
    return  max(x),max(y),min(x),min(y)
def parse_para(input_json):
    with open(input_json, 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)
    return ret_dic
import os
import shutil
def get_max_w_h(img_jsons,label,size=(512,512)):
    print(img_jsons)
    for i in os.listdir(img_jsons):
        ret_dic = parse_para(os.path.join(img_jsons,i))
        shapes = ret_dic['shapes']
        img_name = ret_dic['imagePath']
        for j in shapes:
            if j['label'] in label:
                # print('label',label)
                max_x,max_y,min_x,min_y = count_guashang_size(j['points'])
                w,h = max_x-min_x,max_y-min_y
                shutil.move(os.path.join(img_jsons,i),os.path.join(big_jsons,i))
                break
                # if w>size[0] or h>size[1]:
                #     print('os.path.join(img_jsons,i):',os.path.join(img_jsons,i))
                #     shutil.move(os.path.join(img_jsons,i),os.path.join(big_jsons,i))
                #     break
    return 0

# label_l =['shahenyin', 'baisezaodian', 'shuiyin', 'aokeng', 'cashang', '3Daohen', 'daowenxian']
label_l = ['huanxingdaowen']
img_jsons = '/Users/zhangyan/Desktop/a件_0830damian/0830img/train/jsons'
big_jsons = '/Users/zhangyan/Desktop/yichu'
print('获取最大size:',get_max_w_h(img_jsons,label_l,(512,512)))

