import csv
import os
from src.util.ParserUtil import parse


def readCSVDataset(filePath):
    """
    Parse file

    :param filePath: path to file
    :return: iterator with parsed dataset
    """
    return iter(csv.reader(open(filePath, newline=''), delimiter=','))


def createFolder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def parseCSVFile(file, outFolder, wRatio, hRatio):
    """
    :param file: csv file to parse
    :param outFolder: folder to save images
    :param hRatio: ratio
    :param wRatio: ratio
    :return: void
    """
    dataset = readCSVDataset(file)
    parse(dataset, outFolder, wRatio=wRatio, hRatio=hRatio)
