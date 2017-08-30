(See also [[Management of Units|Management of Units]])

To convert values of physical quantities between different units, Quantarhei provides a simple conversion function. It can be used like this

    from quantarhei.units import convert

    A_eV = 1.0
    A_cm1 = convert(A_eV,from="eV",to="1/cm")

The function is aware of the default Quantarhei units and of units set by the current context manager (see [[Management of Units|Management of Units]]). One of the parameters of the function can be correspondingly be left out. The following converts from default units

    B_THz = convert(1.0,to="THz")

and the following converts to the default units

    B_int = convert(B_THz,from="THz")

Below we convert from inverse centi meters to electron Volts

    with energy_units("1/cm"):
        C_eV = convert(1000, to="eV")

The ``convert`` function searches all types of units used in Quantarhei (energy, dipole, distance, ...) so that the type does not need to be specified.

