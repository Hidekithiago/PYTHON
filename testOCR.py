import os, io, sys
from google.cloud import vision
from google.cloud.vision import types
import re
from google.protobuf.json_format import MessageToDict

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\quaestum\Atestados medicos\Imagens\Imagens com cid\visionapi-manserv-1c5ab86eb39e.json'
client = vision.ImageAnnotatorClient()

with io.open(r'C:\Users\hideki\Downloads\a.jpg', 'rb') as image_file:
# 2, 3, 5
#with io.open(dirImgBD, 'rb') as image_file:
    content = image_file.read()
#image = vision.Image(content=content)
image = types.Image(content=content)
response = client.text_detection(image=image)
texts = response.text_annotations

#print(texts)
am =""
for asd in texts:
    am = am + " " + str(asd.description)
print(am.upper())
v1 = re.findall('SUS', am.upper())
print(v1)
if(len(v1) == 0): v1 = re.findall('\WPREFEITURA',  am.upper())
if(len(v1) == 0): v1 = re.findall('\WSANTA CASA',  am.upper())
if(len(v1) == 0): v1 = re.findall('\WMINISTERI',  am.upper())
if(len(v1) == 0): v1 = re.findall('\WPUBLIC',  am.upper())
if(len(v1) == 0): v1 = re.findall('\WPRONTO ATENDIMENT',  am.upper())
if(len(v1) == 0): v1 = re.findall('\WMUNICIPAL',  am.upper())
if(len(v1) == 0): v1 = re.findall('\WESTADO',  am.upper())
if(len(v1) == 0): 
    sus = "false"
else:
    sus = "true"
print(sus)