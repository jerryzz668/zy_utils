"""
@Description:
@Author     : zhangyan
@Time       : 2021/8/31 下午5:36
"""

import matplotlib.pyplot as plt

x = [0, 2000, 4000, 6000, 8000, 10000,12000, 14000,16000, 18000, 20000, 22000, 24000,26000, 28000, 30000, 32000, 34000,36000, 38000,40000]
y1 = [8.7, 4.4, 5.6, 4.2, 4.8, 4, 3.2, 3.5, 3.1, 2.9, 2.7, 2.8, 2.6, 3.2, 2.5, 2.3, 2.2, 1.8, 1.5, 1.2, 1.5]
y2 = [6.7, 3.4, 5.9, 3.2, 4.7, 4, 3.1, 3.2, 2.8, 2.7, 2.5, 2.9, 2.3, 2.7, 1.8, 1.5, 1.4, 1.39, 1.45, 1.1, 1.2]



# 开始画图
# sub_axix = filter(lambda x:x%200 == 0, x)
# plt.title('识别准确率对比图', fontsize=9)
plt.plot(x, y1, color='blue', label='withoutCA')
plt.plot(x, y2, color='red', label='withCA')
# plt.plot(x, y3,  color='skyblue', label='CRNN')
plt.legend()  # 显示图例

# xticks(locs, [labels], **kwargs)  # Set locations and labels
# plt.xticks(x)  # 正常
# plt.xticks(x, ())  # 有刻度，不现实值
# plt.xticks(x, ('Tom', 'Dick', 'Harry', 'Sally', 'Sue', 'Lily'), color='blue', rotation=60)  # 显示label上的文字
# plt.xticks([])  # x轴数值隐藏

# yticks the same as xticks


miny = -0.94135359  # 下限载荷
maxy = 0.8470985  # 上限载荷

# plt.axis([0, 5, 0, 60])  # 最大坐标视窗
# plt.axhline(miny,color="Red")    # 画参考线方法一
# plt.axhline(maxy,color="Red")    # 画参考线方法一

# plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签


plt.xlabel('step', fontsize=9)
plt.ylabel('loss', fontsize=9)
plt.show()
# plt.savefig('./result.jpg', dpi = 500)