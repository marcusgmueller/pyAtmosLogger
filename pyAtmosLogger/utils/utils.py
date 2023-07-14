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
def getPyAtmosLoggerAttributes():
    now = dt.datetime.utcnow()
    dict = {
        "Processing_date_utc": now.strftime("%Y-%m-%d %H:%M:%S") ,
        "Processing_software": "pyAtmosLogger",
        "Processing_software_version": "v0.3",
        "Processing_software_repository": "https://github.com/marcusgmueller/pyAtmosLogger",
        "Processing_software_doi": "10.5281/zenodo.8138038"
    }
    return dict