	
# -*- coding: cp1252 -*-
#pip install unidecode
# PDF -> PNG + OCR(DATE and value)
from PIL import Image 
import re
from pdf2image import convert_from_path
import cv2
import numpy
import pytesseract
import os
from os import path
from unidecode import  unidecode
from urllib.parse import unquote

urlFileWrite = 'C:\\Quaestum\\res.txt'
urlFolder = 'C:\\Quaestum\\'
count = 0
urlFileOpen = 'C:\\Quaestum\\a.txt'
if path.exists(urlFileWrite) == True:
    os.remove(urlFileWrite)

#Leitura do arquivo TXT
arquivo = open(urlFileOpen, 'r')
files = arquivo.read()
arquivo.close()
urlpdfs = re.findall(".*(?<=pdf)", files)
urlpdf = urlpdfs[0]
urlPngs = re.findall(".*(?<=png)", files)
urlPng = urlPngs[0]
urlPngTomador = urlPngs[2]


pages = convert_from_path(urlpdf, 388)
for page in pages:            
    urlImageSave = urlFolder+str(count)+".jpg"
    page.save(urlImageSave, 'JPEG')
    im = Image.open(urlImageSave) 

    
# Config para pegar o VALOR        
width, height = im.size 
left = 2160
top = 1355
right = left + 565
bottom = top + 65
im1 = im.crop((left, top, right, bottom)) 
#im1.show() 
urlSaveIMG = urlFolder+'valorPagamento.png'
im1.save(urlSaveIMG, 'png')
text = pytesseract.image_to_string(im1, lang = 'por')
text = text.replace("l", "1")
text = text.replace("L", "1")
text = text.replace("i", "1")
text = text.replace("I", "1")
text = text.replace("z", "2")
text = text.replace("Z", "2")
text = text.replace("s", "2")
text = text.replace("E", "3")
text = text.replace("F", "3")
text = text.replace("A", "4")
text = text.replace("H", "4")
text = text.replace("S", "5")
text = text.replace("G", "6")
text = text.replace("T", "7")
text = text.replace("B", "8")
text = text.replace("P", "9")
text = text.replace("O", "0")
text = text.replace("o", "0")
valorPagamento = re.findall("\w*?\.?\w*?\.?\w*,\w*", text) ### Valor Pagamento (PDF)
if path.exists(urlSaveIMG) == True:
    os.remove(urlSaveIMG)
if path.exists(urlImageSave) == True:
    os.remove(urlImageSave)
#print(text)
#print(valorPagamento)

# Config para pegar a Data  
width, height = im.size 
left = 2160
top = 534
right = left + 565
bottom = top + 65
im2 = im.crop((left, top, right, bottom)) 
#im2.show() 
text = pytesseract.image_to_string(im2, lang = 'por')        
x = re.findall("\d{2}", text)
dataVencimento = x[0]+"/"+x[1]+"/"+x[2]+x[3]  ### Captura da Data de Vencimento (PDF)
if path.exists(urlSaveIMG) == True:
    os.remove(urlSaveIMG)


###### Prestador

im = Image.open(urlPng) 
        
width, height = im.size 
left = 737
top = 253
right = left + 103
bottom = top + 18
im1 = im.crop((left, top, right, bottom)) 
urlSaveIMG = urlFolder+'issDevidoPrest.png'
im1.save(urlSaveIMG, 'png')
im = Image.open(urlSaveIMG)
text = pytesseract.image_to_string(im, lang = 'por')
text = text.replace("R", "")
text = text.replace("$", "")
issDevido = re.findall("[\w+\.|\w+,|\w+]+", text)  ### ISS DEVIDO PELO PRESTADOR (png)
os.remove(urlSaveIMG)

im = Image.open(urlPng) 
im2 = im.crop((left, 212, right, 228)) 
#im2.show() 
urlSaveIMG = urlFolder+'vlrServicoPrestador.png'
im2.save(urlSaveIMG, 'png')
im = Image.open(urlSaveIMG)
text = pytesseract.image_to_string(im, lang = 'por')
text = text.replace("R", "")
text = text.replace("$", "")
text = text.replace("l", "1")
text = text.replace("L", "1")
text = text.replace("i", "1")
text = text.replace("I", "1")
text = text.replace("z", "2")
text = text.replace("Z", "2")
text = text.replace("s", "2")
text = text.replace("E", "3")
text = text.replace("F", "3")
text = text.replace("A", "4")
text = text.replace("H", "4")
text = text.replace("S", "5")
text = text.replace("G", "6")
text = text.replace("T", "7")
text = text.replace("B", "8")
text = text.replace("P", "9")
text = text.replace("O", "0")
text = text.replace("o", "0")
vlrServico = re.findall("[\w+\.|\w+,|\w+]+", text)  ### Valor do Servico (png)
os.remove(urlSaveIMG)


##### Tomador
width, height = im.size 
left = 737
top = 203
right = left + 103
bottom = top + 15
im = Image.open(urlPngTomador) 
im2 = im.crop((left, top, right, bottom)) 
#im2.show() 
urlSaveIMG = urlFolder+'vlrServicoTomador.png'
im2.save(urlSaveIMG, 'png')
im = Image.open(urlSaveIMG)
text = pytesseract.image_to_string(im, lang = 'por')
text = text.replace("R", "")
text = text.replace("$", "")
text = text.replace("l", "1")
text = text.replace("L", "1")
text = text.replace("i", "1")
text = text.replace("I", "1")
text = text.replace("z", "2")
text = text.replace("Z", "2")
text = text.replace("s", "2")
text = text.replace("E", "3")
text = text.replace("F", "3")
text = text.replace("A", "4")
text = text.replace("H", "4")
text = text.replace("S", "5")
text = text.replace("G", "6")
text = text.replace("T", "7")
text = text.replace("B", "8")
text = text.replace("P", "9")
text = text.replace("O", "0")
text = text.replace("o", "0")
vlrServicoTomador = re.findall("[\w+\.|\w+,|\w+]+", text)  ### Valor do Servico (png)
os.remove(urlSaveIMG)


##### ISS DEVIDO Tomador
width, height = im.size 
left = 737
top = 285
right = left + 103
bottom = top + 15
im = Image.open(urlPngTomador) 
im2 = im.crop((left, top, right, bottom)) 
#im2.show() 
urlSaveIMG = urlFolder+'issDevidoTomador.png'
im2.save(urlSaveIMG, 'png')
im = Image.open(urlSaveIMG)
text = pytesseract.image_to_string(im, lang = 'por')
text = text.replace("R", "")
text = text.replace("$", "")
text = text.replace("l", "1")
text = text.replace("L", "1")
text = text.replace("i", "1")
text = text.replace("I", "1")
text = text.replace("z", "2")
text = text.replace("Z", "2")
text = text.replace("s", "2")
text = text.replace("E", "3")
text = text.replace("F", "3")
text = text.replace("A", "4")
text = text.replace("H", "4")
text = text.replace("S", "5")
text = text.replace("G", "6")
text = text.replace("T", "7")
text = text.replace("B", "8")
text = text.replace("P", "9")
text = text.replace("O", "0")
text = text.replace("o", "0")
issDevidoTomador = re.findall("[\w+\.|\w+,|\w+]+", text)  ### Valor do Servico (png)
os.remove(urlSaveIMG)

#Criar um arquivo com a resposta

arquivo = open(urlFileWrite, 'w')
try:
  valorPagamentoF = str(valorPagamento[0])
except:
  valorPagamentoF = str(valorPagamento)
try:
  issDevidoF = str(issDevido[0])
except:
  issDevidoF = str(issDevido)

try:
  vlrServicoF = str(vlrServico[0])
except:
  vlrServicoF = str(vlrServico)

try:
  issDevidoTomadorF = str(issDevidoTomador[0])
except:
  issDevidoTomadorF = str(issDevidoTomador)

try:
  vlrServicoTomadorF = str(vlrServicoTomador[0])
except:
  vlrServicoTomadorF = str(vlrServicoTomador)
#print(vlrServicoTomadorF)
#print(valorPagamento)
#print(issDevido)
#print(vlrServico)
#print(issDevidoTomador)
arquivo.write(dataVencimento+"\n"+valorPagamentoF+"\n"+issDevidoF+"\n"+vlrServicoF+"\n"+issDevidoTomadorF+"\n"+vlrServicoTomadorF)
arquivo.close()
print("PDF END")