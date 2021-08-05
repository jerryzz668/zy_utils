from preprocessing.zy_utils import *
from pathlib import Path

def yolo_to_labelme(yolo_folder_path: str, img_folder_path: str, item_name: str,json_path:str):
    '''
    :param yolo_folder_path: yolo文件夹路径
    :param img_folder_path: 图像文件夹绝对路径
    :param item_name: yolo文件中目标节点的name
    :return: yolo文件转换成labelme json放在图片路径下
    '''
    json_dir = Path(json_path)
    if not json_dir.exists():
        os.makedirs(json_path)
    img_files = os.listdir(img_folder_path)
    # 遍历img
    for img_file in img_files:
        img_file_path = os.path.join(img_folder_path, img_file)
        # 过滤文件夹和非图片文件
        if not os.path.isfile(img_file_path) or img_file[img_file.rindex('.')+1:] not in IMG_TYPES: continue
        # 对应的yolo文件
        yolo_file_path = os.path.join(yolo_folder_path, img_file[:img_file.rindex('.')]+'.txt')
        # 对应的json文件
        json_out_path = os.path.join(json_path, img_file[:img_file.rindex('.')]+'.json')

        instance = create_empty_json_instance(img_file_path)
        instance_to_json(instance, json_out_path)
        try:

            with open(yolo_file_path, 'r') as f:
                items = f.readlines()
        except:
            items = []
            print('no ci txt_file')
        height = instance['imageHeight']
        width = instance['imageWidth']
        # print(items)

        for item in items:
            item = item.strip('\n')
            print(item.split(' '))
            item = [eval(it) for it in item.split(' ') if it != '']
            obj = {'label': item_name[item[0]]}
            obj['shape_type'] = 'rectangle'
            obj['points'] = [[(item[1] - item[3] / 2) * width, (item[2] - item[4] / 2) * height], 
                             [(item[1] + item[3] / 2) * width, (item[2] + item[4] / 2) * height]]
            obj['score'] = item[5]
            instance['shapes'].append(obj)
        instance_to_json(instance, json_out_path)

def delete_json(img_folder_path: str):
    '''
    :param img_folder_path: 图像文件夹绝对路径
    :return: 删除该路径下所有json文件
    '''
    for file in os.listdir(img_folder_path):
        if file.endswith('.json'):
            os.remove(os.path.join(img_folder_path, file))

if __name__ == '__main__':
    # 填入yolo folder path
    yolo_to_labelme(yolo_folder_path='/home/jerry/Documents/yolov5-5.0/runs/detect/exp41/labels',  # txt路径

                   img_folder_path='/home/jerry/Documents/yolov5-5.0/runs/detect/exp41',  # 填入image folder path

                   item_name=['huashang', 'yashang'],  # 填入yolo文件中目标标签的name
                   json_path='/home/jerry/data/kesen/31490/31490-guojian-0725/hy_json')  # Automatically create output folders
