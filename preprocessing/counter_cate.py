import json
import glob
def parse_para(input_json):
    with open(input_json, 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)
        # shapes = ret_dic['shapes']
        # img_name = ret_dic['imagePath']
    return ret_dic

def main():
    jsons = glob.glob(r'G:\weiruan_report\hongxing\gt\*.json')
    dic = {}
    gt_num =[]
    for i in jsons:
        ret_dic = parse_para(i)
        shapes = ret_dic['shapes']
        for j in shapes:
            if j['label'] not in dic:
                dic[j['label']] = 1
            else:
                dic[j['label']] += 1
    a = sorted(dic.items(),key=lambda x:x[0],reverse=False)
    print(dic.keys())
    print(a)
    for cls, num in a:
        gt_num.append(num)
    print(len(a))
    print(gt_num)

if __name__ == '__main__':
    main()