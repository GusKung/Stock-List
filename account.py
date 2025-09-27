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
            self.resizable(False, False)

# //-----------------------------------------------------

    account_gui = CTKUI("Stock List", 650, 400, "#D4D4D4", "light")
    account_gui.attributes("-topmost",True)

    Main_Frame = CTkFrame(account_gui, fg_color="#D4D4D4",border_width=0)
    Main_Frame.pack(fill=BOTH,expand=True)

    scroll_gui = CTkScrollableFrame(Main_Frame,fg_color="#D4D4D4",border_width=0)
    scroll_gui.pack(fill=BOTH,expand=True)

    sql = my_sql.cursor()
    sql.execute("SELECT * FROM stock_list.accounts order by `level` desc;")
    resulte = sql.fetchall()
# //-----------------------------------------------------------------------------------------

    data_user = []
    count = -1
# //-----------------------------------------------------------------------------------------
    
    for i in resulte:

        username = StringVar(scroll_gui,value=i[1])
        password = StringVar(scroll_gui,value=i[2])
        level = StringVar(scroll_gui,value=i[3])

        Frame = CTkFrame(scroll_gui, fg_color="#FFFFFF")
        Frame.pack(padx=20, pady=5,fill=X)

        Username_Label = CTkLabel(Frame,text="Username:",font=("Arial",16),text_color="#000000",bg_color="#FFFFFF")
        Username_Label.grid(row=0,column=0,padx=(20,10),pady=20,sticky="w")

        inp_user = CTkEntry(Frame,placeholder_text="Username",textvariable=username,state="disabled",border_color="#C4C4C4",border_width=2,width=150,height=30,corner_radius=20,fg_color="#FCFCFC",font=("Arial",16),text_color="#3F3F3F")
        inp_user.grid(row=0,column=1,padx=(20,10),pady=20,sticky="w")

        btn_level = CTkComboBox(Frame,width=100,height=30,corner_radius=20,variable=level,fg_color="#FFFFFF",font=("Arial",16),text_color="#000000",values=["1","2","3"],state="disabled")
        btn_level.grid(row=0,column=2,padx=(20,10),pady=20,sticky="e")

        Password_Label = CTkLabel(Frame,text="Password:",font=("Arial",16),text_color="#000000",bg_color="#FFFFFF")
        Password_Label.grid(row=1,column=0,padx=(20,10),pady=20,sticky="w")

        inp_password = CTkEntry(Frame,placeholder_text="Password",textvariable=password,show="●",state="disabled",border_color="#C4C4C4",border_width=2,width=200,height=30,corner_radius=20,fg_color="#FCFCFC",font=("Arial",16),text_color="#3F3F3F")
        inp_password.grid(row=1,column=1,padx=(20,10),pady=20,sticky="w")

        data_user.append({"id":i[0],"username":username.get(),"password":password.get(),"level":level.get()})

        def edit(user,pas,lv,btn,num):
            
            if (user.cget("state") == "disabled"):
                user.configure(state="normal",border_color="#000000",fg_color="#FCFCFC",font=("Arial",16),text_color="#000000")

                pas.configure(state="normal",border_color="#000000",fg_color="#FCFCFC",font=("Arial",16),text_color="#000000")

                lv.configure(state="normal",fg_color="#FFFFFF",font=("Arial",16),text_color="#000000")

                btn.configure(text="Save")
            else:
                user.configure(state="disabled",border_color="#C4C4C4",fg_color="#FCFCFC",font=("Arial",16),text_color="#3F3F3F")

                pas.configure(state="disabled",border_color="#C4C4C4",fg_color="#FCFCFC",font=("Arial",16),text_color="#3F3F3F")

                lv.configure(state="disabled",fg_color="#FFFFFF",font=("Arial",16),text_color="#000000")

                data_user[num]["username"] = user.get()
                data_user[num]["password"] = pas.get()
                data_user[num]["level"] = lv.get()

                btn.configure(text="Edit")
                
        count += 1
        btn_edit = CTkButton(Frame,text="Edit",font=("Arial",16),text_color="#FFFFFF",fg_color="#4B8BBE",hover_color="#306998",width=100,height=40,corner_radius=20)
        btn_edit.configure(command=lambda e_user = inp_user, e_pas = inp_password, e_lv = btn_level , e_btn= btn_edit , e_num=count:edit(e_user,e_pas,e_lv,e_btn,e_num))
        btn_edit.grid(row=1,column=2,padx=(40,10),pady=20,sticky="e")

# //----------------------------------------------------------------------------------------

    btn_add = CTkButton(account_gui,text="Add",font=("Arial",16),text_color="#FFFFFF",fg_color="#38f388",hover_color="#6be59e",width=100,height=40,corner_radius=20,bg_color="#D4D4D4")
    btn_add.pack(pady=(0,10),padx=(20,20),side=LEFT)

    def apply():
        for i in data_user:
            id = int(i["id"])
            user = str(i["username"])
            pas = str(i["password"])
            lv = int(i["level"])

            print(id,user,pas,lv)

            sql = my_sql.cursor()
            sql.execute("SELECT * FROM stock_list.accounts WHERE `id` = '%d' AND `username` = '%s' AND `passwords` = '%s' AND `level` = '%d' ;" % (id,user,pas,lv))
            resulte = sql.fetchall()
            if (resulte):
                pass
            else:
                sql.execute("UPDATE stock_list.accounts SET `username` = '%s' , `passwords` = '%s' , `level` = '%d' WHERE `id` = '%d' ;" % (user,pas,lv,id))
                my_sql.commit()
                Message = CTkMessagebox(title="Success",message="Update Success",icon="check",option_1="OK")
                if (Message.get() == "OK"):
                    account_gui.destroy()

    btn_apply= CTkButton(account_gui,text="Apply",font=("Arial",16),text_color="#FFFFFF",fg_color="#38f388",hover_color="#6be59e",width=100,height=40,corner_radius=20,bg_color="#D4D4D4",command=apply)
    btn_apply.pack(pady=(0,10),padx=(20,20),side=RIGHT)

    