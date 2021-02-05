import json
import glob
import os
from shutil import copyfile

def instance_to_json(instance, json_file_path: str):
    '''
    :param instance: json instance
    :param json_file_path: 保存为json的文件路径
    :return: 将json instance保存到相应文件路径
    '''
    with open(json_file_path, 'w', encoding='utf-8') as f:
        content = json.dumps(instance, ensure_ascii=False, indent=2)
        f.write(content)

def json_to_instance(json_file_path: str):
    '''
    :param json_file_path: json文件路径
    :return: json instance
    '''
    with open(json_file_path, 'r', encoding='utf-8') as f:
        instance = json.load(f)
    return instance

def compare_defect(json_file_path, json_path, defect_path, defect_list):

    instance = json_to_instance(json_file_path)

    json_name = os.path.basename(json_file_path)
    img_name = json_name.split('.')[0] + ".jpg"

    json_from = os.path.join(json_path, json_name)
    json_to = os.path.join(defect_path, json_name)

    img_from = os.path.join(json_path, img_name)
    img_to = os.path.join(defect_path, img_name)



    for obj in instance['shapes']:
        if (obj["label"] in defect_list):
            copyfile(json_from, json_to)
            copyfile(img_from, img_to)






defect_list         = ['liewen']
json_path           = '/home/kerry/mnt/mark/apple575/train_data/train_val_all/train/'
defect_path         = '/home/kerry/mnt/mark/apple575/train_data/train_val_all/liewen/'


json_list = glob.glob(json_path + '*.json')




for json_file_path in json_list:

    compare_defect(json_file_path, json_path, defect_path, defect_list)