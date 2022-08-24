import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import weibull_min,relfreq
from scipy import integrate
from dlpf import DLPF
import pandas as pd
import time

class MCS():
    def wind_speed_to_pg2(self,v, v_in, v_rated, v_out, p_max):
        if v < v_in or v > v_out:
            return 0
        if v_in <= v <= v_rated:
            return (v - v_in) * p_max / (v_rated - v_in)
        if v_rated < v <= v_out:
            return p_max



    def __init__(self,simulation_num,branch_data,bus_data):
        self.simulation_num=simulation_num
        self.branch_data=branch_data
        self.bus_data=bus_data
        self.wind_speed=weibull_min.rvs(1.4, loc=0, scale=6, size=self.simulation_num)
        #self.pg2=self.wind_speed_to_pg2(v=self.wind_speed)
        #self.pg2=np.vectorize(self.wind_speed_to_pg2)(v=self.wind_speed)
        self.pg2=[]
        for i in range(self.simulation_num):
            current_wind_speed=self.wind_speed[i]
            current_pg2=self.wind_speed_to_pg2(v=current_wind_speed,v_in=2,v_rated=15,v_out=30,p_max=0.5)#额定功率修改为0.5 不再是课件中原本的0.2
            self.pg2.append(current_pg2)
        self.pd2=np.random.normal(loc=0.5,scale=0.1,size=self.simulation_num)#注意均值和标准差的量纲相同，为了不出现负值应该将标准差调整的较小
        self.pd3=np.random.normal(loc=0.6,scale=0.1,size=self.simulation_num)
        self.qd3=np.random.normal(loc=0.25,scale=1,size=self.simulation_num)
        self.simulation_result=[]
        self.v3=[]
        self.v3_risk=0

    def simulate(self):
        for i in range(self.simulation_num):
            pg2=self.pg2[i]
            pd2=self.pd2[i]
            pd3=self.pd3[i]
            qd3=self.qd3[i]
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
            self.v3.append(v3)
            self.simulation_result.append({'pg2':pg2,'pd2':pd2,'pd3':pd3,'qd3':qd3,'v3':v3})
        self.simulation_result=pd.DataFrame(self.simulation_result)

    def result_analysis(self):
        res=relfreq(self.v3,numbins=200)
        x = res.lowerlimit + np.linspace(0, res.binsize * res.frequency.size, res.frequency.size)
        plt.figure()
        plt.bar(x, res.frequency, width=res.binsize)
        plt.show()
        cdf_value = np.cumsum(res.frequency)
        plt.figure()
        plt.bar(x, cdf_value, width=res.binsize)
        plt.show()
        sum_temp=0
        for i in range(self.simulation_num):
            v=self.v3[i]
            if v<0.94:
                sum_temp+=np.abs(v-0.94)
            if v>1.06:
                sum_temp+=np.abs(v-1.06)
        sum_temp/=self.simulation_num
        self.v3_risk=sum_temp




if __name__=='__main__':
    branch_data = pd.read_excel('test.xlsx', sheet_name=0)
    bus_data = pd.read_excel('test.xlsx', sheet_name=1)
    start=time.time()
    obj=MCS(simulation_num=5000,branch_data=branch_data,bus_data=bus_data)
    obj.simulate()
    #print(obj.simulation_result)
    obj.result_analysis()
    print('v3越限风险指标',obj.v3_risk)
    end=time.time()
    print('运算时间',end-start)

