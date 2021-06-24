from utils import *


def labelme_to_yolo(img_folder_path):
    # 获得所有label并按字母排序
    cls = []
    print('Loading files...')
    for file in os.listdir(img_folder_path):
        if not file.endswith('.json'): continue
        instance = json_to_instance(os.path.join(img_folder_path, file))
        for obj in instance['shapes']:
            if obj['label'] not in cls:
                cls.append(obj['label'])
    cls = sorted(cls)
    print(cls)
    print('Start converting...')
    # 开始写入yolo txt
    img_files = os.listdir(img_folder_path)
    for img_file in img_files:
        img_file_path = os.path.join(img_folder_path, img_file)
        # 过滤文件夹和非图片文件
        if not os.path.isfile(img_file_path) or img_file_path[img_file_path.rindex('.') + 1:] not in IMG_TYPES: continue
        json_file_path = img_file_path[:img_file_path.rindex('.')] + '.json'
        txt_file_path = img_file_path[:img_file_path.rindex('.')] + '.txt'
        try:
            instance = json_to_instance(json_file_path)
        except FileNotFoundError:
            print('\033[1;33m%s has no json file in %s. So as an empty instance.\033[0m' % (img_file_path, img_folder_path))
            instance = create_empty_json_instance(img_file_path)
        with open(txt_file_path, 'w') as f:
            width, height = instance['imageWidth'], instance['imageHeight']
            for obj in instance['shapes']:
                x, y, w, h = points_to_xywh(obj)
                cx, cy = points_to_center(obj)
                box_info = "%d %.03f %.03f %.03f %.03f" % (cls.index(obj['label']), cx/width, cy/height, w/width, h/height)
                f.write(box_info)
                f.write('\n')
    print('Process finished!')


if __name__ == '__main__':
    # 图片文件夹绝对路径
    labelme_to_yolo(img_folder_path='/home/jerry/Documents/0425-now_loushi/labelme_crop')

