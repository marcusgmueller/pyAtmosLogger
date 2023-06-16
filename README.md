# pyAtmosLogger
> **Warning**
> This software is still in development.

Python data logger for Atmospheric Application. This software allows serial data logging for multiple types of atmospherical instruments with a simple python-based syntax. Data can be automaticly converted to NetCDF-fileformat.

# Installation
Download release or clone repository:
```
git clone https://github.com/marcusgmueller/pyAtmosLogger.git
```

# Usage
create custom `configuration.yaml` or edit existing file. You can also create multiple files for different instruments.
## run datalogger
```
python3 pyAtmosLogger.py -m log -p configuration.yaml
```
## convert data to netCDF
run command (or schedule it with cron)
```
python3 pyAtmosLogger.py -m convert -p configuration.yaml
```
