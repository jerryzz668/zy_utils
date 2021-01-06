import json
import os
import cv2
from shutil import copyfile
import glob


def make_points(line, imageHeight, imageWidth):

    x_center = float(line[1]) * imageWidth
    y_center = float(line[2]) * imageHeight
    w2 = float(line[3]) * imageWidth / 2
    h2 = float(line[4]) * imageHeight / 2


    x1 = x_center - w2
    y1 = y_center - h2

    x2 = x_center + w2
    y2 = y_center + h2

    points = [[x1, y1], [x2, y2]]

    return points


def make_shape(line, class_list, imageHeight, imageWidth):
    label = class_list[int(line[0])]
    points = make_points(line, imageHeight, imageWidth)

    shape = {}
    shape['width'] = 1
    shape['label'] = label
    shape['points'] = points
    shape['group_id'] = ""
    shape['shape_type'] = "rectangle"
    shape['flags'] = {}

    return shape

def make_class_list(classes_path):
    fc = open(classes_path)
    class_list = []
    for line in fc.readlines():
        line = line.strip()
        class_list.append(line)
    print(class_list)
    return class_list

def make_shapes(imageHeight, imageWidth, txtpath, class_list):

    ft = open(txtpath)
    shapes = []
    for line in ft.readlines():
        line = line.strip().split()
        shape = make_shape(line, class_list, imageHeight, imageWidth)
        shapes.append(shape)

    return shapes

def save_json(dic, save_path):
    json.dump(dic, open(save_path, 'w',encoding='utf-8'), indent=4)  # indent=4 更加美观显示

def make_json(txtpath, imgbasepath, jsonbasepath, classes_path):

    txtName = os.path.basename(txtpath)
    imgName = txtName.split(".")[0] + '.jpg'
    jsonName = txtName.split(".")[0] + '.json'
    imgpathfrom = os.path.join(imgbasepath, imgName)
    imgpathto = os.path.join(jsonbasepath, imgName)

    img = cv2.imread(imgpathfrom)

    imageHeight = img.shape[0]
    imageWidth = img.shape[1]
    imageDepth = img.shape[2]

    shapes = make_shapes(imageHeight, imageWidth, txtpath, classes_path)

    new_json = {}
    new_json['version'] = "4.5.6"
    new_json['flags'] = {}
    new_json['shapes'] = shapes
    new_json['imageData'] = None
    new_json['imageHeight'] = imageHeight
    new_json['imageWidth'] = imageWidth
    new_json['imageDepth'] = imageDepth
    new_json['imagePath'] = imgName


    save_json(new_json, os.path.join(jsonbasepath, jsonName))
    copyfile(imgpathfrom, imgpathto)




classes_path = '/home/kerry/project/model/modelDetect/data/result/apple601/2020_12_29_13_18_36/label/classes.txt'

imgbasepath = '/home/kerry/project/model/modelDetect/data/result/apple601/2020_12_29_13_18_36/source'
jsonbasepath = '/home/kerry/project/model/modelDetect/data/result/apple601/2020_12_29_13_18_36/json'
txtbasepath = '/home/kerry/project/model/modelDetect/data/result/apple601/2020_12_29_13_18_36/label/'

txtpath_list = glob.glob(txtbasepath + '*.txt')

class_list=make_class_list(classes_path)
for txtpath in txtpath_list:
    if txtpath == classes_path:
        continue
    print(txtpath)
    make_json(txtpath, imgbasepath, jsonbasepath, class_list)
