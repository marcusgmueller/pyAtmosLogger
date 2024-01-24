import sys
sys.path.append('../../pyAtmosLogger')
from serial import Serial
import datetime as dt
import time
import xarray as xr
import pandas as pd
import glob
from ..utils.utils import *
import pause
import pytz
import numpy as np

class thies_laserprecipitationmonitor_actris:
    """Base class for pyAtmosLogger Dummy 1 Instrument.

    Attributes:
        config (str): yaml-string containing pyAtmosLogger configuration
    """
    configuration = None
    filePath = None
    samplingInterval = None
    connection = None

    def create_thies_header():
        header = [
            "datetime [utc]",
            "STX (start identifier)",
            "Device address",
            "Serial number",
            "Software version",
            "Date of the sensor (tt.mm.jj)",
            "Time of the sensor (on request)",
            "5min_SYNOP_4677 (5 minutes mean value)",
            "5min_SYNOP_4680 (5 minutes mean value)",
            "5min_METAR_4678 (5 minutes mean value)",
            "5min_intensity (5 minutes mean value)",
            "1min_SYNOP_4677 (1 minutes mean value)",
            "1min_SYNOP_4680 (1 minutes mean value)",
            "1min_METAR_4678 (1 minutes mean value)",
            "1min_total_intensity [mm/h] total precipitation",
            "1min_liquid_intensity [mm/h] liquid precipitation",
            "1min_solid_intensity [mm/h] solid precipitation",
            "Precipitation amount [mm]",
            "1min Visibility in precipitation [m]",
            "1min_radar_reflectivity [dBZ]",
            "1min_measuring_quality [%]",
            "1min_max_hail_diam [mm]",

            "Status Laser (OK/on:0, off:1)",
            "Status signal (OK:0, Error:1)",
            "Status Laser temperature (OK:0, Error:1)",
            "Status Laser temperature (OK:0, Error:1)",
            "Status Laser current (OK:0, Error:1)",
            "Status Laser current (OK:0, Error:1)",
            "Status Sensor supply (OK:0, Error:1)",
            "Status Current pane heating laser head (OK:0, warning:1)",
            "Status Current pane heating receiver head (OK:0, warning:1)",
            "Status Temperature sensor (OK:0, warning:1)",
            "Status Heating supply (OK:0, warning:1)",
            "Status Current heating housing (OK:0, warning:1)",
            "Status Current heating heads (OK:0, warning:1)",
            "Status Current heating carriers (OK:0, warning:1)",
            "Status Control output laser power (OK:0, warning:1)",
            "Reserve Status",
            "Interior temperature [°C]",
            "Temperature of laser driver 0-80°C",
            "Mean value laser current [1/100 mA]",
            "Control voltage [mV] (reference value: 4010±5)",
            "Optical control output [mV] (2300 … 6500)",
            "Voltage sensor supply [1/10V]",
            "Current pane heating laser head [mA]",
            "Current pane heating receiver head [mA]",
            "Ambient temperature [°C]",
            "Voltage Heating supply [1/10 V]",
            "Current heating housing [mA]",
            "Current heating heads [mA]",
            "Current heating carriers [mA]",
            ]
        header += [
            "Number of all measured particles ",
            "internal_1 (internal data)",
            "Number of particles < minimal speed (0.15m/s)",
            "internal_2 (internal data)",
            "Number of particles > maximal speed (20m/s)",
            "internal_3 (internal data)",
            "Number of particles < minimal diameter (0.15mm)",
            "internal_4 (internal data)",
        ]
        header += [
            "Number of particles no hydrometeor",
            "Total volume (gross) of this class",
            "Number of particles with unknown classification",
            "Total volume (gross) of this class",
        ]
        header += [
            "no_of_type_" + str(int(i / 2 + 1))
            if i % 2 == 0
            else "vol_of_type_" + str(int((i + 1) / 2))
            for i in range(0, 2 * 9)
        ]
        header += [
            "diam_" + str(int(np.floor(i / 20) + 1)) + "_speed_" + str(int((i % 20) + 1))
            for i in range(0, 22 * 20)
        ]
        header += ["checksum"]
        header =  ';'.join(header)
        header = header+"\n"
        return header
    
    csvHeader = create_thies_header()
    serialWriteString = b'00TR00004\r\n' # We would lie to use data protocol 4 and use the polling of the data transfere
    #serialInitialString = b'00BR22/CS/\r\n'# b'TR00004/CS\r\n' # Check baudrate for the instrument do we have to set them here or do we use the already set one? And if the polling request is the right on
    localTimeZone = ""
    def __init__(self,config):
        self.configuration          = config
        self.samplingInterval       = self.configuration["instrument"]["samplingInterval"]
        self.localTimeZone = getLocalTZ()
        consoleLog("setup completed")
    def serialConnect(self):
        """Method to establish serial connection."""
        self.connection             = Serial(self.configuration["instrument"]["port"])
        self.connection.baudrate    = self.configuration["instrument"]["baudrate"]
        self.connection.bytesize    = self.configuration["instrument"]["bytesize"]
        self.connection.parity      = self.configuration["instrument"]["parity"]
        self.connection.stopbits    = self.configuration["instrument"]["stopbits"]
    def log(self):
        """Method to start logging."""
        self.serialConnect()
        consoleLog("instrument configured")
        consoleLog("logging started")
        while True:
            now = datetime.datetime.utcnow()
            self.filePath = checkCsvFolder(self.configuration, now)
            if not os.path.isfile(self.filePath):
                 f = open(self.filePath, 'w')
                 f.write(self.csvHeader)
                 f.close()
                 print(now.strftime("%Y-%m-%d %H:%M:%S")+": header created")
            f = open(self.filePath, 'a')
            #get data
            if self.connection.is_open == False:
                 self.serialConnect()
                 consoleLog("reconnected")
            self.connection.write(self.serialWriteString)
            data = self.connection.readline()
            dataString      = now.strftime("%Y-%m-%d %H:%M:%S")+";"+data.decode()
            dataString = dataString.replace("\x02", "").replace("\x03", "").replace("\x0D", "").replace("\x0A", "")
            f.write(str(dataString)+"\n")
            f.close()
            newDT = now+datetime.timedelta(seconds=self.samplingInterval)
            newDT = newDT.replace(tzinfo=pytz.utc).astimezone(self.localTimeZone)
            pause.until(newDT)
    
    def convert(self, file):
        """Method to convert single-file csv-data to netCDF.
        
        Attributes:
            file (str): file path to csv data
        """

        consoleLog("error: nc-conversion currently not supported for Thies Disdrometer")
    def convertMultipleFiles(self):
        """Method to convert multiple-file csv-data to netCDF."""
        consoleLog("error: nc-conversion currently not supported for Thies Disdrometer")
