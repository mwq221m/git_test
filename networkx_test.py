import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.traversal import depth_first_search
import time
G=nx.Graph()
branch_data=pd.read_excel('test.xlsx',sheet_name=0)
bus_data = pd.read_excel('test.xlsx', sheet_name=1)
G.add_nodes_from([1,2,3])
G.add_edges_from([(1,2),(2,3),(1,3)])

G[1][2]['weight']=10#观察数据结构 本质上是字典数据
G[1][3]['weight']=20
G[2][3]['weight']=30
G.add_node(4)
G.add_node(5)
G.add_edge(4,5,weight=50)
#G.add_edge(1,5,weight=25)
path=nx.dijkstra_path(G,source=1,target=3,weight='weight')
print('节点4是否与1联通',nx.has_path(G,source=1,target=4))
print(path)
#depth_path=nx.edge_dfs(G,source=1)
start=time.time()
depth_path=[i for i in nx.edge_dfs(G,source=5)]#通过深度优先遍历后是否包括所有节点判断网络是否有解列
breadth_path=[i for i in nx.edge_bfs(G,source=5)]
end=time.time()
print('深度优先',depth_path)
print('广度优先',breadth_path)
print('搜索时间',end-start)
G.nodes[1]['type']='R'
nx.add_star(G_to_add_to=G,nodes_for_star=[1])
print(G.edges(data=True))
print(G.nodes(data=True))
print('直接判断是否连接',nx.is_connected(G))
isolated_nodes=[i for i in nx.isolates(G)]
print('孤岛节点',isolated_nodes)
connected_condition=[i for i in nx.connected_components(G)]
print('连通情况',connected_condition)
pos=nx.shell_layout(G)
nx.draw(G,pos,with_labels=True)
plt.show()

