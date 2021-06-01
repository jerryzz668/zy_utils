import json
import cv2
import os
os.path.abspath(r'C:\Users\xie5817026\PycharmProjects\pythonProject1\guashang\result')
from ljq_img_utils import seg2sourceimg as s2img
def parse_para(input_json,dic_img):
    with open(input_json, 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)
        im_id={}
        for ll in ret_dic:
            idd = ll['image_id']
            if idd in im_id:
                im_id[idd] += 1
            else:
                im_id[idd] = 1
        print('-----',im_id)
        dic = {}
        # thr_dic = {'yise':0.05,'heidian':0.01,'guashang':0.05}
        thr_dic = {'yise':0.05,'heidian':0.01,'guashang':0.05, 'daowen': 1, 'penshabujun': 1,
                   'yise': 1, 'cashang':1, 'shuiyin': 1, 'shahenyin': 1, 'aotuhen': 1, 'mianhua': 1,'cashang': 1, 'shuiyin': 1, 'shahenyin': 1, 'aotuhen': 1, 'mianhua': 1}
        c_dic = {'yise':(0,192,255),'heidian':(192,192,255),'guashang':(0,0,255),'daowen':(192,0,255),'penshabujun':(192,192,192),
                 'yise':(255,0,0),'cashang':(192,0,0),'shuiyin':(192,192,0),'shahenyin':(100,100,100),'aotuhen':(120,0,0),'mianhua':(0,255,0),'cashang':(192,0,0),'shuiyin':(192,192,0),'shahenyin':(100,100,100),'aotuhen':(120,0,0),'mianhua':(0,255,0)}#[(0,255,0),(0,0,255),(255,0,0)]
        cat_index = {0:'yise',1:'heidian',2:'guashang', 3: 'daowen', 4: 'penshabujun',
                     5: 'yise', 6: 'cashang', 7: 'shuiyin', 8: 'shahenyin', 9: 'aotuhen', 10: 'mianhua',11:'heidian',12:'guashang', 13: 'daowen', 14: 'penshabujun',
                     15: 'yise', 16: 'cashang',}
        for i in ret_dic:
            image_id = i['image_id']
            bbox = i['bbox']
            score = i['score']
            category_id = i['category_id']
            segmetation = i['segmentation']
            c_name = cat_index[category_id]
            if score>=thr_dic[c_name]:
                category_id = i['category_id']
                # print('category_id---',category_id)
                # print('image_id',image_id)
                f_n = dic_img[image_id]
                l_t = (int(bbox[0]),int(bbox[1]))
                r_d = (int(bbox[0]+bbox[2]),int(bbox[1]+bbox[3]))
                try:
                    l_b = '{}_{}'.format(cat_index[category_id],round(score,4))
                except:
                    print('类别异常',category_id)
                if f_n in dic:
                    dic[f_n].append((f_n,l_t,r_d,l_b,c_dic[cat_index[category_id]],segmetation))
                else:
                    dic[f_n]=[(f_n,l_t,r_d,l_b,c_dic[cat_index[category_id]],segmetation)]
    return dic
    #return 0#(images,categories,annotations)
def save_json(dic,path):
    json.dump(dic, open(path, 'w'))
    return 0
def parse_para_train(input_json):
    with open(input_json, 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)
        images = ret_dic['images']
        categories = ret_dic['categories']
        annotations = ret_dic['annotations']
    return (images,categories,annotations)

def imgs_id(images):
    dic = {}
    for i in images:
        dic[i['id']]=i['file_name']
    return dic
def cat_id(categories):
    dic = {}
    for i in categories:
        dic[i['id']]=i['name']
    return dic

import cv2
import os
def draw_bbox(img,left_top,right_down,color,label,seg):
    cv2.rectangle(img, left_top, right_down, color,1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, label, left_top, font, 1, color, 1)
    img = s2img(seg,img)
    return img

def iter_dic(dic,source_p,save_p):
    for i in dic:
        print('dic[i]:---',len(dic[i]))
        img = cv2.imread(os.path.join(source_p, i))
        for j in dic[i]:
            f_n, l_t, r_d, l_b, c_l,seg = j
            img=draw_bbox(img, l_t, r_d,c_l, l_b,seg)

        cv2.imwrite(os.path.join(save_p,i),img)
if __name__ == '__main__':
    imgs_path = r'D:\work\data\microsoft\damian\damian_source\1027data\classfile\ds\gsyshd\x512cut\dataset\coco\coco\val2017'
    save_baidu = r'D:\work\data\microsoft\damian\damian_source\1027data\classfile\ds\gsyshd\x512cut\dataset\coco\coco\save_val'
    images,categories,annotations = parse_para_train(r'D:\work\data\microsoft\damian\damian_source\1027data\classfile\ds\gsyshd\x512cut\dataset\coco\coco\annotations\instances_val2017.json')
    img_id_dic=imgs_id(images)
    dic_cateies= cat_id(categories)
    dic = parse_para(r'C:\Users\xie5817026\PycharmProjects\pythonProject1\test_tools\.segm.json',img_id_dic)
    iter_dic(dic,imgs_path,save_baidu)
