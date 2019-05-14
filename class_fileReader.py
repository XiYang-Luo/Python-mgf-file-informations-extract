# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 08:34:33 2019

@author: Luo XiYang
"""
import os
import re
from aid import AID
class fileReader:
    def __init__(self):
        pass
    def importFolder(folderPath):
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
                        temp.append(file)
                mgfFileName.append(temp)#获得某个项目下文件名为mgf或者MGF 的文件
                temp=[]
            else:
                pass
        print("所有项目名称\n",folderName)
        print("项目下所有mgf文件\n",mgfFileName)#一般来说 folderName和mgfFileName的长度应该相等
        return folderName,mgfFileName
    
    def MGFFileReaderFunc(file_path):
        with open(file_path,'r') as file_object:
            contents = file_object.readlines()
            #print(type(contents))
            #print(contents[0:100])
        print("\n█████████████████████████████"+file_path+" READ COMPLETED █████████████████████████████\n")
        return contents#data format:['BEGIN IONS\n', 'TITLE=subset_Linfeng_011011_HapMap35_5.382.382.3 File:"", NativeID:"scan=382"\n',...]
    
    '''
    We divide the MGF file into two parts: the string part and the digital part. The string section contains TITLE, CHARGE, PEPMASS and RTINSECONDS.
    '''
    def MGFFileReader_CharactersParts(contents):
        ZContents=[];TempData=[];index=[];
        for i in range(0,len(contents)-1):
            rule0 = re.findall(r'^\D*',contents[i])#Match character beginning
            #rule1 = re.findall(r'^-*([1-9]\d*\.\d*|0\.\d*[1-9]\d*|0?\.0+|0)',contents[i+1])#Matching Floating Points beginning
            rule2 = re.findall(r'^([1-9])',contents[i+1])#match integer  beginning
            if rule0!=[] and rule2==[]:
               index.append(i)
        #print(index[0:30])
        beginAndEndLocal = list(AID.ContinuousDigitalRange2(index))
        #print(beginAndEndLocal)
        begin=beginAndEndLocal[0];end=beginAndEndLocal[1];
        '''extract informations begin with "Z" from all contents list based on local list'''
        for j in range(0,len(begin)):
            TempData = contents[begin[j]:end[j]+1]
            ZContents.append(TempData)
        #print(MZAndIntensityContents)
        '''preprocessing informations extracted.'''
        tempData1=[];CharactersContentsList=[];
        for k in range(0,len(ZContents)):
            for v in range(0,len(ZContents[k])):
                tempData1.append(ZContents[k][v].split("\n")[0])
            CharactersContentsList.append(tempData1)
            tempData1=[]# clean 
            
        #print(CharactersContentsList)
        '''At the end of list,usually,is a character:['END IONS'] Originated from split mgf.This part not mapping a digital part,must be remove'''
        #print(CharactersContentsList)
        for t in range(0,len(CharactersContentsList)):
            if len(CharactersContentsList[t])==1 and CharactersContentsList[t][0]=='END IONS':
                CharactersContentsList.pop(t)
            elif len(CharactersContentsList[t])==2 and CharactersContentsList[t][0]=='END IONS' and CharactersContentsList[t][1]=='':
                CharactersContentsList.pop(t)
            elif len(CharactersContentsList[t])==3 and CharactersContentsList[t][0]=='END IONS' and CharactersContentsList[t][1]=='' and CharactersContentsList[t][2]=='':
                CharactersContentsList.pop(t)
            elif len(CharactersContentsList[t])==4 and CharactersContentsList[t][0]=='END IONS' and CharactersContentsList[t][1]=='' and CharactersContentsList[t][2]=='' and CharactersContentsList[t][3]=='':
                CharactersContentsList.pop(t)
            else:
                pass
        return CharactersContentsList
        '''
        data format: [['BEGIN IONS', 'TITLE=subset_Linfeng_011011_HapMap35_5.382.382.3 File:"", NativeID:"scan=382"', 'RTINSECONDS=930.504', 'PEPMASS=442.26265097792', 'CHARGE=3+'],
        ['END IONS', 'BEGIN IONS', 'TITLE=subset_Linfeng_011011_HapMap35_5.384.384.3 File:"", NativeID:"scan=384"', 'RTINSECONDS=931.98', 'PEPMASS=434.232284311253', 'CHARGE=3+']...]
        '''
    
    '''
    We divide the MGF file into two parts: the string part and the digital part. The string section contains TITLE, CHARGE, PEPMASS and RTINSECONDS.
    '''
    def MGFFileReader_DigitalParts(contents):
        index=[]# indes is a local list that record place of MZ & intensity
        MZAndIntensityContents=[];TempData=[]
        for i in range(0,len(contents)-1):
            rule0 = re.findall(r'^\D*',contents[i])#Match character beginning
            rule1 = re.findall(r'^-*([1-9]\d*\.\d*|0\.\d*[1-9]\d*|0?\.0+|0)',contents[i+1])#Matching Floating Points beginning
            rule2 = re.findall(r'^-*[1-9]\d*',contents[i+1])#match integer  beginning
            if (rule0!=[] and rule1!=[]) or (rule0!=[] and rule2!=[]):
               index.append(i+1)
        #print(index[0:120])
        '''extrat continuous range of local list'''
        beginAndEndLocal = list(AID.ContinuousDigitalRange(index))
        begin=beginAndEndLocal[0];end=beginAndEndLocal[1];
        '''extract MZ & intensity informations from all contents list based on local list'''
        for j in range(0,len(begin)):
            TempData = contents[begin[j]:end[j]+1]
            MZAndIntensityContents.append(TempData)
        #print(MZAndIntensityContents)
        '''preprocessing MZ * intensity informations extracted.'''
        tempData1=[];MZAndIntensityContentsList=[];
        for k in range(0,len(MZAndIntensityContents)):
            for v in range(0,len(MZAndIntensityContents[k])):
                tempData1.append(MZAndIntensityContents[k][v].split("\n")[0])
            MZAndIntensityContentsList.append(tempData1)
            tempData1=[]# clean 
        #print(MZAndIntensityContentsList[0:200])
        return MZAndIntensityContentsList #data format:[['104.3094 85.0', '107.8294 114.0', '110.0711 2221.7'...],['108.0543 154.1', '110.0710 1591.2'...]...]
        
    def generateFolder(projectNameList,mgfFilesNameList,rootPath):          
        file_name = projectNameList
        path = rootPath
        '''第一步建立项目文件夹'''
        for i in range(0,len(file_name)):
            F=os.path.exists(path+"/"+file_name[i])
            if(F==False):
                os.mkdir(path+"/"+file_name[i])
                '''建立mgf文件夹'''
                for i1 in range(0,len(mgfFilesNameList[i])):
                    F1 = mgfFilesNameList[i][i1].endswith('.mgf')
                    F2 = mgfFilesNameList[i][i1].endswith('.MGF')
                    if F1==True:
                        mgfFilesNameListFolder=mgfFilesNameList[i][i1].split(".mgf")[0]
                    elif F2==True:
                        mgfFilesNameListFolder=mgfFilesNameList[i][i1].split(".MGF")[0]
                    else:
                        print("文件中存在非MGF类型的文件")
                    os.mkdir(path+"/"+file_name[i]+"/"+mgfFilesNameListFolder)
                    '''在每个mgf文件夹下面建立电荷为1-8的8个文件夹，用于存放各个范围的母粒子质量下不同电荷的提取的数据'''
                    for i3 in range(8):
                        os.mkdir(path+"/"+file_name[i]+"/"+mgfFilesNameListFolder+"/charge+"+str(i3+1))
                        #print(" \n\n"+path+"/"+file_name[i]+"/"+mgfFilesNameListFolder+"/charge+"+str(i3+1)+" 该文件创建成功")
                print(" \n\n"+path+"/"+file_name[i]+" 该文件创建成功")
            else:
                print("\n\nlog:class_filderReader.generateFolder:\n\n"+path+"/"+file_name[i]+" 该文件已经存在")
 
           