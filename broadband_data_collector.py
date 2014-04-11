import lockin_controller
import time
import numpy as np
import os

class collector():
    def __init__(self,  serial_port='COM6'):
        self.l=lockin_controller.lockinController(serial_port=serial_port)
        self.x_list=[]
        self.y_list=[]
        self.r_list=[]
        self.theta_list=[]
        self.x_std_list=[]
        self.y_std_list=[]
        self.r_std_list=[]
        self.theta_std_list=[]
        self.mickey_turns_list=[]
        self.minnie_turns_list=[]
    
    def collect_data(self, mickey_turns, minnie_turns):
        x_points=[]
        y_points=[]
        r_points=[]
        theta_points=[]
        for i in range(10):
            data_string=self.l.get_data()
            data_string=data_string.strip('\r')
            data_list=data_string.split(',')
            x_points.append(float(data_list[0]))
            y_points.append(float(data_list[1]))
            r_points.append(float(data_list[2]))
            theta_points.append(float(data_list[3]))
            time.sleep(0.01)
        x=np.mean(x_points)
        y=np.mean(y_points)
        r=np.mean(r_points)
        theta=np.mean(theta_points)
        x_std=np.std(x_points)
        y_std=np.std(y_points)
        r_std=np.std(r_points)
        theta_std=np.std(theta_points)
    
        self.mickey_turns_list.append(mickey_turns)
        self.minnie_turns_list.append(minnie_turns)
        self.x_list.append(x)
        self.x_std_list.append(x_std)
        self.y_list.append(y)
        self.y_std_list.append(y_std)
        self.r_list.append(r)
        self.r_std_list.append(r_std)
        self.theta_list.append(theta)
        self.theta_std_list.append(theta_std)
        
    def save(self):
        fn=time.strftime('%Y-%m-%d_%H-%M-%S')
        base_dir='C:\Users\lab computer\Documents\data\mmwave_source_broadband'
        fn = os.path.join(base_dir,fn)
        fn+='.npz'
        np.savez(fn, mickey_turns=self.mickey_turns_list, minnie_turns=self.minnie_turns_list, x=self.x_list, x_std=self.x_std_list, y=self.y_list, y_std=self.y_std_list,
                    r=self.r_list, r_std=self.r_std_list, theta=self.theta_list, theta_std=self.theta_std_list)
                    
    def reset(self):
        self.mickey_turns_list=[]
        self.minnie_turns_list=[]
        self.x_list=[]
        self.y_list=[]
        self.r_list=[]
        self.theta_list=[]
        self.x_std_list=[]
        self.y_std_list=[]
        self.r_std_list=[]
        self.theta_std_list=[]