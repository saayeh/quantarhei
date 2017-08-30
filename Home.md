# Welcome to the Quantarhei wiki!

### What is Quantarhei
Quantarhei is a Molecular Open Quantum Systems Simulator written predominantly in Python. Its name is derived from the famous aphorism "[Panta rhei](https://en.wikipedia.org/wiki/Heraclitus#Panta_rhei.2C_.22everything_flows.22)" of the Greek philosopher [Heraclitus of Ephesus](https://en.wikipedia.org/wiki/Heraclitus). "Panta rhei" means "Everything flows" or "Everything is in flux" which is quite fitting when you change Panta into Quanta. 

In "Quantarhei" the last four letter ("rhei") should be written in Greek, i.e. (using LateX convention) "\rho \epsilon \iota". Unfortunately, I don't know how to render it here. 

### What Quanterhei provides
Quantarhei is in flux, but it already provides helper classes to define molecules, their aggregates and their interaction with external environment. It can calculate absorption spectra of individual molecules and their aggregates and excitation energy transfer dynamics using various types of Redfield and Foerster theories.

Quantarhei provides Python code (optimized with Numpy) for all its implemented methods and theories, and allows extensions and replacements of the reference Python code with optimised routines written in C, Fortran or other lower level languages. 

In the first developmental stage, we concentrate on bringing to you tools to quickly build essential components of a quantum mechanical simulation, such as Hamiltonian and other operators, relaxation tensors, various initial conditions for density matrix etc. 

Read more about Quantarhei philosophy here (more about "panta rhei" philosophy [here](https://en.wikipedia.org/wiki/Heraclitus#Panta_rhei.2C_.22everything_flows.22)):
* [[Quantarhei Philosophy|Quantarhei Philosophy]] 

Dive into Quantarhei here:
* [[Simple Code Examples|Simple Code Examples]]

### Status of Quanterhei
Currently, Quantarhei is at its experimental stage. Current version is 0.0.9 (as of November 25, 2016)

### How to Download
Quantarhei is available in source form on [GitHub](https://github.com/tmancal74/quantarhei). Its distributions are available from [PyPI](https://pypi.python.org/pypi) for install with the `pip` command. Just type on the command line

    $ pip install quantarhei
