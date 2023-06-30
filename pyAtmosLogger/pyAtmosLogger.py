import argparse
from .instruments.ott_parsivel2_default import *
from .instruments.pyAtmosLogger_dummy_1 import *
from .utils.utils import *


def pyAtmosLogger():
    parser = argparse.ArgumentParser(
        prog='python3 pyAtmosLogger.py',
        description='Python Package for automatic serial data logging to csv file and converting to netCDF',
    )
    parser.add_argument("-m", "--mode", help = "selct operation mode", choices=["log", "convert"], default="log")
    parser.add_argument("-p", "--path", help = "path to config file", required=True)
    parser.add_argument("-d", "--days", help = "number of days to convert to netcdf", default=1)
    args = vars(parser.parse_args())
    # select instrument class
    instrumentFile = getInstrumentFile(args["path"])
    if instrumentFile == "pyAtmosLogger_dummy_1.py":
        instrument = pyAtmosLogger_dummy_1(args["path"])
    elif instrumentFile == "ott_parsivel2_default.py":
        instrument = ott_parsivel2_default(args["path"])
    #check working mode
    if args["mode"] == "log":
        instrument.log()
    if args["mode"] == "convert":
         instrument.convertMultipleFiles()
if __name__ == '__main__':
    pyAtmosLogger()

