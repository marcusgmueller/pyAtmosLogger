import argparse
from pyAtmosLogger.instruments import *
from pyAtmosLogger.utils import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='python3 pyAtmosLogger.py',
        description='Python Package for automatic serial data logging to csv file and converting to netCDF',
    )
    parser.add_argument("-m", "--mode", help = "selct operation mode", choices=["log", "convert"], default="log")
    parser.add_argument("-p", "--path", help = "path to config file", required=True)
    args = vars(parser.parse_args())
    # select instrument class
    instrumentFile = getInstrumentFile(args["path"])
    if instrumentFile == "pyAtmosLogger_dummy_1.py":
        instrument = pyAtmosLogger_dummy_1(args["path"])
    #check working mode
    if args["mode"] == "log":
        instrument.log()
        
    if args["mode"] == "convert":
         instrument.convert()