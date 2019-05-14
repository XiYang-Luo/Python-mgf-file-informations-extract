# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:08:17 2019

@author: Luo XiYang
"""
import os
from itertools import groupby
'''some tools'''
class AID:
    '''This function determines whether the numbers in a list are continuous and returns a continuous range.'''
    def ContinuousDigitalRange(list_X):
        minRange=[];maxRange=[];
        fun = lambda x: x[1]-x[0]
        for k, g in groupby(enumerate(list_X), fun):
          l1 = [j for i, j in g]  # A list of consecutive numbers
          if len(l1) > 1:
            scop = str(min(l1)) + '-' + str(max(l1))  # Connect Continuous Digital Range with "-"
            minRange.append(min(l1));maxRange.append(max(l1));
          else:
            scop = l1[0]
            minRange.append(l1[0]);maxRange.append(l1[0]);
          #print("Continuous digital range：{}".format(scop))
        #print(minRange);print(maxRange);
        return minRange,maxRange
    
    def ContinuousDigitalRange2(list_X):
        minRange=[];maxRange=[];
        fun = lambda x: x[1]-x[0]
        for k, g in groupby(enumerate(list_X), fun):
          l1 = [j for i, j in g]  # A list of consecutive numbers
          if len(l1) > 1:
              if  min(l1)==0:
                  minRange.append(min(l1));maxRange.append(max(l1)+1);
              else:
                  minRange.append(min(l1)+1);maxRange.append(max(l1)+1);
          else:
            minRange.append(l1[0]+1);maxRange.append(l1[0]+1);
          #print("Continuous digital range：{}".format(scop))
        #print(minRange);print(maxRange);
        return minRange,maxRange
    
    def StatisticalNumber(listX):
        '''One-dimensional list: False;  other:True'''
        Flag=isinstance(listX[0], list)
        if Flag==False:
            return len(listX)
        else:
            '''Two dimensional list'''
            Flag2=isinstance(listX[0][0], list)
            if(Flag2==False):
                return len(listX),len(listX[0])
            else:
                return "no such a list"
    def countFile(dirX):
        tmp = 0
        for item in os.listdir(dirX):
            if os.path.isfile(os.path.join(dirX, item)):
                tmp += 1
            else:
                tmp += AID.countFile(os.path.join(dirX, item))
        return tmp
 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
