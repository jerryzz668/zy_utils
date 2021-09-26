import os
import json
import subprocess
import numpy as np
import pandas as pd
import glob
import pathlib
import random
from PIL import Image
import shutil


os.chdir(pathlib.Path(__file__).parent)

all_files = glob.glob("liangpin_v1/*.*")
img_files_new = []

for img_file in all_files:
    if '.json' in img_file: continue
    assert '.jpg' in img_file
    json_file = img_file.replace('.jpg', '.json')

    if json_file in all_files: 
        # print(json_file)
        continue

    img_files_new.append(img_file)

img_files_new.sort()
random.seed(1234)
random.shuffle(img_files_new)

train_files = img_files_new[:int(len(img_files_new) * 0.8)]
test_files = [_ for _ in img_files_new if _ not in train_files]

print(len(train_files))
print(len(test_files))

train_dic = json.load(open("annotations/instances_train2017.json"))
test_dic = json.load(open("annotations/instances_val2017.json"))

idx = 100000

print(len(train_dic['images']))
print(len(test_dic['images']))

for train_file in train_files:
    im = Image.open(train_file)
    assert im.width == 780
    assert im.height == 128

    train_dic['images'].append(
        {
            'height': im.height, 
            'width': im.width, 
            'id': idx, 
            'file_name': os.path.basename(train_file)
        }   
    )
    shutil.copy(train_file, "./train2017")
    idx += 1

for test_file in test_files:
    im = Image.open(test_file)
    assert im.width == 780
    assert im.height == 128

    test_dic['images'].append(
        {
            'height': im.height, 
            'width': im.width, 
            'id': idx, 
            'file_name': os.path.basename(test_file)
        }   
    )
    shutil.copy(test_file, "./val2017")
    idx += 1


print(len(train_dic['images']))
print(len(test_dic['images']))


with open("train_new.json", 'w') as fp:
    json.dump(train_dic, fp, indent=4, separators=(',', ': '))

with open("test_new.json", 'w') as fp:
    json.dump(test_dic, fp, indent=4, separators=(',', ': '))


