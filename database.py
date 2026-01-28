import mysql.connector
from pathlib import Path

class Database_Mysql:
    def __init__(self,host,user,password,database,time):
        super().__init__()
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.time = time
        

        self.sql = self.connect_db()

    def connect_db(self):
        try:
            self.connect = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.sql = self.connect.cursor()
            self.sql.execute("SET time_zone = %s;",(self.time,))
            self.connect.commit()
        except mysql.connector.Error as err:
            if (err.errno == 1049):
                self.connect = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                )
                self.sql = self.connect.cursor()

                appdir = Path(__file__).parent
                file = appdir / "stock_list.sql"
                
                with open(file, 'r', encoding='utf-8') as f:
                    sql_script = f.read()
                for result in self.sql.execute(sql_script, multi=True):
                    pass
                self.connect.database = "stock_list"
            elif (err.errno == 2003 or  err.errno == 1045):
                self.connect = None
  

        return self.connect
        
    def Login(self,username,password):
        self.sql.execute("SELECT * FROM `accounts` WHERE `username` = %s AND `passwords` = %s AND `onlines` = 0",(username,password))
        result = self.sql.fetchone()

        if (result):
            self.sql.execute("UPDATE `accounts` SET `onlines` = 1 WHERE `username` = %s;",(username,))
            self.connect.commit()

        return result
    
    def Log_Out(self,username):
        self.sql.execute("UPDATE `accounts` SET `onlines` = 0 WHERE `username` = %s;",(username,))
        self.connect.commit()
