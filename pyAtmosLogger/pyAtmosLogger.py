import argparse
from .utils.utils import *
import importlib

"""
pyAtmosLogger.py
================
The core module of pyAtmosLogger project
"""

def pyAtmosLogger():
    """
    Run pyAtmosLogger from CLI with arguments.
    """
    parser = argparse.ArgumentParser(
        prog='python3 pyAtmosLogger.py',
        description='Python Package for automatic serial data logging to csv file and converting to netCDF',
    )
    parser.add_argument("-m", "--mode", help = "selct operation mode", choices=["log", "convert"], default="log")
    parser.add_argument("-p", "--path", help = "path to config file", required=True)
    args = vars(parser.parse_args())
    printCLIHeader()
    # select instrument class
    #instrumentFile = getInstrumentFile(args["path"])
    config = loadConfig(args["path"])
    #import instrument file
    moduleName = config["instrument"]["instrumentFile"][:-3]
    module = importlib.import_module("pyAtmosLogger.instruments."+moduleName)
    classObject = getattr(module, moduleName)
    instrument = classObject(config)
    #check working mode
    if args["mode"] == "log":
        instrument.log()
    if args["mode"] == "convert":
         instrument.convertMultipleFiles()
if __name__ == '__main__':
    pyAtmosLogger()