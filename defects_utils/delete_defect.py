import json
import glob
import os

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

def cut_defect(json_file_path, defect_list, json_out_path):

    instance = json_to_instance(json_file_path)
    shape_list = []
    for obj in instance['shapes']:
        if (obj["label"]) in defect_list:
            shape_list.append(obj)
    instance['shapes'] = shape_list
    instance_to_json(instance, json_out_path)

defect_list         = ["guashang1"]

json_path           = '/Users/zhangyan/Desktop/guashang1/'
json_o_path         = '/Users/zhangyan/Desktop/json_guashang/'

if not os.path.exists(json_o_path):
    os.makedirs(json_o_path)
json_list = glob.glob(json_path + '*.json')

for json_file_path in json_list:
    json_name = os.path.basename(json_file_path)
    json_out_path = os.path.join(json_o_path , json_name)
    cut_defect(json_file_path, defect_list, json_out_path)