import datetime
import yaml
from pathlib import Path
import os
import importlib
import time


def loadConfig(configPath):
    with open(configPath, 'r') as file:
        configuration = yaml.safe_load(file)
    return configuration

def checkFolder(configuration):
    dt = datetime.datetime.utcnow()
    storagePath = configuration["storage"]["storagePath"]
    Path(storagePath+dt.strftime(configuration["storage"]["datePath"])).mkdir(parents=True, exist_ok=True)
    filePath = storagePath+dt.strftime(configuration["storage"]["datePath"])
    filename = dt.strftime(configuration["storage"]["fileName"])
    return filePath+filename

def getClassName(configPath):
    configuration = loadConfig(configPath)
    return configuration["instrument"]["instrumentFile"][:-3]
