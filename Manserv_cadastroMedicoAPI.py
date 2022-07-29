#pip install selenium install mysql-connector-python==8.0.21 install pandas install regex install urllib3 install unidecode install requests
##############################| IMPORTACAO DE BIBLIOTECAS |##############################
import os, io, sys
import glob
import time as t                                                             # Adicionar tempo para espera
import mysql.connector as mysql                                         # Biblioteca de MYSQL
from mysql.connector import errorcode                                   # Biblioteca de MYSQL
from datetime import datetime, date, time, timedelta                    # Biblioteca de data
import pandas as pd                                                     # Biblioteca de data Adicionar dias
import re                                                               # Biblioteca de REGEX
#from urllib3.packages.six import b
from urllib.request import urlopen                                      # Requisicao de API
import json
import urllib.request
from unidecode import unidecode
import socket
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
##############################| VARIAVEIS GLOBAIS |##############################
##############################| AMBIENTE MANSERV |##############################
ipServidor = socket.gethostbyname(socket.gethostname()) #Pega o ip do servidor
print(ipServidor)
if(ipServidor == "10.20.0.5"):#Ambiente de Producao
    conn = mysql.connect(host="frotaleveprod.cqth4ctrsht2.us-east-1.rds.amazonaws.com", user="sys.atestadosprd", passwd="Syp@7812!66K", db="atestadosprd") #Ambiente de PRODUCAO
elif(ipServidor == "10.20.0.7"):#Ambiente de Homologacao
    conn = mysql.connect(host="frotaleve.cqth4ctrsht2.us-east-1.rds.amazonaws.com", user="sys.atestadosdev", passwd="Js*23676@3", db="atestadosdev") #Ambiente de Homologacao
#conn = mysql.connect(host="frotaleve.cqth4ctrsht2.us-east-1.rds.amazonaws.com", user="sys.atestadosdev", passwd="Js*23676@3", db="atestadosdev") #Ambiente de Homologacao
cursor = conn.cursor()
cursor.execute("SET max_execution_time = 999;")
##############################| AMBIENTE QUAESTUM |##############################
connLog = mysql.connect(host="3.231.63.96", user="root", passwd="T458y8Y8bTLo", db="quaestum_atestados") #Ambiente de PRODUCAO
cursorLog = connLog.cursor()
cursorLog.execute("SET max_execution_time = 999;")

connatestadosDev = mysql.connect(host="3.231.63.96", user="root", passwd="T458y8Y8bTLo", db="atestadosdev") #Ambiente de PRODUCAO
cursoratestadosDev = connatestadosDev.cursor()
cursoratestadosDev.execute("SET max_execution_time = 999;")


global driver;
global dirDownload;

def baixaRelatorio():    
    url = "https://ws1.soc.com.br/WebSoc/exportadados?parametro={%27empresa%27:%27423%27,%27codigo%27:%2714617%27,%27chave%27:%2773c8e84343f193645e7c%27,%27tipoSaida%27:%27csv%27,%27ativo%27:%271%27}"
    response = urllib.request.urlopen(url)    
    rowArq = re.findall(r'.*\n', str(response.read().decode("latin-1", errors='replace')))
    
    count = 0
    for line in rowArq:
        count += 1
        print(count)
        try:
            if(count > -1):
                codigo = ""
                rowArq = re.findall(r".+?(?<=;)", line.upper())                
                
                if rowArq[4].upper() == "MÃ©DICO;" or rowArq[4].upper() == ";" or rowArq[4].upper() == "M\\XC3\\XA9DICO;":                                        
                    codPessoa = rowArq[1].upper(); codPessoa = codPessoa.replace("'", "").replace('"', '').replace(';', '')
                    nome = rowArq[2].upper(); nome = nome.replace("'", "").replace('"', '').replace(';', '')
                    if(len(nome)<2): continue                    
                    regxCodigo = re.findall(r"\d+", rowArq[23].upper())            
                    for numerosCodigo in regxCodigo:
                        codigo += numerosCodigo    
                    if(len(codigo)<2): continue
                    uf = rowArq[24].upper().replace("'", "").replace('"', '').replace(';', '')
                    
                    query = " Select * from medicoCRM where crm = '"+codigo+"' and nome = '"+nome+"' and uf = '"+uf+"'"                    
                    for result in cursor.execute(query, multi=True):                            
                        try:
                            rowBD = result.fetchall()                                       
                            if len(rowBD) < 1:
                                tpo = 'Temp'
                            else:
                                tpo = ''
                        except Exception as e:
                            print(e)
                            tpo = ""                    
                    if tpo == 'Temp':
                        query = " Select * from medicoCRO where cro = '"+codigo+"' and nome = '"+nome+"' and uf = '"+uf+"'"     
                        for result in cursor.execute(query, multi=True):
                            try:
                                rowBD = result.fetchall()
                                if len(rowBD) < 1:
                                    tpo = 'Temp'
                                else:
                                    tpo = ''
                            except Exception as e:
                                print(e)
                                tpo = ""                    
                    if tpo == "Temp":
                        primeiroNome = re.findall('^.+?(?=\s)', nome)
                        try:
                            primeiroNome[0] = re.sub('^\s+','',primeiroNome[0])
                            if len(primeiroNome[0]) < 4:
                                query = r"INSERT IGNORE INTO medicoCRM   (nome, crm,uf, cd_pessoa) VALUES ('"+nome+"', '"+codigo+"', '"+uf+"', '"+codPessoa+"');"  #Buscar todas as tabelas do Banco de Dados                                
                                cursor.execute(query)
                                conn.commit()
                                cursoratestadosDev.execute(query)
                                connatestadosDev.commit()
                                continue
                            chamaAPIDentista = "https://website.cfo.org.br/profissionais-cadastrados/?cro=Todos&categoria=todas&especialidade=todas&inscricao="+codigo+"&nome="+unidecode(primeiroNome[0])+"+"                            
                            my_request = urllib.request.urlopen(chamaAPIDentista)
                            my_HTML = my_request.read().decode("utf8")
                        except Exception as e:
                            print("Erro na verificacao da API de DENTISTA: %s"%(e))
                            query = r"INSERT IGNORE INTO medicoCRM   (nome, crm,uf, cd_pessoa) VALUES ('"+nome+"', '"+codigo+"', '"+uf+"', '"+codPessoa+"');"  #Buscar todas as tabelas do Banco de Dados                            
                            cursor.execute(query)
                            conn.commit()
                            cursoratestadosDev.execute(query)
                            connatestadosDev.commit()
                            continue
                        achou  = re.findall(codigo, my_HTML)
                        if len(achou) > 0:
                            tpo = 'CRO'
                        else:
                            tpo = 'CRM'
                        query = r"INSERT IGNORE INTO medico"+ str(tpo) +"  (nome, "+str(tpo)+",uf, cd_pessoa) VALUES ('"+str(nome)+"', '"+str(codigo)+"', '"+str(uf)+"', '"+str(codPessoa)+"');"  #Buscar todas as tabelas do Banco de Dados                        
                        cursor.execute(query)
                        conn.commit()
                        cursoratestadosDev.execute(query)
                        connatestadosDev.commit()
                updateLog(count,idlog_integracao)                
        except Exception as e:
            print(e)
            sys.exit()
def insertLog():
    #Insere a execucao na tabela log_integracao
    query = "INSERT INTO log_integracao (descricao, local) values ('INTEGRACAO MEDICO', '"+ipServidor+"');"  #Buscar todas as tabelas do Banco de Dados
    cursorLog.execute(query)
    connLog.commit()
    
    cod = ""
    #Busca o ultimo registro incluido para pegar o idlog_integracao
    query = "Select idlog_integracao from log_integracao order by idlog_integracao DESC limit 1"  #Buscar todas as tabelas do Banco de Dados
    for result in cursorLog.execute(query, multi=True):
        rowBD = result.fetchall()        
        cod = rowBD[0][0]        
    return cod
def updateLog(qtd,id):
    #Insere a execucao na tabela log_integracao
    query = r"Update log_integracao set qtd = %s, dtLastUpdate = NOW() where idlog_integracao = %s"%(qtd,id)  #Buscar todas as tabelas do Banco de Dados    
    cursorLog.execute(query)
    connLog.commit()
if __name__ == "__main__":
    idlog_integracao = insertLog()
    print(idlog_integracao)
    baixaRelatorio()