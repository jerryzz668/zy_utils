import os
import xlrd
import numpy as np 
import matplotlib.pyplot as plt 
input_dir = '/home/jerry/Desktop/report/A.xlsx'

book = xlrd.open_workbook(input_dir)

print(book)

# class_name = ['aokeng', 'baidian', 'daowen', 'guashang', 'heidian', 'pengshang', 'shahenyin', 'tabian', 'yise1', 'yise2', 'yiwu']

# n = len(class_name)

for sheet in book.sheets():

    print(sheet.name)
    # needed_info = []
    loujian_num = []
    loujian_rate = []
    guojian_num = []
    # guojian_rate_a = []
    guojian_rate = []
    confidence = []
    nrows = sheet.nrows
    ncols = sheet.ncols
    for i in range(nrows):
        row_value = sheet.row_values(i)
        row_value = [i for i in row_value if i!='']
        # print(row_value)

        if 'confidence' in row_value:
            # print(row_value[1])
            confidence.append(row_value[1])
            # print(confidence)
        if 'gt数量' in row_value:
            gt_num = row_value[1:]
        if '指标' in row_value:
            class_name = row_value[1:]
      
        if '漏检数' in row_value:
            loujian_num.append(row_value[1:])
        if '漏检率' in row_value:
            loujian_rate.append(row_value[1:])
        if '过检数' in row_value:
            guojian_num.append(row_value[1:])
        # if '模型过检率' in row_value:
        #     guojian_rate_a.append(row_value[1:12])
        if '现场过检率' in row_value:
            guojian_rate.append(row_value[1:12])

    loujian_num = np.array(loujian_num)
    
    guojian_num = np.array(guojian_num)
    loujian_rate = np.array(loujian_rate)
    guojian_rate = np.array(guojian_rate)
    plt.figure(figsize=(20,15))  # 调整窗口大小

    for i, name_ in enumerate(class_name):

        print(name_)
        loujian_n = loujian_num[:,i]
        guojian_n = guojian_num[:,i]           
        # print(y)
        gt_n = int(gt_num[i])
        plt.subplot(3,4,i+1)  # 3行4列
        plt.plot(confidence, loujian_n, color='red', label='loujian_num')
        plt.plot(confidence, guojian_n, color='blue', label='guojian_num')
        plt.xlabel('score')
        plt.ylabel('frenquency')
        plt.legend()
        plt.title(name_ + '(' + str(gt_n) + ')')


        # loujian_r = loujian_rate[:,i]
        # guojian_r = guojian_rate[:,i]           
        # plt.subplot(212)
        # plt.plot(confidence, loujian_r, color='red', label='loujian_rate')
        # plt.plot(confidence, guojian_r, color='blue', label='guojian_rate')
        # plt.xlabel('score')
        # plt.ylabel('rate')
        # plt.legend()
        # plt.title(name_)

    # plt.show()
    plt.savefig(str(sheet.name)+'.png')

            


    # for 
    

