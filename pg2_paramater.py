import numpy as np
import pandas as pd
from scipy.stats import weibull_min,relfreq,skew
import matplotlib.pyplot as plt

num=1000000
'''
def wind_speed_to_pg2(v):
    if v < 2 or v > 30:
        return 0
    if 2 <= v <= 15:
        return (v - 0.2)*0.2/13
    if 15 < v <= 30:
        return 0.2
'''
def wind_speed_to_pg2(v,v_in,v_rated,v_out,p_max):
    if v<v_in or v>v_out:
        return 0
    if v_in<=v<=v_rated:
        return (v-v_in)*p_max/(v_rated-v_in)
    if v_rated<v<=v_out:
        return p_max

wind_speed=weibull_min.rvs(1.4, loc=0, scale=6, size=num)
#pg2=np.vectorize(wind_speed_to_pg2)(wind_speed)
pg2=[]
for i in range(num):
    current_wind_speed=wind_speed[i]
    current_pg2=wind_speed_to_pg2(v=current_wind_speed,v_in=2,v_rated=15,v_out=30,p_max=0.5)
    pg2.append(current_pg2)

res=relfreq(pg2,numbins=100)
x=res.lowerlimit+np.linspace(0,res.binsize*res.frequency.size,res.frequency.size)
plt.figure()
plt.bar(x,res.frequency,width=res.binsize)
plt.show()
mean_pg2=np.mean(pg2)
std_pg2=np.std(pg2,ddof=1)
skew_pg2=skew(pg2)
print('均值',mean_pg2)
print('标准差',std_pg2)
print('偏度',skew_pg2)