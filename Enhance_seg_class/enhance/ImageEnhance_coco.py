# -*- coding:UTF-8 -*-
import numpy as np
import cv2
import random
import os
import os.path as osp
import shutil
from enhance import sharpen_enhance,sp_noise_enhance,gasuss_noise_enhance,gamma_enhance,GaussianBlurring_enhance,equalizeHist_enhance,adaptivehistogram_enhance,Contrast_and_Brightness_enhance



def readImage_s(imgpath):
    img = cv2.imread(imgpath)
   
    return img

# def readImage(path):
#     img = cv2.imread(os.path.join(imgPath, path))
#     labelimg = cv2.imread(os.path.join(labelPath, path))
#
#     return img,labelimg

def writeImage_s(img, inputlabelName, imgName, outputlabelName):
    cv2.imwrite(imgName, img)
    shutil.copyfile(inputlabelName,outputlabelName)
    # cv2.imwrite(labelName, label)


def RandomSelectionFile(fileDir,rate=1):
    # 随机选择某些文件名字
        # pathDir = os.listdir(fileDir)    #取图片的原始路径
        filenumber=len(fileDir)
       #自定义抽取图片的比例，比方说100张抽10张，那就是0.1
        picknumber=int(filenumber*rate) #按照rate比例从文件夹中取一定数量图片
        sample = random.sample(fileDir, picknumber)  #随机选取picknumber数量的样本图片

        return sample
def ImageEnhance_seg(Fs_Root_path,sharpen=False,sp_noise=False,gasuss_noise=False,gamma=False,GaussianBlurring=False,equalizeHist=False,adaptivehistogram=False,Brightness=False):
    # imgDirPath=Fs_Root_path+"\\train_seg\\little_image"
    # labelDirPath=Fs_Root_path+"\\train_seg\\little_label"
    imgDirPath=Fs_Root_path+"/images/train/"
    labelDirPath=Fs_Root_path+"/labels/train/"
    imgFiles = sorted(os.listdir(imgDirPath))
    # labelFiles = sorted(os.listdir(labelDirPath))
    RandomImgFiles=RandomSelectionFile(imgFiles,1.0)
    for imgName in RandomImgFiles:
        imgPath=os.path.join(imgDirPath, imgName)
        labelme=imgName[:-4]+'.txt'
        labelPath=os.path.join(labelDirPath, labelme)
        img = readImage_s(imgPath)
        if sharpen:
            flag,sharpen_img=sharpen_enhance(img)
            sharpen_img_path = imgPath[:-4]+'_sharpen.jpg'
            sharpen_label_path = labelPath[:-4]+'_sharpen.txt'
            writeImage_s(sharpen_img,labelPath,sharpen_img_path,sharpen_label_path)
        if sp_noise:
            flag,sp_noise_img=sp_noise_enhance(img,0.015)
            sp_noise_img_path = imgPath[:-4]+'_sp_noise.jpg'
            sp_noise_label_path = labelPath[:-4]+'_sp_noise.txt'
            writeImage_s(sp_noise_img,labelPath,sp_noise_img_path,sp_noise_label_path)
        if gasuss_noise:
            flag,gasuss_noise_img=gasuss_noise_enhance(img)
            gasuss_noise_img_path = imgPath[:-4]+'_gasuss_noise.jpg'
            gasuss_noise_label_path = labelPath[:-4]+'_gasuss_noise.txt'
            writeImage_s(gasuss_noise_img,labelPath,gasuss_noise_img_path,gasuss_noise_label_path)
        # if gamma:
        #     flag,gamma_img= gamma_enhance(img,0,0.005)
        #     gamma_img_path = imgPath.split('.')[0]+'gamma.bmp'
        #     gamma_label_path = labelPath.split('.')[0]+'gamma.bmp'
        #     writeImage_s(gamma_img,label,gamma_img_path,gamma_label_path)
        if GaussianBlurring:
            flag,GaussianBlurring_img=GaussianBlurring_enhance(img,3)
            GaussianBlurring_img_path = imgPath[:-4]+'_GaussianBlurring.jpg'
            GaussianBlurring_label_path = labelPath[:-4]+'_GaussianBlurring.txt'
            writeImage_s(GaussianBlurring_img,labelPath,GaussianBlurring_img_path,GaussianBlurring_label_path)
        if equalizeHist:
            flag,equalizeHist_img=equalizeHist_enhance(img)
            equalizeHist_img_path = imgPath[:-4]+'_equalizeHist.jpg'
            equalizeHist_label_path = labelPath[:-4]+'_equalizeHist.txt'
            writeImage_s(equalizeHist_img,labelPath,equalizeHist_img_path,equalizeHist_label_path)
        if adaptivehistogram:
            flag,adaptivehistogram_img=adaptivehistogram_enhance(img)
            adaptivehistogram_img_path = imgPath[:-4]+'_adaptivehistogram.jpg'
            adaptivehistogram_label_path = labelPath[:-4]+'_adaptivehistogram.txt'
            writeImage_s(adaptivehistogram_img,labelPath,adaptivehistogram_img_path,adaptivehistogram_label_path)
        if Brightness:
            flag,Brightness_img=Contrast_and_Brightness_enhance(img,0.8,0.8)
            flag2,Brightness_img2=Contrast_and_Brightness_enhance(img,1.2,1.2)
            Brightness_img_path = imgPath[:-4]+'_brightness.jpg'
            Brightness_label_path = labelPath[:-4]+'_brightness.txt'
            Brightness_img_path2 = imgPath[:-4]+'_brightness2.jpg'
            Brightness_label_path2 = labelPath[:-4]+'_brightness2.txt'
            writeImage_s(Brightness_img,labelPath,Brightness_img_path,Brightness_label_path)
            writeImage_s(Brightness_img2,labelPath,Brightness_img_path2,Brightness_label_path2)








#使用示例
Fs_Root_path='/home/adt/Desktop/yolo_enhance'
ImageEnhance_seg(Fs_Root_path,sharpen=False,sp_noise=False,gasuss_noise=False,gamma=False,
GaussianBlurring=True,equalizeHist=False,adaptivehistogram=False,Brightness=False)
