import mysql.connector

class Database:
    def __init__(self,host,user,password,database,time):
        super().__init__()
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connect = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.sql = self.connect.cursor()
        self.sql.execute("SET TIMEZONE = %s;",(self.time,))
        self.connect.commit()

    def check_connect(self):
        if (not self.connect):
            self.connect = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.sql = self.connect.cursor()
            self.sql.execute("SET TIMEZONE = %s;",(self.time,))
            self.connect.commit()
        return self.connect
            
    def Login(self,username,password):
        self.sql.execute("SELECT * FROM `accounts` WHERE `username` = %s AND `passwords` = %s AND `onlines` = 0",(username,password))
        result = self.sql.fetchone()
        if (result):
            self.sql.execute("UPDATE `accounts` SET `onlines` = 1 WHERE `username` = %s;",(username,))
            self.connect.commit()
        else:
            return False
        return result
