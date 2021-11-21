import json
import os
import sys

class Modify_COCO_Cate(object):
    def __init__(self, cz_coco, coco, save_coco):
        self.cz_coco = cz_coco  # 参照cocojson
        self.coco = coco  # 待修改的cocojson
        self.save_coco = save_coco  # 修改后的cocojson
        self.modify(cz_coco, coco, save_coco)

    def save_json(self, dic, save_path):
        json.dump(dic, open(save_path, 'w', encoding='utf-8'), indent=4)  # indent=4 更加美观显示

    def parse_para(self, input_json):
        with open(input_json, 'r', encoding='utf-8') as f:
            ret_dic = json.load(f)
        return ret_dic

    def modify(self, cz_json, coco_json, save_coco_json):
        cz_json_data = self.parse_para(cz_json)
        cz_categories = cz_json_data['categories']
        coco_json_data = self.parse_para(coco_json)
        coco_json_cate = coco_json_data['categories']
        save_coco_dic = {}
        cz_cate_dic = {}
        coco_id_2_id_cate_dic = {}
        for i in cz_categories:
            cate_name = i['supercategory']
            cate_id = i['id']
            cz_cate_dic[cate_name] = cate_id
        for i in coco_json_cate:
            coco_cate_id = i['id']
            coco_cate_name = i['supercategory']
            coco_id_2_id_cate_dic[coco_cate_id] = cz_cate_dic[coco_cate_name]

        coco_annotations = coco_json_data['annotations']
        save_coco_annotations = []
        for i in coco_annotations:
            i['category_id'] = coco_id_2_id_cate_dic[i['category_id']]
            save_coco_annotations.append(i)
        for i in range(len(save_coco_annotations)):
            save_coco_annotations[i]['id'] = i + 1
        save_coco_dic['images'] = coco_json_data['images']
        save_coco_dic['categories'] = cz_categories
        save_coco_dic['annotations'] = save_coco_annotations
        self.save_json(save_coco_dic, save_coco_json)

if __name__ == '__main__':
    cz_json = '/home/jerry/Documents/Micro_ADR/R78/coco_val.json'  # 参照cocojson
    coco_path = '/home/jerry/Documents/Micro_ADR/R78/coco_train.json'  # 待修改的cocojson
    save_json_path = os.path.join(os.path.dirname(sys.argv[1]), 'modified_coco.json')
    # Modify_COCO_Cate(cz_json, coco_path, save_json_path)
    Modify_COCO_Cate(sys.argv[1], sys.argv[2], save_json_path)
