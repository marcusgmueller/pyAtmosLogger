pyAtmosLogger Dummy 1
=====================

Minimal configuration
---------------------
instrument.yaml

.. code-block:: yaml

    instrument:
        instrumentFile: pyAtmosLogger_dummy_1.py
        samplingInterval: 60
    attributes:
    storage:
        csvStoragePath: "~/Desktop/dummy_data/csv/"
        DatePath: "%Y/%m/"
        csvFileName: "%Y%m%d_tower_random.csv"
        ncStoragePath: "~/Desktop/dummy_data/nc/"
        ncConversionDays: 1

API
---

.. automodule:: pyAtmosLogger.instruments.pyAtmosLogger_dummy_1
    :members: