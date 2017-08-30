### Redfield Dynamics - example 1:

First import Quantarhei and related classes:

    from quantarhei import Molecule, Aggregate, energy_units, eigenbasis_of, TimeAxis, CorrelationFunction
    from quantarhei.qm import ReducedDensityMatrix
    
Here we study the population dynamics, governed by Redfield theory, in an aggregate
of molecules. We assume that the molecules are two-level systems whose ground states
take the same energy 0.0. For simplicity, consider only two types of molecules
with energies set as follows:

    en1 = [0.0, 22500]
    en2 = [0.0, 22000]

We place 8 molecules on a two-dimensional plane with coordinates:

    locations = [[-6.5, -5, 0.0],
                       [-6.5, 5, 0.0],
                       [6.5, -5, 0.0],
                       [6.5, 5, 0.0],
                       [-20, -5, 0.0], 
                       [-20, 5, 0.0], 
                       [20, -5.7, 0.0], 
                       [20, 5.7, 0.0]]

We may also want to assign transition dipole moments to the molecules. The default unit for dipole moments is Debye. A list of moments will look like:

    dipoles = [[-5.5, 3.2, 0.0],
                     [5.5, 3.2, 0.0],
                     [-5.5, -3.2, 0.0],
                     [5.5, -3.2, 0.0],
                     [5.5, 3.2, 0.0],
                     [5.5, 3.2, 0.0],
                     [1.6 ,  6.3,  0.0],
                     [1.6 ,  6.3,  0.0]]

We can now define the monomers using the class Molecule. To have a simpler and more compact look, let's make a list of monomers: mnr. Also, we may want to divide the molecules into two sets, the first 6 molecules with energy en1 and the last 2 with en2. With the same order, they take dipole moments and locations from the lists above. Hence, we make M1, M2, ... and M8 as follows:

    mnr = [] 

    with energy_units("1/cm"):
        for i in range(6): 
            mnr.append(Molecule("M" + str(i), en1))
            mnr[i].set_dipole(0,1,dipoles[i])

        for i in range(6, 8): 
            mnr.append(Molecule("M" + str(i), en2))
            mnr[i].set_dipole(0,1,dipoles[i])
          
Next, we assign the positions of molecules to mnr:

    for i in range(8):
        mnr[i].position = locations[i]
    

Other needed parameter in the calculations of dynamics is temperature with default unit Kelvin:

    temperature = 300.0 

Time axis on which everything is calculated takes three numbers: (start, number of steps, time step) and the default unit is fs. We define it using TimeAxis imported from Quantarhei:

    time = TimeAxis(0.0,10000,1.)

So far we have been concentrating on the System of monomers. Now we need to introduce the parameters of the Bath (environment). This is done through introducing correlation functions which take different parameters. For instance:

    cfce_params = dict(ftype="OverdampedBrownian",
                                    reorg= 40,
                                    cortime=60.0,
                                    T=temperature,
                                    matsubara=20) 

Correlation functions are then 

    with energy_units("1/cm"):
        cfce = CorrelationFunction(time,cfce_params)

and are connected to the monomers by

    with energy_units("1/cm"):
        for j in range(8):
            mnr[j].set_transition_environment((0,1),cfce)
                   
Finally, an Aggregate object will be

    AG = Aggregate("EightSiteAgg")

to which we add the molecules

    for i in range(8):
        AG.add_Molecule(mnr[i])
    
Now we set dipole-dipole interaction between excited states of the molecules which can also take relative permittivity of the surrounding environment as a parameter:

    AG.set_coupling_by_dipole_dipole(epsr = 2.0)

Aggregate object is now ready to be built. This has to be done before it is used

    AG.build()

Now we ask the Aggregate to give us the Hamiltonian

    H = AG.get_Hamiltonian()

and we can also print it in desired energy units:

    with energy_units("1/cm"):
        print(H.data)

To start simulating the dynamics, let's first define and set the initial reduced density matrix. Quantarhei does it through a class we already imported:

    rho_i = ReducedDensityMatrix(dim=H.dim) 
    
    with energy_units("1/cm"):
        rho_i.data[1,1] = 0.3
        rho_i.data[3,3] = 0.7
            
In this way, we specifically set the initial density matrix in the site basis. Instead, we can initialize the system in the excitonic basis using the context eigenbasis_of(H):

    with energy_units("1/cm"):
        with eigenbasis_of(H):
            rho_i.data[1,1] = 0.3
            rho_i.data[3,3] = 0.7
            
rho_i needs to be normalized for which we use:

    rho_i.normalize2()
    
Once the initial density matrix is prepared, we call the propagator with desired relaxation theory. For instance, let's use standard Refield theory implemented in Quantarhei.
 
    prop_r = AG.get_ReducedDensityMatrixPropagator(time,
                                             relaxation_theory="standard_Redfield", 
                                             secular_relaxation = True)
                                             
    pr_r = prop_r.propagate(rho_i, method="short-exp")

We may now want to save the data of this density matrix:

    pr_r.save_data(FilePath)

or plot it:

    pr_r.plot()
    
This command also accepts arguments like ''coherences = False'' in case we are only interested in the populations. Like before, we can also plot the populations in the excitonic basis for which we use:

    with eigenbasis_of(H):
        pr_r.plot()

This was what standard Redfield theory would produce. In case of strong system-bath interaction, one may apply Foerster theory. For instance, consider 

    cfce_params = dict(ftype="OverdampedBrownian",
                                    reorg= 300,
                                    cortime=60.0,
                                    T=temperature,
                                    matsubara=20) 

We follow the steps that were explained before and set the relaxation theory as

    prop_f = AG.get_ReducedDensityMatrixPropagator(time,
                                             relaxation_theory="standard_Foerster", 
                                             secular_relaxation = True)
                                             
    pr_f = prop_r.propagate(rho_i, method="short-exp")

This then describes the dynamics of the system as Foerster theory would do.


