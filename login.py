from customtkinter import *
from PIL import Image 
import customtkinter
from CTkMenuBar import *
from CTkMessagebox import *
from pathlib import Path
import os 
import mysql.connector
import connect
from cryptography.fernet import Fernet
from dotenv import load_dotenv, dotenv_values 
import main

class CTKUI(CTk):
    def __init__(self,titel,wide,height,color,theme):
        CTk.__init__(self)
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

Login = CTKUI("Login",640,480,"#3E3E3E","light")
Login.resizable(False,False)

# ----------------- Menu Items -----------------
menu = CTkTitleMenu(Login)
file_menu = menu.add_cascade("File",fg_color="white")

def about():
    CTkMessagebox(title="About", message="\tProgram : Stock List\n\n\tVersion : 1.0\n\n\tDevelop By August_Tas", icon="info", option_1="OK")

about_menu = menu.add_cascade("About",fg_color="white",postcommand=about)

# ----------------- Menu Dropdown -----------------
dropdown = CustomDropdownMenu(widget=file_menu,bg_color="white",width=100)
dropdown.add_option(option="Connect",command=connect.connect_gui) 
# ----------------------------------------------

FrameLeft = CTkFrame(master=Login,width=300,fg_color="#3afa80",corner_radius=0)
FrameLeft.pack(side=LEFT,fill=Y,expand=NO,ipadx=60)

appdir = Path(__file__).parent
photo = appdir / "icon" / "icon.png"

open_logo = Image.open(photo)

logo_image = CTkImage(light_image=open_logo, dark_image=open_logo , size=(140,140))

logo = CTkLabel(master=FrameLeft,image=logo_image,text="")
logo.pack(fill=Y,expand=YES) 

FrameRight = CTkFrame(Login,fg_color="#FFFFFF",corner_radius=0)
FrameRight.pack(fill=BOTH,expand=YES)

def boder_bottom(gui,obj1,obj2):
    gui.update()
    p_x = obj1.winfo_x() 
    p_y = obj1.winfo_y() + obj1.winfo_height()

    boder = CTkCanvas(obj2,width=400,height=2,bg="black")
    boder.place(x=p_x,y=p_y,anchor="sw",relwidth=.85)

Titel = CTkLabel(FrameRight,text="Stock List",font=("Arial",35))
Titel.place(x=30,y=40)

USER = StringVar(value="")
PASS = StringVar(value="")

inp_username = CTkEntry(FrameRight,placeholder_text="Username",textvariable=USER,width=350,height=35,corner_radius=14,fg_color="transparent",border_width=0,font=("Arial",16))
inp_username.place(x=30,y=120)
boder_bottom(Login,inp_username,FrameRight)

inp_pass = CTkEntry(FrameRight,placeholder_text="Password",show="●",textvariable=PASS,width=350,height=35,corner_radius=14,fg_color="transparent",border_width=0,font=("Arial",16))
inp_pass.place(x=30,y=200)

Login.update()
inp_pass.focus_set()

boder_bottom(Login,inp_pass,FrameRight)

# //------------------------------------------------------------//

mydoc = os.path.expanduser('~\\Documents')

localfile = mydoc + "\\Stock_List"
file_server = localfile+"\\Server.env"
file_account = localfile + "\\Account.env"

check_file_serrver = os.path.exists(file_server)
check_file_account = os.path.exists(file_account)

appdir = Path(__file__).parent
mykey = appdir / "mykey.key"

with open(mykey) as k:
    key = k.read()

fer = Fernet(key)


if (check_file_serrver and check_file_account):
    with open(file_server,"rb") as encode_file:
        decode = encode_file.read()

    decode_file = fer.decrypt(decode)

    with open(file_server,"wb") as original_file:
        original_file.write(decode_file)

    load_dotenv(file_server)
            
    host = os.getenv("Host")
    user = os.getenv("User")
    password = os.getenv("Passwords")

    with open(file_server,"rb") as original_file:
            original = original_file.read()
    
    encode = fer.encrypt(original)
    with open(file_server,"wb") as encode_file:
        encode_file.write(encode)

    try:
        try:
            connect_server = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = "stock_list" )
            sql = connect_server.cursor()
            
            connect_success = CTkMessagebox(title="Connect Server",message="Connected successfully",icon="check",option_1="Ok")
            
        except:
            connect_server = mysql.connector.connect(
            host = host,
            user = user,
            password = password)
            sql = connect_server.cursor()
            appdir = Path(__file__).parent
            file = appdir / "stock_list.sql"

            with open(file,"r",encoding="utf-8") as f:
                sql.execute(f.read())
            connect_success = CTkMessagebox(title="Connect Server",message="Connected successfully",icon="check",option_1="Ok")
            
    except:
        error = CTkMessagebox(title="Connect Server",message="Failed to connect",icon="cancel",option_1="Ok")
        if (error.get() == "Ok"):
            connect.connect_gui()
else:
    
    os.mkdir(localfile)
    server = [
        "Host=localhost",
        "User=root",
        "Passwords="
        ]
    
    account = [
        "Account_User=admin",
        "Account_Passwords=1234",
        "OnOff=0"
    ]
    
    with open(file_server,"w",newline="") as f:
        f.write(f"{server[0]}\n{server[1]}\n{server[2]}")

    with open(file_account,"w",newline="") as f:
        f.write(f"{account[0]}\n{account[1]}\n{account[2]}")

    load_dotenv(file_server)

    host = os.getenv("Host")
    user = os.getenv("User")
    password = os.getenv("Passwords")


    with open(file_server,"rb") as original_file:
        original = original_file.read()
    
    encode = fer.encrypt(original)
    with open(file_server,"wb") as encode_file:
        encode_file.write(encode)

    with open(file_account,"rb") as original_file:
        original = original_file.read()
    
    encode = fer.encrypt(original)

    with open(file_account,"wb") as encode_file:
        encode_file.write(encode)
    try:
        try:
            connect_server = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = "stock_list" )
            sql = connect_server.cursor()
            
            connect_success = CTkMessagebox(title="Connect Server",message="Connected successfully",icon="check",option_1="Ok")
            
        except:
            connect_server = mysql.connector.connect(
            host = host,
            user = user,
            password = password)
            sql = connect_server.cursor()
            appdir = Path(__file__).parent
            file = appdir / "stock_list.sql"
            with open(file,"r",encoding="utf-8") as f:
                sql.execute(f.read())
            
            connect_success = CTkMessagebox(title="Connect Server",message="Connected successfully",icon="check",option_1="Ok")
            
    except:
        error = CTkMessagebox(title="Connect Server",message="Failed to connect",icon="cancel",option_1="Ok")
        if (error.get() == "Ok"):
            connect.connect_gui()

def login_connect():
    username = inp_username.get()
    passwords = inp_pass.get()
    btn = btn_remember.get()

    try:
        # connect_server.config(database = "stock_list")
        # connect_server.reconnect()
        sql.execute("SELECT * FROM `accounts` WHERE `username` = %s AND `passwords` = %s AND `onlines` = 0" , (username,passwords))
        result = sql.fetchone()
    

        if (username == "" or passwords == ""):

            CTkMessagebox(title="Error",message="Please fill in all fields",icon="cancel",option_1="Ok")
        
        elif (result):
            onlines = sql.execute("Update `accounts` SET `onlines` = 1 WHERE `username` = %s" , (username,))
            connect_server.commit()
        
            Login.withdraw()
            main.main_gui(connect_server,username,passwords)
        else:
            error = CTkMessagebox(title="Error",message="The password is incorrect or someone has already connected to this account.",icon="cancel",option_1="Ok")
            if(error.get() == "Ok"):
                onlines = sql.execute("Update `accounts` SET `onlines` = 0 WHERE `username` = %s" , (username,))
                connect_server.commit()
    except:
        try:
            connect.connect_login(username,passwords,Login,connect_server)
        except:
            error = CTkMessagebox(title="Error",message="The program has a problem. Restart the program or notify the developer.",icon="cancel",option_1="Ok")
            if(error.get() == "Ok"):
                onlines = sql.execute("Update `accounts` SET `onlines` = 0 WHERE `username` = %s" , (username,))
                connect_server.commit()
                os._exit(0)


# //--------------------------------------------------------------------

    with open(file_account,"rb") as original_file_account:
        decode = original_file_account.read()
    
    decode_file_account = fer.decrypt(decode)

    with open(file_account,"wb") as original_file_account:
        update =f"Account_User={username}\nAccount_Passwords={passwords}\nOnOff={btn}"
        utf = update.encode("utf-8")
        encode = original_file_account.write(utf)
        
    with open(file_account,"rb") as original_file_account:
        encode_file = original_file_account.read()

    encode = fer.encrypt(encode_file)
    
    with open(file_account,"wb") as encode_file_account:

        encode_file_account.write(encode)


btn_remember = CTkCheckBox(FrameRight,text="Remember",font=("Airal",14))
btn_remember.place(y=300,relx=.22,anchor="center")

btn_login = CTkButton(FrameRight,text="Login",command=login_connect,width=200,height=50,corner_radius=20,fg_color="#0ea0f9",bg_color="transparent",border_width=0,font=("Arial",16))
btn_login.place(y=300,relx=.67,anchor="center")

# //--------------------------------------

inp_pass.bind("<Return>",lambda e:login_connect())

# //--------------------------------------

with open(file_account,"rb") as encode_file_account:
    decode = encode_file_account.read()

decode_file_account = fer.decrypt(decode)

with open(file_account,"wb") as original_file_account:
    encode = original_file_account.write(decode_file_account)


load_dotenv(file_account)

a_user = os.getenv("Account_User")
a_pass = os.getenv("Account_Passwords")
a_on_off = os.getenv("OnOff")

if (int(a_on_off) == 1):
    USER.set(a_user)
    PASS.set(a_pass)
    btn_remember.toggle()
    inp_pass.icursor(END)


with open(file_account,"rb") as original_file_account:
    encode_file = original_file_account.read()

encode = fer.encrypt(encode_file)

with open(file_account,"wb") as encode_file_account:
    encode_file_account.write(encode)

Login.mainloop()

