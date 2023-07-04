CLI
=====

General Usage
----------------

Create a `<configuration_file>.yaml` file using the samples at :ref:`Supported Instruments` .

run datalogger
~~~~~~~~~~~~

.. code-block:: console

   pyAtmosLogger -m log -p <configuration_file>.yaml

convert data to netCDF
~~~~~~~~~~~~

run command (or schedule it with cron)

.. code-block:: console

   pyAtmosLogger -m log -p <configuration_file>.yaml