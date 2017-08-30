We refer to the second order (in system-bath interaction) relaxation tensor with Markov approximation as Redfield relaxation tensor. The derivation in both its time-dependent and constant coefficient forms is given e.g. in May and Kühn (2000).

### Creating the tensor

The tensor is represented by the ``RedfieldRelaxationTensor`` class. The tensor elements are calculated in the constructor and stored in the ``data`` attribute of the class

    from quantarhei import RedfieldRelaxationTensor
    
    HH.protect_basis()
    with eigenbasis_of(HH):
        rt = RedfieldRelaxationTensor(ham=HH, sbi=SBI)
        rate = rt.data[1,1,2,2]
    HH.unprotect_basis()

where HH is of the type ``Hamiltonian`` and SBI is of type ``SystemBathInteraction``. For consistency, the Redfield tensor should be calculated within the basis management context so that the current basis corresponds to the eigenbasis of the electronic Hamiltonian. This is how Redfield tensor is properly formulated. However, we need to know how to transform the Hamiltonian into its diagonal basis so we prevent the Hamiltonian from diagonalising automatically by setting its basis outside the context manager as protected. We remove the protection once we are outside the ``eigenbasis_of`` context.

### Why the change of basis

The code for Redfield tensor calculated it in representation of the states which are eigenstates of the Hamiltonian. If we did not apply the context manager, the tensor ``data`` attribute would be understood as being
in the default basis (which basically is the local basis).

### Using ``Aggregate`` class to create Redfield tensor

The intricacies of the creation of the Redfield tensor can be removed from the user by using the ``Aggregate`` class. Let us assume we have created and initialised a list ``mols`` of molecules. We create an aggregate object and build it

    agg = Aggregate(molecules=mols)
    agg.build()

If the molecules had their interaction with environment specified, we can get the relaxation tensor of any type in the following way

    R = agg.get_RelaxationTensor(time, relaxation_theory="standard_Redfield")


