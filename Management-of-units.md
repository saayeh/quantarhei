(See also: [[Units conversion|Units conversion]] and [[Manager class|Manager class]])

Quantarhei provides a (to some extent) automatic handling of units of physical quantities like energy, time, frequency etc. As a default it uses units which are used internally for numerical calculations. These are the following: time is measured in femto-seconds, energy in radians per femto-second, Planck constant divided by two pi is equal to one, etc.. These units, however, might not be the ones in which you are used to think. Quantarhei therefore provides so-called context managers to enable you to work in units of your choice when you work with certain objects. 


### Context managers

We will use Hamiltonian as an example. [[Here|Two level Molecule]] we showed how to create a Hamiltonian of a two level molecule. This was done without any context manager so the default units were used. Let us create a Hamiltonian with the units of inverse centimeters. This energy unit is common in spectroscopy.

    from quantarhei import Molecule
    from quantarhei import energy_units

    en = [0.0, 12500] # 12500 1/cm corresponds to an absorption
                      # at the wavelength of 800 nm (near infra red light)
    with energy_units("1/cm"):
        m = Molecule("Molecule with units",en)

Now we get the Hamiltonian and print it to see what are the values of its matrix elements.

    H = m.get_Hamiltonian()
    print(H)

The output might be a bit surprising, because it is not in inverse centimeters

    quantarhei.Hamiltonian object
    =============================
    units of energy rad/fs
    data = 
    [[ 0.          0.        ]
     [ 0.          2.35456446]]

This is because we printed outside of a context manager's scope. To get the output in inverse cm, we need to do the following:

    with energy_units("1/cm"):
        print(H)

Now we get

    quantarhei.Hamiltonian object
    =============================
    units of energy 1/cm
    data = 
    [[     0.      0.]
     [     0.  12500.]]

Context managers of the units are meant to help you define physical quantities in units of your convenience. Internally,
all objects are stored in the default units, and they are only converted to other units only if explicitly required by the user. Even then, what you get is a copy of the internal data. Compare the following:

    with energy_units("eV"):
        print("Managed data: \n", H.data)
        print("\nRaw data:\n",H._data)

We get the following output

    Managed data: 
     [[ 0.          0.        ]
     [ 0.          1.54980247]]

    Raw data:
     [[ 0.          0.        ]
     [ 0.          2.35456446]]

While the former output is converted to eV, the latter is still in the internal units. 

### Using multiple context managers

Context managers handling units can be arbitrarily nested. Here for instance, we use inverse centimeters for energy and Debyes for dipole moment


    from quantarhei import dipole_units
    from quantarhei import energy_units

    with energy_units("1/cm"):
        with dipole_units("debye"):
            en = [0.0, 10000]
            dd = [1.0, 0.0, 0.0]
            m = Molecule("A", en)
            m.set_dipole(0,1,dd)

With more than two context managers one would already have an unconveniently deep indentation. Python allows to specify several context managers in one 'with' statement.

    with energy_units("1/cm"), dipole_units("debye"):
        something_to_do()


### Setting units globally

The units management so far discussed is provided for convenience. All calculations are done in the internal Quantarhei units, no matter how the "current" units are set. The context mamagers are meant to allow the user to briefly switch to different units to conveniently define quantities. To be sure that units are not mixed up in internal calculations, Quantarhei always works with these internal units when outside the context manager. Nevertheless, if you trust that all internal calculations are either protected by their own context manager enforcing internal units, or that they are done with private "_data" attributes which ARE ALWAYS in internal units, you might as well want to set some units for all your session and not bother with an additional indent. This is done by using the ``set_current_units()`` and a dictionary of unit settings

    from quantarhei import set_current_units

    uspec = dict(energy="1/cm", dipole="debye")
    set_current_units(uspec)

From now on in the code, energy will be always understood in the units of inverse centimeters. You can of course still use context managers to temporarily switch units anywhere in your script, and the setting does not influence the units in which calculations are done internally. By providing no arguments to the function, you can reset to default units

    set_current_units()

### Setting protected units (proposal)

When using context manager or a global setting for units, it is assumed that all quantities of the same dimension (e.g. energy) want to be expressed in the same units. However, you might want to have certain object always in certain units, or you want objects of the same dimension expressed on different units. Imagine that you want to plot a function of frequency (which is the same as energy in Quantarhei) and the function has a dimension of energy (consider e. g. the spectral density). You want to plot the two axes in different units, but they answer to the same type of context manager. 

This is a somewhat exceptional situation, and it can be solved by setting (temporarily) a protected set of units to a selected object. Protected units will not be overriden by any context manager nor by global setting. 

Any object which is managed by a context manager can be assigned private units

    from quantarhei import FrequencyAxis, SpectralDensity, energy_units

    with energy_units("1/cm"):
        wa = FrequencyAxis(-500.0, 1000, 1.0)
        params = dict(ftype="OverdampedBrownian",reorg=20, cortime=100, T=300)
        sd = SpectralDensity(wa,params)

    sd.set_protected_units("1/cm")

The protected units apply to the values of the sd object, not to the TimeAxis. Now SpectralDensity sd is immune to context managers

    with frequency_units("nm"):
        sd.plot()

Protected units have to be "released" if the object is to be put back under normal units management.

    sd.release_protected_units()

This technique is used in the ``plot`` method, where you can set units used on both x and y axis (SET LINK TO PLOTTING)
        


    