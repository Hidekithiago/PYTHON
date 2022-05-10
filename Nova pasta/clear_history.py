from mysql_handler import Mysql
import config

def run():
    # connect to database
    database = Mysql()
    database.connect(config.mysql_homolog)
    
    database.clearHistory()
    
    try:
        database.disconnect()
    except:
        print("Couldn't disconnect from database.")
    
run()