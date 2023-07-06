Ott Parsivel2 Default
=====================

Minimal configuration
---------------------
instrument.yaml

.. code-block:: yaml
  
  instrument:
    instrumentFile: ott_parsivel2_default.py
    samplingInterval: 60
    port: "/dev/ttyUSB0"
    baudrate: 19200
    bytesize: 8
    parity: "N"
    stopbits: 1
  attributes:
  storage:
    csvStoragePath: "/home/marcus/data/parsivel2/csv/"
    DatePath: "%Y/%m/"
    csvFileName: "%Y%m%d_tower_random.csv"
    ncStoragePath: "/home/marcus/data/parsivel2/netCDF/"
    ncConversionDays: 2

Recommended configuration
-------------------------
instrument.yaml

.. code-block:: yaml
  
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

API
---

.. automodule:: pyAtmosLogger.instruments.ott_parsivel2_default
    :members: