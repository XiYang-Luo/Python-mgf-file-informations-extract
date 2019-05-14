# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 08:42:51 2019

@author: Luo XiYang
"""
import os
from class_fileReader import fileReader
from aid import AID
from class_MGFFileInfromationExtract import MGFFileInfromationExtract
'''writer'''
from class_Writer import Writer

'''binning'''
from class_binning import Binning


def importFiles():
    completePath=[]
    folderPath = r"../files/MGF_train"
    #folderPath = r"../files/X"#测试
    projectNameList,mgfFilesNameList=fileReader.importFolder(folderPath)
    '''合成路径 准备提取所有的mgf文件'''
    projectNumer = AID.StatisticalNumber(projectNameList)
    mgfFilesNumber = list(AID.StatisticalNumber(mgfFilesNameList))[0]
    if mgfFilesNumber==projectNumer:
        for i in range(0,len(projectNameList)):
            for i1 in range(0,len(mgfFilesNameList[i])):
                completePath.append(folderPath+"/"+projectNameList[i]+"/"+mgfFilesNameList[i][i1])
        print("complete path:\n",completePath)
        return completePath,projectNameList,mgfFilesNameList
    else:
        print("-----------------------------项目和项目对应的mgf文件列表数目不相等，请检查项目文件夹-----------------------------")
        
def extractMGFContents(completePathList):
    #contentList=[]
    '''
        这里使用的思想是提取一个mgf的信息就将其后续的解析和写入执行完，而不是将所有的mgf信息提取出来之后在进行解析写入。
        当mgf很多的时候，使用第一种方法比较好。
    '''
    for i in range(0,len(completePathList)):
        path=completePathList[i]
        #print(path)
        #contentList.append(fileReader.MGFFileReaderFunc(path))
        allMGFFileContents=fileReader.MGFFileReaderFunc(path)
        CharactersParts=fileReader.MGFFileReader_CharactersParts(allMGFFileContents)
        DigitalParts=fileReader.MGFFileReader_DigitalParts(allMGFFileContents)
        print("\n"+path+"\n",len(CharactersParts),len(DigitalParts))

        '''Statistical Number. Is the number of lists in the string part the same as in the number part?Generally speaking, they should be the same.'''
        numberCharactersParts=list(AID.StatisticalNumber(CharactersParts))
        numberDigitalParts=list(AID.StatisticalNumber(DigitalParts))
        #print(numberCharactersParts[0],numberDigitalParts[0])
        if numberCharactersParts[0]==numberDigitalParts[0]:
            TITLE=list(MGFFileInfromationExtract.extractTITLEFromMGF(CharactersParts))
            Title=TITLE[0]
            #print("\n\ntitle[0:2]\n\n",Title[0:2])
            
            PEPMASS=list(MGFFileInfromationExtract.extractPEPMASSFromMGF(CharactersParts))
            precursorMass = PEPMASS[0]
            #print("\nprecursorMass[0:2]\n",precursorMass[0:2])
            
            CHARGE=list(MGFFileInfromationExtract.extractCHARGEFromMGF(CharactersParts))
            charge = CHARGE[0]
            #print("\ncharge[0:2]\n",charge[0:2])
            
            #print("\ndigitalPart[0:1]\n",DigitalParts[0:1])
            
            '''
            dic=[]
            for i in range(0,len(precursorMass)):
                dic.append([Title[i],precursorMass[i],charge[i],DigitalParts[i]])
             
            index=sorted(dic,key=(lambda x:x[1]),reverse=True)
            print("sort\n\n\n\n\n\n",index[0])
            DATA=index[0:40]
            dataTitle=[];dataPrecursorMass=[];dataCharge=[];dataDigitalParts=[];
            for i3 in range(0,len(DATA)):
                dataTitle.append(DATA[i3][0]);dataPrecursorMass.append(DATA[i3][1]);
                dataCharge.append(DATA[i3][2]);dataDigitalParts.append(DATA[i3][3]);   
            
            print(dataPrecursorMass)
            '''
            
            '''obtain Da,a company composed of charge*precursor'''
            #Da = MGFFileInfromationExtract.getDa(charge,precursorMass)
            
            ''' write file'''
            #Writer.writeExtractedInformation(Title,precursorMass,charge,DigitalParts)
            #Writer.writeBasedCharge(Title,charge,precursorMass,DigitalParts)
            #Writer.writeBasedCharge(dataTitle,dataCharge,dataPrecursorMass,dataDigitalParts)
            
            '''mgf writer 将提取的mgf文件的信息存储到对应的文件中 这里将要把提取的mgf信息按照母粒子质量大小（10Da为一个单位）写入'''
            path1=r"../files/extract"
            path2=path.split("/")[-2]
            path3=path.split("/")[-1]
            F1 = path.endswith('.mgf')#判断路径下文件的后缀是否为mgf
            F2 = path.endswith('.MGF')
            if F1==True:
                path4=path3.split(".mgf")[0]
            if F2==True:
                path4=path3.split(".MGF")[0]
            '''该路径定位到extract文件夹中的某个项目下的mgf文件的文件夹
                如：../files/extract/PXD001351/qe2_05122014_25sggolgi3_F012569.mzid_qe2_05122014_25sggolgi3_f012569
            '''
            combinePath=path1+"/"+path2+"/"+path4
            #print(combinePath)
            #print(DigitalParts)
            Writer.writeBasedCharge(Title,charge,precursorMass,DigitalParts,combinePath)
            #print("\n█████████████████████████████"+path.split("/")[3]+" scan completed █████████████████████████████\n")
            print("\n█████████████████████████████"+path+" write completed █████████████████████████████\n")
            
            print(path,combinePath)
            '''binning'''
            print("\n█████████████████████████████"+combinePath+" scan charge files █████████████████████████████\n")
            chargeFileNameList=["charge+1","charge+2","charge+3","charge+4","charge+5","charge+6","charge+7","charge+8"]    
            for ch in range(0,len(chargeFileNameList)):
                root=combinePath+"/"+chargeFileNameList[ch]
                mgfNumber =AID.countFile(root)
                if mgfNumber==0:
                    pass
                else:
                    Binning.binning(root)
                    print("\n█████████████████████████████"+root+" binning completed █████████████████████████████\n")
            print("\n█████████████████████████████All files have completed █████████████████████████████\n")
            
            
        else:
            print("The digital parts is not mapped to the character parts.Usually,They are equal in length.Check mgf file or alter the code,please:",path)
        #MGFFileInfromationExtract.extractTITLEFromMGF(allMGFFileContents)
 
    
def testForBinning(percent,completePath,projectNameList,mgfFilesNameList):
    print(percent)
    
    root=r"C:\Users\Luo XiYang\MineCraft\MyFiles\毕业设计周报\pythonWorkSpace"
    Binning.binning(root)


def generateDirectory(projectNameList,mgfFilesNameList):
    rootPath=r"../files/extract"
    fileReader.generateFolder(projectNameList,mgfFilesNameList,rootPath)

if __name__ == "__main__":
    COUNT=1#计数 用于显示现在运行到第几个mgf文件了 还剩多少文件
    '''提取各个项目下面完整的mgf路径'''
    completePath,projectNameList,mgfFilesNameList= importFiles()
    '''根据项目文件构建提取文件的目录'''
    generateDirectory(projectNameList,mgfFilesNameList)
    '''提取mgf文件的数据'''
    extractMGFContents(completePath)
    '''binning分箱策略'''
    #testForBinning(COUNT/len(mgfFilesNameList),completePath,projectNameList,mgfFilesNameList)
    COUNT=COUNT+1
     
    