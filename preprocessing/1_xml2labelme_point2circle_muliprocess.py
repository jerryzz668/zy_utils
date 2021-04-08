import json
from xml.etree import ElementTree as ET
import os
import time
import pypinyin
import multiprocessing
'''
该程序主要将mark工具标注的xml数据转为labelme格式的json                                                   
                       
'''
def pinyin(word):#zhangshan = pinyin('张山')
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        # pinyin return [[py1],[py2],...,[pyn]]
        s += i[0].strip()
    return s
def transform_xml_2labelme(para):
    xml_path,save_json,image_name = para
    transform_shapes_dic = {'polygon':'polygon','line':'linestrip','bndbox':'rectangle','point':'circle','ellipse':'circle'}
    tree = ET.parse(xml_path)
    root_node = tree.getroot()
    imagePath = '{}.jpg'.format(image_name)
    xmlPath = root_node[0].text
    imageWidth =int(root_node[4][0].text) #json_obj['imageWidth']=0
    imageHeight = int(root_node[4][1].text)#json_obj['imageHeight']=0
    imageDepth = int(root_node[4][2].text)#null
    imageLabeled = root_node[3] .text
    time_Labeled = root_node[2].text
    shapes = []
    for i in root_node[1][0]:
        dic_instance = {}
        dic_instance['label']=pinyin(i[0].text)
        points_l = []
        point_axis = []
        flag = 0
        #print('kd----------:',i[1].text,'--',i[2].tag)#像素宽度
        for j in i[2].iter():
            if flag !=0:
                #print('j.text,shape:',j.text,i[2].tag,i[1].text,)
                point_axis.append(float(j.text))
                if len(point_axis)==2:
                    points_l.append(point_axis)
                    point_axis=[]
            else:
                flag = 1
        #point2circle
        if i[2].tag=='point':
            r = int(i[1].text)/2
            x,y = points_l[0]
            r_x = x+r
            r_y = y+r
            points_l.append([r_x,r_y])
        #polygon <3 时转为 linestrip
        if i[2].tag=='polygon' and len(points_l)<3 and len(points_l)>1:
            dic_instance['shape_type'] = 'linestrip'
        else:
            dic_instance['shape_type']=transform_shapes_dic[i[2].tag]
        dic_instance['width']=i[1].text
        dic_instance['points'] = points_l
        dic_instance['group_id']=''
        dic_instance['flags']={}#i[3].text#state
        try:
            dic_instance['level'] = i[4].text#'level'
        except:
            #print('无照片严重程度')
            a=0
        try:
            dic_instance['mlevel'] = i[5].text#'mlevel'
        except:
            #print('无缺陷严重程度')
            a=0
        try:
            dic_instance['describe'] = i[6].text#'describe'
        except:
            #print('无描述')
            a=0
        shapes.append(dic_instance)
    dic_all = {}
    dic_all['version']='1.0'
    dic_all['flags']={}
    dic_all['shapes']= shapes
    dic_all['imagePath']=imagePath
    dic_all['xmlPath']=xmlPath
    print('正在处理：',imagePath)
    dic_all['imageData'] = None
    dic_all['imageHeight']=imageHeight
    dic_all['imageWidth']=imageWidth
    dic_all['imageDepth']= imageDepth
    dic_all['imageLabeled']=imageLabeled
    dic_all['time_Labeled']=time_Labeled
    with open(save_json,"w",encoding="utf-8") as f:
        content = json.dumps(dic_all, ensure_ascii=False)
        f.write(content)
        f.close()

def main(local_path,save_path,process_num=4):
    pool = multiprocessing.Pool(processes=process_num)  # 创建进程个数
    paras = []
    for i in os.listdir(local_path):
        xml_path = os.path.join(local_path,i)#xml_path
        image_name = i.split('.xml')[0]
        json_path = os.path.join(save_path,'{}.json'.format(image_name))
        paras.append((xml_path, json_path, image_name))
    pool.map(transform_xml_2labelme, paras)
    pool.close()
    pool.join()


if __name__ == "__main__":
    s = time.time()
    xml_outputs_path = r'C:\Users\Administrator\Desktop\241294293294723072\xml'
    json_save_path = r'C:\Users\Administrator\Desktop\241294293294723072\jsons'
    process_num = 8
    main(xml_outputs_path,json_save_path,process_num)
    print('run time:', time.time()-s)
