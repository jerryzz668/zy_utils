# -*- coding: utf-8 -*-
import json
def count_guashang_size(points):
    x,y = zip(*points)
    #max_x,max_y,min_x,min_y = max(x),max(y),min(x),min(y)
    return  max(x),max(y),min(x),min(y)
def parse_para(input_json):
    with open(input_json, 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)
        # shapes = ret_dic['shapes']
        # img_name = ret_dic['imagePath']
    return ret_dic
import os
import shutil
def get_max_w_h(img_jsons,label,size=(512,512)):
    for i in os.listdir(img_jsons):
        ret_dic = parse_para(os.path.join(img_jsons,i))
        shapes = ret_dic['shapes']
        img_name = ret_dic['imagePath']
        for j in shapes:
            if j['label'] in label:
                print('label',label)
                max_x,max_y,min_x,min_y = count_guashang_size(j['points'])
                w,h = max_x-min_x,max_y-min_y
                if w>size[0] or h>size[1]:
                    print('os.path.join(img_jsons,i):',os.path.join(img_jsons,i))
                    shutil.move(os.path.join(img_jsons,i),os.path.join(more_jsons,i))
                    shutil.move(os.path.join(imgss,img_name),os.path.join(more_jsons,img_name))
                    break
                # else:
                #     shutil.copy(os.path.join(img_jsons,i),os.path.join(big_jsons,i))
                #     shutil.copy(os.path.join(imgss,img_name),os.path.join(big_jsons,img_name))
                # continue
    return 0
# label_l = ['yise', 'aotuhen', 'penshabujun', 'daowen', 'shahenyin', 'huanxingdaowen', 'mianhua','tabian']
# label_l = ['guashang', 'heidian', 'baisezaodian', 'yise', 'aotuhen', 'aokeng', 'cashang', 'shuiyin', 'pengshang', 'penshabujun', 'daowen', 'yiwu', 'shahenyin', 'huanxingdaowen', 'mianhua', 'tabian']
# label_l = ['guashang','yise','heidian']
# label_l =['heidian', 'guashang', 'yise', 'baisezaodian']
label_l = ['huanxingdaowen']
# img_jsons = r'D:\work\data\microsoft\damian\damian_source\1027data\classfile\ds\bd\les\jsons'
# imgss = r'D:\work\data\microsoft\damian\damian_source\1027data\classfile\ds\bd\les\imgs'
# big_jsons = r'D:\work\data\microsoft\damian\damian_source\1027data\classfile\ds\bd\les'
# more_jsons = r'D:\work\data\microsoft\damian\damian_source\1027data\classfile\ds\bd\big'
img_jsons = r'/Users/zhangyan/Desktop/a件_0830damian/0830img/train/imgs'
imgss = r'/Users/zhangyan/Desktop/a件_0830damian/0830img/train/imgs'
more_jsons = r'/Users/zhangyan/Desktop/huanxingdaowen'
print('获取最大size:',get_max_w_h(img_jsons,label_l,(512,512)))
