#pip install chromedriver-binary == 94.0.4606.61 install selenium install mysql-connector-python==8.0.21 install pandas install regex install urllib3
##############################| IMPORTACAO DE BIBLIOTECAS |##############################
import os, io, sys
import glob
import time as t                                                             # Adicionar tempo para espera
import mysql.connector as mysql                                         # Biblioteca de MYSQL
from mysql.connector import errorcode                                   # Biblioteca de MYSQL
from datetime import datetime, date, time, timedelta                    # Biblioteca de data
#import pandas as pd                                                     # Biblioteca de data Adicionar dias
import re                                                               # Biblioteca de REGEX
#from urllib3.packages.six import b
from urllib.request import urlopen                                      # Requisicao de API
import json                                                             # Leitura de JSON
import ssl
import certifi
import socket
##############################| VARIAVEIS GLOBAIS |##############################
ipServidor = socket.gethostbyname(socket.gethostname()) #Pega o ip do servidor
print(ipServidor)
if(ipServidor == "10.20.0.5"):#Ambiente de Producao
    conn = mysql.connect(host="frotaleveprod.cqth4ctrsht2.us-east-1.rds.amazonaws.com", user="sys.atestadosprd", passwd="Syp@7812!66K", db="atestadosprd") #Ambiente de PRODUCAO
elif(ipServidor == "10.20.0.7"):#Ambiente de Homologacao
    conn = mysql.connect(host="frotaleve.cqth4ctrsht2.us-east-1.rds.amazonaws.com", user="sys.atestadosdev", passwd="Js*23676@3", db="atestadosdev2") #Ambiente de Homologacao
#conn = mysql.connect(host="frotaleve.cqth4ctrsht2.us-east-1.rds.amazonaws.com", user="sys.atestadosdev", passwd="Js*23676@3", db="atestadosdev") #Ambiente de Homologacao

cursor = conn.cursor()
cursor.execute("SET SESSION MAX_EXECUTION_TIME=99999")

global driver;
global dirDownload;


def atualizaUsuario():#Usuários Médicos
#######################################| IMPORTAR OS DADOS DO RELATORIO |#######################################
    url = "https://web.manserv.com.br/sigx/apps/dados_rhfuncs.php?chave=bdsALSnzhrNNhgtWUQKX69vZhbGqiZqtNB5gmMzQ&dataalt="
    response = urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))
    data_json = json.loads(response.read())
    #print(data_json['resultado']['list'])
    a = data_json['resultado']['list']
    #print(a)
    count = 0
    for item in a:
        if(count>-1):
            #rint(item)
            nm = ""+item['NOME']
            #print(nm)
            nm = nm.replace("'", "");
            emai = ""+str(item['EMAIL'])
            #print(emai)
            emai = emai.replace("'", "");
            nmCol = ""+item['NOMECOLIGADA']
            #print(nmCol)
            #nmCol = nmCol.replace(/'/g, "");
            dtNasc1 = item['DTNASCIMENTO']['date']
            #print(dtNasc1)
            dtNasc = dtNasc1[0:10]
            #print(dtNasc)
            query = "CALL  pro_insertUsuario('"+str(item['CHAPA'])+"','"+str(item['CPF'])+"','"+nm+"','"+emai+"','"+str(item['CODCOLIGADA'])+"','"+str(item['CODCOLIGADA'])+"','"+nmCol+"','"+str(item['STATUS'])+"','"+str(item['CODSECAO'])+"','"+str(item['ASSISTENCIA_MEDICA'])+"','"+str(item['ESTADO'])+"','"+dtNasc+"','"+str(item['AD'])+"','"  +str(item['TELEFONE1'])+"','"  +str(item['ESTADOFUNC'])+"');"
            print(query)
            cursor.execute(query)
            conn.commit()
            ''' Inserir os dados na tabela de usuariolog para criar o log de alteracoes '''
            query = "INSERT INTO usuariolog (re_usuario, cpf, nome, email, coligada_id, coligada, nome_coligada, status, ut_cc, assistencia_medica, uf, dt_nascimento, possui_ad, telefone, estadofunc,dtInsert, dtLastUpdate) values ('"+str(item['CHAPA'])+"','"+ str(item['CPF'])+"','"+ nm+"','"+ emai+"','"+ str(item['CODCOLIGADA'])+"','"+ str(item['CODCOLIGADA'])+"','"+nmCol+"','" +str(item['STATUS'])+ "','"+str(item['CODSECAO'])+"','" +str(item['ASSISTENCIA_MEDICA'])+"','"+str(item['ESTADO'])+"','" +dtNasc+"','"+str(item['AD'])+"','"+str(item['TELEFONE1'])+"','"  +str(item['ESTADOFUNC'])+"',now(), now())"

            print(query)
            cursor.execute(query)
            
            conn.commit()
        count +=1
        print(count)
    query = "Update usuario set status = 'D' where SUBSTRING(CAST(AES_DECRYPT(AES_DECRYPT(dtLastUpdate,'odiaquevem'),SHA2(`atestadosmedicos`.`id2`, 512)) AS CHAR (10000) CHARSET UTF8MB4), 1, 10) != DATE_FORMAT(Now(), \"%Y-%m-%d\")";
    print(query)
    #cursor.execute(query)
    #conn.commit()
if __name__ == "__main__":
    #dirDownload = r"C:\quaestum\robo\cadastroMedico"    
    atualizaUsuario()