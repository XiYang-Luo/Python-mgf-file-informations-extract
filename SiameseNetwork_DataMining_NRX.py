 # -*- coding:utf-8 -*-
#---------------------------------
# This is a Demo of SiameseNetwork
# Use pytorch.
# March 28,2019, created by qincy
#---------------------------------

import os
import logging
from pyteomics.mgf import read
from torch.utils import data
import matplotlib.pyplot as plt
from numpy import concatenate
import numpy as np
import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
import pandas as pd

class NewMGFDataSet(data.dataset.Dataset):

    def __init__(self, mgf_file, csv_file):
        if not os.path.exists(mgf_file):
            raise RuntimeError("Can not find mgf file: '%s'" % mgf_file)
        if not os.path.exists(csv_file):
            raise RuntimeError("Can not find csv file: '%s'" % csv_file)
        self.MGF = {}
        self.mgf_dataset = []
        self.load_file(mgf_file, csv_file)
        self.transform()

    def load_file(self, mgf_path, csv_path):
        print('Start to load file data...')
        info = pd.read_csv(csv_path, header=None)
        self.spectrum1 = info[0].tolist()
        self.spectrum2 = info[1].tolist()
        self.label = info[2].tolist()
        for mgf in read(mgf_path, convert_arrays=1):
            self.MGF[mgf.get('params').get('title')] = mgf
        print('Finish to load data...')

    def transform(self):
        print('Start to calculate data set...')

        global spectrum_dict
        spectrum_dict = {}

        #五百个参考的谱图
        # rfDataFrame = pd.read_csv("../Data/500RfSpectraBinData.csv", header=None, index_col=None)
        # reference_intensity = rfDataFrame.values

        peakslist1, precursor_feature_list1 = [], []
        peakslist2, precursor_feature_list2 = [], []
        for s1, s2, l in zip(self.spectrum1, self.spectrum2, self.label):
            s1 = self.MGF[s1]
            s2 = self.MGF[s2]

            bin_s1 = self.bin_spectrum(s1.get('m/z array'), s1.get('intensity array'))
            peakslist1.append(bin_s1)

            mass1 = float(s1.get('params').get('pepmass')[0])
            charge1 = int(s1.get('params').get('charge').__str__()[0])
            mz1 = mass1 / charge1
            precursor_feature1 = np.concatenate((self.gray_code(mass1), self.gray_code(mz1), self.charge_to_one_hot(charge1)))
            precursor_feature_list1.append(precursor_feature1)

            bin_s2 = self.bin_spectrum(s2.get('m/z array'), s2.get('intensity array'))
            peakslist2.append(bin_s2)

            mass2 = float(s2.get('params').get('pepmass')[0])
            charge2 = int(s2.get('params').get('charge').__str__()[0])
            mz2 = mass2 / charge2
            precursor_feature2 = np.concatenate((self.gray_code(mass2), self.gray_code(mz2), self.charge_to_one_hot(charge2)))
            precursor_feature_list2.append(precursor_feature2)

        intensList01 = np.array(peakslist1)
        intensList02 = np.array(peakslist2)
        # refMatrix = np.transpose(reference_intensity)

        # DPList01 = np.dot(intensList01, refMatrix)
        # DPList02 = np.dot(intensList02, refMatrix)

        precursor_feature_list1 = np.array(precursor_feature_list1)
        precursor_feature_list2 = np.array(precursor_feature_list2)

        label = np.array(self.label)

        # tmp01 = concatenate((DPList01, intensList01), axis=1)
        # tmp02 = concatenate((DPList02, intensList02), axis=1)
        spectrum01 = concatenate((intensList01, precursor_feature_list1), axis=1)
        spectrum02 = concatenate((intensList02, precursor_feature_list2), axis=1)

        label = np.array(label.reshape(label.shape[0], 1))
        tmp_data = concatenate((spectrum01, spectrum02), axis=1)
        self.mgf_dataset = concatenate((tmp_data, label), axis=1)

        del self.MGF
        print('Finish to calculate data set...')

    def __getitem__(self, item):
        return self.mgf_dataset[item]

    def __len__(self):
        return len(self.mgf_dataset)

    def gray_code(self, number):
        """
        to get the gray code:\n
            1. a = get the num's binary form
            2. b = shift a one bit from left to right, put zero at the left position
            3. gray code = a xor b
            bin(num ^ (num >> 1))
        :param number:
        :return:np.array  gray code array for num
        """
        # assert num.is_integer(), 'Parameter "num" must be integer'
        number = np.int(number)
        # we need 27-bit "Gray Code"
        bit = 27
        shift = 1
        gray_code = np.binary_repr(np.bitwise_xor(number, np.right_shift(number, shift)), bit)
        # print(type(gray_code))
        return np.asarray(' '.join(gray_code).split(), dtype=float)

    def charge_to_one_hot(self, c: int):
        """
        encode charge with one-hot format for 1-7
        :param c:
        :return:
        """
        maximum_charge = 7
        charge = np.zeros(maximum_charge, dtype=float)
        # if charge bigger than 7, use 7 instead
        if c > maximum_charge: c = maximum_charge
        charge[c - 1] = c
        return charge

    def get_bin_index(self, mz, min_mz, bin_size):
        relative_mz = mz - min_mz
        return max(0, int(np.floor(relative_mz / bin_size)))

    def bin_spectrum(self, mz_array, intensity_array, max_mz=2500, min_mz=50.5, bin_size=1.0005079):
        """
        bin spectrum and this algorithm reference from 'https://github.com/dhmay/param-medic/blob/master/parammedic/binning.pyx'
        :param mz_array:
        :param intensity_array:
        :param max_mz:
        :param min_mz:
        :param bin_size:
        :return:
        """
        key = mz_array.__str__()
        if key in spectrum_dict.keys():  # use cache just take 4s
            # if False: use the old one may take 7s for 50
            return spectrum_dict[key]
        else:
            nbins = int(float(max_mz - min_mz) / float(bin_size)) + 1
            results = np.zeros(nbins)
            for index in range(len(mz_array)):
                mz = mz_array[index]
                intensity = intensity_array[index]
                intensity = np.math.sqrt(intensity)
                if mz < min_mz or mz > max_mz:
                    continue
                bin_index = self.get_bin_index(mz, min_mz, bin_size)

                if bin_index < 0 or bin_index > nbins - 1:
                    continue

                if results[bin_index] == 0:
                    results[bin_index] = intensity
                else:
                    results[bin_index] += intensity

            intensity_sum = results.sum()
            if intensity_sum > 0:
                results /= intensity_sum
                spectrum_dict[key] = results
            else:
                logging.debug('zero intensity found')
        return results

class SiameseNetwork1(nn.Module):

    def __init__(self):
        super(SiameseNetwork1, self).__init__()

        self.fc1_1 = nn.Linear(61, 32)
        self.fc1_2 = nn.Linear(32, 5)

        self.cnn1 = nn.Conv1d(1, 30, 3)
        self.maxpool1 = nn.MaxPool1d(2)

        self.cnn2 = nn.Conv1d(1, 30, 3)
        self.maxpool2 = nn.MaxPool1d(2)

        self.fc2 = nn.Linear(1 * 36695, 32)

    def forward_once(self, preInfo, fragInfo):
        preInfo = self.fc1_1(preInfo)
        preInfo = F.selu(preInfo)
        preInfo = self.fc1_2(preInfo)
        preInfo = F.selu(preInfo)
        preInfo = preInfo.view(preInfo.size(0), -1)

        fragInfo = self.cnn1(fragInfo)
        fragInfo = F.selu(fragInfo)
        fragInfo = self.maxpool1(fragInfo)
        fragInfo = fragInfo.view(fragInfo.size(0), -1)

        output = torch.cat((preInfo, fragInfo), 1)
        output = self.fc2(output)
        return output

    def forward(self, spectrum01, spectrum02):

        spectrum01 = spectrum01.reshape(spectrum01.shape[0], 1, spectrum01.shape[1])
        spectrum02 = spectrum02.reshape(spectrum02.shape[0], 1, spectrum02.shape[1])

        # input1_1 = spectrum01[:, :, :500]
        input1_2 = spectrum01[:, :, :2449]
        input1_3 = spectrum01[:, :, 2449:]

        # input2_1 = spectrum02[:, :, :500]
        input2_2 = spectrum02[:, :, :2449]
        input2_3 = spectrum02[:, :, 2449:]

        output01 = self.forward_once(input1_3, input1_2)
        output02 = self.forward_once(input2_3, input2_2)

        return output01, output02

class SiameseNetwork2(nn.Module):

    def __init__(self):
        super(SiameseNetwork2, self).__init__()

        self.fc1_1 = nn.Linear(61, 32)
        self.fc1_2 = nn.Linear(32, 5)

        self.cnn11 = nn.Conv1d(1, 30, 3)
        self.maxpool11 = nn.MaxPool1d(12)
        self.cnn12 = nn.Conv1d(30, 30, 3)
        self.maxpool12 = nn.MaxPool1d(6)
        self.cnn13 = nn.Conv1d(30, 30, 3)
        self.maxpool13 = nn.MaxPool1d(3)

        self.cnn21 = nn.Conv1d(1, 30, 3)
        self.maxpool21 = nn.MaxPool1d(12)
        self.cnn22 = nn.Conv1d(30, 30, 3)
        self.maxpool22 = nn.MaxPool1d(6)
        self.cnn23 = nn.Conv1d(30, 30, 3)
        self.maxpool23 = nn.MaxPool1d(6)
        self.cnn24 = nn.Conv1d(30, 30, 3)
        self.maxpool24 = nn.MaxPool1d(3)

        self.fc2 = nn.Linear(30 + 30 + 5, 32)

    def forward_once(self, refSpecInfo, fragInfo, preInfo):

        preInfo = self.fc1_1(preInfo)
        preInfo = F.selu(preInfo)
        preInfo = self.fc1_2(preInfo)
        preInfo = F.selu(preInfo)
        preInfo = preInfo.view(preInfo.size(0), -1)

        fragInfo = self.cnn21(fragInfo)
        fragInfo = F.selu(fragInfo)
        fragInfo = self.maxpool21(fragInfo)
        fragInfo = F.selu(fragInfo)
        fragInfo = self.cnn22(fragInfo)
        fragInfo = F.selu(fragInfo)
        fragInfo = self.maxpool22(fragInfo)
        fragInfo = F.selu(fragInfo)
        fragInfo = self.cnn23(fragInfo)
        fragInfo = F.selu(fragInfo)
        fragInfo = self.maxpool23(fragInfo)
        fragInfo = F.selu(fragInfo)
        fragInfo = self.cnn24(fragInfo)
        fragInfo = F.selu(fragInfo)
        fragInfo = self.maxpool24(fragInfo)
        fragInfo = F.selu(fragInfo)
        fragInfo = fragInfo.view(fragInfo.size(0), -1)  # 改变数据的形状，-1表示不确定，视情况而定

        refSpecInfo = self.cnn11(refSpecInfo)
        refSpecInfo = F.selu(refSpecInfo)
        refSpecInfo = self.maxpool11(refSpecInfo)
        refSpecInfo = F.selu(refSpecInfo)
        refSpecInfo = self.cnn12(refSpecInfo)
        refSpecInfo = F.selu(refSpecInfo)
        refSpecInfo = self.maxpool12(refSpecInfo)
        refSpecInfo = F.selu(refSpecInfo)
        refSpecInfo = self.cnn13(refSpecInfo)
        refSpecInfo = F.selu(refSpecInfo)
        refSpecInfo = self.maxpool13(refSpecInfo)
        refSpecInfo = F.selu(refSpecInfo)
        refSpecInfo = refSpecInfo.view(refSpecInfo.size(0), -1)  # 改变数据的形状，-1表示不确定，视情况而定

        output = torch.cat((preInfo, fragInfo, refSpecInfo), 1)
        output = self.fc2(output)
        return output

    def forward(self, spectrum01, spectrum02):
        refSpecInfo1, fragInfo1, preInfo1 = spectrum01
        refSpecInfo2, fragInfo2, preInfo2 = spectrum02

        refSpecInfo1 = refSpecInfo1.reshape(refSpecInfo1.shape[0], 1, refSpecInfo1.shape[1])
        fragInfo1 = fragInfo1.reshape(fragInfo1.shape[0], 1, fragInfo1.shape[1])
        preInfo1 = preInfo1.reshape(preInfo1.shape[0], 1, preInfo1.shape[1])

        refSpecInfo2 = refSpecInfo2.reshape(refSpecInfo2.shape[0], 1, refSpecInfo2.shape[1])
        fragInfo2 = fragInfo2.reshape(fragInfo2.shape[0], 1, fragInfo2.shape[1])
        preInfo2 = preInfo2.reshape(preInfo2.shape[0], 1, preInfo2.shape[1])

        output01 = self.forward_once(refSpecInfo1, fragInfo1, preInfo1)
        output02 = self.forward_once(refSpecInfo2, fragInfo2, preInfo2)

        return output01, output02

class ContrastiveLoss(torch.nn.Module):
    """
    Contrastive loss function.
    """
    def __init__(self, margin=1.0):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin

    def forward(self, output1, output2, label):
        euclidean_distance = F.pairwise_distance(output1, output2)
        euclidean_distance = euclidean_distance.double()
        label = label.double()
        loss_contrastive = torch.mean(label * euclidean_distance + (1-label) * torch.pow(torch.clamp(self.margin - euclidean_distance, min=0), 2))

        return loss_contrastive

if __name__ == '__main__':

    #基本训练参数
    train_batch_size = 128

    #训练轮数
    epoches = 50

    #学习率
    learning_rate = 0.0005

    #训练与测试集合加载
    train_dataset = NewMGFDataSet('complete.mgf', 'train.csv')
    test_dataset = NewMGFDataSet('complete.mgf', 'test.csv')

    train_dataloader = data.DataLoader(dataset=train_dataset, batch_size=train_batch_size, shuffle=True, num_workers=1)
    test_dataloader = data.DataLoader(dataset=test_dataset, batch_size=1, shuffle=True, num_workers=1)

    #初始化神经网络，损失函数和优化的参数
    net = SiameseNetwork1().double()
    criterion = ContrastiveLoss()
    optimizer = optim.Adam(net.parameters(), lr=learning_rate)

    counter, loss_history, acc = [], [], []
    iteration_number = 0

    #开始训练，每训练完成一轮训练集进行一次分类正确率的计算
    for epoch in range(0, epoches):

        #训练过程
        for i, data in enumerate(train_dataloader, 0):
            spec0, spec1 = data[:, :2510], data[:, 2510:-1]
            label = data[:, -1]
            #每个batch都需要设置梯度归零
            optimizer.zero_grad()
            output1, output2 = net(spec0, spec1)
            loss_contrastive = criterion(output1, output2, label)
            loss_contrastive.backward()
            #下面语句执行模型的参数更新
            optimizer.step()
            if i % 10 == 0:
                print("Epoch number {}, Current loss {}".format(epoch, loss_contrastive.item()))
                iteration_number += 10
                counter.append(iteration_number)
                loss_history.append(loss_contrastive.item())

        dis_list, flag_list = [], []
        total, correct, accuracy = 0, 0, 0

        #测试过程
        for j, test_data in enumerate(test_dataloader, 0):
            total += 1
            test_spec0, test_spec1 = test_data[:, :2510], test_data[:, 2510:-1]
            test_label = test_data[:, -1]
            out1, out2 = net(test_spec0, test_spec1)
            euclidean_distance = F.pairwise_distance(out1, out2)
            value = euclidean_distance.data
            label = test_label.numpy()[0]
            if epoch%10==0:
                print(value)
            #print(label)

            #0.7作为相似与不相似谱图之间的欧式距离的阈值
            if value <= 0.4:
                if label == 1:
                    correct += 1
            elif label == 0:
                correct += 1
        accuracy = correct / total
        acc.append(accuracy)
        print('Accuracy:{}\n '.format(accuracy))

    plt.figure(figsize=(16, 9))
    plt.subplot(2, 1, 1)
    plt.plot(np.arange(len(acc)), acc)
    plt.title('Acc for Epoch: %s Batch_size: %s' % (len(acc), train_batch_size))
    plt.xlabel('Epoch')
    plt.ylabel('Acc')
    plt.subplot(2, 1, 2)
    plt.plot(np.arange(len(loss_history)), loss_history, 'r')
    plt.title('Loss for Iteration: %s Batch_size: %s' % (len(loss_history), train_batch_size))
    plt.xlabel('Iteration')
    plt.ylabel('Loss')
    plt.show()




