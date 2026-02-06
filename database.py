import mysql.connector
from pathlib import Path
from CTkMessagebox import *
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
        err = None
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
        except mysql.connector.Error as e:
            err = e
            if (err.errno == 1049):
                err = None
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
                self.sql.execute("SET time_zone = %s;",(self.time,))
                self.connect.commit()
            else:
                self.connect = None

        return self.connect ,err
        
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

    def all_row(self,types,search=False,id=None):
        if (search == False and id == None):
            if (types == "ทั้งหมด"):
                self.sql.execute("SELECT COUNT(*) FROM `products`;")
                
            else:
                self.sql.execute("SELECT COUNT(*) FROM `products` WHERE `p_type` = %s;",(types,))
        else:
            self.sql.execute("SELECT count(*) FROM `products` WHERE `p_amount` > 0 AND `p_name` LIKE %s;",(f"%{id}%",))

        all_amount = self.sql.fetchone()
        all_row = int(all_amount[0] / 40)

        return all_row
    
    def all_type(self):
        self.sql.execute("SELECT DISTINCT p_type FROM `products`;")
        all_type = self.sql.fetchall()

        type_list = ["ทั้งหมด"] + [i[0] for i in all_type]

        return type_list

    def show_products(self,types,num):
        
        if (types != "ทั้งหมด"):
            self.sql.execute("SELECT `p_id` , `p_name` , `p_price` FROM `products` WHERE `p_amount` > 0 AND `p_type` = %s ORDER BY `p_type`,`p_id`,`p_name` ASC LIMIT 40 OFFSET %s;" , (types,(num)*40,))
        else:
             self.sql.execute("SELECT `p_id` , `p_name` , `p_price` FROM `products` WHERE `p_amount` > 0 ORDER BY `p_type`,`p_id`,`p_name` ASC LIMIT 40 OFFSET %s;" , (num*40,))
        
        products = self.sql.fetchall()
        
        return products
    
    def search_products(self,id,num=0):
        self.sql.execute("SELECT `p_id` , `p_name` , `p_price` FROM `products` WHERE `p_amount` > 0 AND `p_id` = %s ",(id,))
        result = self.sql.fetchone()
        search = None

        if (result != None):
            p_id = result[0]
            p_name = result[1]
            p_price = result[2]
        else:
            self.sql.execute("SELECT `p_id` , `p_name` , `p_price` FROM `products` WHERE `p_amount` > 0 AND `p_name` LIKE %s LIMIT 40 OFFSET %s",(f"%{id}%",num*40))
            search = self.sql.fetchall()
            p_id = None
            p_name = None
            p_price = None

        return p_id, p_name, p_price, search
        