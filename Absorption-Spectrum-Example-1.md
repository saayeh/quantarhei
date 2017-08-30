### Absorption Spectrum - example 1:

    import matplotlib.pylab as plt
    from quantarhei import AbsSpect, Molecule, Aggregate, energy_units, TimeAxis, CorrelationFunction
    from quantarhei.qm import ReducedDensityMatrix


    en1 = [0.0, 22500]
    en2 = [0.0, 22000]
    en3 = [0.0, 21300]

    lcn = [[-6.5, -5, 0.0],
                       [-6.5, 0., 0.0],
                       [6.5, -5, 0.0],
                       [-20, -5, 0.0], 
                       [20, -2.4, 0.0], 
                       [10, 2.7, 0.0]]


    dpl = [[-7, 3.2, 0.0],
                     [5.5, 3.2, 0.0],
                     [5.5, -3.2, 0.0],
                     [-5.5, -3.2, 0.0],
                     [1.6 ,  6.3,  0.0],
                     [1.6 ,  6.3,  0.0]]
                     
                     
    plt.figure("sheet-opt0")
    plt.plot([lcn[i][0] for i in range(len(lcn))], [lcn[i][1] for i in range(len(lcn))], 'or')
    plt.grid()


    mnr = [] 
    with energy_units("1/cm"):
        for i in range(2): 
            mnr.append(Molecule("M" + str(i), en1))
            mnr[i].set_dipole(0,1,dpl[i])
        for i in range(2,4): 
            mnr.append(Molecule("M" + str(i), en2))
            mnr[i].set_dipole(0,1,dpl[i])
        for i in range(4,6): 
            mnr.append(Molecule("M" + str(i), en3))
            mnr[i].set_dipole(0,1,dpl[i])
        
        

    for i in range(6):
        mnr[i].position = lcn[i]
    

    temperature = 300.0 # in Kelvins

    time = TimeAxis(0.0,10000,1.) # (start, number of steps, time step) in fs


    cfce_params = dict(ftype="OverdampedBrownian",
                   reorg= 140,
                   cortime=60.0,
                   T=temperature,
                   matsubara=20)


    with energy_units("1/cm"):
        cfce = CorrelationFunction(time,cfce_params)


    with energy_units("1/cm"):
        for j in range(6):
            mnr[j].set_transition_environment((0,1),cfce)


    AG = Aggregate("TestAggregate")

    for i in range(6):
        AG.add_Molecule(mnr[i])

    AG.set_coupling_by_dipole_dipole(epsr = 1.0)

    AG.build()

    HH = AG.get_Hamiltonian()

    (RRr,hamr) = AG.get_RelaxationTensor(time,
                                   relaxation_theory="standard_Redfield",
                                   time_dependent=False)

   
    a_r = AbsSpect(time, AG, relaxation_tensor=RRr, effective_hamiltonian=hamr)


    plt.figure('abs')

    with energy_units("1/cm"):
        a_r.calculate(rwa=25000)
        a_r.plot(axis=[19000,26000,0,numpy.max(a_r.data)*2.1], how = '-g')
