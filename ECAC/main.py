import readTxt, jsonn
import sys, os
from pathlib import Path
#os.system('cmd /c "cd '+str(Path.home())+'\\AppData\\Local\\Programs\\Python\\Python310\\Scripts && pip3 install ')
import re
import locale

locale.setlocale(locale.LC_NUMERIC, 'pt_BR.UTF-8')
def run():
    file = readTxt.read(r'C:\Users\hidek\Downloads\a.txt')    
    count = 0
    jsonFile = '['
    for x in file:
        
        try: listcnpjFilial = re.findall(r'(?<=Beneficiário : )\d+\.\d+\.\d+\/\d+-\d+',file[1]); cnpjFilial = listcnpjFilial[0].rstrip() 
        except: pass
        print (x)
        
        print(type(count))
        print(count)
        try:
            listCNPJCPF_FONTE = re.findall(r'^\d+',x); CNPJCPF_FONTE = listCNPJCPF_FONTE[0]; CNPJCPF_FONTE = str(CNPJCPF_FONTE[0:2])+'.'+str(CNPJCPF_FONTE[2:5])+'.'+str(CNPJCPF_FONTE[5:8])+'/'+str(CNPJCPF_FONTE[8:12])+'-'+str(CNPJCPF_FONTE[12:14])
            listNOME_DA_FONTE_PAGADORA = re.findall(r'(?<= \d )\w.+(?=\s{8})',x); NOME_DA_FONTE_PAGADORA = listNOME_DA_FONTE_PAGADORA[0].rstrip()
            listENTREGA = re.findall(r'\d{8}(?= \d{4} )',x); ENTREGA = listENTREGA[0]; ENTREGA = str(ENTREGA[6:8])+'/'+ str(ENTREGA[4:6])+'/'+str(ENTREGA[0:4])            
            listCOD = re.findall(r'(?<= \d{8} )\d+',x); COD = listCOD[0].rstrip()
            listRENDIMENTO = re.findall(r'(?<= \d{8} \d{4} )\d+',x); RENDIMENTO = listRENDIMENTO[0].rstrip(); RENDIMENTO = locale.format('%.2f', (float(RENDIMENTO)/100), True)
            listIMPOSTO = re.findall(r'\d+   $',x); IMPOSTO = listIMPOSTO[0].rstrip(); IMPOSTO = locale.format('%.2f', (float(IMPOSTO)/100), True)
            print('CNPJ: %s\nNome: %s\nDTENTREGA: %s\nCodigo: %s\nRENDIMENTO: %s\nIMPOSTO: %s\nCNPJFILIAL: %s\n\n\n\n' % (CNPJCPF_FONTE, NOME_DA_FONTE_PAGADORA, ENTREGA, COD , RENDIMENTO, IMPOSTO, cnpjFilial))
            a = jsonn.createJsonFile(COD, RENDIMENTO, IMPOSTO, CNPJCPF_FONTE, NOME_DA_FONTE_PAGADORA, ENTREGA, cnpjFilial)
            print(a)
            jsonFile += '['+a+']'
            count += 1
        except Exception as a:
            print(a)
    jsonFile += ']'
    print(jsonFile)

if __name__ == "__main__":
    run()    
