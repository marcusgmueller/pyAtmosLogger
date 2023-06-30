import sys
sys.path.append('../../pyAtmosLogger')
from pyAtmosLogger import utils
import sds011 as sds011Package
import datetime as dt
import time

class sds011:

    connection = None
    configuration = None
    filePath = None
    samplingInterval = None
    def __init__(self,configPath):
        self.configuration = loadConfig(configPath)
        self.samplingInterval = self.configuration["instrument"]["samplingInterval"]
        port = self.configuration["instrument"]["port"]
        self.connection = sds011Package.SDS011(port=port)
        self.connection.set_working_period(rate=1)
        print("setup done")
        print("created")

    def checkFile(self):
        print("create header")
        f = open(self.filePath, 'w')
        f.write("utcDatetime, pm2.5, pm10, serialNumber\n")
        f.close()

    def log(self):
        print("logging started")
        while True:
            self.filePath = checkFolder(self.configuration)
            self.checkFile()
            f = open(self.filePath, 'a')
            data = self.connection.read_measurement()
            dataString   = dt.strftime("%Y-%m-%d %H:%M:%S")+","+str(data["pm2.5"])+","+str(data["pm10"])+","+str(data["device_id"])
            f.write(dataString+"\n")
            f.close()
            time.sleep(self.samplingInterval)

    def convertNC(self):
        print("not implemented yet")
    

