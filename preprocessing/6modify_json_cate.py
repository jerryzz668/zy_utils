import json
json_two = r'/Users/zhangyan/Desktop/annotations/instances_train2017.json'  # 模版
json_one = r'/Users/zhangyan/Desktop/annotations/instances_val2017.json'  # 需修改
def save_json(dic,save_path):
    json.dump(dic, open(save_path, 'w',encoding='utf-8'), indent=4)  # indent=4 更加美观显示
def parse_para(input_json):
    with open(input_json, 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)
    return ret_dic
json_1 = parse_para(json_one)
json_2 = parse_para(json_two)
json_1_cate = json_1['categories']
json_2_cate = json_2['categories']
dic_2_2_1 ={}
dic_1 ={}
dic_2 ={}
for i in json_2_cate:
    dic_2[i['supercategory']]=i['id']
print('json_1_cate_b',json_1_cate)
for i in json_1_cate:
    dic_1[i['id']]= dic_2[i['supercategory']]
    i['id']=dic_2[i['supercategory']]
json_1_annotations = json_1['annotations']
print('dic_1,',dic_1)
for i in json_1_annotations:
    i['category_id']=dic_1[i['category_id']]
print('json_1_cate',json_1_cate)
print('json_2_cate',json_2_cate)
save_json(json_1,r'/Users/zhangyan/Desktop/instances_val.json')  # 存储
label = []
for i in json_2_cate:
    label.append(i['supercategory'])
print(label)



