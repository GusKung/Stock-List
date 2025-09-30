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

    ID = StringVar(value="")
    USER = StringVar(value="")
    PASS = StringVar(value="")
    LEVEL = StringVar(value="")

    inp_user = CTkEntry(FLeft,placeholder_text="Username",text_color="#818181",textvariable=USER,width=200,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16),state="disabled")
    inp_user.grid(row=0,column=0,pady=(40,10),padx=20)

    inp_level = CTkComboBox(FLeft,values=["1","2","3"],variable=LEVEL,state="disabled",width=100,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16))
    inp_level.grid(row=0,column=1,pady=(40,10),padx=20)

    inp_pass = CTkEntry(FLeft,placeholder_text="Password",text_color="#818181",textvariable=PASS,show="●",width=200,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16),state="disabled")
    inp_pass.grid(row=1,column=0,pady=20,padx=20)

    def edit():
        if (inp_user.cget("state") == "disabled"):
            inp_user.configure(state="normal",text_color="#000000",border_color="#000000",fg_color="#FFFFFF")
            inp_level.configure(state="normal",border_color="#000000",fg_color="#FFFFFF")
            inp_pass.configure(state="normal",text_color="#000000",border_color="#000000",fg_color="#FFFFFF")
            data_employee.configure(state="normal",text_color="#000000",border_color="#8D8D8D",fg_color="#FFFFFF")
            btn_edit.configure(text="Save")
        else:
            inp_user.configure(state="disabled",text_color="#818181",border_color="#8D8D8D",fg_color="#FCFCFC")
            inp_level.configure(state="disabled",border_color="#8D8D8D",fg_color="#FCFCFC")
            inp_pass.configure(state="disabled",text_color="#818181",border_color="#8D8D8D",fg_color="#FCFCFC")
            data_employee.configure(state="disabled",text_color="#818181",border_color="#A7A7A7",fg_color="#FCFCFC")
            btn_edit.configure(text="Edit")

            print(ID.get(),USER.get(),LEVEL.get(),PASS.get())
            print(data_employee.get("1.0","1.end"))
            print(data_employee.get("2.0","2.end"))
            print(data_employee.get("3.0","3.end"))
            print(data_employee.get("4.0","4.end"))


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
    scrollbar.pack(side="right", fill=Y)

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

    table_account.pack(fill=BOTH,expand=True,pady=20,padx=20)

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
        data_employee.insert("1.0",f"Employee ID : {id_employee}\n\n")
        data_employee.insert("2.0",f"Name : {f_name} {l_name}\n\n")
        data_employee.insert("3.0",f"Address : {address}\n\n")
        data_employee.insert("4.0",f"Contact : {contact}\n\n")
        data_employee.configure(state="disabled")

    table_account.bind("<Double-1>", select_data)

    sql = my_sql.cursor()
    sql.execute("SELECT * FROM stock_list.employee join `stock_list`.`accounts` on `employee`.`account_id` = `accounts`.`id` order by `accounts`.`level` desc;")
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
