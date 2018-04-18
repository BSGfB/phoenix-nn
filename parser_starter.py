import configparser
import sys
import os.path
from src.util.FileUtil import createFolder, parseCSVFile

config = configparser.RawConfigParser()
config.read('./resources/application.properties')

wRatio = int(config.get('DataSet', 'wRatio'))
hRatio = int(config.get('DataSet', 'hRatio'))

dataSetFolder = config.get('DataSet', 'dataSetFolder')
parseFolder = config.get('DataSet', 'parseFolder')


if len(sys.argv) < 2:
    raise ValueError('Wrong number of argv. Must be specified files name')

files = sys.argv[1:]

for file in files:
    pathToFile = '{}/{}.csv'.format(parseFolder, file)
    if not os.path.isfile(pathToFile):
        print('ERROR: {} does not exist'.format(pathToFile))
        continue

    out = '{}/{}'.format(dataSetFolder, file)
    createFolder(out)
    parseCSVFile(pathToFile, out, hRatio=hRatio, wRatio=wRatio)
