# -*- coding: utf-8 -*-
"""
Created on Sat May  4 12:35:18 2019

@author: Luo XiYang
"""

import shutil
import os

def file_name(file_dir):   
    L=[]   
    for root, dirs, files in os.walk(file_dir):  
        for file in files:  
            if os.path.splitext(file)[1] == '.fasta': 
                if file.split("--")[-1]=='binning.fasta':
                    L.append(os.path.join(root, file))  
    #print(root,dirs,files)
    return L  

if __name__ == "__main__":
    path = file_name(r'C:\Users\Luo XiYang\MineCraft\MyFiles\毕业设计周报\alpha\LTQ-XL-OrbitrapP@65MGF')
    #print(path)
    
    for file1 in path:
        F1=os.path.exists(r'C:\Users\Luo XiYang\MineCraft\MyFiles\毕业设计周报\alpha\LTQ-XL-OrbitrapP@65MGFBinning'+'/'+file1.split("\\")[-3]);
       # print(F1)
        if F1==False:
            os.mkdir(r'C:\Users\Luo XiYang\MineCraft\MyFiles\毕业设计周报\alpha\LTQ-XL-OrbitrapP@65MGFBinning'+'/'+file1.split("\\")[-3])
            F2=os.path.exists(r'C:\Users\Luo XiYang\MineCraft\MyFiles\毕业设计周报\alpha\LTQ-XL-OrbitrapP@65MGFBinning'+'/'+file1.split("\\")[-3]+'/'+file1.split("\\")[-2]);
            if F2==False:
                os.mkdir(r'C:\Users\Luo XiYang\MineCraft\MyFiles\毕业设计周报\alpha\LTQ-XL-OrbitrapP@65MGFBinning'+'/'+file1.split("\\")[-3]+'/'+file1.split("\\")[-2])
            else:
                pass
        else:
            F3=os.path.exists(r'C:\Users\Luo XiYang\MineCraft\MyFiles\毕业设计周报\alpha\LTQ-XL-OrbitrapP@65MGFBinning'+'/'+file1.split("\\")[-3]+'/'+file1.split("\\")[-2]);
            if F3==False:
                os.mkdir(r'C:\Users\Luo XiYang\MineCraft\MyFiles\毕业设计周报\alpha\LTQ-XL-OrbitrapP@65MGFBinning'+'/'+file1.split("\\")[-3]+'/'+file1.split("\\")[-2])
            else:
                pass
    for file in path:
        file_dir = r'C:\Users\Luo XiYang\MineCraft\MyFiles\毕业设计周报\alpha\LTQ-XL-OrbitrapP@65MGFBinning'+'/'+file.split("\\")[-3]+'/'+file.split("\\")[-2]+"/"+file.split("\\")[-1]
        shutil.copy(file,file_dir)