import cv2
import numpy as np 
import os.path as osp
import os
import random
def readImage(MaskPath):
    mask=cv2.imread(MaskPath,0)
    ret,graymask=cv2.threshold(mask,50,255,cv2.THRESH_BINARY)
    return graymask

def img_to_coco(Fs_Root_path):
    InputMaskPath=Fs_Root_path+"\\train_seg\\label_0018"
    InputImagePath=Fs_Root_path+"\\train_seg\\image_0018"
    OutLabelPath=Fs_Root_path+"\\train_seg\\label_0018txt"
    OutShapePath=Fs_Root_path+"\\train_seg\\shape_0018"
    if not osp.exists(InputImagePath):
        os.mkdir(InputImagePath)
    if not osp.exists(OutLabelPath):
        os.mkdir(OutLabelPath)
    if not osp.exists(OutShapePath):
        os.mkdir(OutShapePath)

    TrainOutShapePath=OutShapePath+"\\train"
    ValOutShapePath=OutShapePath+"\\val"
    TrainOutLabelPath=OutLabelPath+"\\train"
    ValOutLabelPath=OutLabelPath+"\\val"

    if not osp.exists(TrainOutShapePath):
        os.mkdir(TrainOutShapePath)
    if not osp.exists(ValOutShapePath):
        os.mkdir(ValOutShapePath)
    if not osp.exists(TrainOutLabelPath):
        os.mkdir(TrainOutLabelPath)
    if not osp.exists(ValOutLabelPath):
        os.mkdir(ValOutLabelPath)

    MaskNane=os.listdir(InputMaskPath)
    random.shuffle(MaskNane)
    print("n",len(MaskNane))
    n=int(len(MaskNane)*0.2)
    TrainMaskFiles=MaskNane[:-n]
    ValMaskFiles=MaskNane[-n:]
    # MaskFiles=sorted(os.listdir(InputMaskPath))
    if 1:
        OutShapelName=TrainOutShapePath+"\\"+"image_shunmei_Train.shapes"
        OutImageName=TrainOutShapePath+"\\"+"image_shunmei_Train.txt"
        f_shape=open(OutShapelName,'w+')
        f_image=open(OutImageName,'w+')
        for Maskname in TrainMaskFiles:
            print("Maskname",Maskname)
            MaskPath=os.path.join(InputMaskPath,Maskname)
            ImagePath=os.path.join(InputImagePath,Maskname)
            f_image.write(ImagePath)
            f_image.write('\n')
            print("MaskPath==",MaskPath)
            Mask=readImage(MaskPath)
            print("Mask.shape",Mask.shape)
            Height=Mask.shape[0]
            Width=Mask.shape[1]
            OutLabelName=TrainOutLabelPath+"\\"+Maskname.split('.')[0]+".txt"
            f_shape.write(str(Width))
            f_shape.write(' ')
            f_shape.write(str(Height))
            f_shape.write('\n')
            f=open(OutLabelName,'w+')
            Contours,Hierarchy = cv2.findContours(Mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            for i in range(0,len(Contours)):
                x,y,w,h=cv2.boundingRect(Contours[i])
                if w>2 and h>2:
                    centerx=x+w/2
                    centery=y+h/2
                    x_out=centerx/Width
                    y_out=centery/Height
                    w_out=w/Width
                    h_out=h/Height
                    Class_idx=str(0)
                    f.write(Class_idx)
                    f.write(' ')
                    f.write(str(x_out))
                    f.write(' ')
                    f.write(str(y_out))
                    f.write(' ')
                    f.write(str(w_out))
                    f.write(' ')
                    f.write(str(h_out))
                    f.write('\n')
            f.close()
        f_shape.close()
        f_image.close()
    if 1:
        OutShapelName=ValOutShapePath+"\\"+"image_shunmei_Val.shapes"
        OutImageName=ValOutShapePath+"\\"+"image_shunmei_Val.txt"
        f_shape=open(OutShapelName,'w+')
        f_image=open(OutImageName,'w+')
        for Maskname in ValMaskFiles:
            print("Maskname",Maskname)
            MaskPath=os.path.join(InputMaskPath,Maskname)
            ImagePath=os.path.join(InputImagePath,Maskname)
            f_image.write(ImagePath)
            f_image.write('\n')
            print("MaskPath==",MaskPath)
            Mask=readImage(MaskPath)
            print("Mask.shape",Mask.shape)
            Height=Mask.shape[0]
            Width=Mask.shape[1]
            OutLabelName=ValOutLabelPath+"\\"+Maskname.split('.')[0]+".txt"
            f_shape.write(str(Width))
            f_shape.write(' ')
            f_shape.write(str(Height))
            f_shape.write('\n')
            f=open(OutLabelName,'w+')
            Contours,Hierarchy = cv2.findContours(Mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            for i in range(0,len(Contours)):
                x,y,w,h=cv2.boundingRect(Contours[i])
                if w>2 and h>2:
                    centerx=x+w/2
                    centery=y+h/2
                    x_out=centerx/Width
                    y_out=centery/Height
                    w_out=w/Width
                    h_out=h/Height
                    Class_idx=str(0)
                    f.write(Class_idx)
                    f.write(' ')
                    f.write(str(x_out))
                    f.write(' ')
                    f.write(str(y_out))
                    f.write(' ')
                    f.write(str(w_out))
                    f.write(' ')
                    f.write(str(h_out))
                    f.write('\n')
            f.close()
        f_shape.close()
        f_image.close()

Fs_Root_path="D:\\MakeSample"
img_to_coco(Fs_Root_path)



        

