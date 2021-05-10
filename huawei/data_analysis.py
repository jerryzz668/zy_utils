from preprocessing.utils import *


def objs_labels(json_folder_path):
    '''
    :param json_folder_path: labelme json文件夹
    :return: 显示所有label
    '''
    labels = []
    shape_types = []
    for json_file in os.listdir(json_folder_path):
        if not json_file.endswith('.json'): continue
        instance = json_to_instance(os.path.join(json_folder_path, json_file))
        for obj in instance['shapes']:
            label= obj['label']
            shape_type = obj['shape_type']
            if label not in labels: labels.append(label)
            if shape_type not in shape_types: shape_types.append(shape_type)
    print(labels)
    print(shape_types)

def objs_rm_prefixs(json_folder_path):
    '''
    :param json_folder_path: labelme json文件夹
    :return: 删除label的loushi_、cuowu_、hard_等前缀
    '''
    for json_file in os.listdir(json_folder_path):
        if not json_file.endswith('.json'): continue
        need = False
        json_file_path = os.path.join(json_folder_path, json_file)
        instance = json_to_instance(json_file_path)
        for obj in instance['shapes']:
            label= obj['label']
            if '_' in label and not label.startswith('guojian'):
                obj['label'] = label[label.rindex('_')+1:]
                print('Json file %s: from label %s to %s' % (json_file, label, obj['label']))
                need = True
        if need:
            instance_to_json(instance, json_file_path)

def objs_rm_guojian(json_folder_path):
    '''
    :param json_folder_path: labelme json文件夹
    :return: 删除guojian的obj
    '''
    for json_file in os.listdir(json_folder_path):
        if not json_file.endswith('.json'): continue
        need = False
        json_file_path = os.path.join(json_folder_path, json_file)
        instance = json_to_instance(json_file_path)
        for obj in instance['shapes'][:]:
            if obj['label'].startswith('guojian'):
                instance['shapes'].remove(obj)
                print('Json file %s: delete label %s' % (json_file, obj['label']))
                need = True
        if need:
            instance_to_json(instance, json_file_path)

def objs_statistic(json_folder_path):
    # 统计label
    cls_statistic = {}
    # 统计图片尺寸
    img_sizes = {}
    # 统计中心坐标分布
    locations = ([], [])
    for json_file in os.listdir(json_folder_path):
        if not json_file.endswith('.json'): continue
        instance = json_to_instance(os.path.join(json_folder_path, json_file))
        width, height = instance['imageWidth'], instance['imageHeight']
        if (width, height) not in img_sizes: img_sizes[(width, height)] = [instance['imagePath']]
        else: img_sizes[(width, height)].append(instance['imagePath'])
        for obj in instance['shapes']:
            label = obj['label']
            x, y, w, h = points_to_xywh(obj)
            locations[0].append(y+h/2)
            locations[1].append(x+w/2)
            if label not in cls_statistic: cls_statistic[label] = 1
            else: cls_statistic[label] += 1
    return cls_statistic, img_sizes, locations

if __name__ == '__main__':
    # 删除labelme json文件中的cuowu、loushi、hard前缀
    objs_rm_prefixs(json_folder_path=r'/Users/zhangyan/Desktop/loushi_guashang1')
    # 删除labelme json文件中的guojian前缀
    objs_rm_guojian(json_folder_path=r'/Users/zhangyan/Desktop/loushi_guashang1')
    # 显示labelme json文件夹中所有labels
    objs_labels(json_folder_path=r'/Users/zhangyan/Desktop/loushi_guashang1')




























