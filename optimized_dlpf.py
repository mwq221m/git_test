import numpy as np

from dlpf import DLPF
import pandas as pd
import gurobipy as grb
import numpy as np
class OptimizedDLPF(DLPF):
    def __init__(self,branch_data,bus_data):
        super(OptimizedDLPF, self).__init__(branch_data=branch_data,bus_data=bus_data)
        self.model=grb.Model()
        self.P=self.model.addMVar(shape=self.bus_num,name='P')
        self.Q=self.model.addMVar(shape=self.bus_num,lb=-grb.GRB.INFINITY,name='Q')
        self.V=self.model.addMVar(shape=self.bus_num,name='V')
        self.THETA=self.model.addMVar(shape=self.bus_num,name='THETA')
        self.model.addConstr(self.P==-self.B_without_shunt@self.THETA+self.G@self.V)
        self.model.addConstr(self.Q==-self.G@self.THETA-self.B@self.V)

        self.model.addConstr(self.P.sum()==0)
        self.model.addConstr(self.Q.sum() == 0)


    def runpf(self):
        cut_list=[]
        p_dic={}
        q_dic={}
        for i in range(self.bus_num):
            temp=self.bus_data.iloc[i]
            type=temp['type']
            p=temp['p']
            q=temp['q']
            v=temp['v']
            theta=temp['theta']
            if type=='R':
                self.model.addConstr(self.V[i]==v)
                self.model.addConstr(self.THETA[i]==theta)
            if type=='S':
                # self.model.addConstr(self.P[i]==p)
                p_dic[i]=p
                self.model.addConstr(self.V[i]==v)
                cut_list.append(i)
            if type=='L':
                #self.model.addConstr(self.P[i]==p)
                #self.model.addConstr(self.Q[i]==q)
                p_dic[i]=p
                q_dic[i]=q
                cut_list.append(i)
        self.c=self.model.addVars(cut_list)
        print(p_dic)
        print(cut_list)
        self.model.addConstr(self.P[1] == p_dic[1] + self.c[1])#需改成这样后依旧报错 也许矩阵形式变量在gurobi不能这样写
        self.model.addConstrs(self.P[i]==p_dic[i]+self.c[i] for i in cut_list)########这里报错
        self.model.setObjective(grb.quicksum(self.c[i] for i in cut_list))
        self.model.optimize()






        





if __name__=='__main__':
    branch_data = pd.read_excel('test.xlsx', sheet_name=0)
    bus_data = pd.read_excel('test.xlsx', sheet_name=1)
    obj=OptimizedDLPF(branch_data=branch_data,bus_data=bus_data)
    obj.runpf()