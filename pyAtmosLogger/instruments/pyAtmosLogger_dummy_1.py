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

    configuration = None
    filePath = None
    samplingInterval = None
    
    def __init__(self,config):
        self.configuration = config
        self.samplingInterval = self.configuration["instrument"]["samplingInterval"]
        now = dt.datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S")+": setup completed")

    def log(self):
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

    def convert(self):
        now = dt.datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S")+": converter started")
        fileList = glob.glob(self.configuration["storage"]["csvStoragePath"]+'/**/*.csv', recursive=True)
        csvFile = fileList[-1]
        df = pd.read_csv(csvFile)
        df["utcDatetime"] = pd.to_datetime(df["utcDatetime"])
        df.set_index('utcDatetime', inplace=True)
        ds = xr.Dataset(df)
        for attr in self.configuration["attributes"]:
            ds.attrs[attr] = self.configuration["attributes"][attr]
        ncFilePath = checkNcFolder(self.configuration, csvFile)        
        ds.to_netcdf(ncFilePath, format="NETCDF4")
        now = dt.datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S")+": converter finished")
    

