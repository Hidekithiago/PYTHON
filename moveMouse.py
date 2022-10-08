import pyautogui
import sys, io
import time
import os, sys
from pathlib import Path
os.system('cmd /c "cd '+str(Path.home())+'\\AppData\\Local\\Programs\\Python\\Python310\\Scripts && pip3 install pyautogui')


def moveMouse(x, y):    
    pyautogui.moveTo(x, y)

def moveMouseClick(x, y):
    pyautogui.click(x, y)

def get_position():
    for i in range(5, 0, -1):
        print('Aguarde %s segundos' % i)
        time.sleep(1)
    print(pyautogui.position())

if __name__ == "__main__":
    a = sys.argv[1]
    try: x = sys.argv[2]; x=int(x); 
    except: pass
    try: y = sys.argv[3]; y=int(y);
    except: pass
    
    if a == 'moveMouse':        
        moveMouse(x, y)
    elif a == 'moveMouseClick':        
        moveMouseClick(x, y)
    elif a == 'getPosition':        
        get_position()
    else: print('Nao achou o comando')
    
    