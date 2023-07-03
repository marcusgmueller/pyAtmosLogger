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

