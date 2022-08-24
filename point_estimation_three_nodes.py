import numpy as np
import pandas as pd
from scipy.stats import weibull_min,relfreq,skew
import matplotlib.pyplot as plt
from dlpf import DLPF
import time

class PEM():
    def __init__(self,data,branch_data,bus_data):
        self.data=data
        self.branch_data=branch_data
        self.bus_data=bus_data
        self.m=len(data)
        self.name=[]
        self.mean=[]
        self.std=[]
        self.skew=[]
        self.probability=np.zeros((self.m,2))
        self.epsi=np.zeros((self.m,2))
        self.eta=np.zeros(self.m)
        self.v3=[]
        self.v3_risk=0
        for i in range(self.m):
            temp=data.iloc[i]
            name=temp['name']
            mean=temp['mean']
            std=temp['std']
            skew=temp['skew']
            self.name.append(name)
            self.mean.append(mean)
            self.std.append(std)
            self.skew.append(skew)
        self.mean=np.array(self.mean)
        self.std=np.array(self.std)
        self.skew=np.array(self.skew)
        self.eta=2*np.sqrt(self.m+(self.skew/2)**2)

    def epsi_calculate(self,skew,k):
        temp=skew/2+(-1)**(2-k)*np.sqrt(self.m+(skew/2)**2)#原文里是3-k 这里改为2-k 因为从0开始数
        return temp


    def calculate(self):
        for i in range(self.m):
            for j in range(2):
                self.epsi[i,j]= self.epsi_calculate(skew=self.skew[i],k=j)
                #self.probability[i,j]=1/self.m*(-1)**(j+1)*self.epsi[]
        for i in range(self.m):
            for j in range(2):
                self.probability[i,j]=1/self.m*(-1)**(j+1)*self.epsi[i,1-j]/self.eta[i]

        sum_temp=0
        for i in range(self.m):
            for j in range(2):
                epsi_temp=np.zeros((self.m,2))
                epsi_temp[i,j]=self.epsi[i,j]
                epsi=epsi_temp[:,0]+epsi_temp[:,1]
                temp=self.mean+epsi*self.std
                #print('*******')
                #print(temp)
                pg2=temp[0]
                pd2=temp[1]
                pd3=temp[2]
                qd3=temp[3]
                p2=pg2-pd2
                p3=-pd3
                q3=-qd3
                self.bus_data.loc[1,'p']=p2
                self.bus_data.loc[2,'p']=p3
                self.bus_data.loc[2,'q']=q3
                pf_obj=DLPF(branch_data=self.branch_data,bus_data=self.bus_data)
                pf_obj.rundlpf()
                pf_obj.show_result()
                v3=pf_obj.bus_result.loc[2,'v']
                if v3<0.94:
                    sum_temp+=(0.94-v3)*self.probability[i,j]
                if v3>1.06:
                    sum_temp+=(v3-1.06)*self.probability[i,j]
                self.v3.append(v3)
        self.v3_risk=sum_temp











if __name__=='__main__':
    data=pd.read_excel('point_estimation_information.xlsx')
    branch_data = pd.read_excel('test.xlsx', sheet_name=0)
    bus_data = pd.read_excel('test.xlsx', sheet_name=1)
    start=time.time()
    obj=PEM(data=data,branch_data=branch_data,bus_data=bus_data)
    obj.calculate()
    print('位置系数',obj.epsi)
    print('概率',obj.probability)
    print(obj.v3)
    print('点估计v3风险指标',obj.v3_risk)
    end=time.time()
    print('运算时间',end-start)





