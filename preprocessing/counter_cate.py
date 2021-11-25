import glob
import argparse
import sys
from preprocessing.zy_utils import json_to_instance


parser = argparse.ArgumentParser()
parser.add_argument('json_dir', default='', type=str, help='json file which need to be counted')
args = parser.parse_args()
jsons = glob.glob('{}/*.json'.format(args.json_dir))

def main():
    dic = {}
    for i in jsons:
        ret_dic = json_to_instance(i)
        shapes = ret_dic['shapes']
        for j in shapes:
            if j['label'] not in dic:
                dic[j['label']] = 1
            else:
                dic[j['label']] += 1
    a = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    total_defects = sum(dic.values())
    print(sorted(dic.keys()))
    print(a)
    print(len(a))
    print('目标汇总数：', total_defects)
    return len(a)

if __name__ == '__main__':
    main()
