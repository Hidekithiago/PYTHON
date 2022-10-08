# -*- coding: utf-8 -*-
#pip3 install requests install matplotlib install matplotlib==3.2.2 install QtPy==1.9.0 install google.cloud.vision==1.0.0 install google-cloud-datastore==2.0.1 install Pillow==7.2.0 install mysql-connector-python==8.0.21 install pdf2image install requests install opencv-python

import os, io, sys
#################### MYSQL ####################
import mysql.connector as mysql
from mysql.connector import errorcode
from datetime import datetime
from pdf2image import convert_from_path
from pathlib import Path
import requests
import json
import numpy as np
import cv2
from PIL import Image

conn = mysql.connect(host="34.229.239.145", user="root", passwd="T458y8Y8bTLo", db="manserv")
cursor = conn.cursor()

def rotationImagem(angulo_atestado, dirImgBD):
##################################################| END |##################################################
    newDirImg = '/home/bitnami/htdocs/Manserv-Atestados/storage/temp/'+ dirImgBD
    imagem = cv2.imread(newDirImg)
    altura, largura = imagem.shape[:2]
    imgRotacionada = '/home/bitnami/htdocs/Manserv-Atestados/storage/temp/' + dirImgBD
    if(angulo_atestado == "0"):
        ponto = (largura / 2, altura / 2) #ponto no centro da figura
        rotacao = cv2.getRotationMatrix2D(ponto, 0, 1.0)
        rotacionado = cv2.warpAffine(imagem, rotacao, (largura, altura))        
        cv2.imwrite(imgRotacionada, rotacionado)
    elif(angulo_atestado == "270"):
        ponto = (largura / 2, altura / 2) #ponto no centro da figura
        rotacao = cv2.getRotationMatrix2D(ponto, 270, 1.0)
        rotacionado = cv2.warpAffine(imagem, rotacao, (largura, altura))
        cv2.imwrite(imgRotacionada, rotacionado)
    elif(angulo_atestado == "90"):        
        ponto = (largura / 2, altura / 2) #ponto no centro da figura
        rotacao = cv2.getRotationMatrix2D(ponto, 90, 0.9)
        rotacionado = cv2.warpAffine(imagem, rotacao, (altura, largura))
        cv2.imwrite(imgRotacionada, rotacionado)
    elif(angulo_atestado == "180"):
        ponto = (largura / 2, altura / 2) #ponto no centro da figura
        rotacao = cv2.getRotationMatrix2D(ponto, 180, 1)
        rotacionado = cv2.warpAffine(imagem, rotacao, (largura, altura ))
        cv2.imwrite(imgRotacionada, rotacionado)
    
def postImageRest(nome_paciente, dirImgBD):
    # api-endpoint
    URL = "http://34.229.239.145/atestados_quaestum/web_services/atestados.php/ler"    
        
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'nome_paciente' : nome_paciente, 
            'tipo_requisicao' : 'manserv'}  
    dirImagem = '/home/bitnami/htdocs/Manserv-Atestados/storage/temp/'+ dirImgBD
    try:
        myfile = {"file": (open(dirImagem, 'rb'))}
        print("postImageRest", dirImagem, myfile)
        response = requests.request("POST", verify=False, url=URL, data=PARAMS, files = myfile)            
        print(response.status_code)
        if (response.status_code == 200):            
            resJson = response.json()
            try:                
                nome_paciente = resJson['data']['nome_paciente']                
                nome_medico = resJson['data']['medico']
                crm = resJson['data']['crm']
                cid = resJson['data']['cid']
                dias_afastamento = resJson['data']['dias']
                data_consulta = resJson['data']['data_consulta']                
                #local_consulta = resJson['data']['local_consulta']
                local_consulta = ''
                angulo_atestado = resJson['data']['rotacao']
                print(angulo_atestado)
                validade = resJson['data']['validade']
                sus = resJson['data']['sus']
                local = resJson['data']['endereco']['local']
                cep = resJson['data']['endereco']['cep']
                logradouro = resJson['data']['endereco']['logradouro']
                bairro = resJson['data']['endereco']['bairro']
                localidade = resJson['data']['endereco']['localidade']
                uf = resJson['data']['endereco']['uf']
                print(validade)
                status = '0'
                if validade == 'true':
                    status = '97'
                else:
                    status = '93'
                return nome_paciente, nome_medico, crm, cid, dias_afastamento, data_consulta, local_consulta, angulo_atestado, status, sus, local, cep, logradouro, bairro, localidade, uf
                print("ENVIADO PARA A API")
            except:
                return "", "", "", "", "", "", "", "", "93", "", "", "", "", "", "", ""
        elif (response.status_code == 404):
            print("Result not found!")
            return "", "", "", "", "", "", "", "", "93", "","", "", "", "", "", ""
    except Exception as e:
        print("ENTROU NO EXCEPT")
        print ("Exception:", e)
        return "", "", "", "", "", "", "", "", "93", "","", "", "", "", "", ""
    
    #return nome_paciente, nome_medico, crm, cid, dias_afastamento, data_consulta, local_consulta, angulo_atestado, status

def mysql():#################### MYSQL Pegar os registros ####################        
    query = " Select `idAtestadosMedicos`, CONVERT(CAST(CONVERT(AES_DECRYPT(AES_DECRYPT(`urlDirImagem`,  'odiaquevem'), SHA2(id2,512))  USING latin1) AS BINARY) USING utf8) as `urlDirImagem`, CONVERT(CAST(CONVERT(AES_DECRYPT(AES_DECRYPT(`nomeUser`,  'odiaquevem'), SHA2(id2,512))  USING latin1) AS BINARY) USING utf8) as `nomeUser` from atestadosmedicos where status is null limit 1"
    idBD = ""
    dirImgBD = ""
    nomePacienteBD = ""
    for result in cursor.execute(query, multi=True):        
        try:
            rowBD = result.fetchall()       #Seta o resultado na variavel
            idBD = rowBD[0][0]
            dirImgBD = rowBD[0][1]
            nomePacienteBD = rowBD[0][2]            
            query =  "Update atestadosmedicos set status = '0' where idAtestadosMedicos = '" + str(idBD) + "'"
            cursor.execute(query)            
            conn.commit()
        except:            
            sys.exit()
            
    return idBD, dirImgBD, nomePacienteBD

def update_MYSQL(nome_paciente, nome_medico, crm, cid, dias_afastamento, data_consulta, local_consulta, angulo_atestado, status, sus, local, cep, logradouro, bairro, localidade, uf, nomePacienteBD):#################### MYSQL Pegar os registros ####################    
    categoria = 'ATESTADO MEDICO'
    query = " update atestadosmedicos set "    
    query +=" nomePaciente = '"+ str(nome_paciente)             #####   NOME DO PACIENTE
    query +="', nomeMedico = '"+ str(nome_medico)               #####   NOME DO MEDICO    
    query +="', crmMedico = '"+ str(crm)                        #####   CRM DO MEDICO        
    query +="', cid = '"+ str(cid)                              #####   CID    
    query +="', diaAfastamento = '"+ str(dias_afastamento)      #####   DIA AFASTAMENTO
    query +="', dataConsulta = '"+ str(data_consulta)           #####   DATA DA CONSULTA        
    query +="', tipoAtestado = 'ATESTADO"                       #####   TIPO ATESTADO
    if sus == "false":
        categoria = 'ATESTADO MEDICO'
        query +="', categoria = '"+ str(categoria)                #####   CATEGORIA
    else:
        categoria = 'ATESTADO MEDICO SUS'
        query +="', categoria = '"+ str(categoria)           #####   CATEGORIA
    query +="', local = '"+ str(local)                          #####   LOCAL
    query +="', cep = '"+ str(cep)                              #####   CEP
    query +="', logradouro = '"+ str(logradouro)                #####   LOGRADOURO
    query +="', bairro = '"+ str(bairro)                        #####   BAIRRO
    query +="', localidade = '"+ str(localidade)                #####   LOCALIDADE
    query +="', uf = '"+ str(uf)                                #####   UF    
    query +="', userInsert = '"+ str(nomePacienteBD)            #####   USER INSERT 
    query +="', status = '"+ str(status)                        #####   STATUS
    query +="' where idAtestadosMedicos = '"+str(idBD)+"'"
    print("Query de UPDATE \n" + query)
    cursor.execute(query)
    conn.commit()
    
    #query = "insert into robolog(nomeMedico,crmMedico,nomePaciente,cid,dataConsulta,diaAfastamento,idatestadosmedicos, status, userInsert ) values ('"+str(nome_medico)+"','"+ str(crm) +"','"+ str(nome_paciente)  +"','"+ str(cid)+"','"+ str(data_consulta) +"','"+str(dias_afastamento)+"','"+ str(idBD)+"','"+str(status)+"','"+ str(nomePacienteBD)+ "')"
    query1 = "insert into robolog(nomeMedico,crmMedico,nomePaciente,cid,dataConsulta,diaAfastamento,idatestadosmedicos, status, userInsert, cep, logradouro, bairro, localidade, uf, local,categoria) values ('"+str(nome_medico)+"','"+ str(crm) +"','"+ str(nome_paciente)  +"','"+ str(cid)+"','"+ str(data_consulta) +"','"+str(dias_afastamento)+"','"+ str(idBD)+"','"+str(status)+"','"+ str(nomePacienteBD)+ "','"+ str(cep)+"','"+ str(logradouro)+"','"+ str(bairro)+"','"+ str(localidade)+"','"+ str(uf)+"','"+ str(local)+"','"+ str(categoria)+"')"
    cursor.execute(query1)
    print("Query ROBOLOG \n" + query1)
    conn.commit()

def verificaPDF(nomeArq, dirArq):
    imagemFinal = nomeArq
    path = Path(nomeArq)
    extensaoArq = path.suffix    
    if extensaoArq ==".pdf":
        nomeArq = dirArq+nomeArq
        arqnome = os.path.splitext(os.path.basename(path.name))[0]        
        convertPDF(nomeArq, dirArq+arqnome+".png")
        imagemFinal = arqnome+".png"
        print(imagemFinal)
    return  imagemFinal 

def convertPDF(dirPDF, dirFinal):
    pages = convert_from_path(dirPDF, 500)
    for page in pages:        
        page.save(dirFinal, 'PNG')        

if __name__ == "__main__":
    idBD, dirImgBD, nomePacienteBD  = mysql()
    dirImgBD = verificaPDF(dirImgBD, r'/home/bitnami/htdocs/Manserv-Atestados/storage/temp/')
    nome_paciente, nome_medico, crm, cid, dias_afastamento, data_consulta, local_consulta, angulo_atestado, status, sus, local, cep, logradouro, bairro, localidade, uf = postImageRest(nomePacienteBD, dirImgBD)    
    rotationImagem(angulo_atestado, dirImgBD)    
    update_MYSQL(nome_paciente, nome_medico, crm, cid, dias_afastamento, data_consulta, local_consulta, angulo_atestado, status, sus, local, cep, logradouro, bairro, localidade, uf, nomePacienteBD)