import lockin_controller
import hittite_controller
import numpy as np
import time
import os

l=lockin_controller.lockinController(serial_port='COM6')
# For running this script on the windows laptop by the source.
h=hittite_controller.hittiteController()

start=10e9
stop=14.05e9
step=0.05e9

freq_list=[]
x_list=[]
y_list=[]
r_list=[]
theta_list=[]

h.on()
time.sleep(0.1)
for freq in np.arange(start,stop,step):
    freq_list.append(freq)
    h.set_freq(float(freq))
    time.sleep(20)
    data_string=l.get_data()
    data_string=data_string.strip('\r')
    data_list=data_string.split(',')
    x_list.append(float(data_list[0]))
    y_list.append(float(data_list[1]))
    r_list.append(float(data_list[2]))
    theta_list.append(float(data_list[3]))
h.off()

fn=time.strftime('%Y-%m-%d_%H-%M-%S')
base_dir='C:\Users\lab computer\Documents\data\mmwave_source_sweeps'
fn = os.path.join(base_dir,fn)
fn+='.npz'
np.savez(fn, freq=freq_list, x=x_list, y=y_list, r=r_list, theta=theta_list)

print freq_list
print x_list
print y_list
print r_list
print theta_list
