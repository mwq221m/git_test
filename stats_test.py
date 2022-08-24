import numpy as np
#import scipy as sp
from scipy import stats
from scipy import integrate
import matplotlib.pyplot as plt

def central_moment_n(data,n):
    length=data.shape[0]
    #print(length)
    data_mean=data.mean()
    sum_temp=0
    for i in range(length):
        sum_temp+=1/(length-1)*(data[i]-data_mean)**n
    return sum_temp

data=np.random.normal(loc=5,scale=2,size=100000)#scale指代标准差
print(data.mean())
var=np.var(data,ddof=1)
print('样本方差',var)
std=np.std(data,ddof=1)#不加ddof=1 则是总体方差（分母为N） 现在为N-1
print('样本标准差',std)
res=stats.relfreq(data,numbins=200)
print(res)
x=res.lowerlimit+np.linspace(0,res.binsize*res.frequency.size,res.frequency.size)
plt.figure()
plt.bar(x,res.frequency,width=res.binsize)
plt.show()
cdf_value=np.cumsum(res.frequency)
plt.figure()
plt.bar(x,cdf_value,width=res.binsize)
plt.show()
pdf_value=res.frequency/res.binsize
plt.figure()
plt.plot(x,pdf_value)
plt.show()
#inte=integrate.trapz(x,pdf_value)
inte=integrate.trapz(pdf_value,x)
mean_test=integrate.trapz(pdf_value*x,x)
var_test=integrate.trapz(pdf_value*(x-mean_test)**2,x)
central_moment_three_test=integrate.trapz(pdf_value*(x-mean_test)**3,x)
skew_test=central_moment_three_test/var_test**1.5
print('密度函数积分',inte)
print('数值积分计算出的期望',mean_test)
print('数值积分计算出的方差',var_test)
print('数值积分计算出的三阶中心矩*****',central_moment_three_test)
print('数值积分计算出的偏度********',skew_test)
skew_temp=stats.skew(data)
print('样本偏度*********',skew_temp)
kurtosis_temp=stats.kurtosis(data)#定义中对对结果-3 以抵消正态分布的影响
print('样本峰度',kurtosis_temp)

skew_cal=central_moment_n(data,n=3)
print('定义计算三阶中心矩*********',skew_cal)

'''
计算结果想尽可能的准确：
最好知道具体的函数表达
如果只知道离散点 则样本尽可能大 且分区数numbins尽可能多，这样的pdf更准确
可以计算pdf的数值积分看pdf是否准确
对于正态分布的pdf离散点计算三阶矩和四阶矩容易产生误差 因为正态分布下两个统计量应该为零
'''

