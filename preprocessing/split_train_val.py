"""
@Description:
@Author     : zhangyan
@Time       : 2021/11/22 下午7:13
"""
import argparse
import os, sys
import random
import shutil, glob
from tqdm import tqdm
from preprocessing.zy_utils import make_dir2, make_dir3

parser = argparse.ArgumentParser()
parser.add_argument('input_dir', default='', type=str, help='input')
parser.add_argument('ratio', default=0.2, type=float, help='val_ratio')
parser.add_argument('coco_or_yolo', default='', type=str, help='dataset type')
args = parser.parse_args()

def split_train_val(input_dir, ratio, coco_or_yolo):
    output_path = os.path.join(os.path.dirname(input_dir), coco_or_yolo)    #移动到新的文件夹路径
    print(output_path)
    if coco_or_yolo == 'coco':  # 生成coco文件夹
        make_dir2(output_path, ['annotations', 'train2017', 'val2017'])
    elif coco_or_yolo == 'yolo':  # 生成yolo文件夹
        make_dir3(output_path, ['images', 'labels'], ['train', 'val'])

    img_path = glob.glob('{}/*.jpg'.format(input_dir))
    val_num = int(len(img_path)*ratio)  # 按照rate比例从文件夹中取一定数量图片
    val_sample = random.sample(img_path, val_num)  # 从img_path中随机选取val_num数量的样本图片
    train_sample = [i for i in img_path if i not in val_sample]

    for sample in tqdm(train_sample):
        json_path = sample[:sample.rindex('.')] + '.json'
        if coco_or_yolo == 'coco':
            shutil.copy(sample, os.path.join(output_path, 'train2017'))
            shutil.copy(json_path, os.path.join(output_path, 'train2017'))
        elif coco_or_yolo == 'yolo':
            shutil.copy(sample, os.path.join(output_path, 'images', 'train'))
            shutil.copy(json_path, os.path.join(output_path, 'images', 'train'))

    for sample in tqdm(val_sample):
        json_path = sample[:sample.rindex('.')] + '.json'
        if coco_or_yolo == 'coco':
            shutil.copy(sample, os.path.join(output_path, 'val2017'))
            shutil.copy(json_path, os.path.join(output_path, 'val2017'))
        elif coco_or_yolo == 'yolo':
            shutil.copy(sample, os.path.join(output_path, 'images', 'val'))
            shutil.copy(json_path, os.path.join(output_path, 'images', 'val'))

if __name__ == '__main__':

    # input_dir = '/home/jerry/Desktop/garbage/xxx'   #源图片文件夹路径
    # ratio = 0.2
    # coco_or_yolo = 'yolo'
    split_train_val(input_dir=args.input_dir, ratio=args.ratio, coco_or_yolo=args.coco_or_yolo)