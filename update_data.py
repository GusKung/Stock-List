from PIL import Image 
from CTkMenuBar import *
from CTkMessagebox import *
from pathlib import Path
import os 
import mysql.connector
import math
from PIL import Image
from cryptography.fernet import Fernet
from dotenv import load_dotenv, dotenv_values 
from CTkScrollableDropdown import *
from customtkinter import *
import customtkinter
from tkinter import ttk

def gui_account(my_sql):
# //-----------------------------------------------------
    class CTKUI(CTkToplevel):
        def __init__(self,titel,wide,height,color,theme):
            CTkToplevel.__init__(self)
            self.title(f"{titel}")
            screen_x = self.winfo_screenwidth()
            screen_y = self.winfo_screenheight()

            x = int((screen_x / 2) - (wide/2))
            y = int((screen_y / 2) - (height / 2))
            self.geometry(f"{wide}x{height}+{x}+{y-25}")
            
            self.config(bg=f"{color}")
            customtkinter.set_appearance_mode(theme)

            appdir = Path(__file__).parent
            icon = appdir / "icon" / "icon.ico"
            
            self.iconbitmap(icon)
            self.after(200, lambda: self.iconbitmap(icon)) 

# //-----------------------------------------------------

    account_gui = CTKUI("Stock List", 1280, 600, "#7cffac", "light")
    account_gui.attributes("-topmost",True)

    FLeft = CTkFrame(account_gui,width=400,fg_color="#7cffac", corner_radius=0)
    FLeft.pack(side=LEFT, fill=BOTH)

    FLeft.columnconfigure(0,weight=1)
    FLeft.rowconfigure(2,weight=1)

    FRight = CTkFrame(account_gui,fg_color="#FFFFFF", corner_radius=0)
    FRight.pack(side=RIGHT, fill=BOTH,expand=True)

    FRight.columnconfigure(0,weight=1)
    FRight.rowconfigure(0,weight=1)

    ID = StringVar(value="")
    USER = StringVar(value="")
    PASS = StringVar(value="")
    LEVEL = StringVar(value="")

    data_account = []

    inp_user = CTkEntry(FLeft,placeholder_text="Username",text_color="#818181",textvariable=USER,width=200,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16),state="disabled")
    inp_user.grid(row=0,column=0,pady=(40,10),padx=20)

    inp_level = CTkComboBox(FLeft,values=["1","2","3"],variable=LEVEL,state="disabled",width=100,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16))
    inp_level.grid(row=0,column=1,pady=(40,10),padx=20)

    inp_pass = CTkEntry(FLeft,placeholder_text="Password",text_color="#818181",textvariable=PASS,show="●",width=200,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16),state="disabled")
    inp_pass.grid(row=1,column=0,pady=20,padx=20)


    id_ac = 8000  
    id_em = 6000
    def add_track():
        nonlocal id_ac , id_em
        sql = my_sql.cursor()
        sql.execute("SELECT id FROM `stock_list`.`accounts`;")
        resulte = sql.fetchall()
        len_id_ac = len(resulte) + id_ac
        len_id_em = len(resulte) + id_em

        table_account.insert("",END,values=(len_id_em,len_id_ac,"New","","","","","","",""))
        id_ac += 1
        id_em += 1
        

    btn_add = CTkButton(FLeft,width=100,height=40,text="Add",corner_radius=20,command=add_track)
    btn_add.grid(row=3,column=0,sticky="sw",padx=20,pady=20)

    def del_track():
        sure = CTkMessagebox(title="Delete Account",message="Are you sure to delete this account?",icon="warning",option_1="No",option_2="Yes")
        if (sure.get() == "No"):
            return
        else:
            selected_item = table_account.selection()
            if selected_item:
                for item in selected_item:
                    values = table_account.item(item, "values")
                id_account = values[1]  
                sql = my_sql.cursor()
                sql.execute("DELETE FROM `stock_list`.`accounts` WHERE `id` = %s;", (id_account,))
                my_sql.commit()
                load_data()


    btn_del = CTkButton(FLeft,width=100,height=40,text="Remove",corner_radius=20,fg_color="#FF3939",hover_color="#DF4949",cursor="hand2",command=del_track)
    btn_del.grid(row=3,column=1,sticky="se",padx=20,pady=20)

    def apply():
        for id_account , user , level , password , id , f_name , l_name , contact , address in data_account:

            sql = my_sql.cursor()
            sql.execute("SELECT id FROM `stock_list`.`accounts` WHERE id = %s;", (id_account,))
            resulte = sql.fetchall()
            if (not resulte):
                sql.execute("INSERT INTO `stock_list`.`accounts` (`id`, `username`, `passwords`, `level` , `onlines`) VALUES (%s, %s, SHA2(%s,256), %s,%s);", (id_account, user, password, level, 0))
                my_sql.commit()

                sql.execute("INSERT INTO `stock_list`.`employee` (`emp_id` ,`account_id`, `first_name`, `last_name` , `address` , `contact`) VALUES (%s,%s, %s, %s, %s, %s);", (id,id_account, f_name, l_name , address , contact))
                my_sql.commit()
            else:
                sql.execute("""update `stock_list`.`employee` join `stock_list`.`accounts` on `employee`.`account_id` = `accounts`.`id` set `accounts`.`username` = %s, `accounts`.`passwords` = SHA2(%s,256), `accounts`.`level` = %s, `employee`.`emp_id` = %s ,`employee`.`first_name` = %s, `employee`.`last_name` = %s, `employee`.`contact` = %s, `employee`.`address` = %s where `accounts`.`id` = %s;""" , (user,password,level,id,f_name,l_name,contact,address,id_account))
                my_sql.commit()
         
        succ = CTkMessagebox(title="Success",message="Apply Changes Successfully!",icon="check",option_1="OK")
        if (succ.get() == "OK"):
            load_data()

     
    btn_apply = CTkButton(FRight,width=100,height=40,text="Apply",corner_radius=20,command=apply)
    btn_apply.grid(row=1,column=0,sticky="se",padx=20,pady=20)

    def edit():
        if (inp_user.cget("state") == "disabled"):
            inp_user.configure(state="normal",text_color="#000000",border_color="#000000",fg_color="#FFFFFF")
            inp_level.configure(state="normal",border_color="#000000",fg_color="#FFFFFF")
            inp_pass.configure(state="normal",text_color="#000000",border_color="#000000",fg_color="#FFFFFF")
            data_employee.configure(state="normal",text_color="#000000",border_color="#8D8D8D",fg_color="#FFFFFF")
            btn_edit.configure(text="Save")

            def protect_readonly(event):
                cursor_pos = data_employee.index("insert")
                
                prev_index = data_employee.index(f"{cursor_pos} -1c")
                
                if event.keysym in ("BackSpace", "Delete"):
                    if "readonly" in data_employee.tag_names(prev_index):
                        return "break"
                
                if event.keysym not in ("BackSpace", "Delete"):
                    if "readonly" in data_employee.tag_names(cursor_pos):
                        
                        insert_after = data_employee.index(f"{prev_index} +1c")
                        data_employee.mark_set("insert", insert_after)


            data_employee.bind("<Key>", protect_readonly)
            data_employee.bind("<BackSpace>", protect_readonly)
            data_employee.bind("<Delete>", protect_readonly)

        else:
            inp_user.configure(state="disabled",text_color="#818181",border_color="#8D8D8D",fg_color="#FCFCFC")
            inp_level.configure(state="disabled",border_color="#8D8D8D",fg_color="#FCFCFC")
            inp_pass.configure(state="disabled",text_color="#818181",border_color="#8D8D8D",fg_color="#FCFCFC")
            data_employee.configure(state="disabled",text_color="#818181",border_color="#A7A7A7",fg_color="#FCFCFC")
            btn_edit.configure(text="Edit")

            em_id = data_employee.get("1.0","3.0").rstrip("\n").replace("Employee ID : ","")

            name = data_employee.get("3.0","5.0").rstrip("\n").replace("Name : ","").split("\n")[0]
            full_name = name.split(" ")
            f_name = full_name[0]
            l_name = full_name[1]

            contact = data_employee.get("5.0","7.0").rstrip("\n").replace("Contact : ","")
            address = data_employee.get("7.0","9.0").rstrip("\n").replace("Address : ","")

            if (ID.get(),USER.get(),LEVEL.get(),PASS.get(),em_id,f_name,l_name,contact,address) not in data_account:

                for i, record in enumerate(data_account):
                    if record[0] == ID.get():
                        data_account[i] = (ID.get(),USER.get(),LEVEL.get(),PASS.get(),em_id,f_name,l_name,contact,address)

                        data_account.remove(data_account[i])
                data_account.append((ID.get(),USER.get(),LEVEL.get(),PASS.get(),em_id,f_name,l_name,contact,address))

    btn_edit = CTkButton(FLeft,text="Edit",width=150,corner_radius=14,height=30,font=("Arial", 16),command=edit)
    btn_edit.grid(row=1,column=1,pady=20,padx=20)

    data_employee = CTkTextbox(FLeft,width=400,height=200,corner_radius=20,font=("Arial", 16),border_width=2,border_color="#A7A7A7",fg_color="#FCFCFC",text_color="#818181")
    data_employee.configure(state="disabled")
    data_employee.grid(row=2,column=0,columnspan=2,pady=10,padx=20,sticky="nsew")

    style = ttk.Style(account_gui)
    style.configure("Treeview", font=("Arial", 12), rowheight=40,borderwidth=0, highlightthickness=0)       
    style.configure("Treeview.Heading", font=("Arial Bold", 12))  

    table_account = ttk.Treeview(FRight,columns=("ID_EM","ID","Username","Level","Employee","First_Name","Last_Name","Password","Address","Contact"),show="headings")

    scrollbar = ttk.Scrollbar(FRight, orient="vertical", command=table_account.yview)
    table_account.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    table_account.heading("ID",text="ID")
    table_account.heading("Username",text="Username")
    table_account.heading("Level",text="Level")
    table_account.heading("Employee",text="Employee")

    table_account.column("ID_EM",width=0,stretch=False)
    table_account.column("ID",width=30,anchor=CENTER)
    table_account.column("Username",width=100,anchor=CENTER)
    table_account.column("Level",width=30,anchor=CENTER)
    table_account.column("Employee",width=100,anchor=CENTER)

    table_account.column("First_Name",width=0,stretch=False)
    table_account.column("Last_Name",width=0,stretch=False)
    table_account.column("Password",width=0,stretch=False)
    table_account.column("Address",width=0,stretch=False)
    table_account.column("Contact",width=0,stretch=False)

    table_account.grid(row=0, column=0, sticky="nsew")

    def select_data(event):
        select = table_account.focus()
        values = table_account.item(select,"values")

        id_employee = values[0]
        id_user = values[1]
        user = values[2]
        password = values[7]
        level = values[3]

        employee = values[4]

        f_name = values[5]
        l_name = values[6]
        
        address = values[8]
        contact = values[9]

        ID.set(id_user)
        USER.set(user)
        PASS.set(password)
        LEVEL.set(level)

        data_employee.configure(state="normal")
        data_employee.delete("0.0","end")

        data_employee.insert("1.0","Employee ID : ","readonly")
        data_employee.insert("1.end",f"{id_employee}\n\n")

        data_employee.insert("3.0",f"Name : ","readonly")
        data_employee.insert("3.end",f"{f_name} {l_name}\n\n")

        data_employee.insert("5.0",f"Contact : ","readonly")
        data_employee.insert("5.end",f"{contact}\n\n")

        data_employee.insert("7.0",f"Address : ","readonly")
        data_employee.insert("7.end",f"{address}\n\n")

        data_employee.configure(state="disabled")

    table_account.bind("<Double-1>", select_data)

    def load_data():
        table_account.delete(*table_account.get_children())
        sql = my_sql.cursor()
        sql.execute("SELECT * FROM stock_list.employee join `stock_list`.`accounts` on `employee`.`account_id` = `accounts`.`id` order by `accounts`.`id` asc;")
        resulte = sql.fetchall()

        for i in resulte:
            id_employee = i[0] 
            id_user = i[1]
            user = i[7]
            level = i[9]
            employee = i[2]

            f_name = i[2]
            l_name = i[3]
            password = i[8]
            address = i[4]
            contact = i[5]

            table_account.insert("",END,values=(id_employee,id_user,user,level,employee,f_name,l_name,password,address,contact))
    load_data()