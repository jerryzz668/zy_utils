import json
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--json_dir', default='', type=str, help='json file which need to be counted')
args = parser.parse_args()


def parse_para(input_json):
    with open(input_json, 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)
        # shapes = ret_dic['shapes']
        # img_name = ret_dic['imagePath']
    return ret_dic

def main():
    jsons = glob.glob('{}/*.json'.format(args.json_dir))
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

if __name__ == '__main__':
    main()
