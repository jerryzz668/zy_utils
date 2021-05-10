import glob
import os
from shutil import copyfile

source_path = "/home/kerry/mnt/mark/apple575/train_data/1221/label_575_1221/"

wai_path = '/home/kerry/mnt/mark/apple575/train_data/1221/label_575_1221_wai/'
nei_path = '/home/kerry/mnt/mark/apple575/train_data/1221/label_575_1221_nei/'
pos_path = '/home/kerry/mnt/mark/apple575/train_data/1221/label_575_1221_pos/'
neg_path = '/home/kerry/mnt/mark/apple575/train_data/1221/label_575_1221_neg/'

if not os.path.exists(wai_path):
    os.makedirs(wai_path)
if not os.path.exists(nei_path):
    os.makedirs(nei_path)
if not os.path.exists(pos_path):
    os.makedirs(pos_path)
if not os.path.exists(neg_path):
    os.makedirs(neg_path)

img_list = glob.glob(source_path+"*.jpg")


for imgpath in img_list:
    imgName = os.path.basename(imgpath)
    jsonName = imgName.split('.')[0] + '.json'
    jsonpath = os.path.join(source_path, jsonName)


    imgto_wai = os.path.join(wai_path, imgName)
    jsonto_wai = os.path.join(wai_path, jsonName)

    imgto_nei = os.path.join(nei_path, imgName)
    jsonto_nei = os.path.join(nei_path, jsonName)

    imgto_pos = os.path.join(pos_path, imgName)
    jsonto_pos = os.path.join(pos_path, jsonName)

    imgto_neg = os.path.join(neg_path, imgName)
    jsonto_neg = os.path.join(neg_path, jsonName)

    flag_num = int(imgName.split('.')[0].split('-')[-1])

    if flag_num <= 2:

        copyfile(imgpath, imgto_neg)
        copyfile(jsonpath, jsonto_neg)

    elif flag_num <= 5:

        copyfile(imgpath, imgto_pos)
        copyfile(jsonpath, jsonto_pos)

    elif flag_num <= 15:
        copyfile(imgpath, imgto_wai)
        copyfile(jsonpath, jsonto_wai)
    else:
        copyfile(imgpath, imgto_nei)
        copyfile(jsonpath, jsonto_nei)



