from os import chdir, getcwd, listdir
from os.path import isfile
import sys
import math
import os, io, sys
import re
import json
import csv
import codecs
import time
import requests
from unidecode import unidecode
from google.cloud import vision
from google.cloud.vision_v1 import types
from datetime import datetime, date
import numpy as np 
from PIL import Image

import mysql.connector as mysql
#conn = mysql.connect(host="frotaleve.cqth4ctrsht2.us-east-1.rds.amazonaws.com", user="sys.atestadosdev", passwd="Js*23676@3", db="atestadosdev")       #Ambiente de PRODUCAO
conn = mysql.connect(host="3.231.63.96", user="root", passwd="T458y8Y8bTLo", db="atestadosdev",auth_plugin='mysql_native_password')       #Ambiente de PRODUCAO
mycursor = conn.cursor()
#mycursor.execute("SET SESSION MAX_EXECUTION_TIME=99999")

# Recebe os parametros
argumentos = sys.argv[1]
file = argumentos.split('|')[0]
nome_argumento = argumentos.split('|')[1].replace("\\", "")

# cd "/home/bitnami/htdocs/atestados_quaestum/web_services/"
# "/home/bitnami/htdocs/atestados_quaestum/storage/2021/12/01/ADRIANA MONACI DOS SANTOS MARTINS-1638381201.png | ADRIANA MONACI DOS SANTOS MARTINS"
# "C:\quaestum\Imagens\Baixados\ADRIANA MONACI DOS SANTOS MARTINS-1638381201.png | ADRIANA MONACI DOS SANTOS MARTINS"
#seleciona o diretório
# file = '../temp/Leonardo da silva Oliveira_.jpeg'

# os.remove('./resultados/resultado_txt.txt')
# os.remove('./resultados/resultado.txt')
# arquivo_txt = codecs.open('./resultados/resultado_txt.txt', 'x', 'utf-8')
# arquivo = codecs.open('./resultados/resultado.txt', 'x', 'utf-8')
# chdir('./imagens')

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/bitnami/htdocs/atestados_quaestum/web_services/functions/visionapi-manserv-681136a258f6.json'
# "C:\quaestum\Imagens\Baixados\ADRIANA MONACI DOS SANTOS MARTINS-1638381201.png | ADRIANA MONACI DOS SANTOS MARTINS"
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\quaestum\visionapi-manserv-1c5ab86eb39e.json'  #Caso for testar em Windows
client = vision.ImageAnnotatorClient()

#################################| Alterando o tamanho/formato da imagem |################################
img = Image.open(file)
height = img.size[1]
width = img.size[0]

if(height > 1000 or width > 1000):
    tamH = height / 1000
    tamW = width / 1000
    if tamH < 1: tamH = 1 
    else: tamH = int(tamH)
    if tamW < 1: tamW = 1
    else: tamW = int(tamW)
    img.thumbnail((int(height/tamH), int(width/tamW)))

newDirImg = file.split("_.")[0] + str(time.time()).split(".")[1] + ".png"
# print(file.split("_.")[0])
img.save(newDirImg)
##################################################| END |##################################################

if isfile(newDirImg):
    # print(newDirImg)
    novo_nome = unidecode(nome_argumento).upper()

    with io.open(newDirImg, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Valida se é MANUSCRITO OU TIPGRAFADO

    response2 = client.label_detection(image=image)
    labels2 = response2.label_annotations

    tipo_letras = re.search('description:\s"Handwriting"\sscore: ([01].?\d{0,18})\s', str(labels2))

    if(str(tipo_letras) == "None"):
        tipo_letras = "Tipografado"
    else:
        if(float(tipo_letras[1]) < 0.85):
            tipo_letras = "Tipografado"
        else:
            tipo_letras = "Manuscrito"
            
    response = client.text_detection(image=image)
    if(len(response.text_annotations)>0):
        text = unidecode(response.text_annotations[0].description.replace("\n", " ").replace("_", " ").upper())

        vertexList = response.text_annotations[1].bounding_poly.vertices
        centerX = 0
        centerY = 0

        for ponto in vertexList:
            centerX +=ponto.x        
            centerY +=ponto.y

        centerX /= 4
        centerY /= 4

        x0 = vertexList[0].x
        y0 = vertexList[0].y
            
        val_rotacao = 0

        if (x0 < centerX):
            if (y0 < centerY):
                val_rotacao = 0
            else:
                val_rotacao = 270
        else:
            if(y0 < centerY):
                val_rotacao = 90
            else:
                val_rotacao = 180
        
        # Procurando valor do CID
        group_cid = 2
        cid = re.search("C\.?I\.?D\.?(10)?\W?\s?:?\s?([A-Z]\s?\d{2}\.?\d?)", text)
        if (str(cid) == str('None')):
            cid = re.search("([A-Z]\.?.?\d{2}\.?\d)\s?C\.?I\.?D\.?", text)
            group_cid = 1

        if (str(cid) == str('None')):
            cid = re.search("C\.?I\.?D\.?(10)?(\W{0,2}\s?[A-Z]\.?-?\s?[\dS][\dS]\.?\s?\d?)\s|C\.?I\.?D\.?(10)?.{0,80}\s([A-Z]\.?-?\s?[\dS][\dS]\.?\s?\d?)\s", text)
            group_cid = 3

        if (str(cid) == str('None')):
            cid = re.search("C\.?I\.?D\.?(10)?(\W{0,2}\s?[A-Z1]\.?-?\s?[\dS][\dS]\.?\s?\d?)\s|C\.?I\.?D\.?(10)?.{0,80}\s([A-Z1]\.?-?\s?[\dS][\dS]\.?\s?\d?)\s", text)
            group_cid = 3

        # Procurando valor do CRM
        crm = re.findall("(CRM|RM|MS|CBM).\W{0,2}[\.\/\-]?(\d{2,8}.?\d{3})[\s\/\)]|(CRM|RM|MS|CBM).{0,20}[\s:](\d{2,8}[\.\/\-]?\d{3})[\s\/\)]", text)       
        if (len(crm) == 0): 
            crm = re.findall("(CRO|RO|MS|CBO).\W{0,2}[\.\/\-]?(\d{2,8}.?\d{3})[\s\/\)]|(CRO|RO|MS|CBO).{0,20}[\s:](\d{2,8}[\.\/\-]?\d{3})[\s\/\)]", text)            
        # crm = re.findall("(CRM|RM|MS|CBM).\W{0,2}\s?(\d{2,8}.?\d{3})\s|(CRM|RM|MS|CBM).{0,20}[\s:](\d{2,8}.?\d{3})\s", text)
        # crm = re.findall("(CRM|RM|MS)\s?:?\s?(\d{2,8}.?\d{3})\s|(CRM|RM|MS).{0,20}[\s:](\d{2,8}.?\d{3})\s", text)

        # Procurando valor dos Dias de Afastamento
        #dias = re.search("(\d{1,2}).?(\(?\s?\w{2,9}\s?\)?)?\s?.?DIAS?.?", text)
        dias = re.findall("(\d{1,2}).?(\(?\s?\w{2,9}\s?\)?)?\s?.?DIAS?.?", text)

        # Procurando valor dos Dias de Afastamento
        #dias = re.search("(\d{1,2}).?(\(?\s?\w{2,9}\s?\)?)?\s?.?DIAS?.?", text)
        #if len(dias == 0):
        #    dias = re.findall("(\d{1,2}).?(\(?\s?\w{2,9}\s?\)?)?\s?.?HORAS?.?", text)

        # Procurando valor dos Nome do Médico
        group_medico = 2
        medico = re.search("(DR\(?A?\)?)\W{1,3}\s?([A-Z]{2,12}\.?\s[A-Z]{1,12}\.?\s[A-Z]{1,12})", text)
        if (str(medico) == str('None')):
            medico = re.search("([A-Z]{2,12}?\s?[A-Z]{2,12}\s[A-Z]{2,12}).{0,3}MEDI.{0,3}(CRM|RM|MS)", text)
            group_medico = 1

        # Procurando valor da Data Consulta
        data_consulta = re.findall("\d{1,2}\/\d{2}\/\d{2,4}", text)
        group_data = 1
        if (len(data_consulta) == 0):
            data_consulta = re.findall("((\d{1,2})\s?(DE)?\s?(JANEIRO|FEVEREIRO|MARCO|MARÇO|ABRIL|MAIO|JUNHO|JULHO|AGOSTO|SETEMBRO|OUTUBRO|NOVEMBRO|DEZEMBRO)\s(DE)?\s?(\d{2,4}))", text)
            group_data = 2
        
        retorno = {}

        # Procurando Local do atendimento
        local_atendimento = re.search("((( [RP]UA )|( AV )( R ))[\w\s\,-]{1,75}\s?[-\s][A-Z]{2}[\s,])|((([RP]UA )|(AV.? )|( R ))[\w\s\,-]{1,75})", text)
        cep = re.search("(CEP:?\s)?\d{5}-?\d{3}", text)

        if(str(local_atendimento) != str('None')):
            local_atendimento = local_atendimento[0]
        else:
            local_atendimento = ''

        if(str(cep) != str('None')):
            cep = cep[0].replace(".","").replace("-","")
            cep = re.search("\d{8}", cep)
            cep = cep[0]
            url = "http://viacep.com.br/ws/"+cep+"/json/"
            try:
                response = requests.request("GET", verify=False, url=url)
                bairro = response.json()["bairro"]
                logradouro = response.json()["logradouro"]
                cidade = response.json()["localidade"]
                uf = response.json()["uf"]
            except:
                bairro = ""
                logradouro = ""
                cidade = ""
                uf = ""
        else:
            cep = ''
            bairro = ""
            logradouro = ""
            cidade = ""
            uf = ""
        retorno = {}

        # Procurando Local do atendimento
        v1 = re.findall('\WSUS', text)
        if(len(v1) == 0): v1 = re.findall('\WPREFEITURA', text)
        if(len(v1) == 0): v1 = re.findall('\WSANTA CASA', text)
        if(len(v1) == 0): v1 = re.findall('\WMINISTERI', text)
        if(len(v1) == 0): v1 = re.findall('\WPUBLIC', text)
        if(len(v1) == 0): v1 = re.findall('\WPRONTO ATENDIMENT', text)
        if(len(v1) == 0): v1 = re.findall('\WMUNICIPAL', text)
        if(len(v1) == 0): v1 = re.findall('\WESTADO', text)

        if(len(v1) == 0): 
            sus = "false"
        else:
            sus = "true"

        ###################### Tratamento da informação do CID ######################
        if (str(cid) != 'None'):
            if (group_cid == 3):
                if(str(cid[2]) == 'None'):
                    cid = cid[4]
                else:
                    cid = cid[2]
            else:
                cid = cid[group_cid]

            cid = re.sub(r'\W', '', str(cid))
            cid = cid[0].replace('5', "S").replace("1", "I") + cid[1:].replace('S', "5")
            if (len(str(cid)) == 4):
                    cid = cid[0:3] + "." + cid[-1:] 
            retorno['cid'] = cid
        else:
            retorno['cid'] = ''

        ###################### Tratamento da informação do CRM ######################
        if (len(crm) > 0):
            crm = crm[len(crm) - 1]
            if(crm[1] == ''):
                crm = crm[3].split(' ')[0]
                crm = int(crm.replace(".", ""))
            else:
                crm = crm[1].split(' ')[0]
                crm = int(crm.replace(".", ""))
            retorno['crm'] = crm
        else:
            retorno['crm'] = ''

        ###################### Tratamento da quantidade de dias ######################        
        for verifica in dias:            
            reg = 'MESE?S?.?.?.?'+str(verifica[0])            
            v1 = re.findall(reg, text)            
            try:
                
                if len(v1[0]) > 0: pass
                
            except:            
                if (str(dias) != str('None')):
                    retorno['dias'] = verifica[0]
                else:
                    retorno['dias'] = 1
        
        ###################### Tratamento do nome do Médico ######################
        '''
        if (str(medico) != str('None')):
            medico = medico[group_medico]
            medico = medico.split('ORGAO')[0]
            medico = medico.split('CIRURGI')[0]
            medico = medico.split('PEDIATRA')[0]
            medico = medico.split('ORTOPED')[0]
            medico = medico.split('MEDI')[0]
            medico = medico.split('CLINIC')[0]
            medico = medico.split('CRM')[0]
            medico = medico.split('(')[0]
            medico = medico.split('NECESSITA')[0]
            medico = medico.split('DATA')[0]
            medico = medico.split('CBM')[0]
        '''               
        #print('Verifica CRM')
        if (len(str(crm)) > 0):
            query = "SELECT nome FROM medicoCRM where crm = "+ str(crm)
            
            mycursor.execute(query)
            myresult = mycursor.fetchall()           
            for x in myresult:
                v1 = re.findall('\w+', unidecode(x[0]).upper())
                count=0
                for y in v1:                    
                    if(text.find(y) != -1): count+=1
                if count > 1:
                    medico = x[0]
                    retorno['medico'] = x[0]
                    break
                else:
                    retorno['medico'] = ''
        #print('Verifica CRO')
        if (len(str(crm)) > 0 and str(medico) == str('None')):
            query = "SELECT nome FROM medicoCRO where cro = "+ str(crm)
            
            mycursor.execute(query)
            myresult = mycursor.fetchall()           
            for x in myresult:
                v1 = re.findall('\w+', unidecode(x[0]).upper())
                count=0
                for y in v1:                    
                    if(text.find(y) != -1): count+=1
                if count > 1:
                    medico = x[0]
                    retorno['medico'] = x[0]
                    break
                else:
                    retorno['medico'] = ''
        if (len(str(crm)) < 1):
                retorno['medico'] = ''
        
        ###################### Tratamento da data da consulta ######################
        data_atual = date.today()
        ano_atual = data_atual.strftime('%y')
        if (group_data == 1):
            if (len(data_consulta) > 0):
                for data_encontrada in data_consulta:
                    data_corrigida = data_encontrada
                    if(len(data_encontrada.split('/')[0]) == 1):
                        data_corrigida = '0' + data_encontrada
                    if(int(data_corrigida[0:2]) > 31 or int(data_corrigida[3:5]) > 12 or int(data_corrigida[-2:]) > int(ano_atual)):
                        retorno['data_consulta'] = ''
                    else:
                        if(int(data_corrigida[-2:]) < 40):
                            if(len(data_corrigida) == 10):
                                d1 = data_corrigida
                                d1 = datetime.strptime(d1, "%d/%m/%Y")
                                d2 = datetime.today()
                                if (abs((d2 - d1).days) < 730):
                                    data_consulta = d1
                                    retorno['data_consulta'] = str(data_consulta.strftime("%d/%m/%Y"))
                                    # break
                                else:
                                    retorno['data_consulta'] = ""
                            elif (len(data_corrigida) == 8):
                                d1 = data_corrigida[0:6] + "20" + data_corrigida[-2:]
                                d1 = datetime.strptime(d1, "%d/%m/%Y")
                                d2 = datetime.today()
                                if (abs((d2 - d1).days) < 730):
                                    data_consulta = d1
                                    retorno['data_consulta'] = str(data_consulta.strftime("%d/%m/%Y"))
                                    # break
                                else:
                                    retorno['data_consulta'] = ''
                            else:
                                if(data_corrigida[6:8] == '20'):
                                    if(int(data_corrigida[3:5]) == 12):
                                        data_corrigida = data_corrigida[0:8] + ano_atual
                                    else:
                                        data_corrigida = data_corrigida[0:8] + str(int(ano_atual)-1)
                                else:
                                    data_corrigida = ''
                                retorno['data_consulta'] = data_corrigida
                        else:
                            retorno['data_consulta'] = ''
            else:
                retorno['data_consulta'] = ''
        else:
            if (len(data_consulta) > 0):
                data_consulta = data_consulta[0][0]
                data_consulta = data_consulta.replace("JANEIRO", "01").replace("FEVEREIRO", "02").replace("MARCO", "03").replace("ABRIL", "04").replace("MAIO", "05").replace("JUNHO", "06").replace("JULHO", "07").replace("AGOSTO", "08").replace("SETEMBRO", "09").replace("OUTUBRO", "10").replace("NOVEMBRO", "11").replace("DEZEMBRO", "12")
                data_consulta = data_consulta.replace(" ", "")
                data_consulta = data_consulta.replace("DE", "")
                if(len(data_consulta) < 8):
                    if(int(data_consulta[-4:]) > 2000):
                        data_consulta = "0" + str(data_consulta)
                data_consulta = data_consulta[0:2] + "/" + data_consulta[2:4] + "/" + data_consulta[4:8]
                if(int(data_consulta[0:2]) > 31 or int(data_consulta[3:5]) > 12 or int(data_consulta[-2:]) > int(ano_atual)):
                    retorno['data_consulta'] = ''
                else:
                    if(int(data_consulta[-2:]) < 40):
                        if (len(data_consulta) == 8):
                            d1 = data_consulta[0:6] + "20" + data_consulta[-2:]
                            d1 = datetime.strptime(d1, "%d/%m/%Y")
                            d2 = datetime.today()
                            if (abs((d2 - d1).days) < 730):
                                data_consulta = d1
                                retorno['data_consulta'] = str(data_consulta.strftime("%d/%m/%Y"))
                                # break
                            else:
                                retorno['data_consulta'] = ''
                        else:
                            retorno['data_consulta'] = data_consulta
                    else:
                        retorno['data_consulta'] = ''
            else:
                retorno['data_consulta'] = ''

        ###################### Tratamento do nome do Paciente ######################
        nomePacienteBD = novo_nome
        
        v1 = re.findall(r'\w+', nomePacienteBD.upper())
        nomes_encontrados = 0
        indice_nome = 0
        for nmPaciente in v1:
            indice_nome += 1
            if(indice_nome != 0):
                if (text.find(nmPaciente) != -1):
                    nomes_encontrados += 1
                else:
                    break

            if len(nmPaciente) > 3:
                if (text.find(nmPaciente) != -1):
                    nomes_encontrados += 1

        if(nomes_encontrados >= 2):
            # nmPaciente = nomePacienteBD
            retorno['nome_paciente'] = nomePacienteBD
        else:
            # nmPaciente = ''
            retorno['nome_paciente'] = ''   #Colocar para sempre mostrar a o nome do Paciente mesmo que nao ache 

        retorno['rotacao'] = val_rotacao
        retorno['api_response'] = text

        if(len(text) < 50):
            retorno['validade'] = "false"
        else:
            retorno['validade'] = "true"
    else:
        retorno = {}
        retorno['validade'] = "false"
        retorno['api_response'] = ""
        retorno['data_consulta'] = ""
        retorno['medico'] = ""
        retorno['dias'] = ""
        retorno['crm'] = ""
        retorno['cid'] = ""
        retorno['rotacao'] = ""
        retorno['nome_paciente'] = ""


    retorno["arquivo_saida"] = newDirImg.replace("../temp/", "")

    retorno["local_atendimento"] = local_atendimento

    retorno["bairro"] = bairro
    retorno["logradouro"] = logradouro
    retorno["cidade"] = cidade
    retorno["sus"] = sus
    retorno["uf"] = uf

    retorno['cep'] = cep

    retorno['tipo_letras'] = tipo_letras
    
    # Criação do JSON com as informações encontradas
    json_retorno = json.dumps(retorno)

    print (json_retorno)

    # row = retorno['nome_paciente'] + ";" + retorno['medico'] + ";" + retorno['data_consulta'] + ";" + str(retorno['dias']) + ";" + str(retorno['crm']) + ";" + str(retorno['cid']) + ";" + unidecode(file) + "\n"
    # arquivo.write(row)
    # arquivo_txt.write(text + '\n\n')
    # f = open("../resultados/"+novo_nome+"txt", "x")
    # f.write(unidecode(str(text).replace("\n", " ")))

# arquivo.close()

# print("Fim")