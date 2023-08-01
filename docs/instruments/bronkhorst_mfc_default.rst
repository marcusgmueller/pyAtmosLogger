Bronkhorst MFC Default
======================

Minimal configuration
---------------------
configuration.yaml

.. code-block:: yaml
  
   instrument:
      instrumentFile: "bronkhorst_mfc_default.py"
      samplingInterval: 60
      port: "/dev/ttyUSB0"
      setFlow: 13
   attributes:
      Title: "Bronkhorst MFC Default Test"
   storage:
      csvStoragePath: "~/mfc_data/nc/"
      DatePath: "%Y/%m/"
      csvFileName: "%Y%m%d_tower_mfc.csv"
      ncStoragePath: "~/mfc_data/nc/"
      ncConversionDays: 1


API
---

.. automodule:: pyAtmosLogger.instruments.bronkhorst_mfc_default
    :members: