# pyAtmosLogger
> **Warning**
> This software is in development and currently not working.

Python serial data logger for Atmospheric Application. This software allows the serial data logging for multiple types of atmospherical serial instruments with a simple python-based syntax. Data can be automaticly converted to NetCDF-fileformat.

# Installation
1. Using Python-pip
2. Using github-Release

# Usage
## run datalogger
1. Set preferences in `configuration.yaml`
2. run command
```
pyAtmosLogger -m log -p configuration.yaml
```
## convert data to csv
1. Set preferences in `configuration.yaml`
2. run command (or shedule it with cron)
```
pyAtmosLogger -m convert -p configuration.yaml
```
