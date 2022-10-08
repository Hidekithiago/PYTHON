from email import encoders
from email.mime.base import MIMEBase
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage

def sendMail():
    msg = MIMEText("<h3><strong>Prezado Gerente/Responsavel,</strong></h3>", 'html')
    mail.sendmail(emailFrom, destinations, msg.as_string())
    mail.quit()

def sendMailAttachment():
    msg = MIMEMultipart()
    files = str(Path.home())+r"\Downloads\a"    
    print(files)

    msgText  = MIMEText("<h3><strong>Prezado Gerente/Responsavel,</strong></h3>", 'html')
    msg.attach(msgText)    
    emailFrom = 'noreplyquaestum@gmail.com'
    passFrom = 'lttjxgyrbpuouxia'
    servidorSmtp = 'smtp.gmail.com'
    portSmtp = '587'
    msg['Subject'] = 'TESTE'
    msg['From'] = emailFrom
    msg['To'] = ''
    print('Config OK')
    mail = smtplib.SMTP(servidorSmtp, portSmtp)
    print('1')
    mail.starttls()
    print('2')
    mail.login(emailFrom, passFrom)
    print('3')
    destinations = [
        "a@gmail.com"
        ,"b@gmail.com"
        ,"c@gmail.com"
    ]
    #Set up crap for the attachments
    print('SMTP OK')
    filenames = [os.path.join(files, f) for f in os.listdir(files)]

    for file in filenames:
        print(file)
        #with open('example.jpg', 'rb') as fp:
        #    img = MIMEImage(fp.read())
        #    img.add_header('Content-Disposition', 'attachment', filename="example.jpg")
        #   msg.attach(img)

        pdf = MIMEApplication(open(file, 'rb').read())
        pdf.add_header('Content-Disposition', 'attachment', filename= "example.pdf")
        msg.attach(pdf)

    mail.sendmail(emailFrom, destinations, msg.as_string())
    mail.quit()


if __name__ == "__main__":
    sendMailAttachment()