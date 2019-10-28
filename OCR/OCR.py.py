import pytesseract
import cv2
import numpy as np
import os
from PIL import Image

Original_img = "C:\quaestum\captcha\\borelli.png"
OCR_img = "C:\quaestum\captcha\\input-NEAREST.png"
url_arq = "C:\quaestum\ocr_python.txt"
#xi=65
yi=260
#xf=130
yf=280
area = (xi, yi, xf, yf);
count = 0
while(count < 100):
    count = 0
    while(count<8):
        img = Image.open(Original_img)
        if(count == 0):
            area = (65, yi, 275, yf) #0 e 1
        elif(count == 1):
            area = (275, yi, 355, yf) #2
        elif(count == 2):
            area = (355, yi, 520, yf) #3 e 4
        elif(count == 3):
            area = (520, yi, 790, yf) #5 e 6
        elif(count == 4):
            area = (790, yi, 1035, yf) #7 e 8
        elif(count == 5):
            area = (1035, yi, 1120, yf) #9
        elif(count == 6):
            area = (1120, yi, 1300, yf) #10
        elif(count == 7):
            area = (1300, yi, 1350, yf) #10
        elif(count == 8):
            area = (65, yi, 1350, yf)

        count+=1;
        cropped_img = img.crop(area)
        cropped_img.show()
        cropped_img.save(OCR_img)

        image = Image.open(OCR_img)
        res = pytesseract.image_to_string(image)

        image.close()
        if not res and count == 0:
            sys.exit()
        #Renomear o arquivo
        #os.rename("C:\quaestum\captcha\\input-NEAREST.png", "C:\quaestum\captcha\\dtCarreg"+res+".png")
        try:    
            arquivo = open(url_arq, 'a+')
        except FileNotFoundError:
            arquivo = open(url_arq, 'w+')
        arquivo.write(res+";")
        arquivo.close()
    yi = yf
    yf = yf+25
    