# Tabata

*Tabata* is a python module that helps you putting together and mixing your
preferenced music for your own [Tabata Training](http://en.wikipedia.org/wiki/High-intensity_interval_training#Tabata_regimen).

## Installation

It is recommended to install `tabata` package in a virtual python environment,
see [Virtualenv](https://virtualenv.pypa.io).

1. Install `virtualenv` with your favourite package manager on your system
(e.g. `apt install virtualenv`).

1. Download the source of the `tabata` package:

		$ git clone https://github.com/machste/tabata.git

1. Create the virtual environment in a folder (e.g. `venv`) right in the root
folder of the downloaded `tabata` source package. You can of course use a
different location.

		$ cd tabata
		$ virtualenv venv

1. Activate the virtual environment:

		$ . venv/bin/activate

1. Install the `tabata` package to your virtual environment:

		$ python setup.py install
