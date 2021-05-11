# 制作训练样本、正样本、负样本
# #使用示例
# Sample（）制作训练样本、PosSample（）制作正样本、NegSample（）制作负样本；Fs_Root_path表示根目录
# Fs_Root_path='D:\\test'  表示根目录
# Sample(Fs_Root_path)  制作训练样本
# PosSample(Fs_Root_path)   制作正样本
# NegSample(Fs_Root_path)   制作负样本


import cv2
import os
import numpy as np



def readImage_s(resultpath, labelPath):
    # result = cv2.imread(resultpath)
    result = cv2.imread(resultpath,cv2.IMREAD_GRAYSCALE)
    labelImg = cv2.imread(labelPath,cv2.IMREAD_GRAYSCALE)
    # ret,graylabelImg = cv2.threshold(labelImg,0,255,cv2.THRESH_BINARY)
    return result, labelImg
count=0
def AccuracyJudgment(Fs_Root_path,Area=100):
    resultDirPath=Fs_Root_path+"\\guashang\\result"
    labelDirPath=Fs_Root_path+"\\guashang\\label"

    resultFiles = sorted(os.listdir(resultDirPath))
    labelFiles = sorted(os.listdir(labelDirPath))
    # print(labelFiles)
    AllLabelDetect=0
    AllTrueDetect=0
    AllOverInspection=0
    for labeltName,resultName in zip(labelFiles,resultFiles):
        resultPath=os.path.join(resultDirPath, labeltName)
        labelPath=os.path.join(labelDirPath, labeltName)
        print(labelPath)
        result, label = readImage_s(resultPath, labelPath)
        
#         ret, frame = cv2.threshold(bitwiseAndImage, 50, 255, cv2.THRESH_BINARY)       
        ResultContours,BitwiseHierarchy = cv2.findContours(result,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#         print("number of ResultContours:%d" % len(ResultContours))
        resultindex = []
        print(len(ResultContours))
        for i in range(len(ResultContours)):
#             print("i",i)
#             print("cv2.contourArea(Contours[i])",cv2.contourArea(ResultContours[i]))
            if Area<cv2.contourArea(ResultContours[i]):
                resultindex.append(i)
        print(resultindex)

        if result is None:
            continue

        result2 = np.zeros(result.shape,np.uint8)
#         result2 = np.ones(result.shape,np.uint8)*255
        for i in range(len(resultindex)):
             cv2.drawContours(result2, ResultContours,resultindex[i], (255, 255, 255), -1)
#             cv2.fillConvexPoly(result2, Contours[index[i]], 255)

        LabelContours,LabelHierarchy = cv2.findContours(label,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#         print("number of LabelContours:%d" % len(LabelContours))
        Labelindex = []
        for i in range(len(LabelContours)):
#             print("i",i)
#             print("cv2.contourArea(LabelContours[i])",cv2.contourArea(LabelContours[i]))
            if Area<cv2.contourArea(LabelContours[i]):
                Labelindex.append(i)
        print(Labelindex)
        label2 = np.zeros(label.shape,np.uint8)
#         result2 = np.ones(result.shape,np.uint8)*255
        for i in range(len(Labelindex)):
             cv2.drawContours(label2, LabelContours,Labelindex[i], (255, 255, 255), -1)
#             cv2.fillConvexPoly(result2, Contours[index[i]], 255)
       
        bitwiseAndImage = cv2.bitwise_and(result2,label2)
        


        
        Result2Contours,BitwiseHierarchy = cv2.findContours(result2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        ResultDefectnNumber=len(Result2Contours)
        print("number of ResultDefectnNumber:%d" % ResultDefectnNumber)
        
        Label2Contours,LabelHierarchy = cv2.findContours(label2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        LabelDefectnNumber=len(Label2Contours)
        print("number of LabelDefectnNumber:%d" % LabelDefectnNumber)      
        
        TrueContours,LabelHierarchy = cv2.findContours(bitwiseAndImage,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        TrueDefectnNumber=len(TrueContours)
        print("number of TrueDefectnNumber:%d" % TrueDefectnNumber)
        
        


        if  ResultDefectnNumber<TrueDefectnNumber:
            ResultDefectnNumber=TrueDefectnNumber
        
        OverInspection=ResultDefectnNumber-TrueDefectnNumber
        
        if TrueDefectnNumber>LabelDefectnNumber:
            TrueDefectnNumber=LabelDefectnNumber
        
        AllLabelDetect=AllLabelDetect+LabelDefectnNumber
        AllTrueDetect=AllTrueDetect+TrueDefectnNumber
        AllOverInspection=AllOverInspection+OverInspection
        
        OverdetectionRate=AllOverInspection/(AllLabelDetect+0.001)
        DetectionRate=AllTrueDetect/(AllLabelDetect+0.001)
        
        print("number of AllLabelDetect:%d" % AllLabelDetect)
        print("number of AllTrueDetect:%d" % AllTrueDetect)
        print("number of AllOverInspection:%d" % AllOverInspection)
        print("OverdetectionRate:%f" % OverdetectionRate)
        print("DetectionRate:%f" % DetectionRate)
        global count
        count=count+1
        print("count",count)
    return   OverdetectionRate,DetectionRate
#         print(bitwiseAndImage)
#         cv2.namedWindow('bitwiseAndImage', cv2.WINDOW_NORMAL)
#         cv2.imshow('bitwiseAndImage', bitwiseAndImage)
#         cv2.namedWindow('result', cv2.WINDOW_NORMAL)
#         cv2.imshow('result', result)
#         cv2.namedWindow('label', cv2.WINDOW_NORMAL)
#         cv2.imshow('label', label)
#         cv2.namedWindow('result2', cv2.WINDOW_NORMAL)
#         cv2.imshow('result2', result2)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()

Fs_Root_path='D:\\ProjectMap\\AOI\\xiangjibaioding\\all\\'
Sample=True
PosSample=False
NegSample=False
Area=200
OverdetectionRate,DetectionRate=AccuracyJudgment(Fs_Root_path,Area)
print("OverdetectionRate",OverdetectionRate)
print("DetectionRate",DetectionRate)