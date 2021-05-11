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

    InputImagePath=Fs_Root_path+"\\yolov3\\images"
    # OutLabelPath=Fs_Root_path+"\\yolov3\\label_0018txt"
    OutShapePath=Fs_Root_path+"\\yolov3\\shape_screw"
    if not osp.exists(InputImagePath):
        os.mkdir(InputImagePath)
    # if not osp.exists(OutLabelPath):
    #     os.mkdir(OutLabelPath)
    if not osp.exists(OutShapePath):
        os.mkdir(OutShapePath)

    TrainOutShapePath=OutShapePath+"\\train"
    ValOutShapePath=OutShapePath+"\\val"


    if not osp.exists(TrainOutShapePath):
        os.mkdir(TrainOutShapePath)
    if not osp.exists(ValOutShapePath):
        os.mkdir(ValOutShapePath)


    MaskNane=os.listdir(InputImagePath)
    random.shuffle(MaskNane)
    print("n",len(MaskNane))
    n=int(len(MaskNane)*0.2)
    TrainMaskFiles=MaskNane[:-n]
    ValMaskFiles=MaskNane[-n:]
    # MaskFiles=sorted(os.listdir(InputMaskPath))
    if 1:
        OutShapelName=TrainOutShapePath+"\\"+"image_screw_Train.shapes"
        OutImageName=TrainOutShapePath+"\\"+"image_screw_Train.txt"
        f_shape=open(OutShapelName,'w+')
        f_image=open(OutImageName,'w+')
        for Maskname in TrainMaskFiles:
            print("Maskname",Maskname)

            ImagePath=os.path.join(InputImagePath,Maskname)
            f_image.write(ImagePath)
            f_image.write('\n')
            print("ImagePath==",ImagePath)
            Mask=readImage(ImagePath)
            print("Mask.shape",Mask.shape)
            Height=Mask.shape[0]
            Width=Mask.shape[1]
            f_shape.write(str(Width))
            f_shape.write(' ')
            f_shape.write(str(Height))
            f_shape.write('\n')

        f_shape.close()
        f_image.close()
    if 1:
        OutShapelName=ValOutShapePath+"\\"+"image_screw_Val.shapes"
        OutImageName=ValOutShapePath+"\\"+"image_screw_Val.txt"
        f_shape=open(OutShapelName,'w+')
        f_image=open(OutImageName,'w+')
        for Maskname in ValMaskFiles:
            print("Maskname",Maskname)
     
            ImagePath=os.path.join(InputImagePath,Maskname)
            f_image.write(ImagePath)
            f_image.write('\n')
            print("MaskPath==",ImagePath)
            Mask=readImage(ImagePath)
            print("Mask.shape",Mask.shape)
            Height=Mask.shape[0]
            Width=Mask.shape[1]

            f_shape.write(str(Width))
            f_shape.write(' ')
            f_shape.write(str(Height))
            f_shape.write('\n')

        f_shape.close()
        f_image.close()

Fs_Root_path="E:\\DLNetwork\\datas\\screw"
img_to_coco(Fs_Root_path)



        

