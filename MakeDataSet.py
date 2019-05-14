# -*- coding: utf-8 -*-
"""
Created on Wed May  8 19:23:48 2019

@author: Luo XiYang
"""
from random import shuffle #将列表的数据打乱
import os
import re
from aid import AID
import random
from pyteomics import mgf

def Shuffle(List):
    return shuffle(List)

def reader(folderPath):
    folderName=[];mgfFileName=[];
    for root, dirs, files in os.walk(folderPath):
        #print("Current directory path",root) #当前目录路径  
        #print("All subdirectories in the front path ",dirs) #当前路径下所有子目录  
        #print("All non-directory subfiles in the current path ",files) #当前路径下所有非目录子文件 
        if dirs!=[]:
            folderName=dirs#获得所有的项目名称
        else:
            pass
            
        temp=[]
        if files!=[]:
            for file in files:  
                if os.path.splitext(file)[1] == '.mgf' or os.path.splitext(file)[1] == '.MGF':
                    temp.append(folderPath+"/"+file)
            mgfFileName.append(temp)#获得某个项目下文件名为mgf或者MGF 的文件
            temp=[]
        else:
            pass
    #print("所有项目名称\n",folderName)
    #print("项目下所有mgf文件\n",mgfFileName[0])#一般来说 folderName和mgfFileName的长度应该相等
    return folderName,mgfFileName[0]

def filePathCircle(filePathList,n,instrum):
    for i in range(len(filePathList)):
        extractAndAppend(filePathList[i],n,instrum)

def extractAndAppend(filePath,n,instrum):
    intensity=[];MZ=[];charge=[];title=[];pepmass=[];
    print("\n█████████████████████████████开始读入"+filePath+"的信息█████████████████████████████\n")
    for spectrum in mgf.read(filePath):
        #print ("\n\n Spectrum  \n\n\n",spectrum)
        params = spectrum.get('params')
        MZ.append(spectrum.get('m/z array'))
        intensity.append(spectrum.get("intensity array"))
        charge.append(params.get('charge'))
        title.append(params.get('title'))
        pepmass.append(params.get('pepmass'))
    print("\n█████████████████████████████读入"+filePath+"信息完毕█████████████████████████████\n")
    resultList=random.sample(range(0,len(charge)),int(len(charge)*0.2))
    index=sorted(resultList)
    #print(index)
    
    """write"""
    for i in range(0,len(index)):
        Mz=list(MZ[index[i]]);Intensity=list(intensity[index[i]]);
        #print(Mz)
        PepMass=list(pepmass[index[i]])
        with open("D"+str(n)+".mgf","a") as f1:
            f1.write("BEGIN IONS\n")
            f1.write("TITLE="+title[index[i]]+"-MGF-instrumentation="+instrum+"\n")
            f1.write("PEPMASS="+str(PepMass[0])+"\n")
            f1.write("CHARGE="+str(charge[index[i]])+"\n")
            for i1 in range(len(Mz)):
                f1.write(str(Mz[i1])+" "+str(Intensity[i1])+"\n")
            f1.write("END IONS\n")
    
 


if __name__ == "__main__":
    '''train'''
    #path1=r"../../files/data/train/LTQ-OrbitrapO@65MGF"
    #path2=r"../../files/data/train/LTQ-XL-OrbitrapP@65MGF"
    '''test'''
    path1=r"../../files/data/test/LTQ-OrbitrapO@65MGF"
    path2=r"../../files/data/test/LTQ-XL-OrbitrapP@65MGF"
    
    '''第一类仪器 mam'''
    
    completePath1Temp=list(reader(path1))[1]
    filePathCircle(completePath1Temp,1,"mam")
    
    
    '''第二类仪器 klc'''
    completePath2Temp=list(reader(path2))[1]
    filePathCircle(completePath2Temp,2,"klc")
