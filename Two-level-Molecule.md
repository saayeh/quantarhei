### Creating a Hamiltonian of a two level molecule:
Here is one of the ways to import Quantarhei package

    import quantarhei as qr

We create a molecule with two states and energies 0.0 and 1.0 (we will discuss units of energy used in Quanterhei elsewhere)

    en = [0.0 1.0]
    M = qr.Molecule("My first two-level molecule",en)

Below we ask the object M to return an object which represents the Hamiltonian operator of the molecule.

    H = M.get_Hamiltonian()
   
All objects are printable

    print(H)

The `print` command will produce:

    quantarhei.Hamiltonian object
    =============================
    data = 
    [[ 0.  0.]
     [ 0.  1.]]    
