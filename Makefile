all: reinst

VERSION = 0.0.12

uninst: 
	pip uninstall -y quantarhei 

sdist:
	python setup.py sdist

install: sdist 
	pip install dist/quantarhei-${VERSION}.tar.gz

reinst: uninst install
	@echo "Reinstallation completed."
