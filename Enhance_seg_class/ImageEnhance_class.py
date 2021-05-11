# -*- coding:UTF-8 -*-
import numpy as np
import cv2
import random
import os
import os.path as osp
from enhance import sharpen_enhance,sp_noise_enhance,gasuss_noise_enhance,gamma_enhance,GaussianBlurring_enhance,equalizeHist_enhance,adaptivehistogram_enhance,Contrast_and_Brightness_enhance



def readImage_c(imgpath):
    img = cv2.imread(imgpath)
    return img

def readImage(path):
    img = cv2.imread(os.path.join(imgPath, path))
    return img

def writeImage_c(img, imgName):
    cv2.imwrite(imgName, img)

def RandomSelectionFile(fileDir,rate=0.3):
    # 随机选择某些文件名字
        # pathDir = os.listdir(fileDir)    #取图片的原始路径
        filenumber=len(fileDir)
       #自定义抽取图片的比例，比方说100张抽10张，那就是0.1
        picknumber=int(filenumber*rate) #按照rate比例从文件夹中取一定数量图片
        sample = random.sample(fileDir, picknumber)  #随机选取picknumber数量的样本图片

        return sample
def ImageEnhance_class(Fs_Root_path,sharpen=False,sp_noise=False,gasuss_noise=False,gamma=False,GaussianBlurring=False,equalizeHist=False,adaptivehistogram=False):
    imgDirPath=Fs_Root_path+"\\train_class\\little_image"
    imgFiles = sorted(os.listdir(imgDirPath))
    RandomImgFiles=RandomSelectionFile(imgFiles,0.2)
    for imgName in RandomImgFiles:
        imgPath=os.path.join(imgDirPath, imgName)
        img = readImage_c(imgPath)
        if sharpen:
            flag,sharpen_img=sharpen_enhance(img)
            sharpen_img_path = imgPath[:-4]+'_sharpen.bmp'
            print(sharpen_img_path)
            writeImage_c(sharpen_img,sharpen_img_path)
        if sp_noise:
            flag,sp_noise_img=sp_noise_enhance(img,0.015)
            sp_noise_img_path = imgPath[:-4]+'_sp_noise.bmp'
            writeImage_c(sp_noise_img,sp_noise_img_path)
        if gasuss_noise:
            flag,gasuss_noise_img=gasuss_noise_enhance(img)
            gasuss_noise_img_path = imgPath[:-4]+'_gasuss_noise.bmp'
            writeImage_c(gasuss_noise_img,gasuss_noise_img_path)
        # if gamma:
        #     flag,gamma_img= gamma_enhance(img,0,0.005)
        #     gamma_img_path = imgPath.split('.')[0]+'gamma.bmp'
        #     gamma_label_path = labelPath.split('.')[0]+'gamma.bmp'
        #     writeImage_s(gamma_img,label,gamma_img_path,gamma_label_path)
        if GaussianBlurring:
            flag,GaussianBlurring_img=GaussianBlurring_enhance(img,9)
            GaussianBlurring_img_path = imgPath[:-4]+'_GaussianBlurring.bmp'
            writeImage_c(GaussianBlurring_img,GaussianBlurring_img_path)
        if equalizeHist:
            flag,equalizeHist_img=equalizeHist_enhance(img)
            equalizeHist_img_path = imgPath[:-4]+'_equalizeHist.bmp'
            writeImage_c(equalizeHist_img,equalizeHist_img_path)
        if adaptivehistogram:
            flag,adaptivehistogram_img=adaptivehistogram_enhance(img)
            adaptivehistogram_img_path = imgPath[:-4]+'_adaptivehistogram.bmp'
            writeImage_c(adaptivehistogram_img,adaptivehistogram_img_path)








#使用示例
Fs_Root_path='C:\\Users\\xinghe.zhou\\Desktop\\dir_img'
ImageEnhance_class(Fs_Root_path,sharpen=True,sp_noise=True,gasuss_noise=True,
gamma=True,GaussianBlurring=True,equalizeHist=True,adaptivehistogram=True)
