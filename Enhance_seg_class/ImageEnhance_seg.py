# -*- coding:UTF-8 -*-
import numpy as np
import cv2
import random
import os
import os.path as osp
#图像锐化
def sharpen_enhance(img):
    flag=0
    if img is None:
        print('图像为空')
        return flag,img
    if len(img.shape)==2:
        flag=1
    if len(img.shape)==3:
        flag=3
    if img.sum()==0:
        print('warning:全为零')
        
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
    img = cv2.filter2D(img, -1, kernel=kernel)
    #print(img.shape)
    return flag,img


#椒盐噪声，prob:噪声比例
def sp_noise_enhance(img,prob=0.015):
    flag=0
    if img is None:
        print('图像为空')
        return flag,img
    if len(img.shape)==2:
        flag=1
    if len(img.shape)==3:
        flag=3
    if img.sum()==0:
        print('warning:全为零')
        
    output = np.zeros(img.shape,np.uint8)
    thres = 1 - prob
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = img[i][j]
    #print(output.shape)
    return flag,output


#高斯噪声，mean:均值，var:方差
def gasuss_noise_enhance(img, mean=0, var=0.001):
    flag=0
    if img is None:
        print('图像为空')
        return flag,img
    if len(img.shape)==2:
        flag=1
    if len(img.shape)==3:
        flag=3
    if img.sum()==0:
        print('warning:全为零')
        
    image = np.array(img/255, dtype=float)
    noise = np.random.normal(mean, var ** 0.5, image.shape)
    out = image + noise
    if out.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.
    out = np.clip(out, low_clip, 1.0)
    out = np.uint8(out*255)
    #print(out.shape)
    return flag,out


#伽马变换，c:倍数，v:指数
def gamma_enhance(img, c, v):
    flag=0
    if img is None:
        print('图像为空')
        return flag,img
    if len(img.shape)==2:
        flag=1
    if len(img.shape)==3:
        flag=3
    if img.sum()==0:
        print('warning:全为零')
        
    lut = np.zeros(256, dtype=np.float32)
    for i in range(256):
        lut[i] = c * i ** v
        if lut[i]>=254:
           lut[i]=254
    output_img = cv2.LUT(img, lut) #像素灰度值的映射
    output_img = np.uint8(output_img+0.5)  
    #print(output_img.shape)
    return flag,output_img



#高斯模糊，k:核的大小
def  GaussianBlurring_enhance(img,k):
    flag=0
    if img is None:
        print('图像为空')
        return flag,img
    if len(img.shape)==2:
        flag=1
    if len(img.shape)==3:
        flag=3
    if img.sum()==0:
        print('warning:全为零')
        
    img = cv2.GaussianBlur(img,(k,k),0)
    # print(img.shape)
    return flag,img



#直方图均衡
def equalizeHist_enhance(img):
    flag=0
    if img is None:
        print('图像为空')
        return flag,img
    if len(img.shape)==2:
        flag=1
    if len(img.shape)==3:
        flag=3
        print('图像为三通道')
        return flag,img
    if img.sum()==0:
        print('warning:全为零')
        
    equ = cv2.equalizeHist(img)
    print(equ.shape)
    return flag,equ




#自适应直方图均衡
def adaptivehistogram_enhance(img,clipLimit=2.0, tileGridSize=(8,8)):
    flag=0
    if img is None:
        print('图像为空')
        return flag,img
    if len(img.shape)==2:
        flag=1
    if len(img.shape)==3:
        flag=3
        print('图像为三通道')
        return flag,img
    if img.sum()==0:
        print('warning:全为零')
        
    clahe = cv2.createCLAHE(clipLimit, tileGridSize)
    cl1 = clahe.apply(img)
    
    return flag,cl1



#亮度变化，α调节对比度， β调节亮度 
def Contrast_and_Brightness_enhance(img, alpha, beta):
    flag=0
    if img is None:
        print('图像为空')
        return flag,img
    if len(img.shape)==2:
        flag=1
    if len(img.shape)==3:
        flag=3
    if img.sum()==0:
        print('warning:全为零')
        
    blank = np.zeros(img.shape, img.dtype)
    dst = cv2.addWeighted(img, alpha, blank, 1-alpha, beta)
    print(dst.shape)
    return flag,dst

def readImage_s(imgpath, labelPath):
    img = cv2.imread(imgpath)
    labelImg = cv2.imread(labelPath,cv2.IMREAD_GRAYSCALE)
    ret,graylabelImg = cv2.threshold(labelImg,10,255,cv2.THRESH_BINARY)
    return img, graylabelImg

def readImage(path):
    img = cv2.imread(os.path.join(imgPath, path))
    labelimg = cv2.imread(os.path.join(labelPath, path))

    return img,labelimg

def writeImage_s(img, label, imgName, labelName):
    cv2.imwrite(imgName, img)
    cv2.imwrite(labelName, label)

def RandomSelectionFile(fileDir,rate=0.3):
    # 随机选择某些文件名字
        # pathDir = os.listdir(fileDir)    #取图片的原始路径
        filenumber=len(fileDir)
       #自定义抽取图片的比例，比方说100张抽10张，那就是0.1
        picknumber=int(filenumber*rate) #按照rate比例从文件夹中取一定数量图片
        sample = random.sample(fileDir, picknumber)  #随机选取picknumber数量的样本图片

        return sample
def ImageEnhance_seg(Fs_Root_path,sharpen=False,sp_noise=False,gasuss_noise=False,gamma=False,GaussianBlurring=False,equalizeHist=False,adaptivehistogram=False):
    imgDirPath=Fs_Root_path+"\\train_seg\\little_image"
    labelDirPath=Fs_Root_path+"\\train_seg\\little_label"
    imgFiles = sorted(os.listdir(imgDirPath))
    labelFiles = sorted(os.listdir(labelDirPath))
    RandomImgFiles=RandomSelectionFile(imgFiles,0.2)
    for imgName in RandomImgFiles:
        imgPath=os.path.join(imgDirPath, imgName)
        labelPath=os.path.join(labelDirPath, imgName)
        img, label = readImage_s(imgPath, labelPath)
        if sharpen:
            flag,sharpen_img=sharpen_enhance(img)
            sharpen_img_path = imgPath.split('.')[0]+'sharpen.bmp'
            sharpen_label_path = labelPath.split('.')[0]+'sharpen.bmp'
            writeImage_s(sharpen_img,label,sharpen_img_path,sharpen_label_path)
        if sp_noise:
            flag,sp_noise_img=sp_noise_enhance(img,0.015)
            sp_noise_img_path = imgPath.split('.')[0]+'sp_noise.bmp'
            sp_noise_label_path = labelPath.split('.')[0]+'sp_noise.bmp'
            writeImage_s(sp_noise_img,label,sp_noise_img_path,sp_noise_label_path)
        if gasuss_noise:
            flag,gasuss_noise_img=gasuss_noise_enhance(img)
            gasuss_noise_img_path = imgPath.split('.')[0]+'gasuss_noise.bmp'
            gasuss_noise_label_path = labelPath.split('.')[0]+'gasuss_noise.bmp'
            writeImage_s(gasuss_noise_img,label,gasuss_noise_img_path,gasuss_noise_label_path)
        # if gamma:
        #     flag,gamma_img= gamma_enhance(img,0,0.005)
        #     gamma_img_path = imgPath.split('.')[0]+'gamma.bmp'
        #     gamma_label_path = labelPath.split('.')[0]+'gamma.bmp'
        #     writeImage_s(gamma_img,label,gamma_img_path,gamma_label_path)
        if GaussianBlurring:
            flag,GaussianBlurring_img=GaussianBlurring_enhance(img,9)
            GaussianBlurring_img_path = imgPath.split('.')[0]+'GaussianBlurring.bmp'
            GaussianBlurring_label_path = labelPath.split('.')[0]+'GaussianBlurring.bmp'
            writeImage_s(GaussianBlurring_img,label,GaussianBlurring_img_path,GaussianBlurring_label_path)
        if equalizeHist:
            flag,equalizeHist_img=equalizeHist_enhance(img)
            equalizeHist_img_path = imgPath.split('.')[0]+'equalizeHist.bmp'
            equalizeHist_label_path = labelPath.split('.')[0]+'equalizeHist.bmp'
            writeImage_s(equalizeHist_img,label,equalizeHist_img_path,equalizeHist_label_path)
        if adaptivehistogram:
            flag,adaptivehistogram_img=adaptivehistogram_enhance(img)
            adaptivehistogram_img_path = imgPath.split('.')[0]+'adaptivehistogram.bmp'
            adaptivehistogram_label_path = labelPath.split('.')[0]+'adaptivehistogram.bmp'
            writeImage_s(adaptivehistogram_img,label,adaptivehistogram_img_path,adaptivehistogram_label_path)








#使用示例
Fs_Root_path='D:\\test'
ImageEnhance_seg(Fs_Root_path,sharpen=False,sp_noise=False,gasuss_noise=False,gamma=True,GaussianBlurring=False,equalizeHist=False,adaptivehistogram=False)
