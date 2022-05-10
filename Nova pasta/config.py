from datetime import *

# wsdl auth
username = '529768'
password = 'b81efe0d7ebd94b'
codigo_empresa_principal = '423'
codigo_responsavel= '213'

# database auth
mysql_local = {
    'host': 'localhost',
    'database': 'manserv_soc',
    'user': 'root',
    'password': '',
    'table': 'atestados'
}
mysql_homolog = {
    'host': 'frotaleve.cqth4ctrsht2.us-east-1.rds.amazonaws.com',
    'database': 'atestadosdev2',
    'user': 'sys.atestadosdev',
    'password': 'Js*23676@3',
    'table': 'atestadosmedicos',
    'table_history': 'historicoAtestado_temp'
}

mysql_prd = {
    'host': 'frotaleve.cqth4ctrsht2.us-east-1.rds.amazonaws.com',
    'database': 'atestadosdev2',
    'user': 'sys.atestadosdev',
    'password': 'Js*23676@3',
    'table': 'atestadosmedicos'
}

# database compare day
reference_date = date(2021, 12, 30)

# database number of rows to fetch
rows = 5
id = 28098