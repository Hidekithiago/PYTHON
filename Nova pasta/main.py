import config, sys, os
from mysql_handler import Mysql
from Atestado import Atestado, History, getRecents
import Manserv_integracaoSOC as generate_history
from mail import sendMail

def run():
    # connect to database
    database = Mysql()
    database.connect(config.mysql_homolog)

    # # force status 1 to first atestado
    # database.updateTable(database.auth['table'], '75485', 'status', '1')

    # fetch atestados and declare a list
    # atestados_list = database.fetchTable(1, database.auth["table"], 'idatestadosmedicos', config.id)
    atestados_list = database.fetchTable(0, database.auth["table"], 'status', 1)
    atestados = []
    dias_list = []
    
    # instanciate each atestado to an object and store in list
    for row_atestados in atestados_list:
        atestado = Atestado(row_atestados)
        atestados.append(atestado)
        print(f'\nn {atestados.index(atestado)}:')
        print(f'Atestado: {atestado.id}')
        print(f'Paciente: {atestado.paciente}')
        print(f'CPF: {atestado.cpf}')
        print(f'CID: {atestado.cid}\n')
        
        # api que gera tabela temporária pra criar o history list
        print('Gerando historico..')
        sys.stdout = open(os.devnull, 'w')
        generate_history.run(atestado.cpf)
        sys.stdout = sys.__stdout__
        
        # dando fetch nessa tabela nova, que é o historico de atestados do paciente atual
        history_list = database.fetchTable(0, database.auth["table_history"], 'CPFFUNCIONARIO', atestado.cpf)
        history = []
        recents = False
        for row_history in history_list:
            atestado_history = History(row_history)
            # get only the recents
            if atestado_history.isRecent():
                recents = True
                if atestado_history.isSameCID(atestado.cid):
                    if atestado_history.canSum(atestado.dias):
                        dias_afastamento = atestado_history.sumDays(atestado.dias)
                        dias_list.append(dias_afastamento)
                    else:
                        # ENVIAR EMAIL SOLICITANDO ABERTURA DO ATESTADO NO MAESTRO
                        sendMail(atestado.data, atestado.paciente, atestado_history.unidade)
                        break
                history.append(atestado_history)
        
        if not recents:
            print('Não existem atestados no histórico com menos de 60 dias')
            # TODO: incluir um atestado novo através do webservice


    # end of program
    try:
        database.disconnect()
    except:
        print("Couldn't disconnect")
        
    return dias_list
        
dias = run()
print(dias)
