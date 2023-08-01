import sys
sys.path.append('../../pyAtmosLogger')
from serial import Serial
import datetime as dt
import time
import xarray as xr
import pandas as pd
import glob
from ..utils.utils import *
import socket
import json

class tsi_ops3330_default:
    """Base class for TSI OPS 3330 instrument.

    Attributes:
        config (str): yaml-string containing pyAtmosLogger configuration
    """
    configuration = None
    filePath = None
    samplingInterval = None
    samplingDuration = None
    connection = None
    ip = None
    port = None
    metadata = {}
    channelSetup = "16,0.300,0.374,0.465,0.579,0.721,0.897,1.117,1.391,1.732,2.156,2.685,3.343,4.162,5.182,6.451,8.032,10.000"
    csvHeader = "utcDatetime,secondSampleInSet,secondSample,validSamples3,dC_bin_1,dC_bin_2,dC_bin_3,dC_bin_4,dC_bin_5,dC_bin_6,dC_bin_7,dC_bin_8,dC_bin_9,dC_bin_10,dC_bin_11,dC_bin_12,dC_bin_13,dC_bin_14,dC_bin_15,dC_bin_16,dC_bin_17,dN_bin_1,dN_bin_2,dN_bin_3,dN_bin_4,dN_bin_5,dN_bin_6,dN_bin_7,dN_bin_8,dN_bin_9,dN_bin_10,dN_bin_11,dN_bin_12,dN_bin_13,dN_bin_14,dN_bin_15,dN_bin_16,dN_bin_17,dNdD_bin_1,dNdD_bin_2,dNdD_bin_3,dNdD_bin_4,dNdD_bin_5,dNdD_bin_6,dNdD_bin_7,dNdD_bin_8,dNdD_bin_9,dNdD_bin_10,dNdD_bin_11,dNdD_bin_12,dNdD_bin_13,dNdD_bin_14,dNdD_bin_15,dNdD_bin_16,dNdD_bin_17,dNdLogD_bin_1,dNdLogD_bin_2,dNdLogD_bin_3,dNdLogD_bin_4,dNdLogD_bin_5,dNdLogD_bin_6,dNdLogD_bin_7,dNdLogD_bin_8,dNdLogD_bin_9,dNdLogD_bin_10,dNdLogD_bin_11,dNdLogD_bin_12,dNdLogD_bin_13,dNdLogD_bin_14,dNdLogD_bin_15,dNdLogD_bin_16,dNdLogD_bin_17,dM_bin_1,dM_bin_2,dM_bin_3,dM_bin_4,dM_bin_5,dM_bin_6,dM_bin_7,dM_bin_8,dM_bin_9,dM_bin_10,dM_bin_11,dM_bin_12,dM_bin_13,dM_bin_14,dM_bin_15,dM_bin_16,dM_bin_17,dMdD,_bin_1,dMdD,_bin_2,dMdD,_bin_3,dMdD,_bin_4,dMdD,_bin_5,dMdD,_bin_6,dMdD,_bin_7,dMdD,_bin_8,dMdD,_bin_9,dMdD,_bin_10,dMdD,_bin_11,dMdD,_bin_12,dMdD,_bin_13,dMdD,_bin_14,dMdD,_bin_15,dMdD,_bin_16,dMdD,_bin_17,dMdLogD_bin_1,dMdLogD_bin_2,dMdLogD_bin_3,dMdLogD_bin_4,dMdLogD_bin_5,dMdLogD_bin_6,dMdLogD_bin_7,dMdLogD_bin_8,dMdLogD_bin_9,dMdLogD_bin_10,dMdLogD_bin_11,dMdLogD_bin_12,dMdLogD_bin_13,dMdLogD_bin_14,dMdLogD_bin_15,dMdLogD_bin_16,dMdLogD_bin_17,total_dC,total_dN,total_dM,unknown\n"

    def __init__(self,config):
        self.configuration          = config
        self.samplingInterval       = self.configuration["instrument"]["samplingInterval"]
        self.samplingDuration       = self.configuration["instrument"]["samplingDuration"]
        self.ip                     = self.configuration["instrument"]["ip"]
        self.port                   = self.configuration["instrument"]["port"]
        self.channelSetup           = self.configuration["instrument"]["channelSetup"]
        consoleLog("setup completed")
    def opsConnect(self):
        """Method to establish serial connection."""
        self.connection     = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.ip, self.port))
    def opsCommand(self,command):
        """Method to execute command on OPS.
        
        Attributes:
            command (str): command to execute
        """
        command = command + "\r"
        try:
            self.connection.send(bytes(command,'ascii'))
            time.sleep(2)
            return self.connection.recv(1024).decode('ascii')
        except:
            self.opsConnect()
            self.connection.send(bytes(command,'ascii'))
            time.sleep(2)
            return self.connection.recv(1024).decode('ascii')
    def opsLockDevice(self):
        """Method to lock device."""
        self.opsCommand("MLOCK")
    def opsUnlockDevice(self):
        """Method to unlock device."""
        self.opsCommand("MUNLOCK")
    def createNewDataFile(self):
        """Method to create new csv file."""
        self.metadata["model_number"] = self.opsCommand("RDMN").replace("\r\n","")
        self.metadata["serial_number"] = self.opsCommand("RDSN").replace("\r\n","")
        self.metadata["firmware"] = self.opsCommand("RDBS").replace("\r\n","")
        self.metadata["units"] = self.opsCommand("RMUNITMEAS").replace("\r\n","")
        self.metadata["loginfo"] = self.opsCommand("RMLOGINFO").replace("\r\n","")
        self.metadata["db_memory"] = self.opsCommand("RMMEMORY").replace("\r\n","")
        self.metadata["log_mode"] = self.opsCommand("RMODELOG").replace("\r\n","")
        self.metadata["channel_setup"] = self.opsCommand("RMODECHSETUP").replace("\r\n","")
        self.metadata["user_calibration"] = self.opsCommand("RMODEUSERCAL").replace("\r\n","")
        self.metadata["flow_calibration"] = self.opsCommand("RMODEFLOWCAL").replace("\r\n","")
        self.metadata["calibration_date"] = self.opsCommand("RSCALDATE").replace("\r\n","")
        self.metadata["flow_calibration"] = self.opsCommand("RMODEFLOWCAL").replace("\r\n","")
        #write to file
        with open(self.filePath, 'w') as outfile:
            json.dump(self.metadata, outfile)
            outfile.write("\n")
        with open(self.filePath, 'a') as f:  
            f.write(self.csvHeader)
        consoleLog("header created")
    def log(self):
        """Method to start logging."""
        self.opsConnect()
        self.opsCommand("WMODECHSETUP "+self.channelSetup)
        self.opsCommand("WMODELOG 0:0,0/0/0,0:0:"+str(self.samplingDuration)+",1,1,0:0:1,0,0,0,0,0,0")
        consoleLog("logging started")
        while True:
            #try:
            now = datetime.datetime.utcnow()
            self.filePath = checkCsvFolder(self.configuration, now)
            if not os.path.isfile(self.filePath):
                self.createNewDataFile()
            #get data
            self.opsCommand("MSTART")
            time.sleep(self.samplingDuration+5)
            #get data
            measurement = self.opsCommand("RMLOGGEDMEAS")
            measurement = measurement[2:-2].replace(",\r\n",",").replace("\r\n",",")
            measurement = now.strftime("%Y-%m-%d %H:%M:%S")+","+measurement+"\n"
            #write to file
            f = open(self.filePath,'a')
            f.write(measurement)
            f.close()
            time.sleep(self.samplingInterval-5-self.samplingDuration)
            #except:
            #    consoleLog("log error")
    def convert(self, file):
        """Method to convert single-file csv-data to netCDF.
        
        Attributes:
            file (str): file path to csv data
        """
        consoleLog("converting file: "+file)
        with open(file, 'r') as f:  
            attributes = json.loads(f.readline())
        binStr = attributes["channel_setup"].split(",")[:-1]
        binFloat = [float(x) for x in binStr]
        df = pd.read_csv(file, delimiter=",", index_col=False, header=1)
        df.index = pd.to_datetime(df["utcDatetime"], format = '%Y-%m-%d %H:%M:%S')
        ds = xr.Dataset()
        #1D-Data
        keys = ['utcDatetime','secondSampleInSet','secondSample','validSamples3','total_dC','total_dN','total_dM','unknown']
        keysNew = ['datetime','secondSampleInSet','secondSample','validSamples3','total_dC','total_dN','total_dM','unknown']
        singleDimensionDF = df[keys].copy()
        singleDimensionDF.columns = keysNew
        singleDimensionDF.loc[:,"datetime"] = pd.to_datetime(singleDimensionDF["datetime"], format = '%Y-%m-%d %H:%M:%S')
        singleDimensionDF.set_index(["datetime"], inplace=True)
        newDs = singleDimensionDF.to_xarray()
        ds = ds.merge(newDs)
        #2D-Fields
        keys = ["dC_bin_", "dN_bin_", "dNdD_bin_", "dNdLogD_bin_","dM_bin_", "dMdD_bin_","dMdLogD_bin_"]
        bins = {}
        for i in range(18):
            bins[i] = binFloat[i]
            
        for key in keys:
            twoDimensionDF = df[df.filter(like=key).columns]
            twoDimensionDF = pd.DataFrame(twoDimensionDF.stack()).reset_index()
            twoDimensionDF.columns = ['datetime','bin', key[:-5]]
            twoDimensionDF.replace(to_replace=key,value="",regex=True,inplace=True)
            twoDimensionDF["bin"] = twoDimensionDF["bin"].astype("int")
            twoDimensionDF.bin.replace(bins,inplace=True)
            twoDimensionDF.set_index(["datetime", "bin"], inplace=True)
            newDs = twoDimensionDF.to_xarray()
            newDs["datetime"] = pd.to_datetime(newDs.datetime)
            ds = ds.merge(newDs)
        # set attributes
        ds.datetime.attrs = {
            'encoding': 'nanoseconds since 1970-01-01',
            'long_name': "time UTC"
        }
        ds.bin.attrs = {
            'unit': '1e-6 m',
            'long_name': "Bin Lower Limit - Optical Diameter"
        }
        ds.dC.attrs = {
            'unit': '#',
            'long_name': "Counts"
        }
        ds.dN.attrs = {
            'unit': '#/cm3',
            'long_name': "Number Concentration"
        }
        ds.dNdD.attrs = {
            'unit': '(#/(cm3 x μm))e3',
            'long_name': "Number Concentration Linearly Normalized"
        }
        ds.dNdLogD.attrs = {
            'unit': '(#/cm3)e3',
            'long_name': "Number Concentration Logarithmically Normalized"
        }
        ds.dM.attrs = {
            'unit': 'μg/m3',
            'long_name': "Mass Concentration"
        }
        ds.dMdD.attrs = {
            'unit': 'μg/(m3 x μm)',
            'long_name': "Mass Concentration Linearly Normalized"
        }
        ds.dMdLogD.attrs = {
            'unit': 'μg/m3',
            'long_name': "Mass Concentration Logarithmically Normalized"
        }
        ds.secondSampleInSet.attrs = {
            'unit': 's',
            'long_name': "Current Second in set"
        }
        ds.secondSample.attrs = {
            'unit': 's',
            'long_name': "Current Second in Sample"
        }
        ds.validSamples3.attrs = {
            'long_name': "Valid Sample in RMLOGGEDBINS (used for Aerosol Instrument Manager® software)"
        }
        ds.total_dC.attrs = {
            'unit': '#',
            'long_name': "Total Counts"
        }
        ds.total_dN.attrs = {
            'unit': '#/cm3',
            'long_name': "Total Number Concentration"
        }
        ds.total_dM.attrs = {
            'unit': 'μg/m3',
            'long_name': "Total Mass Concentration"
        }
            
        for attr in self.configuration["attributes"]:
            ds.attrs[attr] = self.configuration["attributes"][attr]
        dsAttributes = ds.attrs
        dsAttributes.update(getPyAtmosLoggerAttributes())
        dsAttributes.update(attributes)
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