import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import weibull_min,relfreq
from scipy import integrate
def f(v,k,c):
    f=(k/c)*(v/c)**(k-1)*np.exp(-(v/c)**k)
    return f
def fp(p,k,a,b,c):
    f=(k/(b*c))*((p-a)/(b*c))**(k-1)*np.exp(-((p-a)/(b*c))**k)
    return f
x=np.linspace(0,30,1000)
y=f(v=x,k=1.4,c=6)
plt.figure()
plt.plot(x,y)
plt.show()
data=weibull_min.rvs(1.4,loc=0,scale=6,size=10000)
res=relfreq(data,numbins=100)
print(res)
x=res.lowerlimit+np.linspace(0,res.binsize*res.frequency.size,res.frequency.size)
plt.figure()
plt.bar(x,res.frequency,width=res.binsize)
plt.show()
p=np.linspace(-5,5,1000)
yp=fp(p=p,k=1.4,a=-1,b=0.25,c=6)
plt.figure()
plt.plot(p,yp)
plt.show()
#inte=integrate.quad(fp(x,k=1.4,a=-1,b=0.25,c=6),a=-1,b=0)
inte=integrate.quad(fp,a=-1,b=0,args=(1.4,-1,0.25,6))
