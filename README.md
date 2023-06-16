# pyAtmosLogger
> **Warning**
> This software is in development and currently not working.

Python serial data logger for Atmospheric Application. This software allows the serial data logging for multiple types of atmospherical serial instruments with a simple python-based syntax. Data can be automaticly converted to NetCDF-fileformat.

# Installation
Download release or clone repository:
```
git clone https://github.com/marcusgmueller/pyAtmosLogger.git
```

# Usage
1. change into `pyAtmosLogger` directory
2. Set preferences in `configuration.yaml`
## run datalogger
3. run logger
```
python3 pyAtmosLogger.py -m log -p configuration.yaml
```
## convert data to netCDF
3.. run command (or schedule it with cron)```
pyAtmosLogger -m convert -p configuration.yaml
```
