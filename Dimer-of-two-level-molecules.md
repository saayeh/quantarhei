### Creating a dimer of two-level molecules

The preferred way to import Quantarhei is to explicitly import individual components. 
This way you have a full control over what is imported

    from quantarhei import Molecule, Aggregate
    
Let us create two molecules with the same energies

    en = [0.0 1.0]
    m1 = Molecule("Mol1",en)
    m2 = Molecule("Mol2",en)

and an Aggregate object

    ag = Aggregate("Homodimer")

to which we add the molecules

    ag.add_Molecule(m1)
    ag.add_Molecule(m2)

Now we set resonance interaction between excited states of the molecules

    ag.set_resonance_coupling(0,1,0.1)

Aggregate object is now ready to be built. This has to be done before it is used

    ag.build()

Now we ask the Aggregate to give us Hamiltonian

    H = ag.get_Hamiltonian()

and we print it

    print(H)

This results in

    quantarhei.Hamiltonian object
    =============================
    data = 
    [[ 0.   0.   0. ]
     [ 0.   1.   0.1]
     [ 0.   0.1  1. ]]

By default, Quantarhei Aggregate object builds a Hamiltonian of an aggregate of molecules using maximum one excited state per molecule. This is a so-called Frenkel exciton Hamiltonian in single exciton approximation.
