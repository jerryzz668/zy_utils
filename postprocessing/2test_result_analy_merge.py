import shutil
import json
import os
import numpy as np
def get_box(object1):
    xmin,ymin,w,h = object1['bbox']
    xmax,ymax = xmin+w,ymin+h
    return [xmin,ymin,xmax,ymax]
def get_box_score(object1):
    xmin,ymin,w,h = object1['bbox']
    xmax,ymax = xmin+w,ymin+h
    score = object1['score']
    return [xmin,ymin,xmax,ymax,score]
def save_json(dic,path):
    json.dump(dic, open(path, 'w',encoding='utf-8'), indent=4)
    return 0
def parse_para_train(input_json):#解析标注数据
    with open(input_json, 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)
        images = ret_dic['images']
        categories = ret_dic['categories']
        annotations = ret_dic['annotations']
    return (images,categories,annotations)
def imgs_id(images):#{’1‘：’123.jpg‘}
    dic = {}
    for i in images:
        dic[i['id']]=i['file_name']
    return dic
def cat_id(categories):#{'1':12,'2':'6'}
    dic = {}
    for i in categories:
        dic[i['id']]=i['name']
    return dic
def compute_iou(bbox1, bbox2):
    """
    compute iou
    :param bbox1:
    :param bbox2:
    :return: iou
    """
    bbox1xmin = bbox1[0]
    bbox1ymin = bbox1[1]
    bbox1xmax = bbox1[2]
    bbox1ymax = bbox1[3]
    bbox2xmin = bbox2[0]
    bbox2ymin = bbox2[1]
    bbox2xmax = bbox2[2]
    bbox2ymax = bbox2[3]
    area1 = (bbox1ymax - bbox1ymin) * (bbox1xmax - bbox1xmin)
    area2 = (bbox2ymax - bbox2ymin) * (bbox2xmax - bbox2xmin)
    bboxxmin = max(bbox1xmin, bbox2xmin)
    bboxxmax = min(bbox1xmax, bbox2xmax)
    bboxymin = max(bbox1ymin, bbox2ymin)
    bboxymax = min(bbox1ymax, bbox2ymax)
    if bboxxmin >= bboxxmax:
        return 0
    if bboxymin >= bboxymax:
        return 0
    area = (bboxymax - bboxymin) * (bboxxmax - bboxxmin)
    iou = area / (area1 + area2 - area)
    return iou
def single_img_annotation(annotations,thr=0,flag=0):#预测结果json,annotations=[{'image_id':1,...},{}]，flag=1预测标注；flag=0实际标注
    img_id_anno_dic={}
    c =0
    if flag:
        score_1 = 0
    for annotation in annotations:
        image_id = annotation['image_id']
        c+=1
        if flag:
            ss=annotation['score']
            if ss<thr:
                score_1+=1
        if image_id in img_id_anno_dic:
            img_id_anno_dic[image_id].append(annotation)
        else:
            img_id_anno_dic[image_id]=[annotation]
    if not flag:
        print('实际标注数量:',c)
    else:
        print('预测目标数量',c)
    return img_id_anno_dic#{'1':[{},{}]}
def parse_para_re(input_json,thr=0):
    with open(input_json, 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)
        anno = single_img_annotation(ret_dic,thr,1)
    return anno
def select_img(source_imgs_path,seg_path,save_path):
    img_dic = []

    for i in img_dic:
        source_img_path = os.path.join(source_imgs_path,i)
        save_img_path = os.path.join(save_path,i)
        json_name = i.split('.jpg')[0]
        source_jsons_path = os.path.join(source_imgs_path,'{}.json'.format(json_name))
        save_jsons_path = os.path.join(save_path,'{}.json'.format(json_name))
        shutil.copy(source_img_path,save_img_path)
        shutil.copy(source_jsons_path,save_jsons_path)

def l_g_ls(require,part,iou_thr):#过检记录：某个预测框与所有gt的iou等于0，表明该预测框为过检框,一张图预测不出结果时需要考虑漏检如何计算。
    result_l = []
    for j in require:
        result_flag = 0
        for k in part:
            bbox_gt = get_box(j)
            bbox_re = get_box(k)
            iou=compute_iou(bbox_gt,bbox_re)
            if iou<iou_thr:#<iou_thr:
                #print('iou:',iou),过检和漏检与gt的iou都为0
                result_flag+=1
        if result_flag==len(part):#iou为0的数量与所有预测标注的数量是否相等，若相等表明缺陷漏检，若为0的记录小于0则表明缺陷未漏检。
            result_l.append(j)
    return result_l
def jiandui_ls(require,part,iou_thr):
    jd=[]
    for j in require:
        for k in part:
            bbox_gt = get_box(j)
            bbox_re = get_box(k)
            iou=compute_iou(bbox_gt,bbox_re)
            if iou>=iou_thr:
                if not k in jd:
                    jd.append(k)
    return jd
def jiandui_nms_no_by_score_ls(require,part,iou_thr):
    jd=[]
    for j in require:
        for k in part:
            bbox_gt = get_box(j)
            bbox_re = get_box(k)
            iou=compute_iou(bbox_gt,bbox_re)
            if iou>=iou_thr:
                if not k in jd:
                    jd.append(k)
    return jd
def reg_right_ls(require,part,iou_thr):#过检记录：某个预测框与所有gt的iou等于0，表明该预测框为过检框,一张图预测不出结果时需要考虑漏检如何计算。
    result_l = []
    for j in require:#j为具体的一个标注
        pre_annotation={}
        iou_dic={}
        result_flag = 0
        flag_lost=0
        for k in part:
            bbox_gt = get_box(j)
            bbox_re = get_box(k)
            iou=compute_iou(bbox_gt,bbox_re)

            if iou<iou_thr:#<iou_thr:
                #print('iou:',iou),过检和漏检与gt的iou都为0
                result_flag+=1
            else:
                if iou in iou_dic:
                    iou_dic[iou].append(k)
                else:
                    iou_dic[iou]=[k]
        if result_flag==len(part):#iou为0的数量与所有预测标注的数量是否相等，若相等表明缺陷漏检，若为0的记录小于0则表明缺陷未漏检。
            result_l.append(j)
            flag_lost=1
        pre_annotation['annotation_content']=j#gt标注
        pre_annotation['pre_annotation']=iou_dic#有iou的所有预测
        pre_annotation['pre_best']=max(iou_dic)#最好的预测
        pre_annotation['pre_max_bbox']='merge_all_annotations'#最好预测合并bbox
        pre_annotation['pre_max_seg']='merge_all_annotations'#最好预测合并seg
        pre_annotation['lj_flag']=flag_lost#是否漏检，1漏检，0未漏检

    return result_l
'''
输入：图像的真实标注列表，图像的预测标注列表，
'''
def single_img_anno_in(gt_img_id_anno,re_img_id_anno,iou_thr):#gt:{'1':[{},{}],'2':[{},{}]},predict: {'1':[{},{}],'2':[{},{}]}
    all_merge = {}
    l_g_dic = {}
    lou_c = 0#86
    guojian_c=0#1096  ----1182----1525
    gt_c=0
    jd_c=0
    print('imgs_num:',len(re_img_id_anno))#计算漏检时考虑整张图无检出的情况
    no_reg = {}#全部未识别图
    all_no_reg = []#全部未识别图
    for i in gt_img_id_anno:#一张图
        gt_ann = gt_img_id_anno[i]#一张图的gt
        loujian=[]#一张图的漏检
        jiandui=[]
        try:
            re_ann = re_img_id_anno[i]
            gt_c+=len(gt_ann)
            loujian = l_g_ls(gt_ann,re_ann,iou_thr)#一张图的漏检
            lou_c+=len(loujian)
            guojian = l_g_ls(re_ann,gt_ann,iou_thr)#一张图的过检
            guojian_c+=len(guojian)
            jiandui = jiandui_ls(gt_ann,re_ann,iou_thr)#一张图检测对的
            jd_c += len(jiandui)
        except:
            no_reg[i]= gt_img_id_anno[i]
            lou_c+=len(gt_ann)#未检出出目标的图像gt为漏检
            gt_c+=len(gt_ann)
            loujian.extend(gt_img_id_anno[i])
        if len(gt_ann)==len(loujian):
            all_no_reg.append(i)
        l_g_dic[i]={'gt':gt_ann,'loujian':loujian,'guojian':guojian,'jiandui':jiandui}
        #print('l_g_dic[i]',l_g_dic[i])
    print('lou_c',lou_c,'guojian_c',guojian_c,'gt_c',gt_c,'jiandui_c',jd_c)
    # print('l_g_dic',l_g_dic)
    # lou_0=0
    # for i in l_g_dic:
    #     lou_0 += len(l_g_dic[i]['guojian'])
    # print('guojian',lou_0)
    return (l_g_dic,no_reg,all_no_reg)

def py_cpu_nms(dets, thresh):
    #print('det',dets)
    x1 = dets[:,0]
    y1 = dets[:,1]
    x2 = dets[:,2]
    y2 = dets[:,3]
    areas = (y2-y1+1) * (x2-x1+1)
    scores = dets[:,4]
    keep = []
    index = scores.argsort()[::-1]
    while index.size >0:
        i = index[0]       # every time the first is the biggst, and add it directly
        keep.append(i)
        x11 = np.maximum(x1[i], x1[index[1:]])    # calculate the points of overlap
        y11 = np.maximum(y1[i], y1[index[1:]])
        x22 = np.minimum(x2[i], x2[index[1:]])
        y22 = np.minimum(y2[i], y2[index[1:]])
        w = np.maximum(0, x22-x11+1)    # the weights of overlap
        h = np.maximum(0, y22-y11+1)    # the height of overlap

        overlaps = w*h
        ious = overlaps / (areas[i]+areas[index[1:]] - overlaps)
        idx = np.where(ious<=thresh)[0]
        index = index[idx+1]   # because index start from 1
    return keep
def get_guojian(czjson,data,savejson='guojian.json'):
    images,categories,annotations= parse_para_train(czjson)
    test_dic = {}
    test_dic['images'] = images
    test_dic['categories'] = categories
    test_dic['annotations'] = data
    save_json(test_dic,savejson)


if __name__ == '__main__':
    imgs_path = r'D:\work\data\microsoft\jalama\test1231\testdataset\test1231'#imgs_nums=1667,annotations_nums=2528,pre_annotations_nums=10376
    coco_json = r'C:\Users\xie5817026\PycharmProjects\pythonProject1\1228\instances_test1231pre.json'
    pre_json = r'C:\Users\xie5817026\PycharmProjects\pythonProject1\1228\1231.segm.json'
    out_p = r'C:\Users\xie5817026\PycharmProjects\pythonProject1\1228'
    savejson_flag = '310_cut'
    score_thr=0.6
    iou_thr = 0.5
    images,categories,annotations = parse_para_train(coco_json)
    img_id_dic=imgs_id(images)#img_id-->name
    dic_cateies= cat_id(categories)#cate_id-->cate_name
    gt_img_id_anno = single_img_annotation(annotations)

    re_img_id_anno = parse_para_re(pre_json,score_thr)
    print('re_img_id_anno',len(re_img_id_anno))
    print('gt_img_id_anno',len(gt_img_id_anno))
    #lost_img_name,regc_img_name,json_data_gt,json_data_rec = single_img_anno_in(gt_img_id_anno,re_img_id_anno)
    l_g_dic,no_reg,all_no_reg = single_img_anno_in(gt_img_id_anno,re_img_id_anno,iou_thr)
    jd_nms_after = []
    jd_nms_before = []
    for img_id in l_g_dic:
        jiandui = l_g_dic[img_id]['jiandui']
        #print(jiandui)
        boxxes = []
        for anno_obj in jiandui:
            bbox = get_box_score(anno_obj)
            boxxes.append(bbox)
            jd_nms_before.append(anno_obj)
        #print(boxxes)#所有框
        if len(boxxes)==0:
            print('det is zero')
        else:
            keep = py_cpu_nms(np.array(boxxes), thresh=0.1)#抑制后的索引
            nms_after = np.array(boxxes)[keep]
            #print('keep:',keep)
            nms_af_jiandui = []
            for index_s in keep:
                nms_af_jiandui.append(jiandui[index_s])
                jd_nms_after.append(jiandui[index_s])
            #print('nms_before',len(annotations),'after',len(nms_after),len(nms_af_jiandui))
            #print(nms_af_jiandui)

    print('抑制前',len(jd_nms_before),'抑制后',len(jd_nms_after),'rate',len(jd_nms_after),len(jd_nms_before))

    #过检数据过滤
    data_guojian = []
    data_loujian = []
    data_jiandui = []
    for img_id in l_g_dic:
        guojian = l_g_dic[img_id]['guojian']
        loujian = l_g_dic[img_id]['loujian']
        jiandui = l_g_dic[img_id]['jiandui']
        data_guojian.extend(guojian)
        data_loujian.extend(loujian)
        data_jiandui.extend(jiandui)
    s_j = os.path.join(out_p,'{}jiandui_nms.json'.format(savejson_flag))
    # get_guojian(coco_json,data_guojian,savejson='{}guojian.json'.format(savejson_flag))
    # get_guojian(coco_json,data_loujian,savejson='{}loujian.json'.format(savejson_flag))
    # get_guojian(coco_json,data_jiandui,savejson='{}jiandui.json'.format(savejson_flag))
    get_guojian(coco_json,jd_nms_after,savejson=s_j)
    #print('louguo:',dic_lg)
    # lost_img_gt_set = r'C:\Users\xie5817026\PycharmProjects\pythonProject1\1223\l.json'
    # # lost_img_rec_set = 'D:\work\data\microsoft\jalama\second_data_merge_3\jalama_160_test_rec.segm.json'
    # lost_save=r'D:\work\data\microsoft\jalama\fourthdata\tt\lost'
    # imgs_p = r'D:\work\data\microsoft\jalama\fourthdata\tt\imgs'
    # print('no_reg',all_no_reg)
    #select_img(source_imgs_path=imgs_path,img_dic=no_reg,save_path=lost_save)
    # select_img(source_imgs_path=imgs_path,img_dic=regc_img_name,save_path=save_baidu)
    # print('所有未识别的图像：',len(lost_img_name))
    #漏检3%
    #nms结果
