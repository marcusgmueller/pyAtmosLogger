import datetime
import yaml
from pathlib import Path
import os
import importlib
import time
import datetime as dt

def loadConfig(configPath):
    with open(configPath, 'r') as file:
        configuration = yaml.safe_load(file)
    return configuration
def checkCsvFolder(configuration, datetime):
    storagePath = configuration["storage"]["csvStoragePath"]
    Path(storagePath+datetime.strftime(configuration["storage"]["DatePath"])).mkdir(parents=True, exist_ok=True)
    filePath = storagePath+datetime.strftime(configuration["storage"]["DatePath"])
    filename = datetime.strftime(configuration["storage"]["csvFileName"])
    return filePath+filename
def checkNcFolder(configuration, filename):
    string = filename[:-4]
    string = string.replace(configuration["storage"]["csvStoragePath"],"")
    datePath = string.rsplit("/", 1)[0]
    fileName = string.rsplit("/", 1)[1]
    storagePath = configuration["storage"]["ncStoragePath"]
    Path(storagePath+datePath).mkdir(parents=True, exist_ok=True)
    return storagePath+datePath+"/"+fileName+".nc"
def consoleLog(message):
    now = dt.datetime.utcnow()
    print(now.strftime("%Y-%m-%d %H:%M:%S")+": "+message)