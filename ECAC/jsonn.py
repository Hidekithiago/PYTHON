import sys, os
from pathlib import Path
#os.system('cmd /c "cd '+str(Path.home())+'\\AppData\\Local\\Programs\\Python\\Python310\\Scripts && pip3 install ')
import json

def createJsonFile(cod, rend, imp, cnpj, nome, data, cnpj_filial):
    a = json.dumps({"codigo":cod,"rendimento":rend,"imposto":imp,"cnpj":cnpj,"nome":nome,"data":data,"cnpj_filial":cnpj_filial})
    return a
