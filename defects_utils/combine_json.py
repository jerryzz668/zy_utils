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

def compare_defect(json_file_path, json_to, defect_list):

    instancefrom = json_to_instance(json_file_path)
    shape_list = []
    have_defect = False
    for obj in instancefrom['shapes']:
        if (obj["label"] in defect_list):
            shape_list.append(obj)
            have_defect = True


    if have_defect == True:
        json_name = os.path.basename(json_file_path)
        json_to_path = os.path.join(json_to, json_name)
        instanceto = json_to_instance(json_to_path)

        for shape in shape_list:
            instanceto['shapes'].append(shape)

        instance_to_json(instanceto, json_to_path)

        print(json_to_path)


defect_list        = ['yisiliewen']
json_from          = '/home/kerry/mnt/mark/apple575/train_data/1217/lll/weixi_1217/'
json_to            = '/home/kerry/mnt/mark/apple575/train_data/1217/lll/xi_1217/'


json_list = glob.glob(json_from + '*.json')



for json_file_path in json_list:

    compare_defect(json_file_path, json_to, defect_list)