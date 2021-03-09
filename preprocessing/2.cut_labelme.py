import json
import os
import cv2
import math
import glob
import multiprocessing
import time
'''
@Description: 根据给定size(w,h)和标注切图
            主要功能：将mark工具标注的xml标注转为json标注，方便labelme查看及生成coco格式数据
            关键处理：1.将全图标注数据根据给定size计算终止切图策略，由digui函数实现；
                    2.切图策略计算过程中，记录最新框的中心位置；
                    3.计算切图的大小和对应新json中坐标位置；
                    4.超出边界的目标切落在区域内的。
@author: lijianqing
@date: 2020/11/24 16:45
@return 
'''
def save_json(dic,save_path):
    json.dump(dic, open(save_path, 'w',encoding='utf-8'), indent=4)
def save_new_img(img_np,img_name,xmin,ymin,xmax,ymax,out_path,img_x,img_y):
    # 切图并保存
    xmin,ymin,xmax,ymax = int(xmin),int(ymin),int(xmax),int(ymax)
    left,top,right,down = 0,0,0,0#need padding size
    if xmax>img_x:
        right = xmax-img_x
        xmax=img_x
        # print('out of width')
    if ymax>img_y:
        down = ymax-img_y
        ymax=img_y
        # print('out of hight')
    if ymin<0:
        top = abs(ymin)
        ymin=0
        # print('out of hight')
    if xmin<0:
        left = abs(xmin)
        xmin=0
        # # print('out of width')
    img_crop = img_np[ymin:ymax,xmin:xmax]
    ret = cv2.copyMakeBorder(img_crop, top, down, left, right, cv2.BORDER_CONSTANT, value=(0,0,0))#padding
    cv2.imwrite(os.path.join(out_path, img_name), ret)
    return 0
def count_bbox_size(per_object):
    points = per_object['points']
    x,y = zip(*points)#split x,y
    if per_object['shape_type']=='circle':
        center_point = points[0]
        r_p = points[1]
        r = round(math.sqrt((center_point[0]-r_p[0])**2+(center_point[1]-r_p[1])**2),2)
        min_x = round(center_point[0]-r,2)
        min_y = round(center_point[1]-r,2)
        max_x = round(center_point[0]+r,2)
        max_y = round(center_point[1]+r,2)
    else:
        min_x = round(min(x),2)
        min_y= round(min(y),2)
        max_x = round(max(x),2)
        max_y = round(max(y),2)
    # print('max_x,max_y,min_x,min_y',max_x,max_y,min_x,min_y,'---',i['shape_type'])
    return  max_x,max_y,min_x,min_y
def get_new_location(point,mid_point,crop_w=64,crop_h=64):
    #将缺陷放于中心位置
    p_x = point[0]-mid_point[0]+crop_w/2
    p_y = point[1]-mid_point[1]+crop_h/2
    if p_x<0:
        p_x=0
    if p_y<0:
        p_y=0
    if p_x>crop_w:
        p_x=crop_w
    if p_y>crop_h:
        p_y=crop_h
    return [p_x,p_y]
def cut_json(file_tuple):
    json_p,img_sourc,crop_w,crop_h,out_p_im,cut_label,counter_per_cut=file_tuple
    with open(json_p, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    img_n = os.path.join(img_sourc,json_data['imagePath'])#原图像名
    print('img_n',img_n)
    img_np = cv2.imread(img_n)#原图数据
    # print('img_np',img_n)
    shapes_img_l = {}
    c = 0
    #筛选需要切的label
    for i in json_data['shapes']:
        c+= 1
        if i['label'] in cut_label:
            shapes_img_l[c]=i
    #print(shapes_img_l)
    cut_one_img = []
    mid_point = []
    # try:
    recursion_cut(shapes_img_l,counter_per_cut,crop_w,crop_h,cut_one_img,mid_point)#聚类
    # except:
    #     print('-------',json_p)
    ###core    start
    #print('cut_one_img',cut_one_img)
    for index_object in range(len(cut_one_img)):
        for shapes_object in cut_one_img[index_object]:
            new_points = []
            for loc in shapes_object['points']:
                n_p = get_new_location(loc,mid_point[index_object],crop_w,crop_h)
                new_points.append(n_p)
            shapes_object['points'] = new_points
        new_name_img = '{}_{}_{}.jpg'.format(mid_point[index_object][0],mid_point[index_object][1],index_object)
        new_name_json = '{}_{}_{}.json'.format(mid_point[index_object][0],mid_point[index_object][1],index_object)
        #生成新的img文件，抠图过程中会出现超出边界的坐标
        source_x_min,source_x_max = mid_point[index_object][0]-crop_w/2,mid_point[index_object][0]+crop_w/2#抠图位置
        source_y_min,source_y_max= mid_point[index_object][1]-crop_h/2,mid_point[index_object][1]+crop_h/2
        x_min,x_max,y_min,y_max = int(source_x_min),int(source_x_max),int(source_y_min),int(source_y_max)
        save_new_img(img_np,new_name_img,x_min,y_min,x_max,y_max,out_p_im,json_data['imageWidth'],json_data['imageHeight'])
        #生成新的json文件
        # crop_szie_w,crop_szie_h = crop_szie,crop_szie
        def_new_json(json_data,crop_w,crop_h,new_name_json,cut_one_img[index_object],out_p_im,new_name_img)
def def_new_json(json_data,crop_szie_w,crop_size_h,new_name,shapes_img,out_p,new_name_img):
    new_json = {}
    new_json['flags'] = json_data['flags']
    new_json['imageData'] = None
    new_json['imageDepth'] = json_data['imageDepth']
    new_json['imageHeight'] = crop_size_h
    new_json['imageLabeled'] = json_data['imageLabeled']
    new_json['imagePath'] = new_name_img
    new_json['imageWidth'] = crop_szie_w
    new_json['shapes'] = shapes_img
    new_json['time_Labeled'] = json_data['time_Labeled']
    new_json['version'] = json_data['version']
    save_json(new_json,os.path.join(out_p,new_name))
    # print('生成了',os.path.join(out_p,new_name))
    return new_json
def def_dic_element(shapes_img,i,points):
    dic_element = {}
    dic_element['flags']=i['flags']
    dic_element['group_id']=i['group_id']
    dic_element['label']=i['label']
    dic_element['points'] = points
    dic_element['shape_type']=i['shape_type']
    dic_element['width']=i['width']
    shapes_img.append(dic_element)
    return shapes_img

def recursion_cut(shapes_img_l,counter_per_cut,crop_w,crop_h,cut_one_img,mid_point):
    counter_per_cut += 1
    if len(shapes_img_l)==0:
        #print('递归结束了',counter_per_cut)
        return 0
    next_allow = {}#记录不可以放一起的标注
    allow = []
    max_bbox = []
    for i in shapes_img_l:
        max_x,max_y,min_x,min_y = count_bbox_size(shapes_img_l[i])#获取标注的位置
        w,h = max_x-min_x,max_y-min_y
        #与已有点比较距离
        if len(max_bbox)>0:
            a,b,c,d = max_bbox
            mmin_x = min(min_x,c)
            mmin_y = min(min_y,d)
            mmax_x = max(max_x,a)
            mmax_y = max(max_y,b)
            ww,hh = mmax_x-mmin_x,mmax_y-mmin_y
            # print('最大长宽',ww,hh)
            if ww<crop_w and hh <crop_h:
                max_bbox = mmax_x,mmax_y,mmin_x,mmin_y
                allow.append(shapes_img_l[i])
            else:
                next_allow[i]=shapes_img_l[i]#不可以放一起的
        else:
            max_bbox = [max_x,max_y,min_x,min_y]
            allow.append(shapes_img_l[i])
    #计算聚类后类别在原图的中心点。
    w,h = max_bbox[0]-max_bbox[2],max_bbox[1]-max_bbox[3]
    mid_x = math.ceil(max_bbox[2]+w/2)
    mid_y = math.ceil(max_bbox[3]+h/2)
    # print('中心点',math.ceil(mid_x),math.ceil(mid_y))
    cut_one_img.append(allow)
    mid_point.append((mid_x,mid_y))
    recursion_cut(next_allow,counter_per_cut,crop_w,crop_h,cut_one_img,mid_point)

if __name__ == '__main__':
    root_path = r'/Users/zhangyan/Desktop/dataset1_2000/train'

    out_path_root = root_path[:root_path.rindex(os.sep)+1]
    out_path = '{}/crop'.format(out_path_root)
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    json_source='{}/jsons'.format(root_path)
    imgs_path = '{}/imgs'.format(root_path)
    cut_label = ['guashang','pengshang','yise','heidian','penshabujun','baidian','aohen','shahenyin','daowen','maoxu','tabian','tubao','aokeng']
    # cut_label = ['maoxu', 'tubao', 'guashang', 'aohen', 'heidian']

    jsons = glob.glob('{}/*.json'.format(json_source))
    para_list = []
    counter_per_cut = 0
    for json_path in jsons:
        para_list.append((json_path,imgs_path,640,640,out_path,cut_label,counter_per_cut))
    pool = multiprocessing.Pool(processes=32)
    start_time = time.time()
    pool.map(cut_json,para_list)
    print('run time:',time.time()-start_time)
    pool.close()
    pool.join()