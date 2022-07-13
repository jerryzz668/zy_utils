import os
from preprocessing.zy_utils import json_to_instance, instance_to_json, make_dir

def get_max_w_h(img_jsons, s, label_dic):
    make_dir(s)
    for i in os.listdir(img_jsons):
        if i.endswith('.json'):
            ret_dic = json_to_instance(os.path.join(img_jsons, i))
            shapes = ret_dic['shapes']
            # img_name = ret_dic['imagePath']
            for j in shapes:
                label = j['label']
                if label in label_dic:
                    j['label'] = label_dic[label]
            instance_to_json(ret_dic, os.path.join(s, i))
    return 0

if __name__ == '__main__':
    # label_dic = {'loushi_jiaobuliang': 'jiaobuliang', 'hard_jiaobuliang': 'jiaobuliang', 'guojian_jiaobuliang': 'jiaobuliang'}
    label_dic = {'guashang-1': 'guashang'}

    img_jsons = '/home/jerry/Desktop/garbage/yolo_series/gs_data/gs-1'
    save_p = '/home/jerry/Desktop/garbage/yolo_series/gs_data/gs-1-1'  # Automatically create output folders

    get_max_w_h(img_jsons, save_p, label_dic)
