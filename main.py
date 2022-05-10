import readTxt
import sys, os
from pathlib import Path
#os.system('cmd /c "cd '+str(Path.home())+'\\AppData\\Local\\Programs\\Python\\Python310\\Scripts && pip3 install ')


def run():
    file = readTxt.read(r'C:\Users\hidek\Downloads\a.txt')    
    print(file[9])

if __name__ == "__main__":
    run()    
