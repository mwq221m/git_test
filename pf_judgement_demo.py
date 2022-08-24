import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from dlpf import DLPF
from topology_check import TopologyCheck
from dlpf_in_disconnected_conditions import DLPFInDisconnectedConditions
import time
'''
将之前写的模块简单整合测试
枚举n-k故障事故集并判断各个子网能否直接进行潮流计算
'''

branch_data = pd.read_excel('14_bus_test.xlsx', sheet_name=0)
bus_data = pd.read_excel('14_bus_test.xlsx', sheet_name=1)
topology_check_obj=TopologyCheck(branch_data=branch_data,bus_data=bus_data,number_of_faults=3)
#dlpf_in_disconnected_conditions_obj=DLPFInDisconnectedConditions
topology_check_obj.search_disconnected_conditions()
length=len(topology_check_obj.disconnected_conditions)
temp=topology_check_obj.disconnected_conditions['故障元件索引']
temp_list=[]
start=time.time()
for i in range(length):
    #temp=topology_check_obj.disconnected_conditions['故障元件索引']
    fault_idx=temp[i]
    print('计算到%s'%str(fault_idx))
    dlpf_in_disconnected_conditions_obj = DLPFInDisconnectedConditions(branch_data=branch_data,bus_data=bus_data,fault_idx=fault_idx)
    dlpf_in_disconnected_conditions_obj.generate_subgraph_data()
    dlpf_in_disconnected_conditions_obj.pf_judgement()
    pf_flag=dlpf_in_disconnected_conditions_obj.pf_flag
    temp_list.append({'故障索引':fault_idx,'子网能否直接潮流计算':pf_flag})
end=time.time()
df=pd.DataFrame(temp_list)
print(df)
print('计算时间',end-start)



