import pandapower.networks as pn
import pandapower as pp
import pandas as pd
from dlpf import DLPF
import time
import matplotlib.pyplot as plt
'''
已经找出问题：

pandapower支路导纳的单位为nf 即电容 需要乘以2*pi*f
dlpf支路导纳漏乘以1j 对于支路电容不大的情况下很难发现

'''

start=time.time()
net=pn.case24_ieee_rts()
pp.runpp(net)
print(net['res_bus'])
end=time.time()
print('计算时间',end-start)
#pp.to_excel(net,filename='rts_79_pp.xlsx')
print('*********')



branch_data = pd.read_excel('rts79_test.xlsx', sheet_name=0)
bus_data = pd.read_excel('rts79_test.xlsx', sheet_name=1)
obj=DLPF(branch_data=branch_data,bus_data=bus_data)
start=time.time()
obj.rundlpf()
obj.show_result()
end=time.time()
print(obj.bus_result)
print(obj.pf_result)
print('运算时间',end-start)
plt.figure()
plt.title('v comparation')
plt.plot(obj.bus_result['num'],obj.bus_result['v'])
#plt.scatter(obj.bus_result['num'],obj.bus_result['v'])
#plt.show()
x=[];y=[]
for i in range(len(net['res_bus'])):
    x.append(i+1)
    y.append(net['res_bus'].loc[i,'vm_pu'])
#plt.figure()
plt.plot(x,y)
plt.show()
plt.figure()
plt.title('p comparation')
plt.bar([i for i in range(38)],obj.pf_result['p'])
#plt.show()
#plt.figure()
plt.bar([i for i in range(33)],net['res_line']['p_from_mw'])
plt.legend(['dlpf','pandapower'])
plt.show()
plt.figure()
plt.title('q comparation')
plt.bar([i for i in range(38)],obj.pf_result['q'])
plt.bar([i for i in range(33)],net['res_line']['q_from_mvar'])
plt.legend(['dlpf','pandapower'])
plt.show()




