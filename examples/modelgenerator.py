# -*- coding: utf-8 -*-
"""

    Model Generator for Examples and Tests


"""
import numpy

from quantarhei import Manager
from quantarhei import energy_units

from quantarhei import Aggregate
from quantarhei import Molecule
from quantarhei import TimeAxis
from quantarhei import CorrelationFunction


class ModelGenerator():
    
    def __init__(self):
        self.name = ""
        self.molecules = []
    
    
    def get_Aggregate(self, name="dimer-1"):
        
        if name == "dimer-1":
            agg = Aggregate(name=name)
            
        elif name == "trimer-1":
            agg = Aggregate(name=name)
            
            with energy_units("1/cm"):

                m1 = Molecule("Mol 1", [0.0, 10100.0])
                m2 = Molecule("Mol 2", [0.0, 10050.0])
                m3 = Molecule("Mol 3", [0.0, 10000.0])
                
                
                m1.position = [0.0, 0.0, 0.0]
                m2.position = [15.0, 0.0, 0.0]
                m3.position = [10.0, 10.0, 0.0]
                m1.set_dipole(0,1,[5.8, 0.0, 0.0])
                m2.set_dipole(0,1,[5.8, 0.0, 0.0])
                m3.set_dipole(0,1,[numpy.sqrt(12.0), 0.0, 0.0])
                
                agg.add_Molecule(m1)
                agg.add_Molecule(m2)
                agg.add_Molecule(m3)
                
                self.molecules = [m1, m2, m3]
                
            #    m4 = Molecule("Mol 4", [0.0, 11000.0])
            #    m5 = Molecule("Mol 5", [0.0, 11000.0])   
            #    m4.position = [15.0, 15.0, 0.0]
            #    m5.position = [15.0, 10.0, 0.0]
            #    m4.set_dipole(0,1,[5.8, 0.0, 0.0])
            #    m5.set_dipole(0,1,[5.8, 0.0, 0.0])
            #    agg.add_Molecule(m4)
            #    agg.add_Molecule(m5)
                
                agg.set_coupling_by_dipole_dipole()
                
        elif name == "pentamer-1":
            agg = Aggregate(name=name)
            
            with energy_units("1/cm"):

                m1 = Molecule("Mol 1", [0.0, 10100.0])
                m2 = Molecule("Mol 2", [0.0, 10050.0])
                m3 = Molecule("Mol 3", [0.0, 10000.0])
                m4 = Molecule("Mol 4", [0.0, 10200.0])
                m5 = Molecule("Mol 5", [0.0, 10070.0])                
                
                m1.position = [0.0, 0.0, 0.0]
                m2.position = [15.0, 0.0, 0.0]
                m3.position = [10.0, 10.0, 0.0]
                m4.position = [15.0, 15.0, 0.0]
                m5.position = [0, 10.0, 10.0]

                m1.set_dipole(0,1,[5.8, 0.0, 0.0])
                m2.set_dipole(0,1,[5.8, 0.0, 0.0])
                m3.set_dipole(0,1,[numpy.sqrt(12.0), 0.0, 0.0])
                m4.set_dipole(0,1,[5.8, 0.0, 0.0])
                m5.set_dipole(0,1,[5.8, 0.0, 0.0])  
                
                agg.add_Molecule(m1)
                agg.add_Molecule(m2)
                agg.add_Molecule(m3)
                agg.add_Molecule(m4)
                agg.add_Molecule(m5)
                
                self.molecules = [m1, m2, m3, m4, m5]
                
                agg.set_coupling_by_dipole_dipole()
                
        else:
            raise Exception("Unknown model name %s" % name)
            
        return agg
        

    def get_Aggregate_with_environment(self, name="dimer-1_env",
                                       timeaxis=None):

        
        if name == "dimer-1_env":
            agg = self.get_Aggregate(name="dimer-1") 
            agg.name = name
            
            
        elif name == "trimer-1_env":
            agg = self.get_Aggregate(name="trimer-1")
            agg.name = name
            
            if timeaxis is None:
                time = TimeAxis(0, 5000, 1.0)
            else:
                time = timeaxis
                
            with energy_units("1/cm"):
                params = dict(ftype="OverdampedBrownian", reorg=20,
                              cortime=100, T=300)
                print(time)
                cf = CorrelationFunction(time, params)

            m1 = self.molecules[0]
            m1.set_transition_environment((0,1), cf)
            m2 = self.molecules[1]
            m2.set_transition_environment((0,1), cf)
            m3 = self.molecules[2]
            m3.set_transition_environment((0,1), cf)  
            
        elif name == "pentamer-1_env":
            agg = self.get_Aggregate(name="pentamer-1")
            agg.name = name
            
            if timeaxis is None:
                time = TimeAxis(0, 5000, 1.0)
            else:
                time = timeaxis
                
            with energy_units("1/cm"):
                params = dict(ftype="OverdampedBrownian", reorg=20,
                              cortime=100, T=300)
                cf = CorrelationFunction(time, params)

            for m in self.molecules:
                m.set_transition_environment((0,1), cf)

        else:
            raise Exception("Unknown model name %s" % name)
            
        return agg