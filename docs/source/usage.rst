Usage
=====

.. _installation:

Installation
------------

To use pyAtmosLogger, first install it using pip:

.. code-block:: console

   pip install "pyAtmosLogger @ git+https://github.com/marcusgmueller/pyAtmosLogger"

General Usage
----------------

Copy the file ```<instrument_name>.yaml``` from instrument directory to a custom location. Customize this file to you needs.

run datalogger
~~~~~~~~~~~~

.. code-block:: console

   pyAtmosLogger -m log -p <path_to_instrument_name>.yaml

convert data to netCDF
~~~~~~~~~~~~

run command (or schedule it with cron)

.. code-block:: console

   pyAtmosLogger -m log -p <path_to_instrument_name>.yaml

Instruments
------------

.. _ott_parsivel2_default:
Ott Parsivel 2
~~~~~~~~~~~~
instrument.yaml

.. code-block:: console
  
  instrument:
    instrumentFile: ott_parsivel2_default.py
    samplingInterval: 60
    port: "/dev/ttyUSB0"
    baudrate: 19200
    bytesize: 8
    parity: "N"
    stopbits: 1
  attributes:
    Contact_person: 
    Institution: 
    License: 
    Manufacturer:
    Measurement_altitude_AGL:
    Measurement_altitude_AMSL:
    Measurement_latitude:
    Measurement_longitude: 
    Measurement_site: 
    Model: 
    serial_number: 
    Title:
    Type: 
  storage:
    csvStoragePath: "/home/marcus/data/parsivel2/csv/"
    DatePath: "%Y/%m/"
    csvFileName: "%Y%m%d_tower_random.csv"
    ncStoragePath: "/home/marcus/data/parsivel2/netCDF/"
    ncConversionDays: 2

