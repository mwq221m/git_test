import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from itertools import combinations
import time
'''
对一个网络进行N-k下的故障组合枚举，找出所有的基础事故集
'''
class TopologyCheck():
    def __init__(self,branch_data,bus_data,number_of_faults):
        self.branch_data=branch_data
        self.bus_data=bus_data
        self.bus_num=len(self.bus_data)
        self.branch_num=len(self.branch_data)
        self.net=nx.Graph()
        self.node_list=[]
        self.edge_list=[]
        for i in range(self.bus_num):
            temp=self.bus_data.iloc[i]
            num=temp['num']
            self.node_list.append(num)
        for i in range(self.branch_num):
            temp=self.branch_data.iloc[i]
            start=int(temp['start'])
            end=int(temp['end'])
            status=temp['status']
            if status==1:
                self.edge_list.append((start,end))
        self.net.add_nodes_from(self.node_list)
        self.net.add_edges_from(self.edge_list)
        self.connection_flag=nx.is_connected(self.net)
        self.number_connected_components=nx.number_connected_components(self.net)
        self.disconnected_conditions=[]
        self.number_of_faults=number_of_faults

    def draw(self):
        nx.draw(self.net,with_labels=True)
        plt.show()

    def show_result(self):
        if self.connection_flag==False:
            print('网络解列')
            print('连通分量',self.number_connected_components)
        else:
            print('网络连通')

    def search_disconnected_conditions(self):
        self.disconnection_num=0
        for k in range(1,self.number_of_faults+1):#n-k枚举
            #idx_list=[i for i in combinations(range(self.branch_num),self.number_of_faults)]
            idx_list = [i for i in combinations(range(self.branch_num), k)]
            #g=self.net.copy()
            for fault_branches_idx in idx_list:
                g = self.net.copy()
                remove_list=[]
                for i in fault_branches_idx:
                    temp=self.branch_data.iloc[i]
                    start=int(temp['start'])
                    end=int(temp['end'])
                    remove_list.append((start,end))
                g.remove_edges_from(remove_list)
                flag=nx.is_connected(g)
                num=nx.number_connected_components(g)
                if num>1:
                    self.disconnection_num+=1
                #if flag==False:
                connected_info=[i for i in nx.connected_components(g)]
                self.disconnected_conditions.append({'故障元件索引':fault_branches_idx,'连通分量':num,'连通情况':connected_info})
        self.disconnected_conditions=pd.DataFrame(self.disconnected_conditions)











if __name__=='__main__':
    branch_data = pd.read_excel('14_bus_test.xlsx', sheet_name=0)
    bus_data = pd.read_excel('14_bus_test.xlsx', sheet_name=1)
    obj=TopologyCheck(branch_data=branch_data,bus_data=bus_data,number_of_faults=3)
    #obj.connection_check()
    #print(obj.node_list)
    #print(obj.edge_list)
    #print(obj.depth_path)
    #print(obj.connection_check())
    #obj.connection_check()
    print(obj.connection_flag)
    print(obj.number_connected_components)
    obj.show_result()
    start=time.time()
    obj.search_disconnected_conditions()
    end=time.time()
    print(obj.disconnected_conditions)
    print('n-3下解列情况数',obj.disconnection_num)
    print('搜索时间',end-start)
    obj.draw()
    '''
    会造成网络解列的事故集已经能够枚举，要考虑的是各个子网的潮流计算
    平衡节点数应等于子网个数，对故障前的节点信息需要修改
    解列网络中观察是否有孤岛节点
    先做到能够枚举计算完预想事故集的所有潮流
    '''




