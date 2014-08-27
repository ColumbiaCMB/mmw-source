# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 11:21:47 2014

@author: lab computer
"""

import numpy as np
import bisect

import interpolater

class MmwSweepData(object):
    def __init__(self,fundamental_freqs=None,zbd_voltages=None):
        if fundamental_freqs is None:
            self._fundamental_freqs = []
            self._zbd_voltages = []
        else:
            self._fundamental_freqs = fundamental_freqs            
            self._zbd_voltages = zbd_voltages
        self.interpolater = interpolater.interpolater()
    
    def add_points(self,fundamental_freqs, zbd_voltages):
        fundamental_freqs = np.atleast_1d(fundamental_freqs)
        zbd_voltages = np.atleast_1d(zbd_voltages)
        for (fundamental_freq,zbd_voltage) in zip(fundamental_freqs,zbd_voltages):
            index = bisect.bisect(self._fundamental_freqs, fundamental_freq)
            self._fundamental_freqs.insert(index, fundamental_freq)
            self._zbd_voltages.insert(index, zbd_voltage)
    
    @property
    def mmw_freq(self):
        return 12.0 * np.array(self._fundamental_freqs)
        
    @property
    def mmw_freq_ghz(self):
        return self.mmw_freq/1e9
        
    @property
    def fundamental_freq(self):
        return np.array(self._fundamental_freqs)
        
    @property
    def fundamental_freq_ghz(self):
        return self.fundamental_freq/1e9
        
    @property
    def zbd_voltage(self):
        return np.array(self._zbd_voltages)
        
    @property
    def power_watts(self):
        power,freq,scale = self.interpolater.convert(self.fundamental_freq,self.zbd_voltage)
        return np.array(power)
        
    @property
    def power_dbm(self):
        return 10*np.log10(self.power_watts/1e-3)