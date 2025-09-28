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

    data_list = []
    
    count = -1
# //-----------------------------------------------------------------------------------------
    
    for i in resulte:
        data_user = {}
        id = i[0]
        data_user["id"] = id
        username = StringVar(scroll_gui,value=i[1])
        password = StringVar(scroll_gui,value=i[2])
        level = StringVar(scroll_gui,value=i[3])

        Frame = CTkFrame(scroll_gui, fg_color="#FFFFFF")
        Frame.pack(padx=20, pady=5,fill=X)

        Username_Label = CTkLabel(Frame,text="Username:",font=("Arial",16),text_color="#000000",bg_color="#FFFFFF")
        Username_Label.grid(row=0,column=0,padx=(20,10),pady=20,sticky="w")

        data_user["inp_user"] = CTkEntry(Frame,placeholder_text="Username",textvariable=username,state="disabled",border_color="#C4C4C4",border_width=2,width=150,height=30,corner_radius=20,fg_color="#FCFCFC",font=("Arial",16),text_color="#3F3F3F")
        data_user["inp_user"].grid(row=0,column=1,padx=(20,10),pady=20,sticky="w")

        data_user["btn_level"] = CTkComboBox(Frame,width=100,height=30,corner_radius=20,variable=level,fg_color="#FFFFFF",font=("Arial",16),text_color="#000000",values=["1","2","3"],state="disabled")
        data_user["btn_level"].grid(row=0,column=2,padx=(20,10),pady=20,sticky="e")

        Password_Label = CTkLabel(Frame,text="Password:",font=("Arial",16),text_color="#000000",bg_color="#FFFFFF")
        Password_Label.grid(row=1,column=0,padx=(20,10),pady=20,sticky="w")

        data_user["inp_password"] = CTkEntry(Frame,placeholder_text="Password",textvariable=password,show="●",state="disabled",border_color="#C4C4C4",border_width=2,width=200,height=30,corner_radius=20,fg_color="#FCFCFC",font=("Arial",16),text_color="#3F3F3F")
        data_user["inp_password"].grid(row=1,column=1,padx=(20,10),pady=20,sticky="w")

        data_list.append(data_user)

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

                # print( num, user.get(), pas.get(), lv.get())

                data_list[num]["inp_user"].delete(0, 'end')
                data_list[num]["inp_user"].insert(0,user.get())

                data_list[num]["inp_password"].delete(0, 'end')
                data_list[num]["inp_password"].insert(0,pas.get())

                data_list[num]["btn_level"].set(lv.get())

                # print( data_list[num]["id"],data_list[num]["inp_user"].get(), data_list[num]["inp_password"].get() , data_list[num]["btn_level"].get())

                btn.configure(text="Edit")
                
        count += 1

        data_user["btn_edit"] = CTkButton(Frame,text="Edit",font=("Arial",16),text_color="#FFFFFF",fg_color="#4B8BBE",hover_color="#306998",width=100,height=40,corner_radius=20)
        data_user["btn_edit"].configure(command=lambda e_user = data_user["inp_user"], e_pas = data_user["inp_password"], e_lv = data_user["btn_level"] , e_btn= data_user["btn_edit"] , e_num=count:edit(e_user,e_pas,e_lv,e_btn,e_num))
        data_user["btn_edit"].grid(row=1,column=2,padx=(40,10),pady=20,sticky="e")

        btn_remove = CTkButton(Frame,width=40,height=30,corner_radius=20,text="Remove",text_color="white",fg_color="#f33838",hover_color="#f66b6b")
        btn_remove.grid(row=1,column=3,padx=(0,20),pady=(0,80),sticky="nse")

# //----------------------------------------------------------------------------------------
    re_count = 0
    new_count = count
    def add_tarck():
# //-----------------------------------------------------------------------------------------
        new_data_list = []
        nonlocal re_count, new_count
# //-----------------------------------------------------------------------------------------
        new_data_user = {}
        username = StringVar(scroll_gui,value="")
        password = StringVar(scroll_gui,value="")
        level = StringVar(scroll_gui,value="")

        Frame = CTkFrame(scroll_gui, fg_color="#FFFFFF")
        Frame.pack(padx=20, pady=5,fill=X)

        Username_Label = CTkLabel(Frame,text="Username:",font=("Arial",16),text_color="#000000",bg_color="#FFFFFF")
        Username_Label.grid(row=0,column=0,padx=(20,10),pady=20,sticky="w")

        new_data_user["inp_user"] = CTkEntry(Frame,placeholder_text="Username",textvariable=username,state="normal",border_color="#000000",fg_color="#FCFCFC",font=("Arial",16),text_color="#000000",corner_radius=20)
        new_data_user["inp_user"].grid(row=0,column=1,padx=(20,10),pady=20,sticky="w")

        new_data_user["btn_level"] = CTkComboBox(Frame,width=100,height=30,corner_radius=20,variable=level,values=["1","2","3"],state="normal",fg_color="#FFFFFF",font=("Arial",16),text_color="#000000")
        new_data_user["btn_level"].grid(row=0,column=2,padx=(20,10),pady=20,sticky="e")

        Password_Label = CTkLabel(Frame,text="Password:",font=("Arial",16),text_color="#000000",bg_color="#FFFFFF")
        Password_Label.grid(row=1,column=0,padx=(20,10),pady=20,sticky="w")

        new_data_user["inp_password"] = CTkEntry(Frame,placeholder_text="Password",textvariable=password,show="●",state="normal",border_color="#000000",fg_color="#FCFCFC",font=("Arial",16),text_color="#000000",border_width=2,width=200,height=30,corner_radius=20)
        new_data_user["inp_password"].grid(row=1,column=1,padx=(20,10),pady=20,sticky="w")

        new_data_list.append(new_data_user)

        def edit(user,pas,lv,btn,num,new_num):
            
            if (user.cget("state") == "disabled"):
                user.configure(state="normal",border_color="#000000",fg_color="#FCFCFC",font=("Arial",16),text_color="#000000")

                pas.configure(state="normal",border_color="#000000",fg_color="#FCFCFC",font=("Arial",16),text_color="#000000")

                lv.configure(state="normal",fg_color="#FFFFFF",font=("Arial",16),text_color="#000000")

                btn.configure(text="Save")
            else:
                user.configure(state="disabled",border_color="#C4C4C4",fg_color="#FCFCFC",font=("Arial",16),text_color="#3F3F3F")

                pas.configure(state="disabled",border_color="#C4C4C4",fg_color="#FCFCFC",font=("Arial",16),text_color="#3F3F3F")

                lv.configure(state="disabled",fg_color="#FFFFFF",font=("Arial",16),text_color="#000000")

                # new_data_list[num]["inp_user"].delete(0, 'end')
                # new_data_list[num]["inp_user"].insert(0,user.get())

                # new_data_list[num]["inp_password"].delete(0, 'end')
                # new_data_list[num]["inp_password"].insert(0,pas.get())

                # new_data_list[num]["btn_level"].set(lv.get())

                data_list.append(new_data_list[num])
                print(data_list[new_num]["inp_user"].get(), data_list[new_num]["inp_password"].get() , data_list[new_num]["btn_level"].get() )

                btn.configure(text="Edit")
                
        new_count += 1

        print(new_count)
        print(re_count)

        new_data_user["btn_edit"] = CTkButton(Frame,text="Save",font=("Arial",16),text_color="#FFFFFF",fg_color="#4B8BBE",hover_color="#306998",width=100,height=40,corner_radius=20)
        new_data_user["btn_edit"].configure(command=lambda e_user = new_data_user["inp_user"], e_pas = new_data_user["inp_password"], e_lv = new_data_user["btn_level"] , e_btn= new_data_user["btn_edit"] , e_num=re_count,e_newnum = new_count:edit(e_user,e_pas,e_lv,e_btn,e_num,e_newnum))
        new_data_user["btn_edit"].grid(row=1,column=2,padx=(40,10),pady=20,sticky="e")

        btn_remove = CTkButton(Frame,width=40,height=30,corner_radius=20,text="Remove",text_color="white",fg_color="#f33838",hover_color="#f66b6b")
        btn_remove.grid(row=1,column=3,padx=(0,20),pady=(0,80),sticky="nse")

    # //----------------------------------------------------------------------------------------

    btn_add = CTkButton(account_gui,command=add_tarck,text="Add",font=("Arial",16),text_color="#FFFFFF",fg_color="#38f388",hover_color="#6be59e",width=100,height=40,corner_radius=20,bg_color="#D4D4D4")
    btn_add.pack(pady=(0,10),padx=(20,20),side=LEFT)

    def apply():
        for i in data_list:
            try:
                id = int(i["id"])
                user = str(i["inp_user"].get())
                pas = str(i["inp_password"].get())
                lv = int(i["btn_level"].get())

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
            except KeyError as e:
                id = ""
                user = str(i["inp_user"].get())
                pas = str(i["inp_password"].get())
                lv = int(i["btn_level"].get())

                print(id,user,pas,lv)

    btn_apply= CTkButton(account_gui,text="Apply",font=("Arial",16),text_color="#FFFFFF",fg_color="#38f388",hover_color="#6be59e",width=100,height=40,corner_radius=20,bg_color="#D4D4D4",command=apply)
    btn_apply.pack(pady=(0,10),padx=(20,20),side=RIGHT)

    