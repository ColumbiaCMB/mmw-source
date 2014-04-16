import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

class attenuationConverter():
    def __init__(self,prefix='data_for_processing/',datafile='2014-04-11_broadband-attenuator-response.npz'):
        self.data=np.load(prefix+datafile)
        self.output_to_db()
        
    def output_to_db(self):
        self.db_list=range(len(self.data['x']))
        for i in range(len(self.db_list)):
            self.db_list[i]=self.data['x'][i]/self.data['x'][0]
            self.db_list[i]=np.log10(abs(self.db_list[i]))
            # Abs is so negative values don't ruin the interpolation.
            # negative signals are the result of noise, so at this level, we should probably just truncate the function.
            self.db_list[i]*=10.0
            
    def interpolate_db(self):
        #self.interpolating_function=interpolate.splrep(self.data['mickey_turns'][:46],self.db_list,s=0)
        plt.plot(self.db_list[:46],self.data['mickey_turns'][:46],'--o')
        self.interpolating_function=interpolate.splrep(self.db_list,self.data['mickey_turns'][:46],s=0)
        # Why doesn't this work? After cutting off the noise, the function doesn't have multiple y values for a single x value.
        

    def give_turns(self, attenuation):
        # Only use the first 46 points because after that we hit the noise floor (and interpolating for y fails since there are multiple x-values.)
        atten_reduced=np.array(self.db_list[:46])-attenuation
        freduced=interpolate.UnivariateSpline(self.data['mickey_turns'][:46],atten_reduced,s=0)
        return freduced.roots()
        
    def give_watts(self, data_list):
        volt_list=data_list
        first_harmonic_factor=np.pi/2.0
        rms_factor=np.sqrt(2)
        for i in range(len(volt_list)):
            volt_list[i]=volt_list[i]*first_harmonic_factor*rms_factor
        pow_multiplier=2300
        # Grabbed a central value for the broadband conversion.
        pow_list=[0]*len(volt_list)
        for i in range(len(volt_list)):
            # Multiplies each voltage by its associated multiplier, giving a list of powers for the given frequencies.
            pow_list[i]=volt_list[i]/pow_multiplier
        # Power list is now in watts.
        return pow_list
        
    def give_dbm(self, data_list):
        pow_list=self.give_watts(data_list)
        for i in range(len(pow_list)):
            pow_list[i]=np.log10(abs(pow_list[i]))*10.0+30
            # Abs needed because a) power can't be negative and b) because negative voltages are due to the noise floor.
        return pow_list
        
def main():
    ac=attenuationConverter()
    while True:
        response=raw_input('Type attenuation to get number of turns, or exit:\n')
        if response == 'exit':
            break
        try:
            turns=ac.give_turns(float(response))[0]
            print 'Attenuation of %s is given by %f turns.'%(response,turns)
        except ValueError as e:
            print 'Attenuation input must be convertable to a float.'
        except IndexError as e:
            print 'Attenuation input is out of range of the mmwave-source\'s attenuators.'
            
if __name__=='__main__':
    main()
