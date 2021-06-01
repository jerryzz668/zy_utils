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
def getRoiImage(img,label,Roi_y=0,Roi_x=0,Roi_height=200,Roi_width=200):
    RoiImg=img[Roi_y:Roi_y+Roi_height,Roi_x:Roi_x+Roi_width]
    RoiLabel=label[Roi_y:Roi_y+Roi_height,Roi_x:Roi_x+Roi_width]
    return RoiImg,RoiLabel
def randomCrop_s(img, labelImg,threshold,SampleSize=256):
    #截图阈值   
    if  img.shape[0]<SampleSize+4 or img.shape[1]<SampleSize+4:
        return -1
    threshold = threshold
    start3 = time.clock()
    while True:
        random_x = random.randint(0, img.shape[1]-SampleSize-3)
        random_y = random.randint(0, img.shape[0]-SampleSize-3)
        patch = img[random_y:random_y+SampleSize, random_x:random_x+SampleSize, :]
        labelpatch = labelImg[random_y:random_y+SampleSize, random_x:random_x+SampleSize]
        end3 = time.clock()
        if (end3-start3)>4:
            
            return patch, labelpatch
        elif np.sum(labelpatch[:,:] > 0) < threshold:
            continue
        else:
            return patch, labelpatch
# def SequenceCrop(img,labelImg,SampleSize=256):
#     number_y=int(img.shape[0]/SampleSize)
#     number_x=int(img.shape[1]/SampleSize)
#     for j in range(1,number_y+1):
#         for i in range(1,number_x+1):
#             if j==number_y+1:
#                 Sequence_y=img.shape[0]
#             else:
#                Sequence_y=j*SampleSize
#             if i==number_x+1:
#                 Sequence_x=img.shape[1]
#             else:
#                Sequence_x=i*SampleSize
#             if(number_y==0 or number_x==0 ):
#                 return -1
#             else:
#                 Sequence_img=img[Sequence_y-SampleSize:Sequence_y,Sequence_x-SampleSize:Sequence_x:]
#                 Sequence_label=labelImg[Sequence_y-SampleSize:Sequence_y,Sequence_x-SampleSize:Sequence_x]
#                 return Sequence_img,Sequence_label





def writeImage_s(img, label, imgName, labelName):
    cv2.imwrite(imgName, img)
    cv2.imwrite(labelName, label)


def Sample_make(Fs_Root_path,Imgnumber=20,threshold=600,SampleSize=256,RoiRegion=False,Roi_y=1970,Roi_x=887,Roi_height=1853,Roi_width=4027):
    #截图个数
    patchPerImg = Imgnumber
    imgDirPath=Fs_Root_path+"\\train_seg\\image2"
    labelDirPath=Fs_Root_path+"\\train_seg\\label2"
    outimgDirPath=Fs_Root_path+"\\train_seg\\little_image2"
    outlabelDirPath=Fs_Root_path+"\\train_seg\\little_label2"
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
        if RoiRegion:
            if img.shape[0]<(Roi_y+Roi_height) or img.shape[1]<(Roi_x+Roi_width):
                img_roi=img
                label_roi=label
            else:
                img_roi,label_roi=getRoiImage(img,label,Roi_y,Roi_x,Roi_height,Roi_width)
        else:
            img_roi=img
            label_roi=label


        #############随机裁剪制作样本##################
        for t in range(patchPerImg):
            print('processing ...:', imgPath)
            patch_img, patch_label = randomCrop_s(img_roi, label_roi,threshold,SampleSize)
            patch_img_name = imgName.split('.')[0]+'_r'+str(t)+'.bmp'
            outimgPath=os.path.join(outimgDirPath, patch_img_name)
            patch_label_name = labelName.split('.')[0] + '_r'+str(t) + '.bmp'
            outlabelPath=os.path.join(outlabelDirPath, patch_label_name)
            writeImage_s(patch_img, patch_label, outimgPath, outlabelPath)
        ############顺序裁剪制作样本 ################ 
        number_y=int(img_roi.shape[0]/SampleSize)
        number_x=int(label_roi.shape[1]/SampleSize)
        counter=0
        for j in range(1,number_y+2):
            for i in range(1,number_x+2):
                if j==number_y+1:
                    Sequence_y=img_roi.shape[0]
                else:
                    # print("j",j)
                    # print("SampleSize",SampleSize)
                    Sequence_y=j*SampleSize
                if i==number_x+1:
                    Sequence_x=img_roi.shape[1]
                else:
                    Sequence_x=i*SampleSize
                if(number_y==0 or number_x==0 ):
                    break 
                else:
                    Sequence_img=img_roi[Sequence_y-SampleSize:Sequence_y,Sequence_x-SampleSize:Sequence_x,:]
                    Sequence_label_Image=label_roi[Sequence_y-SampleSize:Sequence_y,Sequence_x-SampleSize:Sequence_x]
                   
                    patch_Sequence_img_name = imgName.split('.')[0]+'_s'+str(counter)+'.bmp'
                    outSequenceimgPath=os.path.join(outimgDirPath, patch_Sequence_img_name)
                    patch_Sequence_label_name = labelName.split('.')[0] + '_s'+str(counter) + '.bmp'
                    outSequencelabelPath=os.path.join(outlabelDirPath, patch_Sequence_label_name)
                    writeImage_s(Sequence_img, Sequence_label_Image, outSequenceimgPath, outSequencelabelPath)
                    counter=counter+1
                     



#根据结果图生成正样本
def readImage_p(imgpath, labelPath, SlabelPath):
    img = cv2.imread(imgpath)
    labelImg = cv2.imread(labelPath,0)
    ret,labelImg = cv2.threshold(labelImg,10,255,cv2.THRESH_BINARY)
    SlabelImg = cv2.imread(SlabelPath,0)
    ret,SImg = cv2.threshold(SlabelImg,10,255,cv2.THRESH_BINARY)
    return img, labelImg, SImg

def randomCrop_p(img, labelImg, Slabel,threshold,SampleSize=256):
    threshold = threshold
    start3 = time.clock()
    if  img.shape[0]<SampleSize+4 or img.shape[1]<SampleSize+4:
        return -1
    while True:
        random_x = random.randint(0, img.shape[1]-SampleSize-3)
        random_y = random.randint(0, img.shape[0]-SampleSize-3)
        patch = img[random_y:random_y+SampleSize, random_x:random_x+SampleSize, :]
        labelpatch = labelImg[random_y:random_y+SampleSize, random_x:random_x+SampleSize]
        Slabelpatch = Slabel[random_y:random_y+SampleSize, random_x:random_x+SampleSize]
        end3 = time.clock()
        
        # print('time:%s Seconds'%(end3-start3))
        if (end3-start3)>3:
            
            return patch, labelpatch, Slabelpatch
        if np.sum(Slabelpatch[:,:] > 0) < threshold:
            continue
        else:
            return patch, labelpatch, Slabelpatch

def writeImage_p(img, label, imgName, labelName):
    t_str=datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
    time_str=(t_str[:10]+'-'+t_str[11:13])
    imgName=imgName[:-4]+'_'+time_str+imgName[-4:]
    labelName=labelName[:-4]+'_'+time_str+labelName[-4:]
    cv2.imwrite(imgName, img)
    cv2.imwrite(labelName, label)


def PosSample_make(Fs_Root_path,ImgNumber=12,threshold=400,SampleSize=256):
    patchPerImg = ImgNumber
    er = 0
    outimgDirPath=Fs_Root_path+"\\train_seg\\little_image2"
    outlabelDirPath=Fs_Root_path+"\\train_seg\\little_label2"
    if not osp.exists(outimgDirPath):
        os.mkdir(outimgDirPath)
    if not osp.exists(outlabelDirPath):
        os.mkdir(outlabelDirPath)
    ResultimgDirPath=Fs_Root_path+'\\train_seg\\image2'
    ResultlabelDirPath=Fs_Root_path+'\\train_seg\\image_result2'
    SourcelabelDirPath=Fs_Root_path+'\\train_seg\\label2'
    RimgFiles = sorted(os.listdir(ResultimgDirPath))
    RlabelFiles = sorted(os.listdir(ResultlabelDirPath))
    #SimgFiles = sorted(os.listdir(SourceimgDirPath))
    SlabelFiles = sorted(os.listdir(SourcelabelDirPath))
    for RimgName, RlabelName,SlabelName in zip(RimgFiles, RlabelFiles,SlabelFiles):
        RimgPath=os.path.join(ResultimgDirPath,RimgName)
        RlabelPath=os.path.join(ResultlabelDirPath,RimgName)
        SlabelPath=os.path.join(SourcelabelDirPath,RimgName)
        Rimg, Rlabel, Slabel = readImage_p(RimgPath, RlabelPath, SlabelPath)
        for t in range(patchPerImg):
            print('processing ...:', RimgName)
            patch_img, patch_label, patch_Slabel = randomCrop_p(Rimg, Rlabel, Slabel,threshold,SampleSize)
            # if flag==0:
            #     break
            resultimg = np.sum(patch_label[:,:] > 0)
            #print(source)
            # if(patch_label.shape!=patch_Slabel.shape):
            #     continue
            and_Img = cv2.bitwise_and(patch_label,patch_Slabel)
            numofand = np.sum(and_Img[:,:] > 0)
            or_Img = cv2.bitwise_or(patch_label, patch_Slabel)
            numofor = np.sum(or_Img[:,:] > 0)
            if resultimg == 0:
                label_name = SlabelName.split('.')[0] + str(t) + '_emmiss.bmp'
                OutLabelPath=os.path.join(outlabelDirPath,label_name)
                img_name = RimgName.split('.')[0]+str(t)+'_emmiss.bmp'
                OutImgPath=os.path.join(outimgDirPath,img_name)
                writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
                er = er + 1
                continue
            point1 = numofand/resultimg
            #print(point1)
            point2 = numofor/resultimg
            #print(point2)
            if point2 > 1.5:
                label_name = SlabelName.split('.')[0] + str(t) + '_emmiss.bmp'
                OutLabelPath=os.path.join(outlabelDirPath,label_name)
                img_name = RimgName.split('.')[0]+str(t)+'_emmiss.bmp'
                OutImgPath=os.path.join(outimgDirPath,img_name)
                writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
                continue
            # if point2 > 1.6:
            #     label_name = SlabelName.split('.')[0] + str(t) + '_emmiss.bmp'
            #     OutLabelPath=os.path.join(outlabelDirPath,label_name)
            #     img_name = RimgName.split('.')[0]+str(t)+'_emmiss.bmp'
            #     OutImgPath=os.path.join(outimgDirPath,img_name)
            #     writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
            #     continue
            # if point1 < 0.4:
            #     label_name = SlabelName.split('.')[0] + str(t) + '_emmiss.bmp'
            #     OutLabelPath=os.path.join(outlabelDirPath,label_name)
            #     img_name = RimgName.split('.')[0]+str(t)+'_emmiss.bmp'
            #     OutImgPath=os.path.join(outimgDirPath,img_name)
            #     writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
            #     continue
            # if point2 < 1.15 and point1 > 0.85:
            #     label_name = SlabelName.split('.')[0] + str(t) + '_emmiss.bmp'
            #     OutLabelPath=os.path.join(outlabelDirPath,label_name)
            #     img_name = RimgName.split('.')[0]+str(t)+'_emmiss.bmp'
            #     OutImgPath=os.path.join(outimgDirPath,img_name)
            #     writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
            #     continue
    print(er)


#根据结果图生成负样本
def readImage_n(path, labelPath, SlabelPath):
    img = cv2.imread(os.path.join(ResultimgDirPath, path))
    labelImg = cv2.imread(os.path.join(ResultlabelDirPath, labelPath),0)
    ret,labelImg = cv2.threshold(labelImg,10,255,cv2.THRESH_BINARY)
    SlabelImg = cv2.imread(os.path.join(SourcelabelDirPath, SlabelPath),0)
    ret,SImg = cv2.threshold(SlabelImg,10,255,cv2.THRESH_BINARY)
    return img, labelImg, SImg

def randomCrop_n(img, labelImg, Slabel,threshold,SampleSize=256):
    threshold = threshold
    start3 = time.clock()
    if  img.shape[0]<SampleSize+4 or img.shape[1]<SampleSize+4:
        return -1
    while True:
        random_x = random.randint(0, img.shape[1]-SampleSize-3)
        random_y = random.randint(0, img.shape[0]-SampleSize-3)
        patch = img[random_y:random_y+SampleSize, random_x:random_x+SampleSize, :]
        labelpatch = labelImg[random_y:random_y+SampleSize, random_x:random_x+SampleSize]
        Slabelpatch = Slabel[random_y:random_y+SampleSize, random_x:random_x+SampleSize]
        end3 = time.clock()
        
        # print('time:%s Seconds'%(end3-start3))
        if (end3-start3)>4:
            
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



def NegSample_make(Fs_Root_path,ImgNumber=12,threshold=100,SampleSize=256):
    patchPerImg = ImgNumber
    er = 0
    outimgDirPath=Fs_Root_path+"\\train_seg\\little_image2"
    outlabelDirPath=Fs_Root_path+"\\train_seg\\little_label2"
    if not osp.exists(outimgDirPath):
        os.mkdir(outimgDirPath)
    if not osp.exists(outlabelDirPath):
        os.mkdir(outlabelDirPath)
    ResultimgDirPath=Fs_Root_path+'\\train_seg\\image2'
    ResultlabelDirPath=Fs_Root_path+'\\train_seg\\image_result2'
    SourcelabelDirPath=Fs_Root_path+'\\train_seg\\label2'
    RimgFiles = sorted(os.listdir(ResultimgDirPath))
    RlabelFiles = sorted(os.listdir(ResultlabelDirPath))
    #SimgFiles = sorted(os.listdir(SourceimgDirPath))
    SlabelFiles = sorted(os.listdir(SourcelabelDirPath))
    for RimgName, RlabelName,SlabelName in zip(RimgFiles, RlabelFiles,SlabelFiles):
        RimgPath=os.path.join(ResultimgDirPath,RimgName)
        RlabelPath=os.path.join(ResultlabelDirPath,RimgName)
        SlabelPath=os.path.join(SourcelabelDirPath,RimgName)
        Rimg, Rlabel, Slabel = readImage_p(RimgPath, RlabelPath, SlabelPath)
        for t in range(patchPerImg):
            print('processing ...:', RimgName)
            patch_img, patch_label, patch_Slabel = randomCrop_n(Rimg, Rlabel, Slabel,threshold,SampleSize)
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
                label_name = SlabelName.split('.')[0] + str(t) + '_emneg.bmp'
                OutLabelPath=os.path.join(outlabelDirPath,label_name)
                img_name = RimgName.split('.')[0]+str(t)+'_emneg.bmp'
                OutImgPath=os.path.join(outimgDirPath,img_name)
                writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
                er = er + 1
                continue
            point1 = numofand/resultimg
            #print(point1)
            point2 = numofor/resultimg
            print(point2)
            if point2 > 1.5:
                label_name = SlabelName.split('.')[0] + str(t) + '_emneg.bmp'
                OutLabelPath=os.path.join(outlabelDirPath,label_name)
                img_name = RimgName.split('.')[0]+str(t)+'_emneg.bmp'
                OutImgPath=os.path.join(outimgDirPath,img_name)
                writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
                continue
            if point1 < 0.5:
                label_name = SlabelName.split('.')[0] + str(t) + '_emneg.bmp'
                OutLabelPath=os.path.join(outlabelDirPath,label_name)
                img_name = RimgName.split('.')[0]+str(t)+'_emneg.bmp'
                OutImgPath=os.path.join(outimgDirPath,img_name)
                writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
                continue
            if point1 >0.85 and point2<1.15:
                label_name = SlabelName.split('.')[0] + str(t) + '_emneg.bmp'
                OutLabelPath=os.path.join(outlabelDirPath,label_name)
                img_name = RimgName.split('.')[0]+str(t)+'_emneg.bmp'
                OutImgPath=os.path.join(outimgDirPath,img_name)
                writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
                continue


    print(er)



def MakeSample(Fs_Root_path,Sample=False,PosSample=False,NegSample=False,RoiRegion=False,Roi_y=1970,Roi_x=887,Roi_height=1853,Roi_width=4027,
              Sample_Imgnumber=16,Sample_threshold=1600,PosSample_ImgNumber=36,PosSample_threshold=100,NegSample_ImgNumber=36,NegSample_threshold=100,SampleSize=256):
    if Sample:
        Sample_make(Fs_Root_path,Sample_Imgnumber,Sample_threshold,SampleSize,RoiRegion,Roi_y,Roi_x,Roi_height,Roi_width)
    if PosSample:
        PosSample_make(Fs_Root_path,PosSample_ImgNumber,PosSample_threshold,SampleSize)
    if NegSample:
        NegSample_make(Fs_Root_path,NegSample_ImgNumber,NegSample_threshold,SampleSize)

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
Fs_Root_path='D:\\MakeSample'
Sample=False
PosSample=True
NegSample=True
RoiRegion=True
MakeSample(Fs_Root_path,Sample,PosSample,NegSample,RoiRegion,Roi_y=1960,Roi_x=621,Roi_height=1792,Roi_width=4352)


   
