Welcome to pyAtmosLogger's documentation!
=========================================

Python data logger for Atmospheric Application. This software allows data logging for multiple types of atmospherical instruments with a simple python-based syntax. Data can be automaticly converted to NetCDF-fileformat. The instrument-directory contains two files for each instrument. The file ```<instrument_name>.py``` contains all instrumentspecific scripts and should not be changed by the user. The file  ```<instrument_name>.yaml``` is a configuration file. Here the user can customize the installation to his needs. Therefor he can copy the file to his prefered location and edit it.

Check out the cli section for further information, including
how to installation the project.

.. note::

   This project is under active development.

Contents
--------

.. toctree::

   installation
   usage
   api
   instruments
   changelog
