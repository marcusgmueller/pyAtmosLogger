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
        consoleLog("converting file: "+file)
        df = pd.read_csv(file, delimiter=";", index_col=False)
        ds = xr.Dataset()
        #1D-Data
        def create_keys():
            header = [
                "datetime [utc]",
                "STX (start identifier)",
                "Device address",
                "Serial number",
                "Software version",
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
            header += ["checksum", "CLRF"]
            return header
        keys = create_keys()

        def create_keysNew():
            header = [
                "time",
                "stx",
                "device_address",
                "serial_number",
                "software_version",
                "SYNOP_4677_5min",
                "SYNOP_4680_5min",
                "METAR_4678_5min",
                "intensity",
                "SYNOP_4677_1min",
                "SYNOP_4680_1min",
                "METAR_4678_1min",
                "rr",
                "rr_liquid",
                "rr_solid",
                "rain_accum",
                "visibility",
                "ze",
                "measuring",
                "hail_dim",

                "status_laser",
                "status_signal",
                "status_laser_temp1",
                "status_laser_temp2",
                "status_laser_current1",
                "status_laser_current2",
                "status_sensor",
                "status_heating_laser",
                "status_heating_receiver",
                "status_temp_sensor",
                "status_heating_supply",
                "status_heating_housing",
                "status_heating_heads",
                "status_heating_carriers",
                "status_out_laser_power",
                "reserve_status",
                "interior_temp",
                "temp_laser_driver",
                "laser_current",
                "control_voltage",
                "opt_cont_out",
                "volt_sensor",
                "current_heating_laser",
                "current_heating_receiver",
                "temp",
                "vol_heating_supply",
                "current_heating_housing",
                "current_heating_heads",
                "current_heating_carriers",
                ]
            header += [
                "n_particles",
                "internal_1",
                "n_particles_min_15m/s",
                "internal_2",
                "n_particles_max_20m/s",
                "internal_3",
                "n_particles_min_15cm",
                "internal_4",
            ]
            header += [
                "no_not_hydrometeor",
                "Tot_vol_not_hydrometeor"
                "no_unknown_classification",
                "Tot_volunknown_classification",
            ]
            header += ["checksum", "CLRF"]
            return header
                
        keysNew = create_keysNew()
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
       
        # #3D-Fields
        # datetimeList    = []
        # vedClassList      = []
        # rofClassList      = []
        # MList           = []

        # for entry in df.iterrows():     #date
        #     for i in range(32):         #d_class
        #         for j in range(32):     #v_class
        #             datetimeList.append(pd.to_datetime(entry[1]["datetime_utc"], format = '%Y-%m-%d %H:%M:%S'))
        #             vedClassList.append(j)
        #             rofClassList.append(i)
        #             MList.append(entry[1]["M_"+str(i)+"_"+str(j)])
        # newDF = pd.DataFrame(list(zip(datetimeList, vedClassList, rofClassList, MList)), columns =['time', 'ved_class', 'rof_class', "M"])

        newDF.set_index(["time", "ved_class","rof_class"], inplace=True)
        
        # define some additional vectors
        vclasses = xr.DataArray([0.1, 0.3, 0.5, 0.7, 0.9, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.8, 4.6, 5.4, 6.2, 7.0, 7.8, 8.8, 9.5, 15.0], dims=('ved_class'), coords=[ds.ved_class] )
        vwidth   = xr.DataArray([0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 1.0, 10.0], dims=('ved_class'), coords=[ds.ved_class] )        
        
        dclasses = xr.DataArray([0.0625, 0.1875, 0.3125, 0.375, 0.625, 8.75, 1.25, 1.375, 1.625, 2.250, 2.75, 3.25, 3.75, 4.25, 4.75, 5.25, 5.75, 6.25, 6.75, 7.25, 7.75, 12.0], dims=('rof_class'), coords=[ds.rof_class] )        
        dwidth   = xr.DataArray([ 0.125,  0.125,  0.125,  0.25,  0.25, 0.25, 0.25,  0.25,  0.25,   0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5, 8.0 ], dims=('rof_class'), coords=[ds.rof_class] )          
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
        ds.SYNOP_4680_1min.attrs    = {'units': '1',
                                       'long_name': "weather code according to WMO SYNOP 4680",
                                       'comment': "WMO Code Table 4680: 00: No Precip., 51-53: Drizzle, 57-58: Drizzle and Rain, 61-63: Rain, 67-68: Rain and Snow, 71-73: Snow, 77: Snow Grains, 87-88: Graupel, 89: Hail; Increasing Intensity in one category indicated by increasing numbers"}
        ds.ze.attrs                 = {'units': 'dBZ',
                                       'long_name': "equivalent_reflectivity_factor; identical to the 6th moment of the drop size distribution"}
        ds.visibility.attrs         = {'units': 'm',
                                       'long_name': "visibility_in_air"}
        ds.n_particles.attrs        = {'units': '1', 
                                       'long_name': "number of detected particles"}
        ds.interior_temp.attrs      = {'units': 'deg C',
                                       'long_name': "temperature_of_sensor"}       
        ds.version.attrs            = {'description': 'IOP firmware version'}       
        ds.current_heating_housing.attrs  = {'units': 'A', 
                                       'long_name': 'Current of heating housing of the system'}
        ds.current_heating_heads.attrs  = {'units': 'A', 
                                       'long_name': 'Current of heating instrument heads'}
        ds.current_heating_carriers.attrs  = {'units': 'A', 
                                       'long_name': 'Current of heating carrier of the system'}
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
        # ds.M.attrs                  = {'units': '1', 
        #                                'long_name': "number of particles per volume equivalent diameter class and fall velocity class",
        #                                'description': 'raw data matrix. number of particles per volume diameter and fall velocity'}
        ds.ved_class.attrs          = {'units': '', 
                                       'description': 'volume equivalent diameter (ved) class'}
        ds.rof_class.attrs          = {'units': '', 
                                       'description': 'average rate of fall (rof) class'}
        ds.status_sensor.attrs      = {'units': "1" ,
                                       'long_name': "Status of the Sensor" ,
                                       'comments': "0: everything OK, 1: Error."}
        ds.status_laser.attrs       = {'units': "1" ,
                                       'long_name': "Status of the Sensor" ,
                                       'comments': "0: everything OK, 1: Error."}
        ds.status_temp_sensor.attrs = {'units': "1" ,
                                       'long_name': "Status of the Sensor" ,
                                       'comments': "0: everything OK, 1: Error."}
        ds.status_heating_supply.attrs = {'units': "1" ,
                                       'long_name': "Status of the Sensor" ,
                                       'comments': "0: everything OK, 1: Error."}
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
        ds.attrs["Instrument_serial_number"] = ds.serial_no[1]
        dsAttributes = ds.attrs
        dsAttributes.update(getPyAtmosLoggerAttributes())
        ds.attrs = dsAttributes
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
