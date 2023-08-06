Dtool Lookup Server Plugin Scaffolding
======================================

- GitHub: https://github.com/IMTEK-Simulation/dtool-lookup-server-plugin-scaffolding
- PyPI: https://pypi.python.org/pypi/dtool-lookup-server-plugin-scaffolding
- Free software: MIT License


Features
--------

- Template for dtool-lookup-server plugin developments.


Introduction
------------

`dtool <https://dtool.readthedocs.io>`_ is a command line tool for packaging
data and metadata into a dataset. A dtool dataset manages data and metadata
without the need for a central database.

However, if one has to manage more than a hundred datasets it can be helpful
to have the datasets' metadata stored in a central server to enable one to
quickly find datasets of interest.

The `dtool-lookup-server <https://github.com/jic-dtool/dtool-lookup-server>`_ 
provides a web API for registering datasets' metadata
and provides functionality to lookup, list and search for datasets.

This scaffolding serves as a template for `dtool-lookup-server` plugin 
developments.

Installation
------------

Install the dtool lookup server dependency graph plugin::

    $ pip install dtool-lookup-server-plugin-scaffolding