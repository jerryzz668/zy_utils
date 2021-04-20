import shutil
import json
import os
def get_bbox(points):
    x,y = zip(*points)
    return  max(x),max(y),min(x),min(y)
def parse_para(input_json):
    with open(input_json, 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)
    return ret_dic
def get_max_w_h(img_jsons,s):
    for i in os.listdir(img_jsons):
        if i.endswith('.json'):
            try:
                ret_dic = parse_para(os.path.join(img_jsons,i))
                shapes = ret_dic['shapes']
                img_name = ret_dic['imagePath']
                json_name = img_name.replace('.jpg','.json')
                for j in shapes:
                    label = j['label']
                    if not 'liangpin' in label:
                        if not 'moxing' in label :
                            shutil.move(os.path.join(img_jsons,img_name),os.path.join(s,img_name))#移动图像文件
                            shutil.move(os.path.join(img_jsons,json_name),os.path.join(s,json_name))#移动图像文件
                            break
            except:
                continue
    return 0
def save_json(dic,save_path):
    json.dump(dic, open(save_path, 'w',encoding='utf-8'), indent=4)
def get_max_w_h1(img_jsons,s,label_dic):
    for i in os.listdir(img_jsons):
        if i.endswith('.json'):
            ret_dic = parse_para(os.path.join(img_jsons,i))
            shapes = ret_dic['shapes']
            img_name = ret_dic['imagePath']
            for j in shapes:
                label = j['label']
                if label in label_dic:
                    j['label']=label_dic[label]
            save_json(ret_dic,os.path.join(s,i))
    return 0

img_jsons = '/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/NEWSTART/adcm/cemian/jsons'
save_p = '/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/NEWSTART/adcm/cemian/json'
label_dic = {'maoxu':'yiwu','baidian':'baisezaodian','3Daohen':'daowenxian','aotuhen':'yise','daowenxian':'guashang','shuiyin':'yise'}
get_max_w_h1(img_jsons,save_p,label_dic)
