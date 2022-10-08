from urllib.request import urlopen                                      # Requisicao de API
import json                                                             # Leitura de JSON
import mysql.connector as mysql                                         # Biblioteca de MYSQL
from mysql.connector import errorcode                                   # Biblioteca de MYSQL

conn = mysql.connect(host="frotaleve.cqth4ctrsht2.us-east-1.rds.amazonaws.com", user="sys.atestadosdev", passwd="Js*23676@3", db="atestadosdev")       #Ambiente de PRODUCAO
cursor = conn.cursor()

url = "https://web.manserv.com.br/sigx/apps/dados_hierarquia.php?chave=ZEyU27beV5LDWPqeFzadH6e7k6Sktauq3pTzuvks"
response = urlopen(url)
data_json = json.loads(response.read())
#print(data_json['resultado']['list'])
a = data_json['resultado']['list']
#print(a)
count = 0
for item in a:
    #print(item)
    if count > -1:
        query = r"INSERT IGNORE INTO utcc (numero_ut, descricao, coligada_id, numero_coligada, coligada_fantasia, coligada_cnpj, cidade, status, ano_mes_inicio, ano_mes_fim, negocio_bu, regional, tipo_despesa, regiao, segmento, grupo_cliente, diretor_presidente, diretor_presidente_cpf, diretor_vpresidente, diretor_vpresidente_cpf, diretor, diretor_cpf, gerente, gerente_cpf, responsavel, responsavel_cpf, admin, admin_cpf, sync, uf) values ('"+str(item['codut'])+"', '"+str(item['descricao'])+"', '"+str(item['coligada'])+"','"+str(item['coligada'])+"','"+str(item['coligada_fantasia'])+"','"+str(item['coligada_cnpj'])+"','"+str(item['cidade'])+"','"+str(item['statusut'])+"','"+str(item['anomesini'])+"','"+str(item['anomesfim'])+"','"+str(item['negocio_bu'])+"','"+str(item['regional'])+"','"+str(item['tipo_despesa'])+"','"+str(item['regiao'])+"','"+str(item['Segmento'])+"','"+str(item['grupo_cliente'])+"','"+str(item['diretor_presidente'])+"','"+str(item['diretor_presidente_cpf'])+"','"+str(item['diretor_vpresidente'])+"','"+str(item['diretor_vpresidente_cpf'])+"','"+str(item['diretor'])+"','"+str(item['diretor_cpf'])+"','"+str(item['gerente'])+"','"+str(item['gerente_cpf'])+"','"+str(item['responsavel'])+"','"+str(item['responsavel_cpf'])+"','"+str(item['admin'])+"','"+str(item['admin_cpf'])+"','', '"+str(item['UF'])+"')";
        cursor.execute(query)
        conn.commit()
        #print(query)
    count +=1
    print(count)
    
