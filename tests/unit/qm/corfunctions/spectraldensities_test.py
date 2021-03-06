# -*- coding: utf-8 -*-


import unittest
import numpy

import matplotlib.pyplot as plt

"""
*******************************************************************************


    Tests of the quantarhei.qm.corfunctions.spectraldensities module


*******************************************************************************
"""


from quantarhei import SpectralDensity, CorrelationFunction
from quantarhei import TimeAxis
from quantarhei import energy_units

class TestSpectralDensity(unittest.TestCase):
    """Tests spectral densities module
    
    
    """
    
    def test_underdamped_brownian_oscillator(self):
        """Testing Underdamped Brownian oscillator spectral density
        
        """
        
        par = dict(ftype="UnderdampedBrownian",
                      reorg = 1.0,
                      freq = 500.0,
                      gamma = 1.0/500.0)
        
        parO = dict(ftype="OverdampedBrownian",
                      reorg = 200.0,
                      cortime = 100.0,
                      T = 300.0)
        
        par["T"] = 300.0
        
        params = []
        for i in range(5):
            p = par.copy()
            p["freq"] = par["freq"] + (i+1)*200.0
            params.append(p)
        
        time = TimeAxis(0.0, 100000, 1.0)
        
        #
        # Adding through correlation functions
        #
        with energy_units("1/cm"):
            
            sd = SpectralDensity(time, par)            
            cf = sd.get_CorrelationFunction(temperature=300)
            
            #cf.plot()
            
            tot_cf = cf
            tot_cf.axis = time
            
            for p in params:
                sd = SpectralDensity(time,p)
                cf = sd.get_CorrelationFunction(temperature=300)
                cf.axis = time
                tot_cf += cf
                
            #tot_cf.plot(show=False)
            ct = CorrelationFunction(time, parO)

            tot_cf += ct
            
            tot_sd1 = tot_cf.get_SpectralDensity()
            #tot_sd1.plot(show=False)
            

            #tt.plot()
            
        #
        # Adding through SpectralDensity
        #
        with energy_units("1/cm"):
            
            sd = SpectralDensity(time, par)  
            ax = sd.axis
            tot_sd2 = sd
            
            for p in params:
                sd = SpectralDensity(time, p)  
                sd.axis = ax
                tot_sd2 += sd
                
            ov = SpectralDensity(time, parO)
            ov.axis = ax
            
            tot_sd2 += ov
                
            #tot_sd2.plot(color="-r")
            
        numpy.testing.assert_allclose(tot_sd1.data, tot_sd2.data, atol=1.0e-3)
        
        cf1 = tot_sd1.get_CorrelationFunction(temperature=300)
        cf2 = tot_sd2.get_CorrelationFunction(temperature=300)
        
        #cf1.plot(show=False)
        #cf2.plot(color="-r", axis=[0.0, 2000, 
        #                           numpy.min(cf1.data)-numpy.max(cf1.data)*0.1,
        #                            numpy.max(cf1.data)*1.1])
    
        numpy.testing.assert_allclose(cf1.data, cf2.data, atol=1.0e-3)
        
    