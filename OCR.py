import os, io, sys

from google.cloud import vision
from google.cloud.vision import types
import re
import json
from google.protobuf.json_format import MessageToDict
#from PIL import Image, ImageDraw
from enum import Enum
#from matplotlib.pyplot import imshow
import numpy as np
from pathlib import Path
import unicodedata
#################### FTP ####################
from getpass import getpass
from ftplib import FTP
#from PIL import Image
from datetime import datetime, date, time, timedelta                    # Biblioteca de data
#################### MYSQL ####################
import mysql.connector as mysql
from mysql.connector import errorcode
from datetime import datetime
import hashlib
from pdf2image import convert_from_path
import urllib.request, urllib.parse, urllib.error
from unidecode import unidecode
import cv2

#conn = mysql.connect(host="34.229.239.145", user="root", passwd="T458y8Y8bTLo", db="manserv")
#cursor = conn.cursor()
#Python 3.8.3
#pip install matplotlib==3.2.2 install QtPy==1.9.0 install google.cloud.vision==1.0.0 install google-cloud-datastore==2.0.1 install Pillow==7.2.0 install mysql-connector-python==8.0.21 install pdf2image install unidecode install opencv-python

def OCR_Imagem():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\Hideki\Desktop\Nova pasta\visionapi-manserv-8d737c916e9e.json'
    client = vision.ImageAnnotatorClient()

    with io.open(dirImgBD, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    am =""
    for asd in texts:
        am = am + " " + str(asd.description)
    #print(unidecode(am.upper()))
    return(unidecode(am.upper()))

def verificaPDF(dirPDF, dirPastaPDF):
    global dirImgBD
    path = Path(dirPDF)    
    arqExtensao = path.suffix    
    if arqExtensao ==".pdf":       
        arqnome = os.path.splitext(os.path.basename(path.name))[0]
        convertPDF(dirPDF, dirPastaPDF+"\\"+arqnome+".jpg", arqnome+".jpg")
    else:
        dirImgBD = dirPastaPDF+"\\"+dirPDF
        
def convertPDF(dirPDF, dirFinal, arqnome):
    global dirImgBD
    pages = convert_from_path(dirPDF, 500,poppler_path=r'C:\poppler-0.68.0\bin')
    for page in pages:
        page.save(dirFinal, 'JPEG')
        break
    dirImgBD = dirFinal
    '''
    imagem = cv2.imread(dirImgBD)
    altura, largura = imagem.shape[:2]
        
    ponto = (largura / 2, altura / 2) #ponto no centro da figura
    rotacao = cv2.getRotationMatrix2D(ponto, 0, 1.0)
    rotacionado = cv2.warpAffine(imagem, rotacao, (largura, altura))
    cv2.imwrite(dirImgBD, rotacionado)
    print(dirImgBD)
    '''
def searchDate(dataAproximada, texto_OCR):
    global count; global validacao;
    x = re.findall("\d+", dataAproximada)
    busca = ""
    if x[0] == '01': busca = 'UM'
    elif x[0] == '02': busca = 'DOIS'
    elif x[0] == '03': busca = 'TRES'
    elif x[0] == '04': busca = 'QUATRO'
    elif x[0] == '05': busca = 'CINCO'
    elif x[0] == '06': busca = 'SEIS'
    elif x[0] == '07': busca = 'SETE'
    elif x[0] == '08': busca = 'OITO'
    elif x[0] == '09': busca = 'NOVE'
    elif x[0] == '10': busca = 'DEZ'
    elif x[0] == '11': busca = 'ONZE'
    elif x[0] == '12': busca = 'DOZE'
    elif x[0] == '13': busca = 'TREZE'
    elif x[0] == '14': busca = 'QUATORZE'
    elif x[0] == '15': busca = 'QUINZE'
    elif x[0] == '16': busca = 'DEZESSEIS'
    elif x[0] == '17': busca = 'DEZESSETE'
    elif x[0] == '18': busca = 'DEZOITO'
    elif x[0] == '19': busca = 'DEZENOVE'
    elif x[0] == '20': busca = 'VINTE'
    elif x[0] == '21': busca = 'VINTE E UM'
    elif x[0] == '22': busca = 'VINTE E DOIS'
    elif x[0] == '23': busca = 'VINTE E TRES'
    elif x[0] == '24': busca = 'VINTE E QUATRO'
    elif x[0] == '25': busca = 'VINTE E CINCO'
    elif x[0] == '26': busca = 'VINTE E SEIS'
    elif x[0] == '27': busca = 'VINTE E SETE'
    elif x[0] == '28': busca = 'VINTE E OITO'
    elif x[0] == '29': busca = 'VINTE E NOVE'
    elif x[0] == '30': busca = 'TRINTA'
    elif x[0] == '31': busca = 'TRINTA E UM'
        
    if x[1] == '01': busca += ' DE JANEIRO'
    elif x[1] == '02': busca += ' DE FEVEREIRO'
    elif x[1] == '03': busca += ' DE MARCO'
    elif x[1] == '04': busca += ' DE ABRIL'
    elif x[1] == '05': busca += ' DE MAIO'
    elif x[1] == '06': busca += ' DE JUNHO'
    elif x[1] == '07': busca += ' DE JULHO'
    elif x[1] == '08': busca += ' DE AGOSTO'
    elif x[1] == '09': busca += ' DE SETEMBRO'
    elif x[1] == '10': busca += ' DE OUTUBRO'
    elif x[1] == '11': busca += ' DE NOVEMBRO'
    elif x[1] == '12': busca += ' DE DEZEMBRO'
    
    x = re.findall(busca, texto_OCR)
    if len(x)>0:
        #print("ACHOU")
        #print(x[0])
        validacao = 1
    else:
        count += 1
        #print("Nao ACHOU")
        dTdataAproximada = datetime.strptime(dataAproximada, '%d/%m/%Y')
        diaFinal1 = dTdataAproximada +  timedelta(days=int(-1))
        diaFinal = "" + datetime.strptime(str(diaFinal1), "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
        #print(dTdataAproximada)        
        if qtdTent > count :            
            #print(count)
            #print(diaFinal)
            searchDate(diaFinal, texto_OCR)
        else: 
            validacao = 0
    
def searchDocument(busca, texto_OCR):
    global validacao;
    busca = unidecode(busca.upper())
    
    x = re.findall(busca, texto_OCR)
    if len(x)>0:
        #print("ACHOU DOCUMENTO")
        validacao = 1
    else:
        #print("NAO ACHOU DOCUMENTO")
        validacao = 0
        
def searchName(nome, texto_OCR):
    global validacao;
    nome = unidecode(nome.upper()) 
    kount = 0
    nomeRow = re.findall('\w+', nome)
    for nomePessoa in nomeRow:
        x = re.findall(nomePessoa, texto_OCR)
        if len(x)>0:
            kount += 1
    if kount > 1:
        validacao = 1
        #print('ACHOU O NOME DO FUNCIONARIO')
    else:
        validacao = 0
        #print('NÂo ACHOU O NOME DO FUNCIONARIO')
    
if __name__ == "__main__":
    '''
    Exemplo de chamada para o OCR de Certidão de NASCIMENTO
    py CERTIDAO_DE_NASCIMENTO.py "CamScanner 08-25-2021 09.21.pdf" "CERTIDAO DE NASCIMENTO" "23/08/2021"
    '''
    global count; global qtdTent; global validacao;
    
    print("\n\n\n\n\n")
    dirImgBD = sys.argv[1] #Nome do Arquivo
    tipoArquivo = sys.argv[2] #Tipo de DOCUMENTO
    dataAproximada = sys.argv[3] #Data para Verificação
        
    count = 0; qtdTent = 5; validacao = 0;
    verificaPDF(dirImgBD, r'C:\Users\Hideki\Desktop\Nova pasta')

    texto_OCR = OCR_Imagem()
    searchDocument(tipoArquivo ,texto_OCR)
    if validacao == 1: searchName('ÉRICA De carvalho Alves', texto_OCR)
    if validacao == 1: searchDate(dataAproximada, texto_OCR)
    if validacao == 1: print('DOCUMENTO VALIDADO')
    
    