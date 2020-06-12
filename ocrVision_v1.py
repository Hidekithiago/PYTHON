#pip install mysql-connector-python
#pip install google.cloud.vision
#pip install pyftpdlib
#pip install Pillow-PIL
#pip install mysql.connector
#################### VISION ####################
import os, io
from google.cloud import vision
from google.cloud.vision import types
import re
import json
from google.cloud import vision
from google.cloud.vision import types
from google.protobuf.json_format import MessageToDict
#################### FTP ####################
from getpass import getpass
from ftplib import FTP
from PIL import Image 

#################### MYSQL ####################
import mysql.connector
from mysql.connector import errorcode

#################### MYSQL Pegar os registros ####################

conn = mysql.connector.connect(host="162.241.60.117", user="quaest71_b2p", passwd="b2p@quaestum", db="quaest71_b2p")
c = conn.cursor()
query = " Select `idAtestadosMedicos`,"
query +=" AES_DECRYPT(AES_DECRYPT(`urlDirImagem`, 'odiaquevem'), SHA2(id2,512)) as `urlDirImagem`"
query +=" from AtestadosMedicos where AES_DECRYPT(AES_DECRYPT(`status`, 'odiaquevem'), SHA2(id2,512)) = 0 limit 1"

#print(query)
print('Conectando BD...')
print(' -------------  ATESTADOS:  -------------')
for result in c.execute(query, multi=True):
  if result.with_rows:
    #print("Rows produced by statement '{}':".format(result.statement))
    #print(result.fetchall())
    rowBD = result.fetchall()
    idBD = rowBD[0][0]
    dirImgBD= rowBD[0][1]
  else:
    print("Number of rows affected by statement '{}': {}".format(
      result.statement, result.rowcount))
print('Query Executada...')
#################### FTP PEGAR O ARQUIVO ####################
fileFTP1 = re.findall("(?<=\/).*", dirImgBD)
fileFTP = str(fileFTP1[0])
folderFTP1 = re.findall(".*(?=\/)", dirImgBD)
folderFTP=str(folderFTP1[0])
nonpassive = False
nomeArquivo = dirImgBD
dirNome = '/b2p/web_services/appGam/Imagens/'+folderFTP
ipFTP = 'ftp.quaestum.com.br'


print('Conectando FTP...')
conexao = FTP(ipFTP)
conexao.login(user='painel@quaestum.com.br', passwd='quaestum168363')
conexao.cwd(dirNome)

localfile = open(fileFTP, 'wb')
conexao.retrbinary('RETR '+dirNome+"/"+fileFTP, open('C:\Quaestum\\'+fileFTP, 'wb').write, 1024)


conexao.quit()
localfile.close()
print('Desconectando FTP...')

#################### VISION LEITURA DO ARQUIVO ####################
print('Lendo Arquivo ...')
image_path = r'C:\Users\hidek\Desktop\VISION'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = image_path + r'\vision-api-269502-4a34135aa18b.json'

client = vision.ImageAnnotatorClient()

file_name = '\\'+fileFTP
#file_name = '\\a.jpg'
# TESTE PARA PEGAR OUTRAS IMAGENS
#image_path = r'C:\Quaestum'
#file_name = '\\z.png'


with io.open("C:\Quaestum\\"+file_name, 'rb') as image_file:
    content = image_file.read()

# construct an iamge instance
image = vision.types.Image(content=content)

"""
# or we can pass the image url
image = vision.types.Image()
image.source.image_uri = 'https://edu.pngfacts.com/uploads/1/1/3/2/11320972/grade-10-english_orig.png'
"""

# annotate Image Response
response = client.text_detection(image=image)  # returns TextAnnotation
if response.error.message:
    raise Exception(
    '{}\nFor more info on error messages, check: '
    'https://cloud.google.com/apis/design/errors'.format(
    response.error.message))

#print(response.text())
print('Texts:')
resultOCR=''

for text in response.text_annotations:
    print(text.description)
    resultOCR += text.description+"\n"

print('Termino de Leitura')
print('\n\n\nITENS CAPTURADOS')
try:
    ##### nomeMedico
    nomeMedico = re.findall("(?<=Dra\.).+", resultOCR)
    if not nomeMedico:    
        nomeMedico = re.findall("(?<=Dra\.).+", resultOCR)
    if not nomeMedico:
        nomeMedico = re.findall("(?<=Dr\.).+", resultOCR)
    if not nomeMedico:
        nomeMedico = re.findall("(?<=DR\.).+", resultOCR)
    try:
        nomeMedico = nomeMedico[0]
    except:
        nomeMedico = nomeMedico
    ##### crm
    crm = re.findall("(?<=CRM).\d+\-?\.?\d+", resultOCR)        
    print(crm)
    if not crm:
        crm = re.findall("(?<=CRP:).+", resultOCR)
    try:
        crm = crm[0]
    except:
        crm = crm
    ##### cid
    cid = re.findall("(?<=CID\.).+", resultOCR)
    if not cid:
        cid = re.findall("(?<=CID-10:).+", resultOCR)
    if not cid:
        cid = re.findall("(?<=\(CIDX).+(?=\))", resultOCR)
    try:
        cid = cid[0]
    except:
        cid = cid
    ##### tipoAtestado
    tipoAtestado = re.findall("(?=LAUDO).+", resultOCR)
    if not tipoAtestado:
        tipoAtestado = re.findall("(?=Laudo Médico).+", resultOCR)
    if not tipoAtestado:
        tipoAtestado = re.findall("(?=ATESTADO MÉDICO).+", resultOCR)
    try:
        tipoAtestado = tipoAtestado[0]
    except:
        tipoAtestado = tipoAtestado
except:
    print("An exception occurred")
print('\n\n\nITENS CAPTURADOS')
print(nomeMedico)
print(crm)
print(cid)
print(tipoAtestado)

#################### UPDATE NO BD COM AS INFORMACOES CAPTURADAS ####################
print('Alterando informacoes no BD')
query = " UPDATE `AtestadosMedicos` SET " 
query += " `nomeMedico`= '"+str(nomeMedico)+"',"
query += " `crmMedico`= '"+str(crm)+"',"
query += " `tipoAtestado`= '"+str(tipoAtestado)+"',"
query += " `cid`= '"+str(cid)+"',"
query += " `status`=1,"
query += " `dtLastUpdate`= now(),"
query += " `userLastUpdate`= 'quaestumOCR'"
query += " where idAtestadosMedicos = "+str(idBD)
c.execute(query)
print('Atualizacao concluida')