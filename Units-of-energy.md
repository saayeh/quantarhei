(See also: [[Management of units|Management of Units]], [[Units conversion|Units conversion]] and [[Manager class|Manager class]])

### Default units

``rad/fs``

### Usage

Units of energy are controlled by the *energy_units* context manager. The usage is like this

    from quantarhei import energy_units

    with energy_units("1/cm"):
        do_something_with_energy_quantities()

### Supported units

The units in a table below are supported. Conversion factor is expressed using values from the *scipy.constants* package imported in the following way

    import scipy.constants as const


| Units  | Description| Conversion factor |
|:------:|:-----------|------------------:|
|  int   | internal units          | 1.0  |
| rad/fs | radians per femtosecond | 1.0  |
| 1/cm   | inverse centimeters     | const.pi*const.c*2.0e-13 |
| eV     | electron Volts          | 1.0e-15*const.e/const.hbar |
| meV    | mili electron Volts     | 1.0e-18*const.e/const.hbar |
| THz    | tera Herz               | const.pi*2.0e-03 |
| J      | Joules                  | 1.0e-15/const.hbar |
| SI     | Joules                  | 1.0e-15/const.hbar |

Internal units are rad/fs, but in future, the user will have a choice of different internal units. 

Usage of SI units 'J' or 'SI' is not recommended. They are here for the sake of completeness, but the numbers corresponding to atomic quantities expressed on SI units are extremely small and not suitable for numerics at all.