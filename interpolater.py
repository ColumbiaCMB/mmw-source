import numpy as np
from scipy import interpolate





class interpolater():
    def __init__(self):
        frequency=[
            110000000000.0, 111000000000.0, 112000000000.0, 113000000000.0, 114000000000.0, 115000000000.0, 116000000000.0, 117000000000.0, 118000000000.0, 119000000000.0,
            120000000000.0, 121000000000.0, 122000000000.0, 123000000000.0, 124000000000.0, 125000000000.0, 126000000000.0, 127000000000.0, 128000000000.0, 129000000000.0,
            130000000000.0, 131000000000.0, 132000000000.0, 133000000000.0, 134000000000.0, 135000000000.0, 136000000000.0, 137000000000.0, 138000000000.0, 139000000000.0,
            140000000000.0, 141000000000.0, 142000000000.0, 143000000000.0, 144000000000.0, 145000000000.0, 146000000000.0, 147000000000.0, 148000000000.0, 149000000000.0,
            150000000000.0, 151000000000.0, 152000000000.0, 153000000000.0, 154000000000.0, 155000000000.0, 156000000000.0, 157000000000.0, 158000000000.0, 159000000000.0,
            160000000000.0, 161000000000.0, 162000000000.0, 163000000000.0, 164000000000.0, 165000000000.0, 166000000000.0, 167000000000.0, 168000000000.0, 169000000000.0,
            170000000000.0
        ]

        responsivity=[
            2634.80,1886.23,1945.45,1904.90,1901.05,2011.81,1828.98,1681.79,1580.57,1679.26,
            1668.86,1811.99,1945.44,1870.38,2032.32,1960.00,2141.22,1957.13,1883.44,1975.09,
            2242.32,2229.18,1892.01,2107.90,2040.36,2074.15,2161.17,2187.56,2031.67,2072.25,
            1998.11,2146.09,2171.67,2268.67,2183.66,2170.57,2194.42,2143.93,2364.13,2307.40,
            2539.32,2336.46,2358.05,2345.14,2513.41,2456.84,2283.76,2514.44,2539.59,2530.49,
            2596.32,2469.52,2711.63,2679.13,2699.76,2748.04,2752.60,2782.23,2765.05,2774.69,
            2772.08
        ]
        
        # The responsivity gives us the volts/watt for the give frequencies in frequency. We use our interpolating function to fit a responsivity to points which aren't multiples of 1 GHz.
        # The original responsivity values we are interpolating from we given in the ZBD manufacturer's spec sheet.
        
        self.interpolating_function=interpolate.splrep(frequency,responsivity,s=0)
        
    def convert(self,freq_list,volt_list):
        first_harmonic_factor=np.pi/2.0
        # The first harmonic of a square wave with frequency f and amplitude of 1 is 2/pi sin(2pift).
        rms_factor=np.sqrt(2)
        # The lockin amplifier measures the rms voltage of the 1st harmonic.
        # We need to multiply back in the rms factor.
        for i in range(len(volt_list)):
            # Converts lock-in amplifier voltage to real voltage by multiplying in the 1st harmonic proportionality and the rms factor.
            volt_list[i]=volt_list[i]*first_harmonic_factor*rms_factor
        pow_multiplier=interpolate.splev(freq_list,self.interpolating_function,der=0)
        # Interpolates what the multiplier should be for the voltage to power.
        pow_list=[0]*len(volt_list)
        for i in range(len(volt_list)):
            # Multiplies each voltage by its associated multiplier, giving a list of powers for the given frequencies.
            pow_list[i]=volt_list[i]/pow_multiplier[i]
        return pow_list


