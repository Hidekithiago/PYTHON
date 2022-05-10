from suds.client import Client
import config, entrada
from random import random

# connecting to SOAP
url = 'https://www.p-soc.com.br/WSSoc/services/LicencaMedicaWs?wsdl'
# url = 'https://ws1.soc.com.br/WSSoc/services/ExportaDadosWs?wsdl'
client = Client(url)
# print(client)

# authenticating
header = {
    "Timestamp": "60",
    "Username": config.username,
    "Password": config.password,
    "Nonce": random()
}
client.set_options(soapheaders=header)

complex_object = []
complex_object.append('consultaLicencaMedicaWsVo')

# test = client.factory.create(complex_object[0])
# print(test)

result = client.service.consultarLicencaMedica()
print(result)