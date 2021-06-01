import cv2
import json
import os
import base64
import _io


def imgEncode(img_or_path):
    if isinstance(img_or_path,str):
        i = open(img_or_path,'rb')
    elif isinstance(img_or_path,_io.BufferedReader):
        i = img_or_path
    else:
        raise TypeError('Input type error!')
    
    base64_data = base64.b64encode(i.read())

    return base64_data.decode()

def rm(filepath):
    p = open(filepath,'r+')

    lines = p.readlines()

    d = ""
    for line in lines:
        c = line.replace('"group_id": "null",','"group_id": null,')

        d+=c
    
    p.seek(0)
    p.truncate()
    p.write(d)
    p.close()

def get_approx(img, contour, length_p=0.1):
    """获取逼近多边形

    :param img: 处理图片
    :param contour: 连通域
    :param length_p: 逼近长度百分比
    """
    img_adp = img.copy()
    # 逼近长度计算
    epsilon = length_p * cv2.arcLength(contour, True)
    # 获取逼近多边形
    approx = cv2.approxPolyDP(contour, epsilon, True)

    return approx

def test():
    img = "static/4.png"
    oriImg = "static/4.bmp"
    imgShape = cv2.imread(img).shape

    shapes = []

    imgray =cv2.imread(img,0)
    ret,img_bin = cv2.threshold(imgray,50,255,0)

    contours, hierarchy = cv2.findContours(img_bin,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


    for ii in range(len(contours)):

        region = get_approx(img_bin, contours[ii], 0.002)

        points = []
        
        for i in range(0,region.shape[0]):
            print(region[i][0])
            points.append(region[i][0].tolist())

        obj = dict()
        obj['version'] = '4.2.9'

        obj['flags'] = {}

        shape = dict()
        shape['label'] = '1'  #whatever other label
        shape['points'] = points
        shape['group_id']='null'
        shape['shape_type']='polygon'
        shape['flags']={}

        print(shape)
        shapes.append(shape)


    obj['shapes'] = shapes
    obj['imagePath'] = oriImg.split(os.sep)[-1]
    obj['imageData'] = str(imgEncode(oriImg))
    obj['imageHeight'] = imgShape[0]
    obj['imageWidth'] = imgShape[1]


    j = json.dumps(obj,sort_keys=True, indent=4)

    #print(j)

    with open('static/4.json','w') as f:
        f.write(j)

    
    rm('static/4.json')

            




if __name__ == "__main__":
    test()



