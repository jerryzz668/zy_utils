import glob
from preprocessing.zy_utils import *

def cut_defect(json_file_path, defect_list, json_out_path):
    shape_list = []
    instance = json_to_instance(json_file_path)

    for obj in instance['shapes']:
        if (obj["label"]) in defect_list:
            shape_list.append(obj)
    instance['shapes'] = shape_list
    instance_to_json(instance, json_out_path)

def cut_defects(json_path, defect_list, json_o_path):
    make_dir(json_o_path)
    json_list = glob.glob('{}/*.json'.format(json_path))

    for json_file_path in json_list:
        json_name = os.path.basename(json_file_path)
        json_out_path = os.path.join(json_o_path , json_name)
        cut_defect(json_file_path, defect_list, json_out_path)

if __name__ == '__main__':

    defect_list = ['pengshang']  # 需要保留的缺陷

    json_path = '/home/jerry/Desktop/test'  # input json path
    json_o_path = '/home/jerry/Desktop/test_modify'  # output json path & Automatically create folders

    cut_defects(json_path, defect_list, json_o_path)