import os, io
from pathlib import Path
#os.system('cmd /c "cd '+str(Path.home())+'\\AppData\\Local\\Programs\\Python\\Python310\\Scripts && pip3 install ')

def readEncoding(directory, encodin):
    with open(directory, encoding=encodin) as f:
        lines = f.readlines()
    return lines

def read(directory):
    with open(directory) as f:
        lines = f.readlines()
    return lines