#pip3 install chromedriver-binary==95.0.4638.54.0 install selenium install mysql-connector-python==8.0.21 install pandas install regex install urllib3 install unidecode
##############################| IMPORTACAO DE BIBLIOTECAS |##############################
import os, io, sys
import glob
'''
from selenium import webdriver                                          # Interacao com a tela de navegador
import chromedriver_binary                                              # Adds chromedriver binary to path
from selenium.webdriver.common.keys import Keys                         # Comandos de SendKeys e Click
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
'''
import time as t                                                             # Adicionar tempo para espera
import mysql.connector as mysql                                         # Biblioteca de MYSQL
from mysql.connector import errorcode                                   # Biblioteca de MYSQL
from datetime import datetime, date, time, timedelta                    # Biblioteca de data
import pandas as pd                                                     # Biblioteca de data Adicionar dias
import re                                                               # Biblioteca de REGEX
#from urllib3.packages.six import b
import requests
import urllib.request		#pip install concat("urllib", number of current version)
from unidecode import unidecode
import ssl

##############################| VARIAVEIS GLOBAIS |##############################
ssl._create_default_https_context = ssl._create_unverified_context
conn = mysql.connect(host="frotaleve.cqth4ctrsht2.us-east-1.rds.amazonaws.com", user="sys.atestadosdev", passwd="Js*23676@3", db="atestadosdev")       #Ambiente de PRODUCAO
cursor = conn.cursor()
cursor.execute("SET SESSION MAX_EXECUTION_TIME=99999")

global driver;
global dirDownload;


def baixaRelatorio():
    try:
#######################################| LOGIN NO SOC |#######################################
        options = Options()
        #options.add_argument("--headless")
        #options.headless = True
        options.add_argument("--window-size=1280,720")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        options.add_experimental_option("prefs", {
            "download.default_directory": dirDownload,
            "download.Prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        driver = webdriver.Chrome(chrome_options=options)#Inicia o driver para abrir a janela do Chrome
        driver.maximize_window()
        ##### Login e senha
        driver.get("https://sistema.soc.com.br/WebSoc/")#Vai para o endereco do SOC    
        elem = driver.find_element_by_id("usu"); elem.clear(); elem.send_keys("thideki");
        elem = driver.find_element_by_id("senha"); elem.clear(); elem.send_keys("abc123**5795123");    
        ##### Inserindo ID
        driver.find_element_by_xpath('//*[@value="6"]').click()
        driver.find_element_by_xpath('//*[@value="4"]').click()
        driver.find_element_by_xpath('//*[@value="6"]').click()
        driver.find_element_by_xpath('//*[@value="4"]').click()
        driver.find_element_by_xpath('//*[@id="bt-entrar-0"]/button').click()
#######################################| QUADRO DE AVISO |#######################################
        try:
            t.sleep(2)
            try:
                driver.switch_to.frame(1)  #Muda o Frame para a nova tela
            except:
                pass
            driver.find_element_by_xpath('/html/body/div[11]/div[2]/p/input').click()
            driver.find_element_by_xpath('/html/body/div[11]/div[2]/p/span/a').click()
        except:
            print('SEM QUADRO DE AVISO')
            pass
#######################################| MENSAGEM DE ANIVERSARIO |#######################################
        try:
            t.sleep(2)
            try:
                driver.switch_to.frame(1)  #Muda o Frame para a nova tela
            except:
                pass
            driver.find_element_by_xpath('//*[@id=\"idaniversario\"]/div[1]/a[1]/img').click()        
        except:
            print('SEM Aniversario')
            pass
#######################################| BUSCA EXPORTA DADOS |#######################################
        t.sleep(2)
        driver.switch_to_default_content()
        driver.execute_script('document.querySelector("#cod_programa").setAttribute("value", "733")') #Busca o Relatorio EXPORTA DADOS
        driver.execute_script('document.querySelector("#btn_programa").click()') #Clica para buscar 
#######################################| SELECIONAR RELATORIO |#######################################
        t.sleep(1)
        try:
            driver.switch_to.frame(1)  #Muda o Frame para a nova tela
        except:
            pass
        #elem = driver.find_element_by_xpath('//*[@id="sis165"]/fieldset/p/input'); elem.clear(); elem.send_keys("Usuários Médicos"); #Busca o relatorio Cadastro Pessoa/Usuarios
        elem = driver.find_element_by_xpath('//*[@id="sis165"]/fieldset/p/input'); elem.clear(); elem.send_keys("Cadastro Pessoa/Usuarios"); #Busca o relatorio Cadastro Pessoa/Usuarios
        t.sleep(1)
        driver.find_element_by_xpath('//*[@id="sis165"]/fieldset/p/a/img').click() #Clica na lupa para buscar
        t.sleep(1)
        driver.find_element_by_xpath('//*[@id="listaProgramas"]/td/table/tbody/tr/td/div/a/img').click() #Clica no Relatorio
        t.sleep(1)    
        ddelement= Select(driver.find_element_by_xpath('//*[@id="tipoSaida"]'))
        ddelement.select_by_value('txt') #Seleciona a opcao de saide de TXT    
        t.sleep(1)    
        driver.find_element_by_xpath('//*[@id="coluna3"]/a/img').click() #Faz o download do arquivo
        t.sleep(10) 
    except AssertionError as error1:
        print('Erro no MYSQL')
        print(error1)
        print(sys.error1())

def importaRelatorio():#Usuários Médicos
#######################################| IMPORTAR OS DADOS DO RELATORIO |#######################################
    #######################################| BUSCA O ULTIMO REGISTRO |#######################################    
    query = "Select * from medicoCRM order by CAST(cd_pessoa AS UNSIGNED) DESC limit 1"
    for result in cursor.execute(query, multi=True):
        try:
            rowBD = result.fetchall()
            cd_pessoa = rowBD[0][5]            
        except:
            print("BD - Não possui registro para ser capturado")
            cd_pessoa = 1
    count = 1
    list_of_files = glob.glob(dirDownload+str("/*")) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)
    with open(latest_file, 'r') as f:
        next(f)
        for line in f:
            if count > int(cd_pessoa) :
                #print(line)
                codigo = ""
                rowArq = re.findall(r".+?(?<=;)", line.upper())
                #print(rowArq)
                codPessoa = rowArq[0].upper(); codPessoa = codPessoa.replace("'", "").replace('"', '').replace(';', '')
                nome = rowArq[1].upper(); nome = nome.replace("'", "").replace('"', '').replace(';', '')
                #print(nome)
                regxCodigo = re.findall(r"\d+", rowArq[4].upper())            
                for numerosCodigo in regxCodigo:
                    codigo += numerosCodigo
                #print(codigo)
                tpo = rowArq[3].upper().replace(';', '')
                uf = rowArq[5].upper().replace("'", "").replace('"', '').replace(';', '')
                if tpo == "CRM":
                    #print('CRM')
                    query = r"INSERT IGNORE INTO medico"+ tpo +"  (nome, "+tpo+",uf, cd_pessoa) VALUES ('"+nome+"', '"+codigo+"', '"+uf+"', '"+codPessoa+"');"  #Buscar todas as tabelas do Banco de Dados
                    print(query)
                    cursor.execute(query)
                    conn.commit()
                elif tpo == "CRO":
                    #print('CRO')
                    query = r"INSERT IGNORE INTO medico"+ tpo +"  (nome, "+tpo+",uf, cd_pessoa) VALUES ('"+nome+"', '"+codigo+"', '"+uf+"', '"+codPessoa+"');"  #Buscar todas as tabelas do Banco de Dados
                    print(query)
                    cursor.execute(query)
                    conn.commit()
                #break
                count = int(codPessoa)
            else:
                rowArq = re.findall(r".+?(?<=;)", line.upper())
                #print(rowArq)                        
                codPessoa = rowArq[0].upper(); codPessoa = codPessoa.replace("'", "").replace('"', '').replace(';', '')
                print(codPessoa)
                count =  int(codPessoa)
def importaRelatorio2():#Cadastro Pessoa/Usuarios
#######################################| IMPORTAR OS DADOS DO RELATORIO |#######################################
    #######################################| BUSCA O ULTIMO REGISTRO |#######################################        
    list_of_files = glob.glob(dirDownload+str("/*.txt")) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    
    with open(latest_file, encoding = "ISO-8859-1") as f:
        next(f)
        count = 0        
        for line in f:
            count += 1
            print(count)
            try:
                if(count > 341):
                    codigo = ""
                    rowArq = re.findall(r".+?(?<=;)", line.upper())
                    #print(rowArq[4].upper())
                    if rowArq[4].upper() == "MÃ©DICO;" or rowArq[4].upper() == ";":
                        #print(rowArq)
                        codPessoa = rowArq[1].upper(); codPessoa = codPessoa.replace("'", "").replace('"', '').replace(';', '')
                        nome = rowArq[2].upper(); nome = nome.replace("'", "").replace('"', '').replace(';', '')
                        if(len(nome)<2): continue
                        #print(nome)
                        regxCodigo = re.findall(r"\d+", rowArq[23].upper())            
                        for numerosCodigo in regxCodigo:
                            codigo += numerosCodigo
                        #print(codigo)
                        if(len(codigo)<2): continue
                        uf = rowArq[24].upper().replace("'", "").replace('"', '').replace(';', '')
                        
                        query = " Select * from medicoCRM where crm = '"+codigo+"' and nome = '"+nome+"'"
                        print(query)
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
                            query = " Select * from medicoCRO where cro = '"+codigo+"' and nome = '"+nome+"'"
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
                                    query = r"INSERT IGNORE INTO medicoTemp  (nome, codigo,uf, cd_pessoa) VALUES ('"+nome+"', '"+codigo+"', '"+uf+"', '"+codPessoa+"');"  #Buscar todas as tabelas do Banco de Dados
                                    cursor.execute(query)
                                    continue                                
                                my_request = urllib.request.urlopen(r"https://website.cfo.org.br/profissionais-cadastrados/?cro=Todos&categoria=todas&especialidade=todas&inscricao="+codigo+"&nome="+unidecode(primeiroNome[0])+"+")                                
                                my_HTML = my_request.read().decode("utf8")
                            except Exception as e:
                                print(e)
                                print('INSERT medicoTemp2')
                                query = r"INSERT IGNORE INTO medicoTemp  (nome, codigo,uf, cd_pessoa) VALUES ('"+nome+"', '"+codigo+"', '"+uf+"', '"+codPessoa+"');"  #Buscar todas as tabelas do Banco de Dados
                                cursor.execute(query)
                                continue
                            achou  = re.findall(codigo, my_HTML)                            
                            if len(achou) > 0:
                                tpo = 'CRO'
                            else:
                                tpo = 'CRM'
                            print(tpo)
                            
                            #print('CRM')
                            query = r"INSERT IGNORE INTO medico"+ tpo +"  (nome, "+tpo+",uf, cd_pessoa) VALUES ('"+nome+"', '"+codigo+"', '"+uf+"', '"+codPessoa+"');"  #Buscar todas as tabelas do Banco de Dados
                            #print(query)
                            cursor.execute(query)
                            conn.commit()
            except Exception as e:
                print(e)
                '''
                while "A"=="A":
                    try:
                        conn = mysql.connect(host="frotaleve.cqth4ctrsht2.us-east-1.rds.amazonaws.com", user="sys.atestadosdev", passwd="Js*23676@3", db="atestadosdev")       #Ambiente de PRODUCAO
                        cursor = conn.cursor()
                        cursor.execute("SET SESSION MAX_EXECUTION_TIME=99999")
                        query = r"INSERT IGNORE INTO medico"+ tpo +"  (nome, codigo,uf, cd_pessoa) VALUES ('"+nome+"', '"+codigo+"', '"+uf+"', '"+codPessoa+"');"  #Buscar todas as tabelas do Banco de Dados
                        #print(query)
                        cursor.execute(query)
                        conn.commit()
                        break
                    except:
                        print(count)
                '''
                sys.exit()
            
def test():
    list_of_files = glob.glob(dirDownload+str("/*")) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    print (latest_file)
def test1():
    codigo = "123123"
    my_request = urllib.request.urlopen("https://website.cfo.org.br/profissionais-cadastrados/?cro=Todos&categoria=todas&especialidade=todas&inscricao="+codigo+"&nome="+nome+"")
    my_HTML = my_request.read().decode("utf8")
    achou  = re.findall(codigo, my_HTML)
    print(my_HTML)
    print(achou)
    if len(achou) > 0:
        tpo = 'cro'
    else:
        tpo = 'crm'
    print(tpo)
def test2():
    nome = "João Pedro"
    primeiroNome = re.findall('^.+?(?=\s)', nome)
    print(primeiroNome)
    print(primeiroNome[0])
    
if __name__ == "__main__":
    dirDownload = r"C:\quaestum\robo\cadastroMedico" #Windows
    dirDownload = r"/home/quaestum/robo_soc" #LINUX
    #baixaRelatorio()
    #t.sleep(30)
    importaRelatorio2()
    #test2()