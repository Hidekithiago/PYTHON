import os, io
from suds.client import Client
import requests
import ssl
import datetime
from zeep import Client
from zeep.wsse.username import UsernameToken
from zeep.wsse.utils import WSU
from zeep.plugins import HistoryPlugin
from lxml import etree
#os.system('cmd /c "cd '+str(Path.home())+'\\AppData\\Local\\Programs\\Python\\Python310\\Scripts && pip3 install ')
ssl._create_default_https_context = ssl._create_unverified_context

def queryAPI():
    cep = '01001000'
    url = f'https://viacep.com.br/ws/{cep}/json/'
    headers = {'User-Agent': 'Autociencia/1.0'}
    resposta = requests.request('GET', url, headers=headers)
    conteudo = resposta.content.decode('utf-8')
    resposta.close()
    print(conteudo)        

def queryWebService():
        client = Client('https://apps.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl')        
        response = client.service.consultaCEP(cep='01001000')
        print(response)

def queryWSSecurityWebService():
    timestamp_token = WSU.Timestamp()
    today_datetime = datetime.datetime.today()
    expires_datetime = today_datetime + datetime.timedelta(minutes = 10)

    timestamp_elements = [
        WSU.Created(today_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")),
        WSU.Expires(expires_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"))
    ]

    timestamp_token.extend(timestamp_elements)
    user_name_token = UsernameToken('username', 'password', timestamp_token = timestamp_token)
    
    client = Client(
        'http://www.webservicex.net/ConvertSpeed.asmx?WSDL',
        wsse = user_name_token,
    )

    response = client.service.ConvertSpeed(100.00, 'kilometersPerhour', 'milesPerhour')

    print(response)
    
if __name__ == "__main__":
    #queryAPI()
    #queryWebService()
    queryWSSecurityWebService()