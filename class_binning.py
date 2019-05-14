# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 19:03:30 2019

@author: Luo XiYang
"""
import os
import re
class Binning:
    def __init__(self):
        self=self
    def binning(root):
        ret = [];data=[];
        Binning.findFasta(root, ret)
        #print("\nRET\n",ret)
        for path in ret:
            #print(path)
            with open(path,'r') as f:
                data.append(f.readlines())
                #print(data)
                digital=Binning.extract(data)
                print("-------------------------------------read:"+path+"-------------------------------------finished")
                data=[]#clean
                DigitalIntensity,DigitalMZ=Binning.clean(digital)
                Binning.write(DigitalIntensity,DigitalMZ,path)
                
    def write(DigitalIntensity1,DigitalMZ1,path):
        '''binning interval'''
        count=0;dic={};intensity=0;dic1=[];
        interval=[0.00];
        if DigitalIntensity1==[] or DigitalMZ1==[]:
            pass
        else:
            DigitalMZ=sum(DigitalMZ1,[]);DigitalIntensity=sum(DigitalIntensity1,[]);#Merge two-dimensional lists into one-dimensional lists      
            #print("MAX digitalMZ:\n",max(DigitalMZ))
            for i in range(0,int(max(DigitalMZ))+30):#Because DigitalMZ may be a floating point number, add an integer to DigitalMZ.
                count1=1.00508*(0.18+i)
                interval.append(count1)
            #print(interval[0:10])
            for i1 in range(1,len(interval)):
                for i2 in range(0,len(DigitalMZ)):
                    if DigitalMZ[i2]>=interval[i1-1] and DigitalMZ[i2]<interval[i1]:
                        count=count+1
                        intensity=intensity+DigitalIntensity[i2]
                    else:
                        pass
                dic[str(interval[i1-1])+"--"+str(interval[i1])]=str(count)+":"+str(intensity)
                dic1.append([intensity,count,interval[i1-1],interval[i1]])
                count=0;intensity=0;
            #print(dic1)
            DATA=Binning.extract40N(dic1,interval)
            
            #PATH=os.path.basename(path)#获取对应路径下文件的名字os.path.basename("/usr/local/python3/bin/python3")=>python3
            #father_path=os.path.abspath(os.path.dirname(path)+os.path.sep+".")
            PATH=path.split(".fasta")[0]+"--binning.fasta"
            #print(PATH)
            #PATH=PATH.split(".")[0].split("charge")[1]
            '''
            for d in range(0,len(DATA)):
                with open(PATH+".fasta",'a') as f:
                    f.write(str(DATA[d][2])+"--"+str(DATA[d][3])+":"+str(DATA[d][1])+":"+str(DATA[d][0])+"\n")
            '''
            for k,v in DATA.items():
                with open(PATH,'a') as f:
                    f.write(str(k)+":"+str(v)+"\n")
            print("-------------------------------------write:"+PATH+".fasta-------------------------------------finished")
        
    def extract40N(dic1,interval):
        DATA=[];count=0;intensity=0;dic={};
        index=sorted(dic1,key=(lambda x:x[0]),reverse=True)
        #print("sort\n\n\n\n\n\n",index[0])
        #DATA=index[0:100]
        DATA=index
        for i1 in range(1,len(interval)):
            for i2 in range(0,len(DATA)):
                if DATA[i2][2]==interval[i1-1] and DATA[i2][3]==interval[i1]:
                    count=DATA[i2][1];intensity=DATA[i2][0];
                else:
                    pass
            dic[str(interval[i1-1])+"--"+str(interval[i1])]=str(count)+":"+str(intensity)
            count=0;intensity=0;
        return dic
        
        
    def clean(digital):
        DigitalMZ=[];DigitalIntensity=[];tempMZ=[];tempIntensity=[];
        if digital==[]:
            return DigitalIntensity,DigitalMZ
        else:
            for i in range(0,len(digital)):
                for i1 in range(0,len(digital[i])):
                    temp1=digital[i][i1].split("\n|\t")[0]
                    #print(temp1)
                    #print("xxx:",temp1.split("	")[1])
                    '''
                    tempIntensity.append(float(temp1.split("	")[1]))
                    tempMZ.append(float(temp1.split("	")[0]))
                    '''
                    #print(temp1.split(" ").length==1)
                    if len(temp1.split("	"))!=1:
                        tempIntensity.append(float(temp1.split("	")[1]))
                        tempMZ.append(float(temp1.split("	")[0]))
                    else:
                        tempIntensity.append(float(temp1.split(" ")[1]))
                        tempMZ.append(float(temp1.split(" ")[0]))
                DigitalMZ.append(tempMZ);DigitalIntensity.append(tempIntensity)
                tempMZ=[];tempIntensity=[];
            return DigitalIntensity,DigitalMZ
        '''data format [[102.0552, 102.6149...],[102.0552, 102.6149...]...]'''
            
                
    def extract(data):
        index=[];lenght=0;
        #print("kkkk\n\n",data)
        if(data[0]==[]):
            print("one file is empty")
            index.append(0);index.append(0)
        else:
            lenght=len(data[0])
            for i in range(0,len(data[0])):
                rule0=re.findall(r"^>>>",data[0][i])
                if rule0!=[]:
                    index.append(i)
            index.append(lenght)
        #print(index)
        digital=[];
        if index[0]==0 and index[1]==0:
            digital=[]
        else:
            for i1 in range(1,len(index)):
                tempData=data[0][index[i1-1]+1:index[i1]]
                digital.append(tempData)
        #print("\n\n\nDIGITAL\n\n\n",digital)
        return digital
        '''data format [['102.0552 453.3\n', '102.6149 80.3\n'...],['102.0552 453.3\n', '102.6149 80.3\n'...]...]'''
            
    def findFasta(path, ret):
        """Finding the *.fasta file in specify path"""
        filelist = os.listdir(path)
        for filename in filelist:
            de_path = os.path.join(path, filename)
            if os.path.isfile(de_path):
                if de_path.endswith(".fasta"): #Specify to find the txt file.
                    ret.append(de_path)
            else:
                Binning.findFasta(de_path, ret)
 
