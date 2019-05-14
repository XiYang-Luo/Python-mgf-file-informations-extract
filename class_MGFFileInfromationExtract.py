# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 09:53:27 2019

@author: Luo XiYang
"""

import re
from aid import AID
'''This py class file used to extract TITLE,CHARGE, PEPMASS & RTINSECONDS infromation in mgf'''
class MGFFileInfromationExtract:
    def __init__(self,path):
        self=self
        
    '''extract contents begin with "TITLE" in contents list'''
    def extractTITLEFromMGF(contents_characterParts):
        tempData0=[];Title=[];
        #print(contents_characterParts)
        for i in range(0,len(contents_characterParts)):
            for i1 in range(0,len(contents_characterParts[i])):
                rule0 = re.findall(r'^(TITLE)',contents_characterParts[i][i1])#Match "TITLE" beginning
                if rule0!=[]:
                    tempData0.append(contents_characterParts[i][i1].split("TITLE=")[1])
        Title=tempData0
        return Title,len(Title)
    '''extract contents begin with "PEPMASS" in contents list'''
    def extractPEPMASSFromMGF(contents_characterParts):
        tempData0=[];PEPMASS=[];
        #print(contents_characterParts[0:3])
        for i in range(0,len(contents_characterParts)):
            for i1 in range(0,len(contents_characterParts[i])):
                rule0 = re.findall(r'^(PEPMASS)',contents_characterParts[i][i1])#Match "PEPMASS" beginning
                if rule0!=[]:
                    if(len(contents_characterParts[i][i1].split(" "))>0):
                        tempData0.append(contents_characterParts[i][i1].split("PEPMASS=")[1].split(" ")[0])
                    else:
                        tempData0.append(contents_characterParts[i][i1].split("PEPMASS=")[1])
        PEPMASS=tempData0
        return PEPMASS,len(PEPMASS)
    '''extract contents begin with "CHARGE" in contents list'''
    def extractCHARGEFromMGF(contents_characterParts):
        tempData0=[];CHARGE=[];
        for i in range(0,len(contents_characterParts)):
            for i1 in range(0,len(contents_characterParts[i])):
                rule0 = re.findall(r'^(CHARGE)',contents_characterParts[i][i1])#Match "CHARGE" beginning
                if rule0!=[]:
                    tempData0.append(contents_characterParts[i][i1].split("CHARGE=")[1])
        CHARGE=tempData0
        return CHARGE,len(CHARGE)
    
    def getDa(charge,precursor):
        Da=[]
        for i in range(0,len(charge)):
            Da.append(float(charge[i].split("+")[0])*float(precursor[i]))
        #print(Da[0:10])
        return Da
    
    def extractDigitalPartsFromMGF(contents_digitalParts):
        return contents_digitalParts
        