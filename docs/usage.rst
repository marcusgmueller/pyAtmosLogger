Usage
=====

Configuration-File
------------------
Create a ``<configuration.yaml>`` file. You can use one of the samples provided for each instrument at :ref:`the instrument page <instruments>` and customize it to you needs.

CLI
---

.. code-block:: console
   :caption: run datalogger

   pyAtmosLogger -m log -p <configuration.yaml>

.. code-block:: console
   :caption: convert data to netCDF (run command or schedule it with cron)

   pyAtmosLogger -m convert -p <configuration.yaml>


Python
------

.. nbinput:: ipython3
    :execution-count: 1

    import pyAtmosLogger
    import yaml

.. nbinput:: ipython3
    :execution-count: 2

    yamlString = """
    instrument:
       instrumentFile: pyAtmosLogger_dummy_1.py
       samplingInterval: 60
    attributes:
       title: "Test"
    storage:
       csvStoragePath: "~/Desktop/dummy_data/csv/"
       DatePath: "%Y/%m/"
       csvFileName: "%Y%m%d_tower_random.csv"
       ncStoragePath: "~/Desktop/dummy_data/nc/"
       ncConversionDays: 1
    """
    config = yaml.safe_load(yamlString)

.. nbinput:: ipython3
    :execution-count: 3

    instrument = pyAtmosLogger.pyAtmosLogger_dummy_1.pyAtmosLogger_dummy_1(config)

.. nboutput::
    :execution-count: 3

    2023-07-06 15:33:17: setup completed

.. nbinput:: ipython3
    :execution-count: 4

    instrument.log()

.. nboutput::
    :execution-count: 4

    2023-07-06 15:35:11: logging started

    2023-07-06 15:35:11: header created

.. nbinput:: ipython3
    :execution-count: 5

    instrument.convertMultipleFiles()

.. nboutput::
    :execution-count: 5

    2023-07-06 13:31:25: converter started

    2023-07-06 13:31:25: converting file: ~/Desktop/dummy_data/csv/2023/07/20230706_tower_random.csv
    
    2023-07-06 13:31:25: converter finished
