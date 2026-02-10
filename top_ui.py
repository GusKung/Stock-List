from customtkinter import *
import customtkinter
from pathlib import Path
from CTkMessagebox import *
from CTkMenuBar import *
from CTkScrollableDropdown import CTkScrollableDropdown
from PIL import Image
import encode_file
import database

class top_gui(CTkToplevel):
    def __init__(self,db):
        super().__init__()
        self.withdraw()

        self.data = encode_file.EncodeDecode()
        self.load_data = encode_file.EncodeDecode().load_data()

        self.username = self.load_data.get("USERNAME")
        self.passwords = self.load_data.get("PASSWORD")
        self.pos = self.load_data.get("POS")

        self.user_str = StringVar(value="")
        self.passwords_str = StringVar(value="")

        self.amount_page = StringVar(value="0")
        self.types = StringVar(value="ทั้งหมด")

        self.key_search = StringVar(value="")
        self.on_search = BooleanVar(value=False)
        self.on_reset = BooleanVar(value=False)

        self.appdir = Path(__file__).parent

        self.my_sql = db

    def check_level(self,level=2):
        check = self.my_sql.check_level(self.username,level)
        if (check == None):
            lv = False
            self.level_ui("Login",480,360,"#FFFFFF")
        else:
            lv = True
        return lv
    
    def level_ui(self,title,wide,height,color):
        self.title(f"{title}")
        screen_x = self.winfo_screenwidth()
        screen_y = self.winfo_screenheight()

        x = int((screen_x / 2) - (wide/2))
        y = int((screen_y / 2) - (height / 2))
        self.geometry(f"{wide}x{height}+{x}+{y-25}")
        
        self.config(bg=f"{color}")

        icon = self.appdir / "icon" / "icon.ico"
        
        self.iconbitmap(icon)
        self.after(200, lambda: self.iconbitmap(icon))
        self.deiconify()
        self.resizable(False,False)

        open_bg = Image.open(self.appdir /"icon"/"sql_connect.png")
        background_photo = CTkImage(open_bg,size=(500,500))

        background  = CTkLabel(master=self,text="",image=background_photo)
        background.place(x=0,y=0)

        F_Connect = CTkFrame(master=self,fg_color="#FFFFFF",width=420,height=280,corner_radius=0)
        F_Connect.pack(anchor=CENTER,pady=40,expand=NO)

        titel = CTkLabel(F_Connect,text="Login",font=("Arial",24),fg_color="#FFFFFF",bg_color="black")
        titel.place(relx=.45,rely=.05)

        self.inp_user = CTkEntry(master=F_Connect,border_width=2,corner_radius=8,fg_color="#FBFBFB",border_color="#C1C1C1",placeholder_text="Username",width=300,height=40)
        self.inp_user.place(relx=.14,rely=.25,anchor=NW)

        self.inp_password = CTkEntry(master=F_Connect,border_width=2,corner_radius=8,fg_color="#FBFBFB",border_color="#C1C1C1",placeholder_text="Password",show="●",width=300,height=40)
        self.inp_password.place(relx=.14,rely=.49,anchor=NW)

        button_connect = CTkButton(master=F_Connect,corner_radius=20,text="Connect",width=300,height=45)
        button_connect.place(relx=.14,rely=.75,anchor=NW)
    



 