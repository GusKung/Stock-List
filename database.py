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
                password=self.password
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

    def all_row_user(self):
        self.sql.execute("SELECT COUNT(*) FROM `accounts`")
        result = self.sql.fetchone()

        all_amount = result
        all_row = int(all_amount[0] / 50)

        return all_row
    
    def all_type(self):
        self.sql.execute("SELECT DISTINCT p_type FROM `products`;")
        all_type = self.sql.fetchall()

        type_list = [i[0] for i in all_type]

        return type_list

    def show_products(self,types,num=0):
        
        if (types != "ทั้งหมด"):
            self.sql.execute("SELECT  `p_id` , `p_name` , `p_type` , `p_price` , `p_cost_price` , `p_amount`, `p_sell` FROM `products` WHERE `p_amount` > 0 AND `p_type` = %s ORDER BY `p_type`,`p_id`,`p_name` ASC LIMIT 40 OFFSET %s;" , (types,(num)*40,))
        else:
             self.sql.execute("SELECT  `p_id` , `p_name` , `p_type` , `p_price` , `p_cost_price` , `p_amount`, `p_sell` FROM `products` WHERE `p_amount` > 0 ORDER BY `p_type`,`p_id`,`p_name` ASC LIMIT 40 OFFSET %s;" , (num*40,))
        
        products = self.sql.fetchall()
        
        return products
    
    def search_products(self,id,num=0):
        self.sql.execute("SELECT `p_id` , `p_name` , `p_type` , `p_price` , `p_cost_price` , `p_amount`, `p_sell` FROM `products` WHERE `p_amount` > 0 AND `p_id` = %s ",(id,))
        result = self.sql.fetchone()
        search = None

        if (result != None):
            p_id = result[0]
            p_name = result[1]
            p_type = result[2]
            p_price = result[3]
            p_cost_price = result[4]
            p_amount = result[5]
            p_sell = result[6]

        else:
            self.sql.execute("SELECT `p_id` , `p_name` , `p_type` , `p_price` , `p_cost_price` , `p_amount`, `p_sell` FROM `products` WHERE `p_amount` > 0 AND `p_name` LIKE %s LIMIT 40 OFFSET %s",(f"%{id}%",num*40))
            search = self.sql.fetchall()
            p_id = None
            p_name = None
            p_type = None
            p_price = None
            p_cost_price = None
            p_amount = None
            p_sell = None

        return p_id, p_name,p_type, p_price,p_cost_price,p_amount,p_sell, search
    
    def check_level(self,username,passwords,level):
        self.sql.execute("SELECT `username` FROM `accounts` WHERE `username` = %s AND `passwords` = %s  AND `level` >= %s" ,(username,passwords,level))
        result = self.sql.fetchone()

        return result

    def insert_products(self,id,name,types,cost_price,price,amount,sell=0):
        err = None
        self.sql.execute("SELECT `p_id` FROM `products` WHERE `p_id` = %s;", (id,))
        find = self.sql.fetchall()

        if (not find):
            try:
                self.sql.execute("INSERT IGNORE  `products` VALUES (%s,%s,%s,%s,%s,%s,%s)",(id,name,types,cost_price,price,amount,sell))
                self.connect.commit()
                result = True
            except mysql.connector.Error as e:
                result = False
                err = e
        else:
                try:
                    self.sql.execute("UPDATE `products` SET `p_name` = %s, `p_type` = %s, `p_cost_price` = %s, `p_price` = %s, `p_amount` = %s WHERE `p_id` = %s;", (name, types, cost_price, price, amount, id))
                    self.connect.commit()
                    result = True
                except mysql.connector.Error as e:
                    result = False
                    err = e
           
        return result , err
        
    def load_user(self,num=0):
        self.sql.execute("SELECT * FROM `employee` join `accounts` on `employee`.`account_id` = `accounts`.`id` order by `accounts`.`id` asc limit 50 offset %s;" ,(num*50,))
        result = self.sql.fetchall()

        return result

    def insert_user(self,id,user,level,passwords,emp_id,f_name,l_name,contact,address):
        err = None
        self.sql.execute("SELECT `id` FROM `accounts` WHERE `id` = %s;", (id,))
        resulte = self.sql.fetchall()

        try:
            if (not resulte):
                self.sql.execute("INSERT INTO `accounts` (`id`, `username`, `passwords`, `level` , `onlines`) VALUES (%s, %s, %s, %s,%s);", (id, user, passwords, level, 0))

                self.sql.execute("INSERT INTO `employee` (`emp_id` ,`account_id`, `first_name`, `last_name` , `address` , `contact`) VALUES (%s,%s, %s, %s, %s, %s);", (emp_id,id, f_name, l_name , address , contact))
            else:
                self.sql.execute("UPDATE `employee` join `accounts` on `employee`.`account_id` = `accounts`.`id` set `accounts`.`username` = %s, `accounts`.`passwords` = %s, `accounts`.`level` = %s, `employee`.`emp_id` = %s ,`employee`.`first_name` = %s, `employee`.`last_name` = %s, `employee`.`contact` = %s, `employee`.`address` = %s where `accounts`.`id` = %s;" , (user,passwords,level,emp_id,f_name,l_name,contact,address,id))
    
            self.connect.commit()
            result = True
        except mysql.connector.Error as e:
            result = False
            err = e
        return result , err
        
    def count_user(self):
        self.sql.execute("SELECT id FROM `accounts`;")
        resulte = self.sql.fetchall()

        return resulte

    def del_user(self,id,emp_id):
        self.sql.execute("DELETE FROM `accounts` WHERE `id` = %s;", (id,))
        self.sql.execute("DELETE FROM `employee` WHERE `emp_id` = %s;", (emp_id,))
        self.connect.commit()

    def del_products(self,id):
        self.sql.execute("DELETE FROM `stock_list`.`products` WHERE `p_id` = %s;", (id,))
        self.connect.commit()