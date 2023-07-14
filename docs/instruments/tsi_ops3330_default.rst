TSI OPS 3330 default
====================

Minimal configuration
---------------------
instrument.yaml

.. code-block:: yaml
  
instrument:
   instrumentFile: tsi_ops3330_default.py
   samplingInterval: 120
   samplingDuration: 60
   ip: 192.168.1.111
   port: 3602
   channelSetup: 16,0.300,0.374,0.465,0.579,0.721,0.897,1.117,1.391,1.732,2.156,2.685,3.343,4.162,5.182,6.451,8.032,10.000
attributes:
   title: TSI OPS 3330 pyAtmosLogger Test
storage:
   csvStoragePath: "~/ops_data/csv/"
   DatePath: "%Y/%m/"
   csvFileName: "%Y%m%d_tower_random.csv"
   ncStoragePath: "~/ops_data/nc/"
   ncConversionDays: 1


API
---

.. automodule:: pyAtmosLogger.instruments.tsi_ops3330_default
    :members: