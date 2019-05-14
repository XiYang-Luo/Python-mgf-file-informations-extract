# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 14:31:51 2019

@author: Luo XiYang
"""

class Writer:
    def __init__(self):
        pass
    def writeBasedCharge(Title,charge,preMass,DigitalParts,combinePath):
        #print(charge)
        count=0;dic={};intensity=0;interval=[0.00];
        index1=[];index2=[];index3=[];index4=[];index5=[];index6=[];index7=[];index8=[];
        for i in range(0,len(charge)):
            if charge[i]=="1+":
                index1.append(i)
            elif charge[i]=="2+":
                index2.append(i)
            elif charge[i]=="3+":
                index3.append(i)
            elif charge[i]=="4+":
                index4.append(i)
            elif charge[i]=="5+":
                index5.append(i)
            elif charge[i]=="6+":
                index6.append(i)
            elif charge[i]=="7+":
                index7.append(i)
            elif charge[i]=="8+":
                index8.append(i)
            else:
                pass
        Da=[]
        for k in range(0,len(preMass)):
            Da.append(float(preMass[k]))
        tempPath1=combinePath+"/charge+1/charge--"
        tempPath2=combinePath+"/charge+2/charge--";
        tempPath3=combinePath+"/charge+3/charge--";
        tempPath4=combinePath+"/charge+4/charge--";
        tempPath5=combinePath+"/charge+5/charge--";
        tempPath6=combinePath+"/charge+6/charge--";
        tempPath7=combinePath+"/charge+7/charge--";
        tempPath8=combinePath+"/charge+8/charge--";
        tempMaxDa=int(max(Da))
        #print(tempMaxDa)
        
        for i1 in range(0,tempMaxDa,10):
            count1=i1+10
            interval.append(count1)
        #print(interval)
        for iX in range(1,len(interval)):
            for j in range(0,len(index1)):
                if Da[index1[j]]>=interval[iX-1] and Da[index1[j]]<interval[iX]:
                    with open(tempPath1+str(interval[iX-1])+"--"+str(interval[iX])+".fasta","a") as f1:
                        f1.write(">>>title="+Title[index1[j]]+"*MGF*Da="+str(Da[index1[j]])+"*MGF*charge="+charge[index1[j]]+"\n")
                        for i1 in range(0,len(DigitalParts[index1[j]])):
                            f1.write(DigitalParts[index1[j]][i1]+"\n")
                else:
                    pass
            for j2 in range(0,len(index2)):
                if Da[index2[j2]]>=interval[iX-1] and Da[index2[j2]]<interval[iX]:
                    with open(tempPath2+str(interval[iX-1])+"--"+str(interval[iX])+".fasta","a") as f2:
                        f2.write(">>>title="+Title[index2[j2]]+"*MGF*Da="+str(Da[index2[j2]])+"*MGF*charge="+charge[index2[j2]]+"\n")
                        for i2 in range(0,len(DigitalParts[index2[j2]])):
                            f2.write(DigitalParts[index2[j2]][i2]+"\n")
                else:
                    pass
            for j3 in range(0,len(index3)):
                if Da[index3[j3]]>=interval[iX-1] and Da[index3[j3]]<interval[iX]:
                    with open(tempPath3+str(interval[iX-1])+"--"+str(interval[iX])+".fasta","a") as f3:
                        f3.write(">>>title="+Title[index3[j3]]+"*MGF*Da="+str(Da[index3[j3]])+"*MGF*charge="+charge[index3[j3]]+"\n")
                        for i3 in range(0,len(DigitalParts[index3[j3]])):
                            f3.write(DigitalParts[index3[j3]][i3]+"\n")
                else:
                    pass
            for j4 in range(0,len(index4)):
                if Da[index4[j4]]>=interval[iX-1] and Da[index4[j4]]<interval[iX]:
                    with open(tempPath4+str(interval[iX-1])+"--"+str(interval[iX])+".fasta","a") as f4:
                        f4.write(">>>title="+Title[index4[j4]]+"*MGF*Da="+str(Da[index4[j4]])+"*MGF*charge="+charge[index4[j4]]+"\n")
                        for i4 in range(0,len(DigitalParts[index4[j4]])):
                            f4.write(DigitalParts[index4[j4]][i4]+"\n")
                else:
                    pass
            for j5 in range(0,len(index5)):
                if Da[index5[j5]]>=interval[iX-1] and Da[index5[j5]]<interval[iX]:
                    with open(tempPath5+str(interval[iX-1])+"--"+str(interval[iX])+".fasta","a") as f5:
                        f5.write(">>>title="+Title[index5[j5]]+"*MGF*Da="+str(Da[index5[j5]])+"*MGF*charge="+charge[index5[j5]]+"\n")
                        for i5 in range(0,len(DigitalParts[index5[j5]])):
                            f5.write(DigitalParts[index5[j5]][i5]+"\n")
                else:
                    pass
            for j6 in range(0,len(index6)):
                if Da[index6[j6]]>=interval[iX-1] and Da[index6[j6]]<interval[iX]:
                    with open(tempPath6+str(interval[iX-1])+"--"+str(interval[iX])+".fasta","a") as f6:
                        f6.write(">>>title="+Title[index6[j6]]+"*MGF*Da="+str(Da[index6[j6]])+"*MGF*charge="+charge[index6[j6]]+"\n")
                        for i6 in range(0,len(DigitalParts[index6[j6]])):
                            f6.write(DigitalParts[index6[j6]][i6]+"\n")
                else:
                    pass
            for j7 in range(0,len(index7)):
                if Da[index7[j7]]>=interval[iX-1] and Da[index7[j7]]<interval[iX]:
                    with open(tempPath7+str(interval[iX-1])+"--"+str(interval[iX])+".fasta","a") as f7:
                        f7.write(">>>title="+Title[index7[j7]]+"*MGF*Da="+str(Da[index7[j7]])+"*MGF*charge="+charge[index7[j7]]+"\n")
                        for i7 in range(0,len(DigitalParts[index7[j7]])):
                            f7.write(DigitalParts[index7[j7]][i7]+"\n")
                else:
                    pass
            for j8 in range(0,len(index8)):
                if Da[index8[j8]]>=interval[iX-1] and Da[index8[j8]]<interval[iX]:
                    with open(tempPath8+str(interval[iX-1])+"--"+str(interval[iX])+".fasta","a") as f8:
                        f8.write(">>>title="+Title[index8[j8]]+"*MGF*Da="+str(Da[index8[j8]])+"*MGF*charge="+charge[index8[j8]]+"\n")
                        for i8 in range(0,len(DigitalParts[index8[j8]])):
                            f8.write(DigitalParts[index8[j8]][i8]+"\n")
                else:
                    pass
             
        print("----------------------------------------------charge: finished----------------------------------------------")
        
        
        
        
        
        
        
        
        
        
        
        
        