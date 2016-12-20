# -*- coding: utf-8 -*-
"""
*******************************************************************************

      REDFIELD RATE MATRIX

*******************************************************************************
"""  

import numpy

from ....core.implementations import implementation
from ....core.units import cm2int
from ....core.units import kB_intK

from ...hilbertspace.hamiltonian import Hamiltonian
from ...liouvillespace.systembathinteraction import SystemBathInteraction

   
class RedfieldRateMatrix:
    """Redfield relaxation rate matrix
    
    Redfield population relaxation rate matrix is calculated from the 
    Hamiltonian and system-system bath interation. The bath
    correlation functions are Fourier transformed by FFT and the negative
    frequency part is calculated from the expected thermodynamic
    symmetry. 
    
    Parameters
    ----------
    
    ham : Hamiltonian
        Hamiltonian object 
        
    sbi : SystemBathInteraction
        SystemBathInteraction object
        
    initialize : bool (default True)
        If true, the rates will be calculated when the object is created
        
    cutoff_time : float
        If cutoff time is specified, the tensor is integrated only up to the
        cutoff time
    
    
    """
    
    def __init__(self, ham, sbi, initialize=True, cutoff_time=None):
        
        if not isinstance(ham, Hamiltonian):
            raise Exception("First argument must be a Hamiltonian")
            
        if not isinstance(sbi, SystemBathInteraction):
            raise Exception("Second argument must be a SystemBathInteraction")
            
        self._is_initialized = False            
        self._has_cutoff_time = False
        
        if cutoff_time is not None:
            self.cutoff_time = cutoff_time
            self._has_cutoff_time = True            
            
        self.ham = ham
        self.sbi = sbi
        
        if initialize: 
            self._set_rates()          
            self._is_initialized = True
                
                
    def _set_rates(self):
        """ Reference implementation, completely in Python
        
        """
        
        # dimension of the Hamiltonian (includes excitons
        # with all multiplicities specified at its creation)
        Na = self.ham._data.shape[0]
     
        # number of components
        Nk = self.sbi.N  
        
        if Nk <= 0:
            raise Exception("No system bath intraction components present")
        
        # Eigen problem
        hD,SS = numpy.linalg.eigh(self.ham._data) 
        S1 = numpy.linalg.inv(SS)
        
        # component operators
        KI = self.sbi.KK.copy()
        
        #FIXME: This has to be made configurable
        # frequency cut-off
        freq_cutoff = 3000.0*cm2int
        #print("freq. cut-off",freq_cutoff)
        
        # temperature
        Temp = self.sbi.CC.get_correlation_function(0,0).temperature
        
        
        # transform interaction operators
        for i in range(Nk):
            KI[i,:,:] = numpy.dot(S1,numpy.dot(KI[i,:,:],SS))
            
        #  Find all eigenfrequencies 
        Om = numpy.zeros((Na,Na))
        for a in range(0,Na):
            for b in range(0,Na):
                Om[a,b] = hD[a] - hD[b]
                
        # calculate values of the spectral density at frequencies
        cc = numpy.zeros((Nk,Na,Na),dtype=numpy.float64)
        
        # loop over components
        for k in range(Nk):

            # correlation function
            cf = self.sbi.CC.get_correlation_function(k,k)
            
            # Ft correlation function
            cw = cf.get_Fourier_transform()
            

            # Spectral density at all frequencies
            for i in range(Na):
                for j in range(Na):
                    if i != j:
                        if numpy.abs(Om[j,i]) > freq_cutoff:
                            cc[k,i,j] = 0.0
                        else:
                            if Om[j,i] < 0.0:
                                #cc[k,i,j] = (cf.interp_data(Om[i,j])
                                cc[k,i,j] = numpy.real((cw.at(Om[i,j],
                                approx="spline")
                                *numpy.exp(-Om[i,j]/(kB_intK*Temp))))
                            else:
                                cc[k,i,j] = numpy.real(cw.at(Om[j,i],
                                approx="spline"))
                                

        
        # create storage for the rates
        self.data = numpy.zeros((Na,Na), dtype=numpy.float)

        # calculate rate matrix
        #
        # To submit: 
        #                Na
        #                Nk
        #                KI[Nk,Na,Na]
        #                cc[Nk,Na,Na]
        #                
        #     
        #    To return:
        #                RR
        #                
        werror = numpy.zeros(2,dtype=numpy.int8)
        rtol = 1.0e-6        
        ssRedfieldRateMatrix(Na, Nk, KI,
                             cc, rtol, werror, self.data)
        
        if werror[1] == -1:
            print("Warning: Redfield rates signicantly smaller than 0")     
                               
        self._is_initialized = True
        
        

@implementation("redfield","ssRedfieldRateMatrix",
                at_runtime=True,
                fallback_local=True,
                always_local=True)
def ssRedfieldRateMatrix(Na, Nk, KI, cc, rtol, werror, RR):
    """Standard redfield rates
    
    
    Parameters
    ----------
    
    Na : integer
        Rank of the rate matrix, number of excitons
        
    Nk : integer
        Number of components of the interaction Hamiltonian
    
    KI : float array
        System parts of the interaction Hamiltonian components
        
    cc : float array
        Half of the Fourier transform of the correlation functions 
        at all transition frequencies
        
    RR : real array
        Relaxation rate matrix (to be calculated and returned)
    
    """
    
    # loop over components
    for k in range(Nk):
        
        # interaction operator
        KK = KI[k,:,:]

        for i in range(Na):
            for j in range(Na):
                
                # calculate rates, i.e. off diagonal elements
                if i != j:                                
                            
                    RR[i,j] += (cc[k,i,j]*KK[i,j]*KK[j,i])

                    if RR[i,j] < 0.0:
                        werror[0] = -1
                        if numpy.abs(RR[i,j]) < rtol:
                            RR[i,j] = 0.0
                        else:
                            werror[1] = -1
                            
    # calculate the diagonal elements (the depopulation rates)            
    for i in range(Na):
        for j in range(Na):
            if i != j:
                RR[j,j] -= RR[i,j]
                    
                    
                    
