Quantarhei can calculate absorption spectra based on the information specified in the ``Molecule`` or ``Aggregate`` objects. The simplest molecule can be specified like this:

    from quantarhei import Molecule

    m = Molecule("my molecule", [0.0, 1.0])

This molecule has no absorption, because no transition dipole was specified. Nevertheless we can create an absorption spectrum object which contains it

    from quantarhei import AbsSpect, TimeAxis
    ta = TimeAxis(0.0, 2000, 5.0)
    a1 = AbsSpect(ta, m)

The spectrum is calculated by ``calculate()`` method of the ``AbsSpect`` class. At this moment it would however raise an exception. We need to specify at least the transition dipole moment for one transition, in which case natural Lorenzian linewidth is calculated.

    m.set_dipole(0,1,[0.0, 1.0, 0.0])
    a1.calculate(rwa = 1.0)
   
    a1.plot()

The parameter ``rwa`` species the frequency which is subtracted from the transition frequencies of the molecule to make Fourier transform easier. It is advisable to submit something similar to the average frequency of the transitions.

### Absorption of a molecule embedded in an environment

The spectrum calculated above corresponds to gas phase situation (with the idealisation that molecules do not move and collide). More often one needs to take into account some environment surrounding and interacting with the molecule. Such environment causes the electronic transition energy of the molecule to fluctuate. We can specify the so-called energy gap correlation function for the transition and use it to calculate absorption spectrum. Correlation function is specified by a dictionary of parameters, and created like this (see also [[Bath correlation functions and spectral densities|Bath correlation functions and spectral densities]] section)

    from quantarhei import CorrelationFunction, energy_units

    # Parameters specified in inverse centimeters and fs, temperature in K
    cfce_params = dict(ftype="OverdampedBrownian",
                       reorg=20.0,
                       cortime=100.0,
                       T=100,matsubara=20)
    # Using context manager to switch to inverse centimeters which are not
    # default units
    with energy_units("1/cm"):
        cfce1 = CorrelationFunction(ta,cfce_params)

Now we can set the energy gap correlation function for the molecule, and calculate the spectrum anew

    m.set_egcf((0,1),cfce1)
    a1.calculate(rwa=1.0)

    a1.plot()

This new calculation results in a much broader absorption line.

### Absorption of an aggregate

Interaction between molecules can change absorption spectra significantly.

### Absorption calculated from excitation dynamics

So far we have ignored in our calculations one important aspect of the excitation by light, namely that it might induce some excited state dynamics. 

