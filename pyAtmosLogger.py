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
    #check working mode
    if args["mode"] == "log":
        #className = getClassName(args["path"])
        #classString = className+"("+args["path"]+")"
        #instrument = eval(classString)
        #instrument.setup(args["path"])
        instrument = sds011(args["path"]) # make this variable
        instrument.log()
    #if args["mode"] == "convert":
    #     runConverter(args["path"])