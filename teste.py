import base64
import datetime
import hashlib
import uuid
from zeep import Client
from zeep.wsse.username import UsernameToken
from zeep.wsse.utils import WSU

def genheaders(user_name, user_key):
    random = str(uuid.uuid4()).encode('ascii')
    nonce = hashlib.md5(random).digest()[0:16]
    curdate = datetime.datetime.now().replace(microsecond=0)

    hash_digest = hashlib.sha1()
    hash_digest.update(nonce)
    hash_digest.update(curdate.isoformat().encode('ascii'))
    hash_digest.update(user_key)

    x_wsse =  ', '.join([  'UsernameToken Username="{user}"',
                           'PasswordDigest="{digest}"',
                           'Nonce="{nonce}"',
                           'Created="{created}"'])
    x_wsse = x_wsse.format(
                        user=user_name,
                        digest=base64.b64encode(hash_digest.digest()).decode('utf-8'),
                        nonce=base64.b64encode(nonce).decode('utf-8'),
                        created=curdate.isoformat(),
                    )

    return { 
            'Authorization': 'WSSE profile="UsernameToken"',
            'X-WSSE': x_wsse,
           }

timestamp_token = WSU.Timestamp()
today_datetime = datetime.datetime.today()
expires_datetime = today_datetime + datetime.timedelta(minutes=1)
timestamp_elements = [
         WSU.Created(today_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")),         
         WSU.Expires(expires_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"))
]
print(today_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"))
timestamp_token.extend(timestamp_elements)
user_name_token = UsernameToken('5135245', 'password', timestamp_token=timestamp_token)
client = Client(
     'https://ws1.soc.com.br/WSSoc/services/UploadArquivosWs?wsdl', wsse=user_name_token
)
genheaders('thideki', 'abc123**')