import mysql.connector

mysql_homolog = { #Configuracao para poder fazer a chamada no connect
    'host': 'localhost',
    'database': 'nomeservidor',
    'user': 'root',
    'password': '',
    'table': 'atestados'
}
''' Exemplo de conexao com o BD usando um arquivo de configuracao
# connect to database
database = Mysql()
database.connect(config.mysql_homolog)
'''
class Mysql():
    def __init__(self) -> None:
        pass
    
    def connect(self, auth):
        ''' Try to connect to a database with auth params defined in config file '''
        try:
            self.connection = mysql.connector.connect(host=auth['host'],
                                                database=auth['database'],
                                                user=auth['user'],
                                                password=auth['password'])
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = self.connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                # cursor.close()
                self.auth = auth
                
                return self.connection

        except Exception as e:
            print(e)
    
    def connectHomolog(self):
        try:
            self.connection = mysql.connector.connect(host=config.mysql_homolog['host'],
                                                database=config.mysql_homolog['database'],
                                                user=config.mysql_homolog['user'],
                                                password=config.mysql_homolog['password'])
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = self.connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                # cursor.close()
                
                return self.connection

        except Exception as e:
            print(e)
            
    def disconnect(self):
        ''' Disconnect from database '''
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")
            
    def fetchTable(self, rows, table, condition = None, value = None):
        ''' Fetch a number of rows from a table that exists in database.
        Number of rows and table defined in config file.
        if number of rows equals to 0, will try to fetch all rows.'''
        # atestados_list = database.fetchTable(0, database.auth["table"], 'status', 1) #Exemplo de chamada da funcao fetchTable
        if condition:
            sql = f"SELECT * FROM `{table}` WHERE {condition} = {value}"
        else:
            sql = f"SELECT * FROM `{table}` WHERE 1"
        
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(sql)
        if rows > 0:
            records = cursor.fetchmany(rows)
        else:
            records = cursor.fetchall()
            
        print(f'Total number of rows in table: {cursor.rowcount}')
        print(f'Rows fetched: {len(records)}')
        
        atestados = []
        for row in records:
            row = list(row)
            atestados.append(row)
            
        # cursor.close()
        return atestados
    
    def updateTable(self, table, id, column, value):
        # database.updateTable('atestadosmedicos', atestado.id, 'status', 4, 'idatestadosmedicos') #Exemplo de chamada
        command = f'Update {table} set {column} = {value} where idatestadosmedicos = {id}'
        cursor = self.connection.cursor()
        cursor.execute(command)
        self.connection.commit()
        # cursor.close()
        print("Record Updated successfully ")
    
    def selectMysql(self, query):                
        cursor = self.connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        print(f'Total number of rows in table: {cursor.rowcount}')
        
        atestados = []
        for row in records:
            row = list(row)
            atestados.append(row)
            
        # cursor.close()
        return atestados
    
    def InsertMysql(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        
    def clearHistory(self):
        ''' Delete all rows from history table, clearing it. '''
        sql = f"DELETE FROM {config.mysql_homolog['table_history']} WHERE 1"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        print(cursor.rowcount, 'records deleted.')