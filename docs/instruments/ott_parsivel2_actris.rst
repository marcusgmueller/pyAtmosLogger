Ott Parsivel2 ACTRIS
=====================

Minimal configuration
---------------------
instrument.yaml

.. code-block:: yaml
  
  instrument:
    instrumentFile: ott_parsivel2_actris.py
    samplingInterval: 60
    port: "/dev/ttyUSB0"
    baudrate: 19200
    bytesize: 8
    parity: "N"
    stopbits: 1
  attributes:
  storage:
    csvStoragePath: "~/data/parsivel2/csv/"
    DatePath: "%Y/%m/"
    csvFileName: "%Y%m%d_tower_random.csv"
    ncStoragePath: "~/data/parsivel2/netCDF/"
    ncConversionDays: 2

Recommended configuration
-------------------------
instrument.yaml

.. code-block:: yaml
  
  instrument:
    instrumentFile: ott_parsivel2_actris.py
    samplingInterval: 60
    port: "/dev/ttyUSB0"
    baudrate: 19200
    bytesize: 8
    parity: "N"
    stopbits: 1
  attributes:
    Title: "muster-site Parsivel 1"
    Author: "Max Mustermann, max.mustermann@test.de"
    Author_institution: "muster-institut"
    License_data_recording: "For non-commercial use only"
    Contact_person: "Max Mustermann, max.mustermann@test.de"
    Contact_person_institution: "muster-institut, Cologne, Germany"
    Instrument_manufacturer: "OTT"
    Instrument_model: "Parsivel2"
    Instrument_type: "Distrometer"
    Measurement_site: "Muster-Site"
    Measurement_latitude:  "50 N"
    Measurement_longitude: "6 E"
    Measurement_altitude_AGL: "10"
    Measurement_altitude_AMSL: "110"
    Processing_author: "Max Mustermann, max.mustermann@test.de"
    Processing_author_institution: "muster-institut, Cologne, Germany"
    License_processing: "For non-commercial use only"  
  storage:
    csvStoragePath: "~/data/parsivel2/csv/"
    DatePath: "%Y/%m/"
    csvFileName: "%Y%m%d_tower_random.csv"
    ncStoragePath: "~/data/parsivel2/netCDF/"
    ncConversionDays: 2

API
---

.. automodule:: pyAtmosLogger.instruments.ott_parsivel2_actris
    :members: