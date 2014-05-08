import lockin_controller
import numpy as np
import time
import os

class driftController():
    def __init__(self, serial_port='COM6'):
        # For running this script on the windows laptop by the source.
        self.l=lockin_controller.lockinController(serial_port=serial_port)
        self.x_list=[]
        self.y_list=[]
        self.r_list=[]
        self.theta_list=[]
        self.x_std_list=[]
        self.y_std_list=[]
        self.r_std_list=[]
        self.theta_std_list=[]
        
        self.time_list=[]
        
    def perform_drift(self, length_of_drift):
        time.sleep(0.1)
        start = time.time()
        now = time.time()
        while now-start < length_of_drift:
            time.sleep(0.1)
            self.collect_data()
            now = time.time()
            self.time_list.append(now-start)
        self.save()
            
    def collect_data(self):
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
        base_dir='C:\Users\lab computer\Documents\data\mmwave_source_drifts'
        fn = os.path.join(base_dir,fn)
        fn+='.npz'
        np.savez(fn, time=self.time_list, x=self.x_list, x_std=self.x_std_list, y=self.y_list, y_std=self.y_std_list,
                     r=self.r_list, r_std=self.r_std_list, theta=self.theta_list, theta_std=self.theta_std_list)
                    
    def reset(self):
        self.x_list=[]
        self.y_list=[]
        self.r_list=[]
        self.theta_list=[]
        self.x_std_list=[]
        self.y_std_list=[]
        self.r_std_list=[]
        self.theta_std_list=[]
                    
def main():
    drift=driftController()
    drift.perform_drift()
    
if __name__=='__main__':
    main()
