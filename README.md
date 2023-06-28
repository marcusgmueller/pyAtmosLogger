# pyAtmosLogger
> **Warning**
> This software is still in development.

Python data logger for Atmospheric Application. This software allows data logging for multiple types of atmospherical instruments with a simple python-based syntax. Data can be automaticly converted to NetCDF-fileformat. The instrument-directory contains two files for each instrument. The file ```<instrument_name>.py``` contains all instrumentspecific scripts and should not be changed by the user. The file  ```<instrument_name>.yaml``` is a configuration file. Here the user can customize the installation to his needs. Therefor he can copy the file to his prefered location and edit it.

# Installation
Download release or clone repository:
```
git clone https://github.com/marcusgmueller/pyAtmosLogger.git
```

# Usage
Copy the file ```<instrument_name>.yaml``` from instrument directory to a custom location. Customize this file to you needs.
## run datalogger
```
python3 pyAtmosLogger.py -m log -p <path_to_instrument_name>.yaml
```
## convert data to netCDF
run command (or schedule it with cron)
```
python3 pyAtmosLogger.py -m log -p <path_to_instrument_name>.yaml
```
