# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:47:53 2019

@author: Luo XiYang
"""
import random
from pyteomics import mgf
import csv

def reader(path,flag):
    intensity=[];MZ=[];charge=[];title=[];pepmass=[];
    print("\n█████████████████████████████开始读入"+path+"的信息█████████████████████████████\n")
    for spectrum in mgf.read(path):
        #print ("\n\n Spectrum  \n\n\n",spectrum)
        params = spectrum.get('params')
        MZ.append(spectrum.get('m/z array'))
        intensity.append(spectrum.get("intensity array"))
        charge.append(params.get('charge'))
        title.append(params.get('title'))
        pepmass.append(params.get('pepmass'))
    print("\n█████████████████████████████读入"+path+"信息完毕█████████████████████████████\n")
    #resultList=random.sample(range(0,len(charge)),int(len(charge)*0.2))
    #index=sorted(resultList)
    if flag==1:
        labels=[1 for i in range(0,len(handle(title)))]
    else:
        labels=[2 for i in range(0,len(handle(title)))]
    return handle(title),labels

def handle(title):
    if(len(title)%2==0):
        return title
    else:
        return title[:-1] #确保都是偶数个，这样在后面的“匹配”时不会有一个是单数
    
def RandomArrangement(title1,title2,labels1,labels2):
    Title=title1+title2
    Labels=labels1+labels2
    index = [i0 for i0 in range(0,len(Title))]
    random.shuffle(index)
    ShuffleTitle=[];ShuffleLables=[];LABLES=[];
    for i2 in range(1,len(index),2):
        ShuffleTitle.append([Title[index[i2-1]],Title[index[i2]]])
        ShuffleLables.append([Labels[index[i2-1]],Labels[index[i2]]])
    print(ShuffleLables[0:4])
    print(ShuffleTitle[0:4])
    for i3 in ShuffleLables:
        if i3[0]==i3[1]:
            LABLES.append(1)#表示来自同一个仪器
        else:
            LABLES.append(0)
    print(LABLES[0:4])
    return  ShuffleTitle,LABLES

def writeCSV(path,TitleList,LablesList):
    T1=[];T2=[];
    for i in range(0,len(TitleList)):
        T1.append(TitleList[i][0])
        T2.append(TitleList[i][1])
    print("\n█████████████████████████████开始写入"+path+"/train.csv"+"的信息█████████████████████████████\n")
    with open(path+"/train.csv","a",newline='') as f:
        writer = csv.writer(f)
        writer.writerows(zip(T1,T2,LablesList))
    print("\n█████████████████████████████写入"+path+"/train.csv"+"的信息完毕！█████████████████████████████\n")
    


if __name__ == "__main__":
    path1=r"C:\Users\Luo XiYang\MineCraft\MyFiles\毕业设计周报\alpha\files\data\makeDataAndLabels\data\train\D1.mgf"
    path2=r"C:\Users\Luo XiYang\MineCraft\MyFiles\毕业设计周报\alpha\files\data\makeDataAndLabels\data\train\D2.mgf"
    path=r"C:\Users\Luo XiYang\MineCraft\MyFiles\毕业设计周报\alpha\files\data\makeDataAndLabels\data\train"
    title1,labels1=reader(path1,1)
    title2,labels2=reader(path2,2)
    
    TitleList,LablesList=RandomArrangement(title1,title2,labels1,labels2)
    
    writeCSV(path,TitleList,LablesList)
    
    
    
    
    
    
    
