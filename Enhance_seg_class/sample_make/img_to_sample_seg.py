# 制作训练样本、正样本、负样本
# #使用示例
# Sample（）制作训练样本、PosSample（）制作正样本、NegSample（）制作负样本；Fs_Root_path表示根目录
# Fs_Root_path='D:\\test'  表示根目录
# Sample(Fs_Root_path)  制作训练样本
# PosSample(Fs_Root_path)   制作正样本
# NegSample(Fs_Root_path)   制作负样本

import numpy as np
import cv2
import random
import os
import time 
import datetime
import os.path as osp

#根据原图和标签生成样本
def readImage_s(imgpath, labelPath):
    img = cv2.imread(imgpath)
    labelImg = cv2.imread(labelPath,cv2.IMREAD_GRAYSCALE)
    ret,graylabelImg = cv2.threshold(labelImg,50,255,cv2.THRESH_BINARY)
    return img, graylabelImg

def randomCrop_s(img, labelImg,threshold,width):
    #截图阈值    
    threshold = threshold
    start3 = time.clock()
    while True:
        random_x = random.randint(0, img.shape[1]-width-1)
        random_y = random.randint(0, img.shape[0]-width-1)
        patch = img[random_y:random_y+width, random_x:random_x+width, :]
        labelpatch = labelImg[random_y:random_y+width, random_x:random_x+width]
        end3 = time.clock()
        flag=0
        if (end3-start3)>2:
            flag=1
            return patch, labelpatch,flag
        elif np.sum(labelpatch[:,:] > 0) < threshold:
            continue
        else:
            return patch, labelpatch,flag

def writeImage_s(img, label, imgName, labelName):
    cv2.imwrite(imgName, img)
    cv2.imwrite(labelName, label)


def Sample_make(Fs_Root_path,Imgnumber=20,threshold=600):
    #截图个数
    patchPerImg = Imgnumber
    imgDirPath=Fs_Root_path+"\\image_huawei_AC_20201209"
    labelDirPath=Fs_Root_path+"\\label_huawei_AC_20201209"
    outimgDirPath=Fs_Root_path+"\\little_image_huawei_AC_20201209"
    outlabelDirPath=Fs_Root_path+"\\little_label_huawei_AC_20201209"
    if not osp.exists(outimgDirPath):
        os.mkdir(outimgDirPath)
    if not osp.exists(outlabelDirPath):
        os.mkdir(outlabelDirPath)
    imgFiles = sorted(os.listdir(imgDirPath))
    labelFiles = sorted(os.listdir(labelDirPath))
    
    for imgName, labelName in zip(imgFiles, labelFiles):
        imgPath=os.path.join(imgDirPath, imgName)
        labelPath=os.path.join(labelDirPath, imgName)
        img, label = readImage_s(imgPath, labelPath)
        if img is None or label is None:
            continue
        if img.shape[1]!=label.shape[1]:
            continue
        try:
            if img.shape[0]!=label.shape[0]:
                continue
        except:
            print("图像空")
        threshold2=threshold
        width=256
        for t in range(patchPerImg):
            print('processing ...:', imgPath)
            print("threshold",threshold2)
            try:
                patch_img, patch_label,flag = randomCrop_s(img, label,threshold2,width)
            except:
                print("没有label图")
            
            if flag==1:
                threshold2=threshold2*0.1
                continue


            patch_img_name = imgName.split('.')[0]+str(t)+'1.bmp'
            outimgPath=os.path.join(outimgDirPath, patch_img_name)
            patch_label_name = imgName.split('.')[0] + str(t) + '1_out2.bmp'
            outlabelPath=os.path.join(outimgDirPath, patch_label_name)
            writeImage_s(patch_img, patch_label, outimgPath, outlabelPath)


#根据结果图生成正样本
def readImage_p(imgpath, labelPath, SlabelPath):
    img = cv2.imread(imgpath)
    labelImg = cv2.imread(labelPath,0)
    ret,labelImg = cv2.threshold(labelImg,10,255,cv2.THRESH_BINARY)
    SlabelImg = cv2.imread(SlabelPath,0)
    ret,SImg = cv2.threshold(SlabelImg,10,255,cv2.THRESH_BINARY)
    return img, labelImg, SImg

def randomCrop_p(img, labelImg, Slabel,threshold,width):
    threshold = threshold
    start3 = time.clock()
    while True:
        random_x = random.randint(0, img.shape[1]-width-1)
        random_y = random.randint(0, img.shape[0]-width-1)
        patch = img[random_y:random_y+width, random_x:random_x+width, :]
        labelpatch = labelImg[random_y:random_y+width, random_x:random_x+width]
        Slabelpatch = Slabel[random_y:random_y+width, random_x:random_x+width]
        end3 = time.clock()
        flag=0
        # print('time:%s Seconds'%(end3-start3))
        if (end3-start3)>2:
            flag=1
            return patch, labelpatch, Slabelpatch,flag
        if np.sum(Slabelpatch[:,:] > 0) < threshold:
            continue
        else:
            return patch, labelpatch, Slabelpatch,flag

def writeImage_p(img, label, imgName, labelName):
    t_str=datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
    time_str=(t_str[:10]+'-'+t_str[11:13])
    imgName1=imgName[:-4]+'_'+time_str+imgName[-4:]
    # labelName=labelName[:-4]+'_'+time_str+labelName[-4:]
    labelName2=imgName[:-4]+'_'+time_str+"_OUT2"+imgName[-4:]
    cv2.imwrite(imgName1, img)
    cv2.imwrite(labelName2, label)


def PosSample_make(Fs_Root_path,ImgNumber=12,threshold=400,width=256):
    patchPerImg = ImgNumber
    er = 0
    outimgDirPath=Fs_Root_path+"\\little_image_huawei_AC_20201209_miss"
    outlabelDirPath=Fs_Root_path+"\\little_label_huawei_AC_20201209_miss"
    if not osp.exists(outimgDirPath):
        os.mkdir(outimgDirPath)
    if not osp.exists(outlabelDirPath):
        os.mkdir(outlabelDirPath)
    ResultimgDirPath=Fs_Root_path+'\\image_huawei_AC_20201209'
    ResultlabelDirPath=Fs_Root_path+'\\result_AC'
    SourcelabelDirPath=Fs_Root_path+'\\label_huawei_AC_20201209'
    RimgFiles = sorted(os.listdir(ResultimgDirPath))
    RlabelFiles = sorted(os.listdir(ResultlabelDirPath))
    #SimgFiles = sorted(os.listdir(SourceimgDirPath))
    SlabelFiles = sorted(os.listdir(SourcelabelDirPath))
    for RimgName, RlabelName,SlabelName in zip(RimgFiles, RlabelFiles,SlabelFiles):
        RimgPath=os.path.join(ResultimgDirPath,RimgName)
        RlabelPath=os.path.join(ResultlabelDirPath,RimgName)
        SlabelPath=os.path.join(SourcelabelDirPath,RimgName)
        Rimg, Rlabel, Slabel = readImage_p(RimgPath, RlabelPath, SlabelPath)
        if Rimg is None or Rlabel is None or Slabel is None :
            continue
        # if Rimg is None:
        #     continue
        # width=512
        for t in range(patchPerImg):
            print('processing ...:', RimgName)
            patch_img, patch_label, patch_Slabel,flag = randomCrop_p(Rimg, Rlabel, Slabel,threshold,width)
            if flag==1:
                continue
            resultimg = np.sum(patch_label[:,:] > 0)
            #print(source)
            # if(patch_label.shape!=patch_Slabel.shape):
            #     continue
            and_Img = cv2.bitwise_and(patch_label,patch_Slabel)
            numofand = np.sum(and_Img[:,:] > 0)
            or_Img = cv2.bitwise_or(patch_label, patch_Slabel)
            numofor = np.sum(or_Img[:,:] > 0)
            if resultimg == 0:
                label_name = RimgName.split('.')[0] + str(t) + '_emmiss1209.bmp'
                OutLabelPath=os.path.join(outlabelDirPath,label_name)
                label_name2 = RimgName.split('.')[0] + str(t) + '_emmiss1209_OUT2.bmp'
                OutLabelPath2=os.path.join(outimgDirPath,label_name2)
                img_name = RimgName.split('.')[0]+str(t)+'_emmiss1209.bmp'
                OutImgPath=os.path.join(outimgDirPath,img_name)
                writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
                er = er + 1
                continue
            point1 = numofand/resultimg
            #print(point1)
            point2 = numofor/resultimg
            #print(point2)
            # if point2 > 1.5:
            #     label_name = RimgName.split('.')[0] + str(t) + '_emmiss121.bmp'
            #     OutLabelPath=os.path.join(outlabelDirPath,label_name)
            #     img_name = RimgName.split('.')[0]+str(t)+'_emmiss121.bmp'
            #     OutImgPath=os.path.join(outimgDirPath,img_name)
            #     writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
            #     continue
            # # if point2 > 1.6:
            # #     label_name = SlabelName.split('.')[0] + str(t) + '_emmiss121.bmp'
            # #     OutLabelPath=os.path.join(outlabelDirPath,label_name)
            # #     img_name = RimgName.split('.')[0]+str(t)+'_emmiss121.bmp'
            # #     OutImgPath=os.path.join(outimgDirPath,img_name)
            # #     writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
            # #     continue
            if point1 < 0.2:
                label_name = SlabelName.split('.')[0] + str(t) + '_emmiss.bmp'
                OutLabelPath=os.path.join(outlabelDirPath,label_name)
                img_name = RimgName.split('.')[0]+str(t)+'_emmiss.bmp'
                OutImgPath=os.path.join(outimgDirPath,img_name)
                writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
                continue
            # # if point2 < 1.15 and point1 > 0.85:
            # #     label_name = SlabelName.split('.')[0] + str(t) + '_emmiss121.bmp'
            # #     OutLabelPath=os.path.join(outlabelDirPath,label_name)
            # #     img_name = RimgName.split('.')[0]+str(t)+'_emmiss121.bmp'
            # #     OutImgPath=os.path.join(outimgDirPath,img_name)
            # #     writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
            # #     continue
    print(er)


#根据结果图生成负样本
def readImage_n(path, labelPath, SlabelPath):
    img = cv2.imread(os.path.join(ResultimgDirPath, path))
    labelImg = cv2.imread(os.path.join(ResultlabelDirPath, labelPath),0)
    ret,labelImg = cv2.threshold(labelImg,10,255,cv2.THRESH_BINARY)
    SlabelImg = cv2.imread(os.path.join(SourcelabelDirPath, SlabelPath),0)
    ret,SImg = cv2.threshold(SlabelImg,10,255,cv2.THRESH_BINARY)
    return img, labelImg, SImg

def randomCrop_n(img, labelImg, Slabel,threshold,width):
    threshold = threshold
    start3 = time.clock()
    while True:
        random_x = random.randint(0, img.shape[1]-width-1)
        random_y = random.randint(0, img.shape[0]-width-1)
        patch = img[random_y:random_y+width, random_x:random_x+width, :]
        labelpatch = labelImg[random_y:random_y+width, random_x:random_x+width]
        Slabelpatch = Slabel[random_y:random_y+width, random_x:random_x+width]
        end3 = time.clock()
        
        # print('time:%s Seconds'%(end3-start3))
        if (end3-start3)>2:
            
            return patch, labelpatch, Slabelpatch
        if np.sum(labelpatch[:,:] > 0) < threshold:
            continue
        else:
            return patch, labelpatch, Slabelpatch

def writeImage_n(img, label, imgName, labelName):
    t_str=datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
    time_str=(t_str[:10]+'-'+t_str[11:13])
    imgName=imgName[:-4]+'_'+time_str+imgName[-4:]
    labelName=labelName[:-4]+'_'+time_str+labelName[-4:]
    cv2.imwrite(os.path.join(outImagePath, imgName), img)
    cv2.imwrite(os.path.join(outLabelPath, labelName), label)



def NegSample_make(Fs_Root_path,ImgNumber=12,threshold=100,width=256):
    ##over detect
    patchPerImg = ImgNumber
    er = 0
    outimgDirPath=Fs_Root_path+"\\little_image_huawei_384_all_over"
    outlabelDirPath=Fs_Root_path+"\\little_label_huawei_384_all_over"
    if not osp.exists(outimgDirPath):
        os.mkdir(outimgDirPath)
    if not osp.exists(outlabelDirPath):
        os.mkdir(outlabelDirPath)
    ResultimgDirPath=Fs_Root_path+'\\image_huawei2'
    ResultlabelDirPath=Fs_Root_path+'\\result'
    SourcelabelDirPath=Fs_Root_path+'\\label_huawei2'
    RimgFiles = sorted(os.listdir(ResultimgDirPath))
    RlabelFiles = sorted(os.listdir(ResultlabelDirPath))
    #SimgFiles = sorted(os.listdir(SourceimgDirPath))
    SlabelFiles = sorted(os.listdir(SourcelabelDirPath))
    for RimgName, RlabelName,SlabelName in zip(RimgFiles, RlabelFiles,SlabelFiles):
        RimgPath=os.path.join(ResultimgDirPath,RimgName)
        RlabelPath=os.path.join(ResultlabelDirPath,RimgName)
        SlabelPath=os.path.join(SourcelabelDirPath,RimgName)
        Rimg, Rlabel, Slabel = readImage_p(RimgPath, RlabelPath, SlabelPath)
        # width=256
        for t in range(patchPerImg):
            print('processing ...:', RimgName)
            patch_img, patch_label, patch_Slabel = randomCrop_n(Rimg, Rlabel, Slabel,threshold,width)
            # if flag==0:
            #     break
            resultimg = np.sum(patch_Slabel[:,:] > 0)
            #print(source)
            # if(patch_label.shape!=patch_Slabel.shape):
            #     continue
            and_Img = cv2.bitwise_and(patch_label,patch_Slabel)
            numofand = np.sum(and_Img[:,:] > 0)
            or_Img = cv2.bitwise_or(patch_label, patch_Slabel)
            numofor = np.sum(or_Img[:,:] > 0)
            if resultimg == 0:
                label_name = RimgName.split('.')[0] + str(t) + '_emneg211.bmp'
                OutLabelPath=os.path.join(outlabelDirPath,label_name)
                img_name = RimgName.split('.')[0]+str(t)+'_emneg211.bmp'
                OutImgPath=os.path.join(outimgDirPath,img_name)
                label_name2 = RimgName.split('.')[0] + str(t) + '_emneg211.bmp'
                OutLabelPath2=os.path.join(outimgDirPath,label_name2)
                writeImage_p(patch_img, patch_Slabel, OutImgPath,OutLabelPath)
                er = er + 1
                continue
            point1 = numofand/resultimg
            #print(point1)
            point2 = numofor/resultimg
            print(point2)
            # if point2 > 1.5:
            #     label_name = RimgName.split('.')[0] + str(t) + '_emneg211.bmp'
            #     OutLabelPath=os.path.join(outlabelDirPath,label_name)
            #     img_name = RimgName.split('.')[0]+str(t)+'_emneg211.bmp'
            #     OutImgPath=os.path.join(outimgDirPath,img_name)
            #     writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
            #     continue
            if point1 < 0.5:
                label_name = RimgName.split('.')[0] + str(t) + '_emneg211.bmp'
                OutLabelPath=os.path.join(outlabelDirPath,label_name)
                img_name = RimgName.split('.')[0]+str(t)+'_emneg211.bmp'
                OutImgPath=os.path.join(outimgDirPath,img_name)
                writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
                continue
            # if point1 >0.8 and point2<1.2:
            #     label_name = RimgName.split('.')[0] + str(t) + '_emneg211.bmp'
            #     OutLabelPath=os.path.join(outlabelDirPath,label_name)
            #     img_name = RimgName.split('.')[0]+str(t)+'_emneg211.bmp'
            #     OutImgPath=os.path.join(outimgDirPath,img_name)
            #     writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
            #     continue


    print(er)



def MakeSample(Fs_Root_path,Sample=False,PosSample=False,NegSample=False,
              Sample_Imgnumber=5,Sample_threshold=200,PosSample_ImgNumber=8,PosSample_threshold=40,NegSample_ImgNumber=2,NegSample_threshold=200):
    if Sample:
        Sample_make(Fs_Root_path,Sample_Imgnumber,Sample_threshold)
    if PosSample:
        width=256
        PosSample_make(Fs_Root_path,PosSample_ImgNumber,PosSample_threshold,width=width)
    if NegSample:
        width=256
        NegSample_make(Fs_Root_path,NegSample_ImgNumber,NegSample_threshold,width=width)

#使用示例
# Fs_Root_path表示根目录
# Sample:表示是否制作样本，True表示制作，False表示不制作，默认为不制作
# PosSample:表示是否制作正样本,True表示制作，False表示不制作，默认为不制作
# NegSample:表示是否制作负样本,True表示制作，False表示不制作，默认为不制作
# Sample_Imgnumber:一张图切成小图的数量  默认值：Sample_Imgnumber=20
# Sample_threshold：保存小图时,小图label图片上大于255的像素值的阈值 默认值 ：Sample_threshold=600
# PosSample_Imgnumber：制作正样本的数量  默认值：PosSample_Imgnumber=12
# PosSample_threshold：小图label图片上大于255的像素值的阈值 默认值：PosSample_threshold=400
# NegSample_ImgNumber：制作正样本的数量  默认值：NegSample_ImgNumber=12
# NegSample_threshold：小图result图片上大于255的像素值的阈值 默认值：NegSample_threshold=100
Fs_Root_path='G:\\huawei\\qingxi_shuju\\json_source\\wkx\\feiguaijiao\\'
Sample=False 
PosSample=True
NegSample=False
MakeSample(Fs_Root_path,Sample,PosSample,NegSample)


   
