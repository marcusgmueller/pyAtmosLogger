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

class ott_parsivel2_actris:
    """Base class for pyAtmosLogger Dummy 1 Instrument.

    Attributes:
        config (str): yaml-string containing pyAtmosLogger configuration
    """
    configuration = None
    filePath = None
    samplingInterval = None
    connection = None
    csvHeader = "datetime_utc;rain rate [mm/h];rain accum [mm];wawa;Z [dBz];MOR visibility [m];sample interval [s];Signal amplitude;Number of detected particles;Temperature sensor [°C];Serial number;IOP firmware version;Current heating system [A];Power supply voltage in the sensor [V];Sensor status;Station name;Rain amount absolute [mm];Error code;N00;N01;N02;N03;N04;N05;N06;N07;N08;N09;N10;N11;N12;N13;N14;N15;N16;N17;N18;N19;N20;N21;N22;N23;N24;N25;N26;N27;N28;N29;N30;N31;v00;v01;v02;v03;v04;v05;v06;v07;v08;v09;v10;v11;v12;v13;v14;v15;v16;v17;v18;v19;v20;v21;v22;v23;v24;v25;v26;v27;v28;v29;v30;v31;M_0_0;M_0_1;M_0_2;M_0_3;M_0_4;M_0_5;M_0_6;M_0_7;M_0_8;M_0_9;M_0_10;M_0_11;M_0_12;M_0_13;M_0_14;M_0_15;M_0_16;M_0_17;M_0_18;M_0_19;M_0_20;M_0_21;M_0_22;M_0_23;M_0_24;M_0_25;M_0_26;M_0_27;M_0_28;M_0_29;M_0_30;M_0_31;M_1_0;M_1_1;M_1_2;M_1_3;M_1_4;M_1_5;M_1_6;M_1_7;M_1_8;M_1_9;M_1_10;M_1_11;M_1_12;M_1_13;M_1_14;M_1_15;M_1_16;M_1_17;M_1_18;M_1_19;M_1_20;M_1_21;M_1_22;M_1_23;M_1_24;M_1_25;M_1_26;M_1_27;M_1_28;M_1_29;M_1_30;M_1_31;M_2_0;M_2_1;M_2_2;M_2_3;M_2_4;M_2_5;M_2_6;M_2_7;M_2_8;M_2_9;M_2_10;M_2_11;M_2_12;M_2_13;M_2_14;M_2_15;M_2_16;M_2_17;M_2_18;M_2_19;M_2_20;M_2_21;M_2_22;M_2_23;M_2_24;M_2_25;M_2_26;M_2_27;M_2_28;M_2_29;M_2_30;M_2_31;M_3_0;M_3_1;M_3_2;M_3_3;M_3_4;M_3_5;M_3_6;M_3_7;M_3_8;M_3_9;M_3_10;M_3_11;M_3_12;M_3_13;M_3_14;M_3_15;M_3_16;M_3_17;M_3_18;M_3_19;M_3_20;M_3_21;M_3_22;M_3_23;M_3_24;M_3_25;M_3_26;M_3_27;M_3_28;M_3_29;M_3_30;M_3_31;M_4_0;M_4_1;M_4_2;M_4_3;M_4_4;M_4_5;M_4_6;M_4_7;M_4_8;M_4_9;M_4_10;M_4_11;M_4_12;M_4_13;M_4_14;M_4_15;M_4_16;M_4_17;M_4_18;M_4_19;M_4_20;M_4_21;M_4_22;M_4_23;M_4_24;M_4_25;M_4_26;M_4_27;M_4_28;M_4_29;M_4_30;M_4_31;M_5_0;M_5_1;M_5_2;M_5_3;M_5_4;M_5_5;M_5_6;M_5_7;M_5_8;M_5_9;M_5_10;M_5_11;M_5_12;M_5_13;M_5_14;M_5_15;M_5_16;M_5_17;M_5_18;M_5_19;M_5_20;M_5_21;M_5_22;M_5_23;M_5_24;M_5_25;M_5_26;M_5_27;M_5_28;M_5_29;M_5_30;M_5_31;M_6_0;M_6_1;M_6_2;M_6_3;M_6_4;M_6_5;M_6_6;M_6_7;M_6_8;M_6_9;M_6_10;M_6_11;M_6_12;M_6_13;M_6_14;M_6_15;M_6_16;M_6_17;M_6_18;M_6_19;M_6_20;M_6_21;M_6_22;M_6_23;M_6_24;M_6_25;M_6_26;M_6_27;M_6_28;M_6_29;M_6_30;M_6_31;M_7_0;M_7_1;M_7_2;M_7_3;M_7_4;M_7_5;M_7_6;M_7_7;M_7_8;M_7_9;M_7_10;M_7_11;M_7_12;M_7_13;M_7_14;M_7_15;M_7_16;M_7_17;M_7_18;M_7_19;M_7_20;M_7_21;M_7_22;M_7_23;M_7_24;M_7_25;M_7_26;M_7_27;M_7_28;M_7_29;M_7_30;M_7_31;M_8_0;M_8_1;M_8_2;M_8_3;M_8_4;M_8_5;M_8_6;M_8_7;M_8_8;M_8_9;M_8_10;M_8_11;M_8_12;M_8_13;M_8_14;M_8_15;M_8_16;M_8_17;M_8_18;M_8_19;M_8_20;M_8_21;M_8_22;M_8_23;M_8_24;M_8_25;M_8_26;M_8_27;M_8_28;M_8_29;M_8_30;M_8_31;M_9_0;M_9_1;M_9_2;M_9_3;M_9_4;M_9_5;M_9_6;M_9_7;M_9_8;M_9_9;M_9_10;M_9_11;M_9_12;M_9_13;M_9_14;M_9_15;M_9_16;M_9_17;M_9_18;M_9_19;M_9_20;M_9_21;M_9_22;M_9_23;M_9_24;M_9_25;M_9_26;M_9_27;M_9_28;M_9_29;M_9_30;M_9_31;M_10_0;M_10_1;M_10_2;M_10_3;M_10_4;M_10_5;M_10_6;M_10_7;M_10_8;M_10_9;M_10_10;M_10_11;M_10_12;M_10_13;M_10_14;M_10_15;M_10_16;M_10_17;M_10_18;M_10_19;M_10_20;M_10_21;M_10_22;M_10_23;M_10_24;M_10_25;M_10_26;M_10_27;M_10_28;M_10_29;M_10_30;M_10_31;M_11_0;M_11_1;M_11_2;M_11_3;M_11_4;M_11_5;M_11_6;M_11_7;M_11_8;M_11_9;M_11_10;M_11_11;M_11_12;M_11_13;M_11_14;M_11_15;M_11_16;M_11_17;M_11_18;M_11_19;M_11_20;M_11_21;M_11_22;M_11_23;M_11_24;M_11_25;M_11_26;M_11_27;M_11_28;M_11_29;M_11_30;M_11_31;M_12_0;M_12_1;M_12_2;M_12_3;M_12_4;M_12_5;M_12_6;M_12_7;M_12_8;M_12_9;M_12_10;M_12_11;M_12_12;M_12_13;M_12_14;M_12_15;M_12_16;M_12_17;M_12_18;M_12_19;M_12_20;M_12_21;M_12_22;M_12_23;M_12_24;M_12_25;M_12_26;M_12_27;M_12_28;M_12_29;M_12_30;M_12_31;M_13_0;M_13_1;M_13_2;M_13_3;M_13_4;M_13_5;M_13_6;M_13_7;M_13_8;M_13_9;M_13_10;M_13_11;M_13_12;M_13_13;M_13_14;M_13_15;M_13_16;M_13_17;M_13_18;M_13_19;M_13_20;M_13_21;M_13_22;M_13_23;M_13_24;M_13_25;M_13_26;M_13_27;M_13_28;M_13_29;M_13_30;M_13_31;M_14_0;M_14_1;M_14_2;M_14_3;M_14_4;M_14_5;M_14_6;M_14_7;M_14_8;M_14_9;M_14_10;M_14_11;M_14_12;M_14_13;M_14_14;M_14_15;M_14_16;M_14_17;M_14_18;M_14_19;M_14_20;M_14_21;M_14_22;M_14_23;M_14_24;M_14_25;M_14_26;M_14_27;M_14_28;M_14_29;M_14_30;M_14_31;M_15_0;M_15_1;M_15_2;M_15_3;M_15_4;M_15_5;M_15_6;M_15_7;M_15_8;M_15_9;M_15_10;M_15_11;M_15_12;M_15_13;M_15_14;M_15_15;M_15_16;M_15_17;M_15_18;M_15_19;M_15_20;M_15_21;M_15_22;M_15_23;M_15_24;M_15_25;M_15_26;M_15_27;M_15_28;M_15_29;M_15_30;M_15_31;M_16_0;M_16_1;M_16_2;M_16_3;M_16_4;M_16_5;M_16_6;M_16_7;M_16_8;M_16_9;M_16_10;M_16_11;M_16_12;M_16_13;M_16_14;M_16_15;M_16_16;M_16_17;M_16_18;M_16_19;M_16_20;M_16_21;M_16_22;M_16_23;M_16_24;M_16_25;M_16_26;M_16_27;M_16_28;M_16_29;M_16_30;M_16_31;M_17_0;M_17_1;M_17_2;M_17_3;M_17_4;M_17_5;M_17_6;M_17_7;M_17_8;M_17_9;M_17_10;M_17_11;M_17_12;M_17_13;M_17_14;M_17_15;M_17_16;M_17_17;M_17_18;M_17_19;M_17_20;M_17_21;M_17_22;M_17_23;M_17_24;M_17_25;M_17_26;M_17_27;M_17_28;M_17_29;M_17_30;M_17_31;M_18_0;M_18_1;M_18_2;M_18_3;M_18_4;M_18_5;M_18_6;M_18_7;M_18_8;M_18_9;M_18_10;M_18_11;M_18_12;M_18_13;M_18_14;M_18_15;M_18_16;M_18_17;M_18_18;M_18_19;M_18_20;M_18_21;M_18_22;M_18_23;M_18_24;M_18_25;M_18_26;M_18_27;M_18_28;M_18_29;M_18_30;M_18_31;M_19_0;M_19_1;M_19_2;M_19_3;M_19_4;M_19_5;M_19_6;M_19_7;M_19_8;M_19_9;M_19_10;M_19_11;M_19_12;M_19_13;M_19_14;M_19_15;M_19_16;M_19_17;M_19_18;M_19_19;M_19_20;M_19_21;M_19_22;M_19_23;M_19_24;M_19_25;M_19_26;M_19_27;M_19_28;M_19_29;M_19_30;M_19_31;M_20_0;M_20_1;M_20_2;M_20_3;M_20_4;M_20_5;M_20_6;M_20_7;M_20_8;M_20_9;M_20_10;M_20_11;M_20_12;M_20_13;M_20_14;M_20_15;M_20_16;M_20_17;M_20_18;M_20_19;M_20_20;M_20_21;M_20_22;M_20_23;M_20_24;M_20_25;M_20_26;M_20_27;M_20_28;M_20_29;M_20_30;M_20_31;M_21_0;M_21_1;M_21_2;M_21_3;M_21_4;M_21_5;M_21_6;M_21_7;M_21_8;M_21_9;M_21_10;M_21_11;M_21_12;M_21_13;M_21_14;M_21_15;M_21_16;M_21_17;M_21_18;M_21_19;M_21_20;M_21_21;M_21_22;M_21_23;M_21_24;M_21_25;M_21_26;M_21_27;M_21_28;M_21_29;M_21_30;M_21_31;M_22_0;M_22_1;M_22_2;M_22_3;M_22_4;M_22_5;M_22_6;M_22_7;M_22_8;M_22_9;M_22_10;M_22_11;M_22_12;M_22_13;M_22_14;M_22_15;M_22_16;M_22_17;M_22_18;M_22_19;M_22_20;M_22_21;M_22_22;M_22_23;M_22_24;M_22_25;M_22_26;M_22_27;M_22_28;M_22_29;M_22_30;M_22_31;M_23_0;M_23_1;M_23_2;M_23_3;M_23_4;M_23_5;M_23_6;M_23_7;M_23_8;M_23_9;M_23_10;M_23_11;M_23_12;M_23_13;M_23_14;M_23_15;M_23_16;M_23_17;M_23_18;M_23_19;M_23_20;M_23_21;M_23_22;M_23_23;M_23_24;M_23_25;M_23_26;M_23_27;M_23_28;M_23_29;M_23_30;M_23_31;M_24_0;M_24_1;M_24_2;M_24_3;M_24_4;M_24_5;M_24_6;M_24_7;M_24_8;M_24_9;M_24_10;M_24_11;M_24_12;M_24_13;M_24_14;M_24_15;M_24_16;M_24_17;M_24_18;M_24_19;M_24_20;M_24_21;M_24_22;M_24_23;M_24_24;M_24_25;M_24_26;M_24_27;M_24_28;M_24_29;M_24_30;M_24_31;M_25_0;M_25_1;M_25_2;M_25_3;M_25_4;M_25_5;M_25_6;M_25_7;M_25_8;M_25_9;M_25_10;M_25_11;M_25_12;M_25_13;M_25_14;M_25_15;M_25_16;M_25_17;M_25_18;M_25_19;M_25_20;M_25_21;M_25_22;M_25_23;M_25_24;M_25_25;M_25_26;M_25_27;M_25_28;M_25_29;M_25_30;M_25_31;M_26_0;M_26_1;M_26_2;M_26_3;M_26_4;M_26_5;M_26_6;M_26_7;M_26_8;M_26_9;M_26_10;M_26_11;M_26_12;M_26_13;M_26_14;M_26_15;M_26_16;M_26_17;M_26_18;M_26_19;M_26_20;M_26_21;M_26_22;M_26_23;M_26_24;M_26_25;M_26_26;M_26_27;M_26_28;M_26_29;M_26_30;M_26_31;M_27_0;M_27_1;M_27_2;M_27_3;M_27_4;M_27_5;M_27_6;M_27_7;M_27_8;M_27_9;M_27_10;M_27_11;M_27_12;M_27_13;M_27_14;M_27_15;M_27_16;M_27_17;M_27_18;M_27_19;M_27_20;M_27_21;M_27_22;M_27_23;M_27_24;M_27_25;M_27_26;M_27_27;M_27_28;M_27_29;M_27_30;M_27_31;M_28_0;M_28_1;M_28_2;M_28_3;M_28_4;M_28_5;M_28_6;M_28_7;M_28_8;M_28_9;M_28_10;M_28_11;M_28_12;M_28_13;M_28_14;M_28_15;M_28_16;M_28_17;M_28_18;M_28_19;M_28_20;M_28_21;M_28_22;M_28_23;M_28_24;M_28_25;M_28_26;M_28_27;M_28_28;M_28_29;M_28_30;M_28_31;M_29_0;M_29_1;M_29_2;M_29_3;M_29_4;M_29_5;M_29_6;M_29_7;M_29_8;M_29_9;M_29_10;M_29_11;M_29_12;M_29_13;M_29_14;M_29_15;M_29_16;M_29_17;M_29_18;M_29_19;M_29_20;M_29_21;M_29_22;M_29_23;M_29_24;M_29_25;M_29_26;M_29_27;M_29_28;M_29_29;M_29_30;M_29_31;M_30_0;M_30_1;M_30_2;M_30_3;M_30_4;M_30_5;M_30_6;M_30_7;M_30_8;M_30_9;M_30_10;M_30_11;M_30_12;M_30_13;M_30_14;M_30_15;M_30_16;M_30_17;M_30_18;M_30_19;M_30_20;M_30_21;M_30_22;M_30_23;M_30_24;M_30_25;M_30_26;M_30_27;M_30_28;M_30_29;M_30_30;M_30_31;M_31_0;M_31_1;M_31_2;M_31_3;M_31_4;M_31_5;M_31_6;M_31_7;M_31_8;M_31_9;M_31_10;M_31_11;M_31_12;M_31_13;M_31_14;M_31_15;M_31_16;M_31_17;M_31_18;M_31_19;M_31_20;M_31_21;M_31_22;M_31_23;M_31_24;M_31_25;M_31_26;M_31_27;M_31_28;M_31_29;M_31_30;M_31_31\n"
    serialWriteString = b'CS/P\r\n'
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
                if self.connection.is_open == False:
                    self.serialConnect()
                    consoleLog("reconnected")
                self.connection.write(self.serialWriteString)
                data = self.connection.readline()
                dataString   = now.strftime("%Y-%m-%d %H:%M:%S")+";"+data.decode()
                f.write(str(dataString).rstrip('\n'))
                f.close()
                newDT = now+datetime.timedelta(seconds=self.samplingInterval)
                newDT = newDT.replace(tzinfo=pytz.utc).astimezone(self.localTimeZone)
                pause.until(newDT)
            except:
                consoleLog("log error")
    def convert(self, file):
        """Method to convert single-file csv-data to netCDF.
        
        Attributes:
            file (str): file path to csv data
        """
        consoleLog("converting file: "+file)
        df = pd.read_csv(file, delimiter=";", index_col=False)
        ds = xr.Dataset()
        #1D-Data
        keys = [ 'datetime_utc','rain rate [mm/h]','rain accum [mm]','wawa','Z [dBz]','MOR visibility [m]', 'sample interval [s]','Signal amplitude', 'Number of detected particles','Temperature sensor [°C]','Serial number','IOP firmware version','Current heating system [A]','Power supply voltage in the sensor [V]','Sensor status','Station name','Rain amount absolute [mm]','Error code']
        keysNew = [ 'time'     ,'rr'              ,'rain_accum'     ,'wawa','Ze'     ,'visibility'        , 'sample_interval'    ,'signal_amplitude', 'n_particles'                 ,'T_sensor'               ,'serial_no'    ,'version'             ,'curr_heating'              ,'volt_sensor'                           ,'status_sensor','station_name','rain_absolut'             ,'error_code']
        singleDimensionDF = df[keys].copy()
        singleDimensionDF.columns = keysNew
        singleDimensionDF.loc[:,"time"] = pd.to_datetime(singleDimensionDF["time"], format = '%Y-%m-%d %H:%M:%S')
        singleDimensionDF.set_index(["time"], inplace=True)
        newDs = singleDimensionDF.to_xarray()
        ds = ds.merge(newDs)
        #2D-Fields
        keys            = ["N", "v"]
        classKeys       = ["ved_class", "rof_class"]


        for iKey in range(2):
            datetimeList = []
            classList    = []
            valueList    = []
            for entry in df.iterrows():     #date
                for i in range(32): 
                    datetimeList.append(pd.to_datetime(entry[1]["datetime_utc"], format = '%Y-%m-%d %H:%M:%S'))
                    classList.append(i)
                    valueList.append(entry[1][keys[iKey]+str(i).zfill(2)])
            newDF = pd.DataFrame(list(zip(datetimeList, classList, valueList)), columns =['time', classKeys[iKey], keys[iKey]])
            newDF.set_index(['time', classKeys[iKey]], inplace=True)
            ds = ds.merge(newDF.to_xarray())
        #3D-Fields
        datetimeList    = []
        vedClassList      = []
        rofClassList      = []
        MList           = []

        for entry in df.iterrows():     #date
            for i in range(32):         #d_class
                for j in range(32):     #v_class
                    datetimeList.append(pd.to_datetime(entry[1]["datetime_utc"], format = '%Y-%m-%d %H:%M:%S'))
                    vedClassList.append(j)
                    rofClassList.append(i)
                    MList.append(entry[1]["M_"+str(i)+"_"+str(j)])
        newDF = pd.DataFrame(list(zip(datetimeList, vedClassList, rofClassList, MList)), columns =['time', 'ved_class', 'rof_class', "M"])

        newDF.set_index(["time", "ved_class","rof_class"], inplace=True)

        # define some additional vectors
        vclasses = xr.DataArray([0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 1.1, 1.3, 1.5, 1.7, 1.9, 2.2, 2.6, 3, 3.4, 3.8, 4.4, 5.2, 6, 6.8, 7.6, 8.8, 10.4, 12, 13.6, 15.2, 17.6, 20.8], dims=('ved_class'), coords=[ds.ved_class] )
        dclasses = xr.DataArray([0.062, 0.187, 0.312, 0.437, 0.562, 0.687, 0.812, 0.937, 1.062, 1.187, 1.375, 1.625, 1.875, 2.125, 2.375, 2.75, 3.25, 3.75, 4.25, 4.75, 5.5, 6.5, 7.5, 8.5, 9.5, 11, 13, 15, 17, 19, 21.5, 24.5], dims=('rof_class'), coords=[ds.rof_class] )        
        vwidth   = xr.DataArray([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.8, 0.8, 0.8, 0.8, 0.8, 1.6, 1.6, 1.6, 1.6, 1.6, 3.2, 3.2], dims=('ved_class'), coords=[ds.ved_class] )        
        dwidth   = xr.DataArray([0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3], dims=('rof_class'), coords=[ds.rof_class] )          

        # put variables into DataSet
        ds = ds.merge(newDF.to_xarray())
        # add additional varaibles
        ds["vclasses"] = vclasses        
        ds["dclasses"] = dclasses 
        ds["vwidth"]   = vwidth 
        ds["dwidth"]   = dwidth         

        #set attributes
        ds.rr.attrs                 = {'units': 'mm h-1',
                                       'long_name': "rainfall_rate"}    
        ds.rain_accum.attrs         = {'units': 'km m-2',
                                       'long_name': "precipitation amount",
                                       'comment': "accumulated precipitation amount (32 bit) since start of day"}
        ds.wawa.attrs               = {'units': '1',
                                       'long_name': "weather code according to WMO SYNOP 4680",
                                       'comment': "WMO Code Table 4680: 00: No Precip., 51-53: Drizzle, 57-58: Drizzle and Rain, 61-63: Rain, 67-68: Rain and Snow, 71-73: Snow, 77: Snow Grains, 87-88: Graupel, 89: Hail; Increasing Intensity in one category indicated by increasing numbers"}
        ds.Ze.attrs                 = {'units': 'dBZ',
                                       'long_name': "equivalent_reflectivity_factor; identical to the 6th moment of the drop size distribution"}
        ds.visibility.attrs         = {'units': 'm',
                                       'long_name': "visibility_in_air"}
        ds.sample_interval.attrs    = {'units': 's',
                                       'long_name': "time interval for each sample"}
        ds.signal_amplitude.attrs   = {'units': ''}
        ds.n_particles.attrs        = {'units': '1', 
                                       'long_name': "number of detected particles"}
        ds.T_sensor.attrs           = {'units': 'deg C',
                                       'long_name': "temperature_of_sensor"}       
        ds.version.attrs            = {'description': 'IOP firmware version'}
        ds.curr_heating.attrs       = {'units': 'A', 
                                       'long_name': 'Current of heating system'}
        ds.volt_sensor.attrs        = {'units': 'V', 
                                       'long_name': 'Power supply voltage of the sensor'}
        ds.rain_absolut.attrs       = {'units': 'km m-2',
                                       'long_name': "precipitation absolut",
                                       'comment': "accumulated precipitation amount (32 bit) since start of device (OTT software product)"}
        ds.N.attrs                  = {'units': 'log_10(1/m^3 mm)', 
                                       'long_name': "particle concentration per diameter class",
                                       'description': 'average volume equivalent diameter (ved)'}
        ds.v.attrs                  = {'units': 'm s-1', 
                                       'long_name': "mean falling velocity per diameter class",
                                       'description': 'average rate of fall (rof)'}
        ds.M.attrs                  = {'units': '1', 
                                       'long_name': "number of particles per volume equivalent diameter class and fall velocity class",
                                       'description': 'raw data matrix. number of particles per volume diameter and fall velocity'}
        ds.ved_class.attrs          = {'units': '', 
                                       'description': 'volume equivalent diameter (ved) class'}
        ds.rof_class.attrs          = {'units': '', 
                                       'description': 'average rate of fall (rof) class'}
        ds.status_sensor.attrs      = {'units': "1" ,
                                       'long_name': "Status of the Sensor" ,
                                       'comments': "0: everything OK, 1: Laser protective glass is dirty, but measurements are still possible, 2: Laser protective glass is dirty, partially covered. No further usable measurements are possible."}
        ds.vclasses.attrs            = {'units': "m s-1" ,
 		                               'long_name': "velocity class center"}
        ds.dclasses.attrs            = {'units': "mm" ,
 		                               'long_name': "volume equivalent diameter class center"}
        ds.vwidth.attrs              = {'units': "m s-1" ,
 		                               'long_name': "velocity class width"}
        ds.dwidth.attrs              = {'units': "mm" ,
 		                               'long_name': "volume equivalent diameter class width"}

        for attr in self.configuration["attributes"]:
            ds.attrs[attr] = self.configuration["attributes"][attr]
        now = dt.datetime.now()
        ds.attrs["Instrument_serial_number"] = str(ds.serial_no[1])
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
