import lockin_controller
import hittite_controller
import time

l=lockin_controller.lockinController()
h=hittite_controller.hittiteController()

start=10000000000
stop=10500000000
step=100000000

data=[]

h.on()
time.sleep(0.1)
for freq in range(start,stop,step):
    h.set_freq(float(freq))
    time.sleep(10)
    l.get_idn()
    data_point=l.get_data()
    data.append(data_point)
h.off()

print data
