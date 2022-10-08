#pip install chromedriver-binary ==95.0.4638.69 install selenium install mysql-connector-python==8.0.21 install pandas install regex install urllib3 install unidecode
##############################| IMPORTACAO DE BIBLIOTECAS |##############################
import os, io, sys
import subprocess
import glob
from selenium import webdriver                                          # Interacao com a tela de navegador
import chromedriver_binary                                              # Adds chromedriver binary to path
from selenium.webdriver.common.keys import Keys                         # Comandos de SendKeys e Click
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time as t                                                             # Adicionar tempo para espera
import mysql.connector as mysql                                         # Biblioteca de MYSQL
from mysql.connector import errorcode                                   # Biblioteca de MYSQL
from datetime import datetime, date, time, timedelta                    # Biblioteca de data
import pandas as pd                                                     # Biblioteca de data Adicionar dias
import re                                                               # Biblioteca de REGEX
from urllib3.packages.six import b
import requests
import urllib.request		#pip install concat("urllib", number of current version)
from unidecode import unidecode

##############################| VARIAVEIS GLOBAIS |##############################
#connhomolog = mysql.connect(host="frotaleveprod.cqth4ctrsht2.us-east-1.rds.amazonaws.com", user="sys.atestadosdev", passwd="Js*23676@3", db="atestadosdev")       #Ambiente de Homologacao
connprd = mysql.connect(host="frotaleveprod.cqth4ctrsht2.us-east-1.rds.amazonaws.com", user="sys.atestadosprd", passwd="Syp@7812!66K", db="atestadosprd")       #Ambiente de Homologacao
conn = mysql.connect(host="3.231.63.96", user="root", passwd="T458y8Y8bTLo", db="atestadosdev")       #Ambiente de PRODUCAO
cursorprd = connprd.cursor()
cursor = conn.cursor()
#cursorPRD = conn.cursor()
cursor.execute("SET SESSION MAX_EXECUTION_TIME=99999")
cursorprd.execute("SET SESSION MAX_EXECUTION_TIME=99999")

global driver;
global dirDownload;

def updateChromeDriver():
    #Verifica a versão do Chrome
    output = subprocess.check_output(
        r'wmic datafile where name="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" get Version /value',shell=True
    )
    #Insere a versão em uma variavel
    versaoChrome = output.decode('utf-8').strip().replace('Version=','')
    #Realiza a instalação do chromedriver na versão do computador
    os.system('cmd /c "cd C:\\Users\\Hideki\\AppData\\Local\\Programs\\Python\\Python39\\Scripts && pip3 install chromedriver-binary=="'+versaoChrome)
    print(versaoChrome)
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
        elem = driver.find_element_by_id("senha"); elem.clear(); elem.send_keys("abc123**57951234");    
        ##### Inserindo ID
        driver.find_element_by_xpath('//*[@value="3"]').click()
        driver.find_element_by_xpath('//*[@value="7"]').click()
        driver.find_element_by_xpath('//*[@value="3"]').click()
        driver.find_element_by_xpath('//*[@value="9"]').click()
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
        t.sleep(30) 
    except AssertionError as error1:
        print('Erro no MYSQL')
        print(error1)
        print(sys.error1())


def importaRelatorio2():#Cadastro Pessoa/Usuarios
#######################################| IMPORTAR OS DADOS DO RELATORIO |#######################################
    #######################################| BUSCA O ULTIMO REGISTRO |#######################################        
    list_of_files = glob.glob(dirDownload+str("/*")) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)    
    with open(latest_file, 'r') as f:
        next(f)
        count = 0        
        for line in f:
            count += 1
            print(count)
            try:
                if(count > 1133):
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
                            #print("Medico")
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
                            #print("DENTISTA")
                            primeiroNome = re.findall('^.+?(?=\s)', nome)
                            try:
                                primeiroNome[0] = re.sub('^\s+','',primeiroNome[0])
                                if len(primeiroNome[0]) < 4:
                                    #query = r"INSERT IGNORE INTO medicoTemp  (nome, codigo,uf, cd_pessoa) VALUES ('"+nome+"', '"+codigo+"', '"+uf+"', '"+codPessoa+"');"  #Buscar todas as tabelas do Banco de Dados
                                    #cursor.execute(query)
                                    continue
                            #print("OK")
                                #my_request = urllib.request.urlopen(r"https://website.cfo.org.br/profissionais-cadastrados/?cro=Todos&categoria=todas&especialidade=todas&inscricao="+codigo+"&nome="+unidecode(primeiroNome[0])+"+")
                                #my_HTML = my_request.read().decode("utf8")
                            except:
                                #query = r"INSERT IGNORE INTO medicoTemp  (nome, codigo,uf, cd_pessoa) VALUES ('"+nome+"', '"+codigo+"', '"+uf+"', '"+codPessoa+"');"  #Buscar todas as tabelas do Banco de Dados
                                #cursor.execute(query)
                                continue
                            my_HTML =""
                            achou  = re.findall(codigo, my_HTML)
                            #print("OK")
                            if len(achou) > 0:
                                tpo = 'CRO'
                            else:
                                tpo = 'CRM'
                            #print(tpo)
                            
                            #print('CRM')
                            query = r"INSERT IGNORE INTO medico"+ tpo +"  (nome, "+tpo+",uf, cd_pessoa) VALUES ('"+nome+"', '"+codigo+"', '"+uf+"', '"+codPessoa+"');"  #Buscar todas as tabelas do Banco de Dados
                            #print(query)
                            cursor.execute(query)
                            conn.commit()
                            cursorprd.execute(query)
                            connprd.commit()
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
    dirDownload = r"C:\quaestum\robo\cadastroMedico"
    #baixaRelatorio()
    #time.sleep(40)
    importaRelatorio2()
    #test2()