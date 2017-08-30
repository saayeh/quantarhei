Bath (or energy gap) correlation functions and spectral densities are some of the most important quantities in the theory of open quantum systems and the theory of their spectroscopy. Quantarhei provides the most common forms of these functions to be used as essential inputs for calculations of open molecular quantum system dynamics. 

## Bath correlation function

To define a bath correlation function in Quantarhei is easy. First the CorrelationFunction class is imported

    from quantarhei import CorrelationFunction

Because there are many different possible functional forms of correlation functions with possibly very different parameters, the constructor of the CorrelationFunction class accepts a dictionary of parameters. For every type of correlation function, you have to consult documentation to figure out the required parameters. Let us create parameter set for an overdamped Brownian correlation function. It reads as

    params = {"ftype":"OverdampedBrownian", "reorg":20, "cortime":100, "T":100}

Correlation function is a time dependent quantity. Time has special place in Quantarhei. Most often, one has to define a TimeAxis object, which specifies the time interval on which fuctions and calculations are define. If not specified otherwise, time is given in femto-seconds

    ta = TimeAxis(0.0,1000,0.1)

We specified the start of the time interval (0.0), number of steps (1000) and the time step (0.1), all in femto-seconds. 

The correlation function parameter "reorg", the so-called reorgnization energy, is meant to be 20 1/cm. We have to make sure it is understood that way. We do this with a context manager which specifies the units we use for energy (see [[Management of units|Management of units]] section). Inside the scope if the context manager, we create the correlation function object

    with energy_units("1/cm"):
        cf = CorrelationFunction(ta,params)

The following comes when we plot the newly created correlation function

    cf.plot(ylabel=r'$C(t)$')

[[https://github.com/tmancal74/quantarhei/blob/master/docs/wiki/figs/corfce_t_00001.png]]

Fourier transform of the Correlation function is sometimes called spectral density (see e.g. [1]), but there is a different, more common definition of spectral density, which we use in the SpectralDensity class, and which we discuss below. For now, we can have a look at the Fourier transform

    FT = cf.get_Fourier_transform()
    FT.plot(yabel=r'$\tilda{C}(\omega)$')

[[https://github.com/tmancal74/quantarhei/blob/master/docs/wiki/figs/corfce_om_00001.png]]

## Spectral density

Bath correlation function and its Fourier transform are temperature dependent quantities. To specify system-bath interaction on a similar level as a Hamiltonian operator does, one would like to find a temperature independent quantity which would do the job. 

In Quantarhei, spectral density is obtained from the same set of parameters as the correlation function. In fact, despite that it is a frequency dependent quantity, you can use both TimeAxis and FrequencyAxis objects to create it. Let us assume we use the same 'params' dictionary as above.

    from quantarhei import SpectralDensity
    import numpy

    ta = TimeAxis(0.0, 1000, 0.1)
    fa = ta.get_FrequencyAxis()

    sp_1 = SpectralDensity(ta, params)
    sp_2 = SpectralDensity(fa, params)

    print(numpy.allclose(sp_1.data,sp_2.data)

This code will produce 

    True

because the TimeAxis will be internally converted to a FrequencyAxis.

## More complicated spectral densities

To define more complicated spectral densities and correlation functions, both classes (`CorrelationFunction` and `SpectralDensity`) support addition operation. When two instances of the `CorrelationFunction` class are created, they can be added together as in the following example. 

    cf1 = CorrelationFunction(time, params1)
    cf2 = CorrelationFunction(time, params2)
    cf = cf1 + cf2

Here, a new instance `cf` of the class `CorrelationFunction` is created and it stores data created by addition of the data from `cf1` and `cf2`. We can also perform addition "into" one of the objects, e.g.

    cf2 += cf1

in which case the data of `cf1` are added to the data of `cf2` (`cf2` is changed) and no new object is created. A third way to add correlation functions is to use the `add_to_data` method. This method, when supplied with CorrelationFunction object, is equivalent to inplace addition (`+=`), i.e.

    cf2.add_to_data(cf1) 

is equivalent to `cf2 += cf1`. When we supply a dictionary of parameters, corresponding data are added to the instance of `CorrelationFunction` without explicitly creating a new instance. We can do something like this:

    cf2.add_to_data(params1) 

with the same effect as the two statements above.

Currently, all instances of `CorrelationFunction` and `SpectralDensity` which take part in addition require the SAME object of the type TimeAxis. 

## How non data attributes are handled

Instances of `CorrelationFunction` and `SpectralDensity` hold many more attributes than just the data. When adding the instances these attributes are combined in the following way:

...
 
### References

[1] S. Mukamel, Principles of nonlinear spectroscopy, Oxford University Press, Oxford, 1995


