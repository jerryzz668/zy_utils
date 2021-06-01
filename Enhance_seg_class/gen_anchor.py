from os import listdir
from os.path import isfile, join
import argparse
#import cv2
import numpy as np
import sys
import os
import shutil
import random 
import math

width_in_cfg_file = 942
height_in_cfg_file = 500

def IOU(x,centroids):
    similarities = []
    k = len(centroids)
    for centroid in centroids:
        c_w,c_h = centroid
        w,h = x
        if c_w>=w and c_h>=h:
            similarity = w*h/(c_w*c_h)
        elif c_w>=w and c_h<=h:
            similarity = w*c_h/(w*h + (c_w-w)*c_h)
        elif c_w<=w and c_h>=h:
            similarity = c_w*h/(w*h + c_w*(c_h-h))
        else: #means both w,h are bigger than c_w and c_h respectively
            similarity = (c_w*c_h)/(w*h)
        similarities.append(similarity) # will become (k,) shape
    return np.array(similarities) 

def avg_IOU(X,centroids):
    n,d = X.shape
    sum = 0.
    for i in range(X.shape[0]):
        #note IOU() will return array which contains IoU for each centroid and X[i] // slightly ineffective, but I am too lazy
        sum+= max(IOU(X[i],centroids)) 
    return sum/n

def write_anchors_to_file(centroids,X,anchor_file):
    f = open(anchor_file,'w')
    
    anchors = centroids.copy()
    print(anchors.shape)

    for i in range(anchors.shape[0]):
        anchors[i][0]*=width_in_cfg_file
        anchors[i][1]*=height_in_cfg_file
         

    widths = anchors[:,0]
    sorted_indices = np.argsort(widths)

    print('Anchors = ', anchors[sorted_indices])
        
    for i in sorted_indices[:-1]:
        f.write('%0.2f,%0.2f, '%(anchors[i,0],anchors[i,1]))

    #there should not be comma after last anchor, that's why
    f.write('%0.2f,%0.2f\n'%(anchors[sorted_indices[-1:],0],anchors[sorted_indices[-1:],1]))
    
    f.write('%f\n'%(avg_IOU(X,centroids)))
    print()

def kmeans(X,centroids,eps,anchor_file):
    """
    X.shape = N * dim  N代表全部样本数量,dim代表样本有dim个维度
    centroids.shape = k * dim k代表聚类的cluster数,dim代表样本维度
    """
    print("X.shape=",X.shape,"centroids.shape=",centroids.shape)

    N = X.shape[0]
    iterations = 0
    k,dim = centroids.shape
    prev_assignments = np.ones(N)*(-1)    
    iter = 0
    old_D = np.zeros((N,k))

    while True:
        """
        D.shape = N * k N代表全部样本数量,k列分别为到k个质心的距离
        1. 计算出D
        2. 获取出当前样本应该归属哪个cluster
        assignments = np.argmin(D,axis=1)
        assignments.shape = N * 1 N代表N个样本,1列为当前归属哪个cluster
        numpy里row=0,line=1,np.argmin(D,axis=1)即沿着列的方向,即每一行的最小值的下标
        3. 将样本划分到相对应的cluster后,重新计算每个cluster的质心
           centroid_sums.shape = k * dim k代表刻个cluster,dim列分别为该cluster的样本在该维度的均值
        
        centroid_sums=np.zeros((k,dim),np.float)
        for i in range(N):
            centroid_sums[assignments[i]]+=X[i]     # assignments[i]为cluster x  将每一个样本都归到其所属的cluster.   
        for j in range(k):            
            centroids[j] = centroid_sums[j]/(np.sum(assignments==j))  #np.sum(assignments==j)为cluster j中的样本总量

        """
        D = [] 
        iter+=1           
        for i in range(N):
            d = 1 - IOU(X[i],centroids)
            D.append(d)
        D = np.array(D) # D.shape = (N,k)
        
        print("iter {}: dists = {}".format(iter,np.sum(np.abs(old_D-D))))
            
        assignments = np.argmin(D,axis=1)
        
        #每个样本归属的cluster都不再变化了,就退出
        if (assignments == prev_assignments).all() :
            print("Centroids = ",centroids)
            write_anchors_to_file(centroids,X,anchor_file)
            return

        #calculate new centroids
        centroid_sums=np.zeros((k,dim),np.float)
        for i in range(N):
            centroid_sums[assignments[i]]+=X[i]        
        for j in range(k):  
            print("cluster{} has {} sample".format(j,np.sum(assignments==j)))          
            centroids[j] = centroid_sums[j]/(np.sum(assignments==j))
        
        prev_assignments = assignments.copy()     
        old_D = D.copy()  

def gen_anchor():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-filelist', default = 'D:\\MakeSample\\train_seg\\shape_0018\\image_0018.txt', 
    #                     help='path to filelist\n' )
    # parser.add_argument('-output_dir', default = 'D:\\MakeSample\\train_seg\\shape_0018\\anchor', type = str, 
    #                     help='Output anchor directory\n' )  
    # parser.add_argument('-num_clusters', default = 0, type = int, 
    #                     help='number of clusters\n' )  
   
    # args = parser.parse_args()
    print("f")
    output_dir="E:\\DLNetwork\\datas\\screw\\yolov3\\shape_screw\\anchor"
    filelist="E:\\DLNetwork\\datas\\screw\\yolov3\\shape_screw\\train\\image_screw_Train.txt"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    f = open(filelist)
    print("f",f)
    lines = [line.rstrip('\n') for line in f.readlines()]
    
    #将label文件里的obj的w_ratio,h_ratio存储到annotation_dims
    annotation_dims = []
    for line in lines:               
        #line = line.replace('images','labels')
        #line = line.replace('img1','labels')
        line = line.replace('images','labels')        
        line = line.replace('.jpg','.txt')
        line = line.replace('.png','.txt')
        line = line.replace('.bmp','.txt')
        print(line)
        
        f2 = open(line)
        for line in f2.readlines():
            line = line.rstrip('\n')
            w,h = line.split(' ')[3:]            
            #print(w,h)
            annotation_dims.append(tuple(map(float,(w,h))))
    
    annotation_dims = np.array(annotation_dims)
  
    eps = 0.005
    argsnum_clusters=6
    if argsnum_clusters == 0:
        for num_clusters in range(1,10): #we make 1 through 10 clusters
            print(num_clusters) 
            anchor_file = join( output_dir,'anchors%d.txt'%(num_clusters))

            indices = [ random.randrange(annotation_dims.shape[0]) for i in range(num_clusters)]
            centroids = annotation_dims[indices]
            kmeans(annotation_dims,centroids,eps,anchor_file)
            print('centroids.shape', centroids.shape)
    else:
        anchor_file = join( output_dir,'anchors%d.txt'%(argsnum_clusters))

        ##随机选取args.num_clusters个质心
        indices = [ random.randrange(annotation_dims.shape[0]) for i in range(argsnum_clusters)]
        print("indices={}".format(indices))
        centroids = annotation_dims[indices]
        print("centroids=",centroids)

        ##
        kmeans(annotation_dims,centroids,eps,anchor_file)
        print('centroids.shape', centroids.shape)

gen_anchor()
