'''
@Description: TODO
@author: lijianqing
@date: 2020/12/14 16:39
@return
'''
import json
class MergeTestResult2coco(object):
    def __init__(self,test_result_json,test_coco_json,save_path='./260_test1225.json'):
        self.test_result_json = test_result_json
        self.test_coco_json = test_coco_json
        self.save_path = save_path
        coco_data = self.parse_para(test_coco_json)
        coco_data['annotations'] = self.parse_para(test_result_json)
        self.save_json(coco_data,self.save_path)
    def parse_para(self,input_json):
        with open(input_json, 'r', encoding='utf-8') as f:
            ret_dic = json.load(f)
        return ret_dic
    def save_json(self,dic,save_path):
        json.dump(dic, open(save_path, 'w',encoding='utf-8'), indent=4)

if __name__ == '__main__':
    MergeTestResult2coco('/home/lijq/data/A/380_r/cf380_damian.segm.json',
                         '/home/lijq/data/A/test_a_coco/coco_test_confirm/annotations/instances_test2017dm.json',
                         '/home/lijq/data/A/380_r/dm/htc380dm.json')


















