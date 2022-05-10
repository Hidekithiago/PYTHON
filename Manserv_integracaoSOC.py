import os, sys, config
from pathlib import Path
#os.system('cmd /c "cd '+str(Path.home())+'\\AppData\\Local\\Programs\\Python\\Python310\\Scripts && pip3 install requests')
#os.system('cmd /c "cd '+str(Path.home())+'\\AppData\\Local\\Programs\\Python\\Python310\\Scripts && pip3 install zeep')
#os.system('cmd /c "cd '+str(Path.home())+'\\AppData\\Local\\Programs\\Python\\Python310\\Scripts && pip3 install regex')
#os.system('cmd /c "cd '+str(Path.home())+'\\AppData\\Local\\Programs\\Python\\Python310\\Scripts && pip3 install urllib3')
#os.system('cmd /c "cd '+str(Path.home())+'\\AppData\\Local\\Programs\\Python\\Python310\\Scripts && pip3 install DateTime')
#os.system('cmd /c "cd '+str(Path.home())+'\\AppData\\Local\\Programs\\Python\\Python310\\Scripts && pip3 install mysql-connector-python')
#os.system('cmd /c "cd '+str(Path.home())+'\\AppData\\Local\\Programs\\Python\\Python310\\Scripts && pip3 install socket.py')
#os.system('cmd /c "cd '+str(Path.home())+'\\AppData\\Local\\Programs\\Python\\Python310\\Scripts && pip3 install numpy')
#os.system('cmd /c "cd '+str(Path.home())+'\\AppData\\Local\\Programs\\Python\\Python310\\Scripts && pip3 install ')

import urllib.request
from datetime import datetime
import re
from http.client import OK
import mysql.connector as mysql
from mysql.connector import errorcode
import socket
from datetime import datetime
#ssl._create_default_https_context = ssl._create_unverified_context
from numpy import complex_
import config
from random import random
from mysql_handler import Mysql

ipServidor = socket.gethostbyname(socket.gethostname()) #Pega o ip do servidor
print('IP do servidor: %s' % ipServidor)
if(ipServidor == "10.20.0.5"):#Ambiente de Producao
    database = Mysql()
    database.connectHomolog()
elif(ipServidor == "10.20.0.7"):#Ambiente de Homologacao
    database = Mysql()
    database.connectHomolog()
else:
    database = Mysql()
    database.connectHomolog()

'''
Host: https://www.p-soc.com.br/WSSoc/services/LicencaMedicaWs
Wsdl: https://www.p-soc.com.br/WSSoc/services/LicencaMedicaWs?wsdl

O ambiente é o www.p-soc.com.br/WebSoc/
Configurei inicialmente o ambiente da MANSERV INVESTIMENTOS:

Identificação
Username: 529768
Chave de Acesso/Password: b81efe0d7ebd94b
Código da Empresa Principal: 423
Código Responsável: 213
'''
'''
CODIGO EMPRESA SOCGED
268104	BASE TREINAMENTO NUCLEO	nucleoadm	                        27.692.665/0001-60
423	    GRS+Núcleo de Saúde Empresarial Ltda	nucleoadm	        01.510.209/0001-68
529765	LSI - ADMINISTRACAO E SERVICOS S/A	nucleoadm	            58.034.315/0001-30
529766	LSI - LOGISTICA S/A	nucleoadm	                            04.057.495/0001-46
529769	MANSERV FACILITIES LTDA	nucleoadm	                        20.707.884/0004-79
529768	MANSERV INVESTIMENTOS E PARTICIPACOES S/A	nucleoadm	    11.596.852/0001-00
529759	MANSERV MONTAGEM E MANUTENÇÃO LTDA	nucleoadm	            54.183.587/0002-21

'''
def consultaCodFuncAPI(cpfPaciente): #Cadastro de Funcionarios (Por Empresa)
    print('Entrou na funcao consultaCodFuncAPI')
    codEmpresa = 529759    
    while codEmpresa < 529770:
        print('Entrou no While')
        url = "{'empresa':'529765','codigo':'23402','chave':'917fa0f2b70d8a6fd02b','tipoSaida':'txt','cpf':'"+str(cpfPaciente)+"','empresaTrabalho':'"+str(codEmpresa)+"','parametroData':'0'}"
        print("Chamando a API pela URL: %s" % url)
        response = urllib.request.urlopen(urlAPI+url)        
        rowArq = str(response.read().decode("latin-1", errors='replace'))

        
        
        count = 0
        print("Quantidade de linhas de response %s" % str(len(rowArq)))
        if(len(rowArq) > 242):            
            try:                
                #rowArq = re.findall(r".+?(?<=;)", rowArq.upper()) #Pega todos os dados da linha
                row = re.findall(r".+?(?<=;)", rowArq.upper()) #Pega somente o codigo do Funcionario
                codFunc = re.findall(r"\d+(?=;)", row[22])
                
                return codFunc[0],(codEmpresa)
            except Exception as e:
                print(e)
                sys.exit()
                
        if codEmpresa == 529759:
            codEmpresa += 6
        elif codEmpresa == 529766:
            codEmpresa += 2
        else:
            codEmpresa += 1

def consultaAtestadoAPI(codFuncionario, codEmpresa): #Licença Médica - Consulta em Lote
    print('Entrou na funcao consultaAtestadoAPI')
    print('Entrou no While')
    url = "{'empresa':'"+str(codEmpresa)+"','codigo':'11401','chave':'9246eb8610d571d99a95','tipoSaida':'txt','listaFuncionarios':'"+str(codFuncionario)+"','dataInicio':'','dataFim':''}"
    print("Chamando a API pela URL: %s" % url)
    response = urllib.request.urlopen(urlAPI+url)        
    rowArq = str(response.read().decode("latin-1", errors='replace'))
    count = 0
    print("Quantidade de linhas de response %s" % str(len(rowArq)))
    print(rowArq)
    if(len(rowArq) > 1):
        try:                
            #rowArq = re.findall(r".+?(?<=;)", rowArq.upper()) #Pega todos os dados da linha
            rows = re.findall(r".+", rowArq.upper()) #Pega somente o codigo do Funcionario
            query = ''
            for row in rows:
                if "ABONADO;ACIDENTETRAJETO;" in row: continue;
                rows = re.findall(r".*?;", row.upper()) #Pega somente o codigo do Funcionario                
                if query == "":                   
                    query = r"INSERT INTO `historicoAtestado_temp`(`ABONADO`,`CIDCONTESTADO`,`CODIGOEMPRESAFUNCIONARIO`,`CODIGOFUNCIONARIO`,`CPFFUNCIONARIO`,`DATAFIMAFASTAMENTO`,`DATAINICIOAFASTAMENTO`,`AFASTAMENTOHORAS`) VALUES ('"+str(rows[0])+"', '"+str(rows[2])+"', '"+str(rows[4])+"', '"+str(rows[5])+"', '"+str(rows[21])+"', '"+str(datetime.strptime(str(rows[23].replace(';','')), '%d/%m/%Y'))+"', '"+str(datetime.strptime(str(rows[24].replace(';','')), '%d/%m/%Y'))+"', '"+str(rows[37])+"')"
                else:
                    query += r",('"+str(rows[0])+"', '"+str(rows[2])+"', '"+str(rows[4])+"', '"+str(rows[5])+"', '"+str(rows[21])+"', '"+str(datetime.strptime(str(rows[23].replace(';','')), '%d/%m/%Y'))+"', '"+str(datetime.strptime(str(rows[24].replace(';','')), '%d/%m/%Y'))+"', '"+str(rows[37])+"')"
            print(query)
            query = query.replace(';','')
            database.InsertMysql(query)
            #return codFunc[0],codEmpresa
        except Exception as e:
            print('Exception: %s'%(e))
            sys.exit()
            
def run(cpf):
    global urlAPI
    urlAPI = 'https://ws1.soc.com.br/WebSoc/exportadados?parametro='   
    query = 'SELECT * FROM atestadosmedicos where status = 1' ## Query de producao
    query = f'SELECT * FROM atestadosmedicos where cpfPaciente = {cpf}' ## Query de Homologacao
    res = database.selectMysql(query)
    print(res)
    cpfPaciente = res[0][23]
    print('Detalhes do atestados \n%s' % str(res[0]))
    codFuncionario, codEmpresa = consultaCodFuncAPI(cpfPaciente)
    print('Codigo do Funcionario %s' % codFuncionario)
    consultaAtestadoAPI(codFuncionario, codEmpresa)
    {'empresa':'529759','codigo':'11401','chave':'9246eb8610d571d99a95','tipoSaida':'txt','listaFuncionarios':'212714','dataInicio':'','dataFim':''}
            
if __name__ == "__main__":
    urlAPI = 'https://ws1.soc.com.br/WebSoc/exportadados?parametro='   
    query = 'SELECT * FROM atestadosmedicos where status = 1' ## Query de producao
    #query = f'SELECT * FROM atestadosmedicos where idatestadosmedicos = {config.id} ' ## Query de Homologacao
    res = database.selectMysql(query)
    print(res)
    cpfPaciente = res[0][23]
    print('Detalhes do atestados \n%s' % str(res[0]))
    codFuncionario, codEmpresa = consultaCodFuncAPI(cpfPaciente)
    print('Codigo do Funcionario %s' % codFuncionario)
    consultaAtestadoAPI(codFuncionario, codEmpresa)
    {'empresa':'529759','codigo':'11401','chave':'9246eb8610d571d99a95','tipoSaida':'txt','listaFuncionarios':'212714','dataInicio':'','dataFim':''}

'''
Código	Nome	Unidade	Setor	Cargo	Matrícula	Situação
0000212714	JOSE HIGOR DA SILVA CANDIDO	02.01.0399.013 ENELMICONSTRUÇÃODESONÁREA6SP	OPERACIONAL	AUXILIAR LINHA MORTA	214129	Ativo

Data	Tipo	    Médico / Responsável	Enferm.	Licença	Receita	Acid.	Aso	Encam.	Exames	Resultado
15/02/2022	  Licença Médica  	   	-  	Sim  	Não  	Não  	-  	Não  	Não  	Não  K01
06/01/2022	  Licença Médica  	   	-  	Sim  	Não  	Não  	-  	Não  	Não  	Não  
22/12/2021	  Licença Médica  	   	-  	Sim  	Não  	Não  	-  	Não  	Não  	Não  
20/12/2021	  Licença Médica  	   	-  	Sim  	Não  	Não  	-  	Não  	Não  	Não  
26/11/2021	  Licença Médica  	   	-  	Sim  	Não  	Não  	-  	Não  	Não  	Não  
29/10/2021	  Licença Médica  	   	-  	Sim  	Não  	Não  	-  	Não  	Não  	Não  
16/07/2021	  Licença Médica  	   	-  	Sim  	Não  	Não  	-  	Não  	Não  	Não  
'''

{'empresa':'529769','codigo':'11401','chave':'9246eb8610d571d99a95','tipoSaida':'txt','listaFuncionarios':'4546636','dataInicio':'','dataFim':''}