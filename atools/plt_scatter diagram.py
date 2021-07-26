import sys
sys.path.append(r'/Users/zhangyan/Desktop/python_test/py/networks')
# from DDN import inference
# from IDGAN import IDGAN
# from GCANet import GCANet
from matplotlib import pyplot as plt


class plot():
    def __init__(self, x, y, index, net=None):
        self.x = x
        self.y = y
        self.index = index
        self.net = net
        self.len = len(index[x]) if len(index[x]) == len(index[y]) else print('num of index not match')

    def plot(self, name):
        parameter = {}
        num_params = 0
        c = ['b', 'b', 'b', 'b', 'b', 'b', 'b','b', 'r']  # 颜色设置
        if self.net is not None:
            for i in net:
                for param in i.parameters():
                    num_params += param.numel()
                parameter[str(i).split('(')[0]] = num_params / 1e6
                print('{} has {} million parameters'.format(str(i).split('(')[0], num_params / 1e6))  # 网络参数
        x = self.index[self.x]
        y = self.index[self.y]
        plt.axis([0.770, 1.000, 24.5, 40])  # 设置范围，四个数分别对应x的起点终点和y的起点终点
        # plt.axis([0.800, 0.200, 24.5, 40])  # 设置范围，四个数分别对应x的起点终点和y的起点终点
        # plt.xlabel(self.x+'(sec)', weight='roman')
        plt.xlabel(self.x, weight='roman')
        plt.ylabel(self.y+'(dB)', weight='roman')
        plt.scatter(x, y, c=c)
        plt.grid(color='gray', linewidth=0.2)
        for i in range(self.len):

            if i == 2:
                plt.annotate(name[i], xy=(self.index[self.x][i], self.index[self.y][i]),
                             xytext=(self.index[self.x][i] - 0.03, self.index[self.y][i] - 0.2), weight='roman')
            if i == 4:
                plt.annotate(name[i], xy=(self.index[self.x][i], self.index[self.y][i]),
                             xytext=(self.index[self.x][i] - 0.03, self.index[self.y][i] - 0.2), weight='roman')
            if i == 7:
                plt.annotate(name[i], xy=(self.index[self.x][i], self.index[self.y][i]),
                             xytext=(self.index[self.x][i] - 0.03, self.index[self.y][i] - 0.2), weight='roman')
            if i == 8:
                plt.annotate(name[i], xy=(self.index[self.x][i], self.index[self.y][i]),
                             xytext=(self.index[self.x][i] - 0.02, self.index[self.y][i] + 0.35), weight='roman')
            elif i == 0 or i == 1 or i == 3 or i == 5 or i == 6:
                plt.annotate(name[i], xy=(self.index[self.x][i], self.index[self.y][i]),
                             xytext=(self.index[self.x][i]+0.001, self.index[self.y][i]+0.3), weight='roman')

        # plt.show()
        plt.savefig('./scatter_diagrammetrics.png', dpi=500)

name = ['DDN','ID_CGAN','JORDER', 'DID-MDN', 'RESCAN', 'GCANeT', 'Attentive-GAN','ReMAEN', 'RMUN(ours)']  # 加入自己的网路名字
# net = [U_Net(), Dense_Unet(), R2AttU_Net(), CE_Net_(), ReRPP_Net()]  # 加入自己的网络类
net = []
index = {'SSIM': [0.938, 0.891, 0.970, 0.858, 0.975, 0.788, 0.927, 0.982, 0.984],
         'PSNR': [32.04, 25.88, 36.11, 25.70, 36.64, 25.25, 27.06, 37.80, 38.21]}  # 加入自己的指标
# index = {'Running time': [0.547, 0.286, 0.268, 0.532, 0.750, 0.312, 0.598, 0.531, 0.408],
#          'PSNR': [32.04, 25.88, 36.11, 25.70, 36.64, 25.25, 27.06, 37.80, 38.21]}  # 加入自己的指标

p = plot(x='SSIM', y='PSNR', index=index, net=net).plot(name)  # x横坐标 y纵坐标
# p = plot(x='Running time', y='SSIM', index=index).plot(name)  # x横坐标 y纵坐标
# p = plot(x='Running time', y='PSNR', index=index).plot(name)  # x横坐标 y纵坐标

