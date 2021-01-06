import json
import glob
def parse_para(input_json):
    with open(input_json, 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)
        # shapes = ret_dic['shapes']
        # img_name = ret_dic['imagePath']
    return ret_dic
import os
def main():
    p_t = r'/Users/zhangyan/Desktop/jsons'
    with open(r'/Users/zhangyan/Desktop/cll.txt', 'a+') as fh:
        for k in os.listdir(p_t):
            jsons = glob.glob(r'/Users/zhangyan/Desktop/jsons/{}/*.json'.format(k))
            dic = {}
            for i in jsons:
                ret_dic = parse_para(i)
                shapes = ret_dic['shapes']
                for j in shapes:
                    if j['label'] not in dic:
                        dic[j['label']] = 1
                    else:
                        dic[j['label']] += 1
            a = sorted(dic.items(),key=lambda x:x[1],reverse=True)
            print(dic.keys())
            print(a)
            print(len(a))
            fh.write('{}:{}\n'.format(k,dic.keys()))
            fh.write('{}_{}\n\n'.format(a,len(a)))

if __name__ == '__main__':
    main()