from customtkinter import *
from PIL import Image
import customtkinter
from CTkMenuBar import *
from pathlib import Path
from CTkMessagebox import *
import mysql.connector
from cryptography.fernet import Fernet
import os 
from dotenv import load_dotenv, dotenv_values 
import main

class TOPGUI(CTkToplevel):
    def __init__(self,title,wide,height,color,theme):
        CTkToplevel.__init__(self)
        self.title(f"{title}")
        screen_x = self.winfo_screenwidth()
        screen_y = self.winfo_screenheight()
        x = int((screen_x / 2) - (wide/2))
        y = int((screen_y / 2) - (height / 2))
        self.geometry(f"{wide}x{height}+{x}+{y-20}")

        self.config(bg=f"{color}")
        customtkinter.set_appearance_mode(theme)

        appdir = Path(__file__).parent
        icon = appdir / "icon" / "icon.ico"
        self.iconbitmap(icon)
        self.after(200, lambda: self.iconbitmap(icon))
    
    def lock(self):
        self.grab_set()

    def unlock(self):
        self.grab_release()

def connect_gui():
    global gui 
    gui = TOPGUI("Connect Server",480,360,"#3E3E3E","light")
    gui.resizable(False,False)
    gui.lock()

    appdir = Path(__file__).parent
    photo = appdir / "icon" / "sql_connect.png"
    bg_image = Image.open(photo)
    background_photo= CTkImage(bg_image,size=(500,500))

    background  = CTkLabel(master=gui,text="",image=background_photo)
    background.place(x=0,y=0)


    F_Connect = CTkFrame(master=gui,width=400,height=300,fg_color="white",bg_color="#3E3E3E")
    F_Connect.pack(anchor=CENTER,pady=30,expand=NO)

    title = CTkLabel(master=F_Connect,font=("Airal",24),text="Connect Server")
    title.place(relx=.3,rely=.05)

    inp_host = CTkEntry(master=F_Connect,border_width=2,corner_radius=8,fg_color="#FBFBFB",border_color="#C1C1C1",placeholder_text="Host",width=300,height=40)
    inp_host.place(relx=.12,rely=.2,anchor=NW)

    inp_user = CTkEntry(master=F_Connect,border_width=2,corner_radius=8,fg_color="#FBFBFB",border_color="#C1C1C1",placeholder_text="Username",width=300,height=40)
    inp_user.place(relx=.12,rely=.4,anchor=NW)

    inp_password = CTkEntry(master=F_Connect,border_width=2,corner_radius=8,fg_color="#FBFBFB",border_color="#C1C1C1",placeholder_text="Password",show="●",width=300,height=40)
    inp_password.place(relx=.12,rely=.6,anchor=NW)

    inp_password.bind("<Return>",lambda e:connect())

    def connect():
        global host,user,password
        host = inp_host.get()
        user = inp_user.get()
        password = inp_password.get()

        connectmysql(host,user,password)



    button_connect = CTkButton(master=F_Connect,corner_radius=20,command=connect,text="Connect",width=300,height=45)
    button_connect.place(relx=.12,rely=.8,anchor=NW)

def connectmysql(host,user,password):

    mydoc = os.path.expanduser('~\\Documents')
    localfile = mydoc + "\\Stock_List"
    file_server = localfile+"\\Server.env"
    file_account = localfile + "\\Account.env"

    appdir = Path(__file__).parent
    mykey = appdir / "mykey.key"

    with open(mykey) as k:
        key = k.read()

    fer = Fernet(key)

    with open(file_server,"rb") as encode_file:
        decode = encode_file.read()

    decode_file = fer.decrypt(decode)

    with open(file_server,"wb") as original_file:
        original_file.write(decode_file)

    server = [
        f"Host={host}",
        f"User={user}",
        f"Passwords={password}"
    ]

    with open(file_server,"w",newline="") as f:
        f.write(f"{server[0]}\n{server[1]}\n{server[2]}")

    with open(file_server,"r",newline="") as r:
        text = r.read()

    with open(file_server,"rb") as original_file:
        original = original_file.read()

    encode = fer.encrypt(original)
    with open(file_server,"wb") as encode_file:
        encode_file.write(encode)


    try:
        try:
            connect = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = "stock_list")

            alert_box = CTkMessagebox(title="Connect Server",message="Connected successfully",icon="check",option_1="Ok")
            if (alert_box.get() == "Ok"):
                gui.destroy()
                # os._exit(0)
        except:
            connect = mysql.connector.connect(
            host = host,
            user = user,
            password = password)

            sql = connect.cursor()
            appdir = Path(__file__).parent
            file = appdir / "stock_list.sql"

            with open(file,"r",encoding="utf-8") as f:
                sql.execute(f.read())

            alert_box = CTkMessagebox(title="Connect Server",message="Connected successfully",icon="check",option_1="Ok")
            if (alert_box.get() == "Ok"):
                gui.destroy()
                # os._exit(0)
    except:
        CTkMessagebox(title="Connect Server",message="Failed to connect",icon="cancel",option_1="Ok")


def connect_login(username,passwords,gui,connect_server):
    connect_server.config(database = "stock_list")
    connect_server.reconnect()
    sql = connect_server.cursor()
    sql.execute("SELECT * FROM `accounts` WHERE `username` = %s AND `passwords` = SHA2(%s,256) AND `onlines` = 0" , (username,passwords))
    result = sql.fetchone()

    if (username == "" or passwords == ""):
        CTkMessagebox(title="Error",message="Please fill in all fields",icon="cancel",option_1="Ok")
    elif (result):
        onlines = sql.execute("Update `accounts` SET `onlines` = 1 WHERE `username` = %s" , (username,))
        connect_server.commit()
        
        gui.withdraw()
        main.main_gui(connect_server,username,passwords)
        
    else:
        error = CTkMessagebox(title="Error",message="The password is incorrect or someone has already connected to this account.",icon="cancel",option_1="Ok")
        if(error.get() == "Ok"):
            onlines = sql.execute("Update `accounts` SET `onlines` = 0 WHERE `username` = %s" , (username,))
            connect_server.commit()
