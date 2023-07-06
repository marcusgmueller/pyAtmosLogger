import sys
sys.path.append('../../pyAtmosLogger')
sys.path.append("..")
from ..utils.utils import *
import sds011 as sds011Package
import datetime as dt
import time
import random
import xarray as xr
import pandas as pd
import glob

class pyAtmosLogger_dummy_1:
    """Base class for pyAtmosLogger Dummy 1 Instrument.

    Attributes:
        config (str): yaml-string containing pyAtmosLogger configuration
    """
    configuration = None
    filePath = None
    samplingInterval = None
    
    def __init__(self,config):
        self.configuration = config
        self.samplingInterval = self.configuration["instrument"]["samplingInterval"]
        now = dt.datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S")+": setup completed")

    def log(self):
        """Method to start logging."""
        now = dt.datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S")+": logging started")
        while True:
            now = dt.datetime.now()
            self.filePath = checkCsvFolder(self.configuration, now)
            if not os.path.isfile(self.filePath):
                f = open(self.filePath, 'w')
                f.write("utcDatetime,randomValue\n")
                f.close()
                print(now.strftime("%Y-%m-%d %H:%M:%S")+": header created")
            f = open(self.filePath, 'a')
            data = random.random()
            dataString   = now.strftime("%Y-%m-%d %H:%M:%S")+","+str(data)
            f.write(dataString+"\n")
            f.close()
            time.sleep(self.samplingInterval)

    def convert(self, file):
        """Method to convert single-file csv-data to netCDF.
        
        Attributes:
            file (str): file path to csv data
        """
        consoleLog("converting file: "+file)
        df = pd.read_csv(file, delimiter=",", index_col=False)
        ds = xr.Dataset()
        df["utcDatetime"] = pd.to_datetime(df["utcDatetime"])
        df.set_index('utcDatetime', inplace=True)
        ds = xr.Dataset(df)
        for attr in self.configuration["attributes"]:
            ds.attrs[attr] = self.configuration["attributes"][attr]
        now = dt.datetime.now()
        ds.attrs["Processing_date"] = now.strftime("%Y-%m-%d %H:%M:%S") 
        ds.attrs["Processing_software"] = "pyAtmosLogger"
        ds.attrs["Processing_software_version"] = "v0.1"
        #save file
        ncFilePath = checkNcFolder(self.configuration, file)        
        ds.to_netcdf(ncFilePath, format="NETCDF4")
    def convertMultipleFiles(self):
         """Method to convert multiple-file csv-data to netCDF."""
         nDays = self.configuration["storage"]["ncConversionDays"]
         fileList = glob.glob(self.configuration["storage"]["csvStoragePath"]+'/**/*.csv', recursive=True)
         fileList = sorted(fileList)[-nDays:]
         consoleLog("converter started")
         for file in fileList:
             self.convert(file)
         consoleLog("converter finished")

