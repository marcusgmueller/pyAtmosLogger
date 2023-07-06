Usage
=====

CLI
---

Create a ``<configuration_file>.yaml`` file using the samples in section ``Supported Instruments``.

run datalogger

.. code-block:: console

   pyAtmosLogger -m log -p <configuration_file>.yaml

convert data to netCDF

run command (or schedule it with cron)

.. code-block:: console

   pyAtmosLogger -m log -p <configuration_file>.yaml

Python
------
.. code-block:: Python
   import yaml
   import pyAtmosLogger.instruments.pyAtmosLogger_dummy_1 as test

.. code-block:: Python
   configString = """
   instrument:
   instrumentFile: pyAtmosLogger_dummy_1.py
   samplingInterval: 60
   attributes:
   storage:
   csvStoragePath: "/mnt/c/Users/marc.mueller/Desktop/dummy_data/csv/"
   DatePath: "%Y/%m/"
   csvFileName: "%Y%m%d_tower_random.csv"
   ncStoragePath: "/mnt/c/Users/marc.mueller/Desktop/dummy_data/nc/"
   ncConversionDays: 1
   """
   config = yaml.safe_load(configString)
   instrument = test.pyAtmosLogger_dummy_1(config)

.. code-block:: Python
   instrument.log()



