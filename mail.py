import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendMail(data, nome, unidade):
    msg = MIMEText("<h3><strong>Prezado Gerente/Responsavel,</strong></h3>" +
"Informamos que recebemos no dia " + data + " o atestado médico do funcionário " + nome + " da Unidade de Trabalho " + unidade + 
". De acordo com os dias apresentados, será necessário avaliação da área Gestão de Afastados para possível afastamento. <br><br>FAVOR ABRIR MAESTRO EM GESTÃO INTEGRADA DE ATESTADOS MÉDICOS / AFASTAMENTOS.", 'html')
    
    msg['Subject'] = 'TESTE'
    msg['From'] = "no-reply@manserv.com.br"
    msg['To'] = 'fernando.burgos@quaestum.com.br'

    mail = smtplib.SMTP('smtp.manserv.com.br', 587)
    mail.starttls()
    mail.login('no-reply@manserv.com.br', 'rs6G@KwTdc878@E!')
    
    destinations = [
        "quaestumteste@gmail.com"
        # "afastados@manserv.com.br",
        # "ssma.saude@manserv.com.br"
    ]
    
    mail.sendmail("no-reply@manserv.com.br", destinations, msg.as_string())
    mail.quit()    
    

'''EMAILS
envioEmail = "no-reply@manserv.com.br";
mailMessage.To.Add("quaestumteste@gmail.com");
mailMessage.To.Add("afastados@manserv.com.br");
mailMessage.To.Add("ssma.saude@manserv.com.br");

'''

'''Corpo do Email

mailMessage.Body = "<h3><strong>Prezado Gerente/Responsavel,</strong></h3>" +
"Informamos que recebemos no dia " + dataInsert + " o atestado médico do funcionário " + nomePaciente + " da Unidade de Trabalho " + descricaoUt + ". De acordo com os dias apresentados, será necessário avaliação da área Gestão de Afastados para possível afastamento. <br><br>FAVOR ABRIR MAESTRO EM GESTÃO INTEGRADA DE ATESTADOS MÉDICOS / AFASTAMENTOS.";

'''



'''Credenciais
smtp.Host = "smtp.manserv.com.br";
smtp.Port = 587;
smtp.EnableSsl = false;
smtp.Credentials = new NetworkCredential(envioEmail, "@cE1@@Z;");
smtp.Send(mailMessage);
'''
