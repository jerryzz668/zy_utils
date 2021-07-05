import shutil
import json
import os
def get_bbox(points):
    x,y = zip(*points)
    return  max(x),max(y),min(x),min(y)
def parse_para(input_json):
    with open(input_json, 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)
    return ret_dic
def get_max_w_h(img_jsons,s):
    for i in os.listdir(img_jsons):
        if i.endswith('.json'):
            try:
                ret_dic = parse_para(os.path.join(img_jsons,i))
                shapes = ret_dic['shapes']
                img_name = ret_dic['imagePath']
                json_name = img_name.replace('.jpg','.json')
                for j in shapes:
                    label = j['label']
                    if not 'liangpin' in label:
                        if not 'moxing' in label :
                            shutil.move(os.path.join(img_jsons,img_name),os.path.join(s,img_name))#移动图像文件
                            shutil.move(os.path.join(img_jsons,json_name),os.path.join(s,json_name))#移动图像文件
                            break
            except:
                continue
    return 0
def save_json(dic,save_path):
    json.dump(dic, open(save_path, 'w',encoding='utf-8'), indent=4)
def get_max_w_h1(img_jsons,s,label_dic):
    for i in os.listdir(img_jsons):
        if i.endswith('.json'):
            ret_dic = parse_para(os.path.join(img_jsons,i))
            shapes = ret_dic['shapes']
            img_name = ret_dic['imagePath']
            for j in shapes:
                label = j['label']
                if label in label_dic:
                    j['label']=label_dic[label]
            save_json(ret_dic,os.path.join(s,i))
    return 0

img_jsons = r'D:\BaiduNetdiskDownload\0425-now_loushi_cm\img\jsons1'
save_p = r'D:\BaiduNetdiskDownload\0425-now_loushi_cm\img\jsons'

# label_dic = {0:'良品',1:'异色',2:'白点',3:'3',4:'刮伤',5:'擦伤',6:'黑点',7:'砂痕印',8:'异物',
#              9:'刀纹',10:'刮伤',11:'喷砂不均',12:'应力痕',13:'凸凹痕',14:'凹凸痕',
#              15:'凹坑',16:'16',17:'17',18:'18',19:'碰伤',20:'碰伤',21:'21',22:'刀纹线',23:'塌边',24:'颗粒',
#              25:'毛絮',26:'线痕',27:'掉漆',28:'变形',29:'加铣',
#              30:'过切',31:'31',32:'32',33:'凹凸痕1',34:'凹凸痕2'}#图像和名字对应表
# label_dic = {'1':'yise','2':'baisezaodian','3':'shuiyin','4':'guashang','5':'cashang','6':'heidian',
#              '7':'shahenyin','8':'yiwu','9':'daowen','10':'huashang','11':'penshabujun','12':'aohen',
#              '13':'tuhaohen','14':'aotuhen','15':'aokeng','16':'mian','17':'qingweimianhua','18':'qita',
#              '19':'pengshang','20':'pengshang','21':'huanxingdaowen','22':'daowenxian','23':'tabian','27':'pengshang'}#图像和名字对应表
label_dic = {'heidian':'heidian', 'guashang-heiduan':'guashang', 'guashang-heizhang':'guashang', 'yise-hei':'yise',
'pengshang-mian':'pengshang', 'guashang-baiduan':'guashang', 'daowen-mian':'daowen', 'daowen-dantiao':'daowen','yise-heitiao':'yise',
'pengshang-zhang':'pengshang', 'yise-bai':'yise', 'guashang-baizhang':'guashang', 'penshabujun-bai':'pengshang','yise-hui':'yise','yise-baitiao':'yise',
             'tabian-an':'tabian','baisezaodian':'baidian','pengshang-bian':'pengshang','pengshang-bian':'pengshang','yise-liang':'yise',
             'tabian-an':'tabian','pengshang-jiao':'pengshang','yise-liang':'yise','daowen-jiao':'daowen','penshabujun-hei':'pengshabujun','tabian-liang':'tabian'}
get_max_w_h1(img_jsons,save_p,label_dic)
