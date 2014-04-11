import numpy as np
import matplotlib.pyplot as pyplot
import interpolater

data_files=  [
            '2014-04-10_0_turns_both.npz','2014-04-10_4_turns_both.npz','2014-04-10_6_turns_both.npz',
            '2014-04-10_8_turns_both.npz','2014-04-10_10_turns_both.npz'
            ]

interp=interpolater.interpolater()
pow_list=range(len(data_files))
freq_list=range(len(data_files))
mult_list=range(len(data_files))
prefix='./data_for_processing/'

for i in range(len(data_files)):
    data=np.load(prefix+data_files[i])
    pow_list[i],freq_list[i],mult_list[i]=interp.convert(data['freq'],data['x'])
    
pyplot.subplot(1,1,1)
for i in range(len(data_files)):
    pyplot.plot(freq_list[i],pow_list[i])
pyplot.yscale('log')
pyplot.xlabel('Frequency')
pyplot.ylabel('Power (W)')

pyplot.show()
