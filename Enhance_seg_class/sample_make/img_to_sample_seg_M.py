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
    # ret,graylabelImg = cv2.threshold(labelImg,0,255,cv2.THRESH_BINARY)
    return img, labelImg

def randomCrop_s(img, labelImg,threshold):
    #截图阈值    
    threshold = threshold
    start3 = time.clock()
    while True:
        random_x = random.randint(0, img.shape[1]-259)
        random_y = random.randint(0, img.shape[0]-259)
        patch = img[random_y:random_y+256, random_x:random_x+256, :]
        labelpatch = labelImg[random_y:random_y+256, random_x:random_x+256]
        end3 = time.clock()
        if (end3-start3)>4:
            
            return patch, labelpatch
        elif np.sum(labelpatch[:,:] > 0) < threshold:
            continue
        else:
            return patch, labelpatch

def writeImage_s(img, label, imgName, labelName):
    cv2.imwrite(imgName, img)
    cv2.imwrite(labelName, label)


def Sample_make(Fs_Root_path,Imgnumber=20,threshold=600):
    #截图个数
    patchPerImg = Imgnumber
    imgDirPath=Fs_Root_path+"\\train_seg\\image_test"
    labelDirPath=Fs_Root_path+"\\train_seg\\label_test"
    outimgDirPath=Fs_Root_path+"\\train_seg\\little_image_test"
    outlabelDirPath=Fs_Root_path+"\\train_seg\\little_label_test"
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
        for t in range(patchPerImg):
            print('processing ...:', imgPath)
            patch_img, patch_label = randomCrop_s(img, label,threshold)
            patch_img_name = imgName.split('.')[0]+str(t)+'_.bmp'
            outimgPath=os.path.join(outimgDirPath, patch_img_name)
            patch_label_name = labelName.split('.')[0] + str(t) + '_.bmp'
            outlabelPath=os.path.join(outlabelDirPath, patch_label_name)
            writeImage_s(patch_img, patch_label, outimgPath, outlabelPath)


#根据结果图生成正样本
def readImage_p(imgpath, labelPath, SlabelPath):
    img = cv2.imread(imgpath)
    labelImg = cv2.imread(labelPath,cv2.IMREAD_GRAYSCALE)
    # ret,labelImg = cv2.threshold(labelImg,10,255,cv2.THRESH_BINARY)
    SlabelImg = cv2.imread(SlabelPath,cv2.IMREAD_GRAYSCALE)
    # ret,SImg = cv2.threshold(SlabelImg,10,255,cv2.THRESH_BINARY)
    return img, labelImg, SlabelImg

def randomCrop_p(img, labelImg, Slabel,threshold):
    threshold = threshold
    start3 = time.clock()
    while True:
        random_x = random.randint(0, img.shape[1]-259)
        random_y = random.randint(0, img.shape[0]-259)
        patch = img[random_y:random_y+256, random_x:random_x+256, :]
        labelpatch = labelImg[random_y:random_y+256, random_x:random_x+256]
        Slabelpatch = Slabel[random_y:random_y+256, random_x:random_x+256]
        end3 = time.clock()
        # Rlabelpoint={}
        # Slabelpoint={}
        # row=labelpatch.shape[0]
        # col=labelpatch.shape[1]
        # for i in range(col):
        #     for j in range(row):
        #         if str(labelpatch[j,i]) not in Rlabelpoint:
        #             Rlabelpoint[str(labelpatch[j,i])]=[[i,j]]
        #         else:
        #             Rlabelpoint[str(labelpatch[j,i])].append([i,j])

        # for i in range(col):
        #     for j in range(row):
        #         if str(Slabelpatch[j,i]) not in Slabelpoint:
        #             Slabelpoint[str(Slabelpatch[j,i])]=[[i,j]]
        #         else:
        #             Slabelpoint[str(Slabelpatch[j,i])].append([i,j])            
        
        # print('time:%s Seconds'%(end3-start3))
        if (end3-start3)>2:
            
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


def PosSample_make(Fs_Root_path,ImgNumber=12,threshold=400):
    patchPerImg = ImgNumber
    er = 0
    outimgDirPath=Fs_Root_path+"\\train_seg\\little_image_test"
    outlabelDirPath=Fs_Root_path+"\\train_seg\\little_label_test"
    if not osp.exists(outimgDirPath):
        os.mkdir(outimgDirPath)
    if not osp.exists(outlabelDirPath):
        os.mkdir(outlabelDirPath)
    ResultimgDirPath=Fs_Root_path+'\\train_seg\\image_test'
    ResultlabelDirPath=Fs_Root_path+'\\train_seg\\result_test'
    SourcelabelDirPath=Fs_Root_path+'\\train_seg\\label_test'
    RimgFiles = sorted(os.listdir(ResultimgDirPath))
    RlabelFiles = sorted(os.listdir(ResultlabelDirPath))
    #SimgFiles = sorted(os.listdir(SourceimgDirPath))
    SlabelFiles = sorted(os.listdir(SourcelabelDirPath))
    for RimgName, RlabelName,SlabelName in zip(RimgFiles, RlabelFiles,SlabelFiles):
        RimgPath=os.path.join(ResultimgDirPath,RimgName)
        RlabelPath=os.path.join(ResultlabelDirPath,RimgName)
        SlabelPath=os.path.join(SourcelabelDirPath,RimgName)
        Rimg, Rlabel, Slabel = readImage_p(RimgPath, RlabelPath, SlabelPath)
        count=0
        for t in range(patchPerImg):
            print('processing ...:', RimgName)
            patch_img, patch_label, patch_Slabel = randomCrop_p(Rimg, Rlabel, Slabel,threshold)
            Stype=np.unique(patch_Slabel)
            for i in range(len(Stype)-1):
                Sresult=np.zeros(patch_label.shape,np.uint8)
                Rresult=np.zeros(patch_label.shape,np.uint8)
                the=Stype[i+1]
                Sindex = (patch_Slabel == the)
                Sresult[Sindex] = 255
                Rindex = (patch_label == the)
                Rresult[Rindex] = 255

            # for k,v in Slabelpoint.items():
            #     Sresult=np.zeros(patch_label.shape,np.uint8)
            #     Rresult=np.zeros(patch_label.shape,np.uint8)
            #     for i in range(len(Slabelpoint[k])):
            #         col=Slabelpoint[k][i][0]
            #         row=Slabelpoint[k][i][1]
            #         Sresult[col,row]=255
            #     if k in Rlabelpoint:
            #         for i in range(len(Rlabelpoint[k])):
            #             col=Rlabelpoint[k][i][0]
            #             row=Rlabelpoint[k][i][1]
            #             Rresult[col,row]=255
                and_Img=cv2.bitwise_and(Sresult,Rresult)
                numand=np.sum(and_Img[:,:]>0)
                or_Img=cv2.bitwise_or(Sresult,Rresult)
                numor=np.sum(or_Img[:,:]>0)
                numSresult=np.sum(Sresult[:,:]>0)
                point1=numand/numSresult
                point2=numor/numSresult
                
                if point1==0:
                        label_name = SlabelName.split('.')[0] +'-'+ str(count) + '_emmiss.bmp'
                        OutLabelPath=os.path.join(outlabelDirPath,label_name)
                        img_name = RimgName.split('.')[0]+'-'+str(count)+'_emmiss.bmp'
                        OutImgPath=os.path.join(outimgDirPath,img_name)
                        writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
                        er=er+1
                        count=count+1
                        continue
                if point1 < 0.4:
                    label_name = SlabelName.split('.')[0] +'-'+ str(count) + '_emmiss.bmp'
                    OutLabelPath=os.path.join(outlabelDirPath,label_name)
                    img_name = RimgName.split('.')[0]+'-'+str(count)+'_emmiss.bmp'
                    OutImgPath=os.path.join(outimgDirPath,img_name)
                    writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
                    count=count+1
                    continue
                if point2 > 1.5:
                    label_name = SlabelName.split('.')[0] +'-'+ str(count) + '_emmiss.bmp'
                    OutLabelPath=os.path.join(outlabelDirPath,label_name)
                    img_name = RimgName.split('.')[0]+'-'+str(count)+'_emmiss.bmp'
                    OutImgPath=os.path.join(outimgDirPath,img_name)
                    writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
                    count=count+1
                    continue



            # # if flag==0:
            # #     break
            # resultimg = np.sum(patch_label[:,:] > 0)
            # #print(source)
            # # if(patch_label.shape!=patch_Slabel.shape):
            # #     continue
            
            # and_Img = cv2.bitwise_and(patch_label,patch_Slabel)
            # numofand = np.sum(and_Img[:,:] > 0)
            # or_Img = cv2.bitwise_or(patch_label, patch_Slabel)
            # numofor = np.sum(or_Img[:,:] > 0)
            # if resultimg == 0:
            #     label_name = SlabelName.split('.')[0] + str(t) + '_emmiss.bmp'
            #     OutLabelPath=os.path.join(outlabelDirPath,label_name)
            #     img_name = RimgName.split('.')[0]+str(t)+'_emmiss.bmp'
            #     OutImgPath=os.path.join(outimgDirPath,img_name)
            #     writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
            #     er = er + 1
            #     continue
            # point1 = numofand/resultimg
            # #print(point1)
            # point2 = numofor/resultimg
            # #print(point2)
            # if point2 > 1.5:
            #     label_name = SlabelName.split('.')[0] + str(t) + '_emmiss.bmp'
            #     OutLabelPath=os.path.join(outlabelDirPath,label_name)
            #     img_name = RimgName.split('.')[0]+str(t)+'_emmiss.bmp'
            #     OutImgPath=os.path.join(outimgDirPath,img_name)
            #     writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
            #     continue
            # # if point2 > 1.6:
            # #     label_name = SlabelName.split('.')[0] + str(t) + '_emmiss.bmp'
            # #     OutLabelPath=os.path.join(outlabelDirPath,label_name)
            # #     img_name = RimgName.split('.')[0]+str(t)+'_emmiss.bmp'
            # #     OutImgPath=os.path.join(outimgDirPath,img_name)
            # #     writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
            # #     continue
            # # if point1 < 0.4:
            # #     label_name = SlabelName.split('.')[0] + str(t) + '_emmiss.bmp'
            # #     OutLabelPath=os.path.join(outlabelDirPath,label_name)
            # #     img_name = RimgName.split('.')[0]+str(t)+'_emmiss.bmp'
            # #     OutImgPath=os.path.join(outimgDirPath,img_name)
            # #     writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
            # #     continue
            # # if point2 < 1.15 and point1 > 0.85:
            # #     label_name = SlabelName.split('.')[0] + str(t) + '_emmiss.bmp'
            # #     OutLabelPath=os.path.join(outlabelDirPath,label_name)
            # #     img_name = RimgName.split('.')[0]+str(t)+'_emmiss.bmp'
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

def randomCrop_n(img, labelImg, Slabel,threshold):
    threshold = threshold
    start3 = time.clock()
    while True:
        random_x = random.randint(0, img.shape[1]-259)
        random_y = random.randint(0, img.shape[0]-259)
        patch = img[random_y:random_y+256, random_x:random_x+256, :]
        labelpatch = labelImg[random_y:random_y+256, random_x:random_x+256]
        Slabelpatch = Slabel[random_y:random_y+256, random_x:random_x+256]
        end3 = time.clock()


        # Rlabelpoint={}
        # Slabelpoint={}
        # row=labelpatch.shape[0]
        # col=labelpatch.shape[1]
        # for i in range(col):
        #     for j in range(row):
        #         if str(labelpatch[j,i]) not in Rlabelpoint:
        #             Rlabelpoint[str(labelpatch[j,i])]=[[i,j]]
        #         else:
        #             Rlabelpoint[str(labelpatch[j,i])].append([i,j])

        # for i in range(col):
        #     for j in range(row):
        #         if str(Slabelpatch[j,i]) not in Slabelpoint:
        #             Slabelpoint[str(Slabelpatch[j,i])]=[[i,j]]
        #         else:
        #             Slabelpoint[str(Slabelpatch[j,i])].append([i,j])   
        
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



def NegSample_make(Fs_Root_path,ImgNumber=12,threshold=100):
    patchPerImg = ImgNumber
    er = 0
    outimgDirPath=Fs_Root_path+"\\train_seg\\little_image_test"
    outlabelDirPath=Fs_Root_path+"\\train_seg\\little_label_test"
    if not osp.exists(outimgDirPath):
        os.mkdir(outimgDirPath)
    if not osp.exists(outlabelDirPath):
        os.mkdir(outlabelDirPath)
    ResultimgDirPath=Fs_Root_path+'\\train_seg\\image_test'
    ResultlabelDirPath=Fs_Root_path+'\\train_seg\\result_test'
    SourcelabelDirPath=Fs_Root_path+'\\train_seg\\label_test'
    RimgFiles = sorted(os.listdir(ResultimgDirPath))
    RlabelFiles = sorted(os.listdir(ResultlabelDirPath))
    #SimgFiles = sorted(os.listdir(SourceimgDirPath))
    SlabelFiles = sorted(os.listdir(SourcelabelDirPath))
    for RimgName, RlabelName,SlabelName in zip(RimgFiles, RlabelFiles,SlabelFiles):
        RimgPath=os.path.join(ResultimgDirPath,RimgName)
        RlabelPath=os.path.join(ResultlabelDirPath,RimgName)
        SlabelPath=os.path.join(SourcelabelDirPath,RimgName)
        Rimg, Rlabel, Slabel = readImage_p(RimgPath, RlabelPath, SlabelPath)
        count=0
        for t in range(patchPerImg):
            print('processing ...:', RimgName)
            patch_img, patch_label, patch_Slabel = randomCrop_n(Rimg, Rlabel, Slabel,threshold)


            Rtype=np.unique(patch_label)
            for i in range(len(Rtype)-1):
                Sresult=np.zeros(patch_label.shape,np.uint8)
                Rresult=np.zeros(patch_label.shape,np.uint8)
                the=Rtype[i+1]
                Sindex = (patch_Slabel == the)
                Sresult[Sindex] = 255
                Rindex = (patch_label == the)
                Rresult[Rindex] = 255
            
            # for k,v in Rlabelpoint.items():
            #     Sresult=np.zeros(patch_label.shape,np.uint8)
            #     Rresult=np.zeros(patch_label.shape,np.uint8)
            #     for i in range(len(Rlabelpoint[k])):
            #         col=Rlabelpoint[k][i][0]
            #         row=Rlabelpoint[k][i][1]
            #         Rresult[col,row]=255
            #     if k in Slabelpoint:
            #         for i in range(len(Slabelpoint[k])):
            #             col=Slabelpoint[k][i][0]
            #             row=Slabelpoint[k][i][1]
            #             Sresult[col,row]=255

                and_Img=cv2.bitwise_and(Sresult,Rresult)
                numand=np.sum(and_Img[:,:]>0)
                or_Img=cv2.bitwise_or(Sresult,Rresult)
                numor=np.sum(or_Img[:,:]>0)
                numRresult=np.sum(Rresult[:,:]>0)
                point1=numand/numRresult
                point2=numor/numRresult

                if point1==0:
                        label_name = SlabelName.split('.')[0] +'-'+ str(count) + '_emneg.bmp'
                        OutLabelPath=os.path.join(outlabelDirPath,label_name)
                        img_name = RimgName.split('.')[0]+'-'+str(count)+'_emneg.bmp'
                        OutImgPath=os.path.join(outimgDirPath,img_name)
                        writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
                        er=er+1
                        count=count+1
                        continue
                if point1 >0.85 and point2<1.15:
                        label_name = SlabelName.split('.')[0] +'-'+ str(count) + '_emneg.bmp'
                        OutLabelPath=os.path.join(outlabelDirPath,label_name)
                        img_name = RimgName.split('.')[0]+'-'+str(count)+'_emneg.bmp'
                        OutImgPath=os.path.join(outimgDirPath,img_name)
                        writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
                        count=count+1
                        continue
                if point1 < 0.4:
                    label_name = SlabelName.split('.')[0] +'-'+ str(count) + '_emneg.bmp'
                    OutLabelPath=os.path.join(outlabelDirPath,label_name)
                    img_name = RimgName.split('.')[0]+'-'+str(count)+'_emneg.bmp'
                    OutImgPath=os.path.join(outimgDirPath,img_name)
                    writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
                    count=count+1
                    continue
                if point2 > 1.5:
                    label_name = SlabelName.split('.')[0] +'-'+ str(count) + '_emneg.bmp'
                    OutLabelPath=os.path.join(outlabelDirPath,label_name)
                    img_name = RimgName.split('.')[0]+'-'+str(count)+'_emneg.bmp'
                    OutImgPath=os.path.join(outimgDirPath,img_name)
                    writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
                    count=count+1
                    continue






            # # if flag==0:
            # #     break
            # resultimg = np.sum(patch_Slabel[:,:] > 0)
            # #print(source)
            # # if(patch_label.shape!=patch_Slabel.shape):
            # #     continue
            # and_Img = cv2.bitwise_and(patch_label,patch_Slabel)
            # numofand = np.sum(and_Img[:,:] > 0)
            # or_Img = cv2.bitwise_or(patch_label, patch_Slabel)
            # numofor = np.sum(or_Img[:,:] > 0)
            # if resultimg == 0:
            #     label_name = SlabelName.split('.')[0] + str(t) + '_emneg.bmp'
            #     OutLabelPath=os.path.join(outlabelDirPath,label_name)
            #     img_name = RimgName.split('.')[0]+str(t)+'_emneg.bmp'
            #     OutImgPath=os.path.join(outimgDirPath,img_name)
            #     writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
            #     er = er + 1
            #     continue
            # point1 = numofand/resultimg
            # #print(point1)
            # point2 = numofor/resultimg
            # #print(point2)
            # if point2 > 1.5:
            #     label_name = SlabelName.split('.')[0] + str(t) + '_emneg.bmp'
            #     OutLabelPath=os.path.join(outlabelDirPath,label_name)
            #     img_name = RimgName.split('.')[0]+str(t)+'_emneg.bmp'
            #     OutImgPath=os.path.join(outimgDirPath,img_name)
            #     writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
            #     continue
            # if point1 < 0.4:
            #     label_name = SlabelName.split('.')[0] + str(t) + '_emneg.bmp'
            #     OutLabelPath=os.path.join(outlabelDirPath,label_name)
            #     img_name = RimgName.split('.')[0]+str(t)+'_emneg.bmp'
            #     OutImgPath=os.path.join(outimgDirPath,img_name)
            #     writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
            #     continue
            # if point1 >0.85 and point2<1.15:
            #     label_name = SlabelName.split('.')[0] + str(t) + '_emneg.bmp'
            #     OutLabelPath=os.path.join(outlabelDirPath,label_name)
            #     img_name = RimgName.split('.')[0]+str(t)+'_emneg.bmp'
            #     OutImgPath=os.path.join(outimgDirPath,img_name)
            #     writeImage_p(patch_img, patch_Slabel, OutImgPath, OutLabelPath)
            #     continue


    print(er)



def MakeSample(Fs_Root_path,Sample=False,PosSample=False,NegSample=False,
              Sample_Imgnumber=20,Sample_threshold=30,PosSample_ImgNumber=16,PosSample_threshold=30,NegSample_ImgNumber=16,NegSample_threshold=30):
    if Sample:
        Sample_make(Fs_Root_path,Sample_Imgnumber,Sample_threshold)
    if PosSample:
        PosSample_make(Fs_Root_path,PosSample_ImgNumber,PosSample_threshold)
    if NegSample:
        NegSample_make(Fs_Root_path,NegSample_ImgNumber,NegSample_threshold)

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
Fs_Root_path='D:\\test'
Sample=True
PosSample=True
NegSample=True
MakeSample(Fs_Root_path,Sample,PosSample,NegSample)


   
