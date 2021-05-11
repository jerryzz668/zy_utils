import cv2
import torch
from torch.autograd import Variable
import numpy as np
import xlrd


def readImage_s(imgpath):
    img = cv2.imread(imgpath)
    # print(img)
    return img

def crop(img):
    # 裁剪
     index=0
     print(img.shape)
     image=[]
     col=int(img.shape[1]/512)
     row=int(img.shape[0]/512)
     print(col)
     for j in range(row):
         for i in range(col):
            index=index+1
            img2=img[j*512:j*512+512, i*512:i*512+512, :]
            image.append(img2)


    #  拼接
     imagecol=[]
     for j in range(row):
        for i in range(col-1):
            print(i)
            image2=image[0+j*col]
            image20=image[i+j*col]
            image21=image[i+1+j*col]
            image[0+j*col]=cv2.hconcat([image[0+j*col], image21])
            print(image[0].shape)
        imagecol.append(image[0+j*col])
        
     for j in range(row-1):
         image21=imagecol[j+1]
         imagecol[0]=cv2.vconcat([imagecol[0], image21])
     out_image_name_split = imgpath.split(".")[0] + "_"  + ".bmp"
     cv2.imwrite(out_image_name_split, imagecol[0])




def main(imgpath):
    img=readImage_s(imgpath)
    crop(img)

imgpath="D:\\ProjectMap\\jingdongfang\\bmp\\5.bmp"
main(imgpath)