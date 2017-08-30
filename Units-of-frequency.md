(See also: [[Units conversion|Units conversion]] and [[Manager class|Manager class]])

### Default units

``rad/fs``

### Relation to other quantities

In Quantarhei, frequency essentially is energy. We use frequency for quantities related to optics, e.g. for frequency of light. Frequency dependent quantities such as spectra are alternatively often represented by the light wavelength. In Quantarhei, frequencies and energies can be directly converted to wavelength.

From programming point of view, ``frequency_units`` context manager behaves exactly like ``energy_units`` context manager. They are one and the same thing and no difference between frequency and energy is made internally.

### Usage

Units of energy/frequency can be controlled by the ``frequency_units`` context manager. The usage is like this

    from quantarhei import frequency_units

    with frequency_units("1/cm"):
        do_something_with_frequency_quantities()

### Supported units

The same units as for energy are supported. Consult a table in the [[Units of energy|Units of energy]] section.

### Special conversions

The frequencies can be converted to nano meters *nm*. This can be useful e.g. for plotting absorption spectra.

    import quantarhei as qr
    
    ta = qr.TimeAxis(0.0, 1000, 0.5)

    with qr.energy_units("1/cm"):
        m = qr.Molecule("Molecule",[0.0,10000.0])

    m.set_dipole(0,1,[0.0, 1.0, 0.0])
    abs = qr.AbsSpect(ta,m)

    with qr.frequency_units("nm"):
       abs.plot()

This will result in an absorption spectrum plot against the wavelength axis.
    