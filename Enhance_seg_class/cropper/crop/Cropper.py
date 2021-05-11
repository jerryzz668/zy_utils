import argparse
import cv2
import os
import numpy as np
from .libraryTools import imageRegionOfInterest
# from crop import imageRegionOfInterest



# TODO(unknown):



class Cropper(object):
    """docstring for Cropper"""
    def __init__(self, arg):
        super(Cropper, self).__init__()
        # self.mainWnd = arg

    def CreateBoundingBox(self, dirSource, dirDest, filenameSource, isFirstEmpty = False, classNumber = "0", classNameList = None):
        # show UI
        # path <= image directory
        # classNameList <= ['cat', 'plant']
        # print('hello')
        #dirSource ---> 'd:/fsimages/dlkit/original'
        #dirDest   ---> 'd:/fsimages/dlkit'

        path = dirSource
        valid_images = ['.bmp','.jpg','.png','jpeg']
        # fileNames = []

        filename = filenameSource
        name, ext = os.path.splitext(filename)
        # if (firstEmpty == -1 and not os.path.exists(os.path.join(path,name + '.txt'))):
            # firstEmpty = qtd
        obj = imageRegionOfInterest(path)

        obj.isSavePoints = True
        obj.pathToSave = path
        obj.classNumber = classNumber
        obj.classNameList = classNameList

        obj.loadImage(filename)
        
        cv_window_name = 'Cropper'
        # print('========================> about to enter loop...')     
        wait = 10
        # keep looping until the 'q' key is pressed
        # while True:
        while  cv2.getWindowProperty(cv_window_name,cv2.WND_PROP_VISIBLE) >= 1:
            key = cv2.waitKey(33) & 0xFF
            #if key != 255:
            #    print("Key "+str(key))

            # refresh
            if key == ord("r"):
                print('refresh')
                obj.refresh()

            # save 
            elif key == ord("s"):
                print('savePoints')
                obj.savePoints()

            # change Class Number
            elif key >= ord("0") and key <= ord("9"):
                print('change Class to '+chr(key))
                obj.classNumber = chr(key)
                obj.RefreshSelectedClass()
            
            # change Class 0  (' key is left side 1 key)
            elif key == ord("'"):
                print('change Class to 0')
                obj.classNumber = "0"
                obj.RefreshSelectedClass()

            # # next image or spacebar
            # elif key == ord("n") or key==32:
            #     print('next image')
            #     obj.savePoints()
            #     break

            # # previus image
            # elif key == ord("p"):
            #     print('previus image')
            #     obj.savePoints()
            #     break

            # box to left
            elif key == ord("g"):
                print('box to left')
                obj.moveLastBox(-1,0)
            # box to right
            elif key == ord("h"):
                print('box to right')
                obj.moveLastBox(1,0)

            # box to up
            elif key == ord("y"):
                print('box to up')
                obj.moveLastBox(0,-1)
            # box to down
            elif key == ord("b"):
                print('box to down')
                obj.moveLastBox(0,1)


            # copy last bounding boxes
            elif key == ord("c"):
                print('copy last bounding boxes')
                obj.copyLastBoundingBoxes()
            
            # shift last bounding box
            elif key == ord("x"):
                print('shift last bounding box')
                obj.shiftLastBoundingBox()
            
            
            # quit
            elif key == ord("q") or key == 27 or cv2.getWindowProperty(cv_window_name,1)+wait == -1:
                # print('quit')
                # print('cv2.getWindowProperty(filename,1)+wait --->', cv2.getWindowProperty(cv_window_name,1)+wait)
                if len(obj.points)>0:
                    obj.savePoints()
                    self.SaveClassification(path, dirDest, filename)
                return
            
            wait = wait - 1 if wait > 0 else wait

        # print('========================> loop exited.')       





    def SaveClassification(self, path, destPath, filenameSource):
        margemArea = 0
        finalSquad = 200
        print('--------------> SaveClassification...')
        obj = imageRegionOfInterest(path)

        # valid_images = [".jpg",".gif",".png",".tga",".jpeg"]
        valid_images = ['.bmp','.jpg','.png','jpeg']

        filename = filenameSource
        name, ext = os.path.splitext(filename)

        if (not os.path.exists(os.path.join(path,name+".txt"))):
            print('-------txt does not exist-------')

        obj.setFileImage(filename)
        points = obj.loadBoxFromTxt() 
        print('len(points) == ', len(points))    
    
        if len(points)>0:
            obj.loadFromFile()
            boxNumber = 0
            for point in points:
                name, ext = os.path.splitext(filename)
                if margemArea!=0:
                    obj.extractBoxM(os.path.join(destPath,point[4]),name+"-"+str(boxNumber)+ext, point, margemArea, finalSquad)
                else:
                    # print('------------------------>', os.path.join(destPath,point[4]))
                    # obj.extractBox(os.path.join(destPath,point[4]),name+"-"+str(boxNumber)+ext, point)

                    filename_out = name + '_' + point[4] +'_'+str(boxNumber+1)+ext
                    obj.extractBox(destPath, filename_out, point)
                    # listData[0] =>filepath_1
                    # ...
                    # listData[n-1] =>filepath_n
                    # listData[-2]=>category
                    # listData[-1]=>index_class
                    listData = [destPath + '/' + filename_out, 'xxx', point[4]]
                    # self.mainWnd.addFilesToDataset(listData)
                boxNumber += 1

        

    
