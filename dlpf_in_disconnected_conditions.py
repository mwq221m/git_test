import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
#import pandasgui as pg
from dlpf import DLPF
'''
除了各个子网分区信息需要识别正确 还需要注意可能存在的切负荷问题
例如一个分区只有一个pv节点 其余都是pq且负荷需求远超p
可以现在子图中将节点类型和负荷大小信息加入图中
'''
'''
主要作用是判断网络是否有解列，若有则将各个子网节点重新编号 并且判断当前子网是否适合直接进行潮流计算（网络是否含有平衡节点or子网有功注入大于零）
'''
class DLPFInDisconnectedConditions():
    def __init__(self,branch_data,bus_data,fault_idx):
        self.branch_data=branch_data
        self.bus_data=bus_data
        self.bus_type={}
        self.bus_p={}
        self.bus_q={}
        self.fault_idx=fault_idx
        self.fault_num=len(self.fault_idx)
        self.bus_num = len(self.bus_data)
        self.branch_num = len(self.branch_data)
        self.net = nx.Graph()
        self.node_list = []
        self.edge_list = []
        for i in range(self.bus_num):
            temp = self.bus_data.iloc[i]
            num = temp['num']
            self.node_list.append(num)
            type=temp['type']
            p=temp['p']
            q=temp['q']
            self.bus_type[num]=type
            self.bus_p[num]=p
            self.bus_q[num]=q


        for i in range(self.branch_num):
            temp = self.branch_data.iloc[i]
            start = int(temp['start'])
            end = int(temp['end'])
            status = temp['status']
            if status == 1:
                self.edge_list.append((start, end))
        self.net.add_nodes_from(self.node_list)

        for i,j in self.bus_p.items():
            self.net.nodes[i]['p']=j
        for i,j in self.bus_q.items():
            self.net.nodes[i]['q']=j
        for i,j in self.bus_type.items():
            self.net.nodes[i]['type']=j

        self.net.add_edges_from(self.edge_list)
        self.remove_list=[]
        for i in self.fault_idx:
            temp=self.branch_data.iloc[i]
            start=int(temp['start'])
            end=int(temp['end'])
            status=temp['status']
            self.remove_list.append((start,end))
        self.net.remove_edges_from(self.remove_list)
        self.number_connected_components = nx.number_connected_components(self.net)
        #self.connected_components=nx.connected_components(self.net)
        self.connected_components=[i for i in nx.connected_components(self.net)]
        self.subgraph=[nx.Graph() for i in range(self.number_connected_components)]
        for i in range(self.number_connected_components):
            #g=self.subgraph[i]
            nbunch=self.connected_components[i]
            #print(nbunch)
            self.subgraph[i]=nx.subgraph(self.net,nbunch=nbunch)

        temp_branch_data=self.branch_data.copy()
        temp_branch_data=temp_branch_data.drop([i for i in range(self.branch_num)])#dataframe的drop和append需要x=x.drop()的形式
        temp_bus_data=self.bus_data.copy()
        temp_bus_data=temp_bus_data.drop([i for i in range(self.bus_num)])
        self.branch_data_list=[temp_branch_data for i in range(self.number_connected_components)]
        self.bus_data_list=[temp_bus_data for i in range(self.number_connected_components)]

        self.subgraph_nodes_num=[]
        self.subgraph_edges_num=[]
        for i in range(self.number_connected_components):
            g=self.subgraph[i]
            self.subgraph_nodes_num.append(g.number_of_nodes())
            self.subgraph_edges_num.append(g.number_of_edges())






    def draw(self):
        plt.figure()
        nx.draw(self.net,with_labels=True)
        plt.show()

    def draw_subgraph(self):
        for i in range(self.number_connected_components):
            plt.figure()
            nx.draw(self.subgraph[i],with_labels=True)
            plt.show()

    def generate_subgraph_branches_data(self,subgraph_index):
        branches_num=self.subgraph_edges_num[subgraph_index]
        g=self.subgraph[subgraph_index]
        branches_list=[i for i in g.edges]
        for i in range(branches_num):
            branch=branches_list[i]
            start=branch[0]
            end=branch[1]
            self.branch_data_list[subgraph_index]=self.branch_data_list[subgraph_index].append(self.branch_data[self.branch_data.apply(lambda x:x['start']==start and x['end']==end,axis=1)])

    def generate_subgraph_nodes_data(self,subgraph_index):
        nodes_num=self.subgraph_nodes_num[subgraph_index]
        g=self.subgraph[subgraph_index]
        nodes_list=[i for i in g.nodes]
        for i in range(nodes_num):
            node=nodes_list[i]
            self.bus_data_list[subgraph_index]=self.bus_data_list[subgraph_index].append(self.bus_data[self.bus_data['num']==node])







    def generate_subgraph_data(self):
        for i in range(self.number_connected_components):
            self.generate_subgraph_branches_data(subgraph_index=i)
            self.generate_subgraph_nodes_data(subgraph_index=i)

    def pf_judgement_for_subgraph(self,subgraph_index):
        flag=0
        g=self.subgraph[subgraph_index]
        branch_data=self.branch_data_list[subgraph_index]
        bus_data=self.bus_data_list[subgraph_index]
        if len(branch_data)>0:#判断不是孤岛节点
            if 'R' in list(bus_data['type']):#子网有平衡节点可直接潮流计算
                flag=1
            if bus_data['p'].sum()>0:#没有平衡节点时有功注入大于零可认为电源充足 将一个PV节点替换为平衡节点即可
                flag=1
        return flag

    def pf_judgement(self):
        self.pf_flag=[]
        for i in range(self.number_connected_components):
            flag=self.pf_judgement_for_subgraph(subgraph_index=i)
            self.pf_flag.append(flag)





if __name__=='__main__':
    branch_data = pd.read_excel('14_bus_test.xlsx', sheet_name=0)
    bus_data = pd.read_excel('14_bus_test.xlsx', sheet_name=1)
    fault_idx=(0,1,2)
    obj=DLPFInDisconnectedConditions(branch_data=branch_data,bus_data=bus_data,fault_idx=fault_idx)
    obj.draw()
    obj.draw_subgraph()
    obj.generate_subgraph_data()
    #pg.show(bus_data)
    obj.pf_judgement()




