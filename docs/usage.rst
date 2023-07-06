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

   pyAtmosLogger -m log -p <configuration.yaml>


