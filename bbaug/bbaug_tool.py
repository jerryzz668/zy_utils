from bbaug.policies import policies_zy
from bbaug.policies import policies_v3
from bbaug import policies
import json
import cv2
import glob
import numpy as np
import os
from tqdm import tqdm


label_dict = []


def init_policy() -> policies.PolicyContainer:
    return policies.PolicyContainer(policies_v3())


def data_prepare(img_file) -> tuple:
    img = cv2.imread(img_file)
    with open(img_file.replace('jpg', 'json'), 'r') as f:
        load_dict = json.load(f)
    labels = load_dict['shapes']
    bbox_list = []
    id_list = []
    for item in labels:
        try:
            id_list.append(label_dict.index(item['label']))
        except:
            id_list.append(len(label_dict))
            label_dict.append(item['label'])
        points = [list(map(int, pos)) for pos in np.array(item['points']).T]
        bbox_list.append([min(points[0]), min(points[1]), max(points[0]), max(points[1])])
    return img, bbox_list, id_list


def aug_process(work_dir, out_dir, EXPAND_FACTOR):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    policy_container = init_policy()
    img_list = glob.glob(os.path.join(work_dir, '*.jpg'))
    for img_item in tqdm(img_list):
        if not os.path.exists(img_item.replace('jpg', 'json')):
            print('Warning: {} does not have corresponding json file.'.format(img_item))
            continue
        img, bbox_list, id_list = data_prepare(img_item)
        for index in range(EXPAND_FACTOR):
            random_policy = policy_container.select_random_policy()
            img_aug, bbs_aug = policy_container.apply_augmentation(random_policy, img, bbox_list, id_list)
            img_name = os.path.basename(img_item)
            cv2.imwrite(os.path.join(out_dir, img_name.replace('.jpg', '_{}.jpg'.format(index))), img_aug,
                        [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            bbs_aug = [list(map(int, bb_aug_item)) for bb_aug_item in bbs_aug]
            shapes = [{'shape_type': 'rectangle', 'label': label_dict[bb_item[0]],
                       'points': [[bb_item[1], bb_item[2]], [bb_item[3], bb_item[4]]]} for bb_item in bbs_aug]
            img_size = img_aug.shape
            img_size = {'width': img_size[1], 'height': img_size[0], 'depth': img_size[2]}
            label_json = gen_labelme_json_model(img_size, img_name.replace('.jpg', '_{}.jpg'.format(index)))
            label_json['shapes'] = shapes
            with open(os.path.join(out_dir, img_name.replace('.jpg', '_{}.json'.format(index))), 'w',
                      encoding='utf-8') as out_file:
                json.dump(label_json, out_file, ensure_ascii=False, indent=2)


def gen_labelme_json_model(img_size, img_path) -> dict:
    instance = {'version': '1.0',
                'shapes': [],
                'imageData': None,
                'imageWidth': img_size.get('width') if isinstance(img_size, dict) else None,
                'imageHeight': img_size.get('height') if isinstance(img_size, dict) else None,
                'imageDepth': img_size.get('depth') if isinstance(img_size, dict) else None,
                'imagePath': img_path}
    return instance


if __name__ == '__main__':
    input_dir = '/home/jerry/data/Micro_D/D_loushi/11-24ceshijieguo/jiaodaowen_crop2048'  # input img and jsons
    EXPAND_FACTOR = 7
    aug_process(input_dir, '{}_bbaug'.format(input_dir), EXPAND_FACTOR)
