from cv2 import compare
from config import reference_date
from datetime import *

class Atestado():
    def __init__(self, list) -> None:
        self.id = list[0]
        self.medico = list[1]
        self.paciente = list[25]
        self.dias = int(list[8])
        self.data_entrada = list[28]
        self.data = formatDate(list[18])
        self.cid = list[7]
        self.unidade = list[22]
        self.cpf = list[23]
        
    def isRecent(self):
        ''' Check if this registry is 60 days old or not.
        Return True if newer and False if older or equal'''
        global reference_date
        
        self.data += timedelta(days=60)
        
        if reference_date > self.data:
            # not recent
            return False
        else:
            print(f'Atestado {self.id} com menos de 60 dias.')
            # recent
            return True
        
    def isSameCID(self, cid):
        ''' Check the equality of given CID and existing one '''
        
        if self.cid == cid:
            print(f'\nAtestado {self.id} possui o mesmo CID: {cid}')
            return True
        else:
            return False
        
    def canSum(self, days):
        ''' Check if the sum of days will result in less then 15 days or not '''
        days = int(days)
        total = self.dias + days

        if total < 15:
            print(f'Dias do atestado: {self.dias}')
            print(f'Dias da nova entrada: {days}')  
            print('Dias de afastamento não ultrapassa 15')
            return True
        else:
            print('Dias de afastamento ultrapassa 15')
            return False
        
        
    def sumDays(self, days):
        ''' Increment existing days with given value '''
        days = int(days)
        self.dias += days
        print(f'Dias de afastamento do atestado atualizado para: {self.dias}\n')
        return self.dias

def getRecents(atestados):
    ''' Check and returns which of given objects is newer then 60 days old '''
    recents = []
    print('Selecionando atestados com menos de 60 dias \n')
    for atestado in atestados:
        if atestado.isRecent():
            recents.append(atestado)
            
    return recents

def formatDate(string):
    try:
        day, month, year = [int(x) for x in string.split('/')]
    except:
        year, month, day = [int(x) for x in string.split('-')]
    return date(year, month, day)

class History(Atestado):
    def __init__(self, list) -> None:
        self.id = list[0]
        self.abonado = list[1]
        self.cid = list[2]
        self.cpf = list[5]
        self.data = list[7]
        self.data_fim = list[6]
        self.dias = self.data_fim - timedelta(days=self.data.day)
        self.dias = self.dias.day
        self.cpf = list[5]
