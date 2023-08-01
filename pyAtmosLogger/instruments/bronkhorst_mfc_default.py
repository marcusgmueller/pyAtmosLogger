import sys
sys.path.append('../../pyAtmosLogger')
import minimalmodbus
import datetime as dt
import time
import xarray as xr
import pandas as pd
import serial
import glob
from ..utils.utils import *


class bronkhorst_mfc_default:
    """Base class for Bronkhorst MFC.

    Attributes:
        config (str): yaml-string containing pyAtmosLogger configuration
    """

    configuration = None
    filePath = None
    samplingInterval = None
    connection = None
    csvHeader = "datetime_utc,temperature,fsetpoint,fmeasure,valve_out,capacity_unit,measure,setpoint\n"
    def __init__(self,config):
        self.configuration          = config
        consoleLog("setup completed")
    def serialConnect(self):
        """Method to establish serial connection."""
        self.connection = minimalmodbus.Instrument(self.configuration["instrument"]["port"],1)
        self.connection.serial.parity   = serial.PARITY_EVEN
        newFlow = self.configuration["instrument"]["setFlow"]
        self.connection.write_float(41240, float(newFlow))
    def log(self):
        """Method to start logging."""
        self.serialConnect()
        consoleLog("logging started")
        while True:
            try:
                now = datetime.datetime.utcnow()
                self.filePath = checkCsvFolder(self.configuration, now)
                if not os.path.isfile(self.filePath):
                    f = open(self.filePath, 'w')
                    f.write(self.csvHeader)
                    f.close()
                    print(now.strftime("%Y-%m-%d %H:%M:%S")+": header created")
                f = open(self.filePath, 'a')
                #get data
                data = str(self.connection.read_float(41272))+","+str(self.connection.read_float(41240))+","+str(self.connection.read_float(41216))+","+str(self.connection.read_float(61960))+","+str(self.connection.read_string(33272,3))+","+str(self.connection.read_register(32))+","+str(self.connection.read_register(33))
                dataString   = now.strftime("%Y-%m-%d %H:%M:%S")+","+data+"\n"
                f.write(dataString)
                f.close()
                time.sleep(self.configuration["instrument"]["samplingInterval"])
            except:
                consoleLog("log error")
                self.serialConnect()
                consoleLog("reconnected")
    def convert(self, file):
        """Method to convert single-file csv-data to netCDF.
        
        Attributes:
            file (str): file path to csv data
        """
        consoleLog("converting file: "+file)
        df = pd.read_csv(file, delimiter=",", index_col=False, header=0)
        df.index = pd.to_datetime(df["datetime_utc"], format = '%Y-%m-%d %H:%M:%S')
        df.drop(columns=["datetime_utc"])
        df["capacity_unit"] = df["capacity_unit"].str.replace(' ', '')
        ds = df.to_xarray()

        # set attributes
        ds.datetime_utc.attrs = {
            'encoding': 'nanoseconds since 1970-01-01',
            'long_name': "time UTC"
        }
        ds.fmeasure.attrs = {
            'unit': 'l/min',
            'long_name': "measured Flow"
        }
        ds.fsetpoint.attrs = {
            'unit': 'l/min',
            'long_name': "setpoint Flow"
        }
        ds.temperature.attrs = {
            'unit': 'C',
            'long_name': "measured temperature"
        }  
        for attr in self.configuration["attributes"]:
            ds.attrs[attr] = self.configuration["attributes"][attr]
        dsAttributes = ds.attrs
        dsAttributes.update(getPyAtmosLoggerAttributes())
        ds.attrs = dsAttributes
        #save file
        ncFilePath = checkNcFolder(self.configuration, file)    
        ds.to_netcdf(ncFilePath, format="NETCDF3_CLASSIC")
    def convertMultipleFiles(self):
         """Method to convert multiple-file csv-data to netCDF."""
         nDays = self.configuration["storage"]["ncConversionDays"]
         fileList = glob.glob(self.configuration["storage"]["csvStoragePath"]+'/**/*.csv', recursive=True)
         fileList = sorted(fileList)[-nDays:]
         consoleLog("converter started")
         for file in fileList:
             self.convert(file)
         consoleLog("converter finished")            
