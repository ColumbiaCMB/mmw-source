import lockin_controller
import hittite_controller
import numpy as np
import time
import os

class sweepController():
    def __init__(self, serial_port='COM6'):
        # For running this script on the windows laptop by the source.
        self.l=lockin_controller.lockinController(serial_port=serial_port)
        self.h=hittite_controller.hittiteController()
        self.freq_list=[]
        self.x_list=[]
        self.y_list=[]
        self.r_list=[]
        self.theta_list=[]
        self.x_std_list=[]
        self.y_std_list=[]
        self.r_std_list=[]
        self.theta_std_list=[]
        
    def perform_sweep(self,start=11.6666666666e9, stop=13.4e9, step=0.00083333333333e9):
        sweep_start = time.time()
        self.reset()
        print len(self.x_list)
        self.h.on()
        try:
            time.sleep(0.1)
            for freq in np.arange(start,stop,step):
                self.freq_list.append(freq)
                self.h.set_freq(float(freq))
                time.sleep(.2)
                self.collect_data()
            self.save()
        except Exception as e:
            raise e
        finally:
            sweep_stop = time.time()
            print 'Sweep took %f seconds' % (sweep_stop - sweep_start)
            self.h.off()
            
    def sweep_n_times(self, n):
        for i in range(n):
            self.perform_sweep()
            self.reset()
            time.sleep(60)
            
    def collect_data_with_averaging(self):
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
        
    def collect_data(self):
        # Collects one point at each freq step rather than 10.
        # Doesn't average or find std.
        data_string=self.l.get_data()
        data_string=data_string.strip('\r')
        data_list=data_string.split(',')
        x = float(data_list[0])
        y = float(data_list[1])
        r = float(data_list[2])
        theta = float(data_list[3])
        self.x_list.append(x)
        self.y_list.append(y)
        self.r_list.append(r)
        self.theta_list.append(theta)

    def save(self):
        fn=time.strftime('%Y-%m-%d_%H-%M-%S')
        base_dir='C:\Users\lab computer\Documents\data\mmwave_source_sweeps'
        fn = os.path.join(base_dir,fn)
        fn+='.npz'
        np.savez(fn, freq=self.freq_list, x=self.x_list, x_std=self.x_std_list, y=self.y_list, y_std=self.y_std_list,
                    r=self.r_list, r_std=self.r_std_list, theta=self.theta_list, theta_std=self.theta_std_list)
                    
    def reset(self):
        self.freq_list=[]
        self.x_list=[]
        self.y_list=[]
        self.r_list=[]
        self.theta_list=[]
        self.x_std_list=[]
        self.y_std_list=[]
        self.r_std_list=[]
        self.theta_std_list=[]
                    
    
if __name__=='__main__':
    sweep=sweepController()
    sweep.reset()
    sweep.perform_sweep()
