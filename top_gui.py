from customtkinter import *
import customtkinter
from pathlib import Path
from CTkMessagebox import *
from CTkMenuBar import *
from PIL import Image
import encode_file
import database

class TOPGUI(CTkToplevel):
    def __init__(self):
        super().__init__()
        self.withdraw()
        
    def connect_ui(self,title,wide,height,color,theme):

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
    
        self.resizable(False,False)

        appdir = Path(__file__).parent
        photo = appdir / "icon" / "sql_connect.png"
        bg_image = Image.open(photo)
        background_photo= CTkImage(bg_image,size=(500,500))

        background  = CTkLabel(master=self,text="",image=background_photo)
        background.place(x=0,y=0)


        F_Connect = CTkFrame(master=self,width=400,height=300,fg_color="white",bg_color="#3E3E3E")
        F_Connect.pack(anchor=CENTER,pady=30,expand=NO)

        lable_title = CTkLabel(master=F_Connect,font=("Arial",24),text="Connect Server")
        lable_title.place(relx=.3,rely=.05)

        self.inp_host = CTkEntry(master=F_Connect,border_width=2,corner_radius=8,fg_color="#FBFBFB",border_color="#C1C1C1",placeholder_text="Host",width=300,height=40)
        self.inp_host.place(relx=.12,rely=.2,anchor=NW)

        self.inp_user = CTkEntry(master=F_Connect,border_width=2,corner_radius=8,fg_color="#FBFBFB",border_color="#C1C1C1",placeholder_text="Username",width=300,height=40)
        self.inp_user.place(relx=.12,rely=.4,anchor=NW)

        self.inp_password = CTkEntry(master=F_Connect,border_width=2,corner_radius=8,fg_color="#FBFBFB",border_color="#C1C1C1",placeholder_text="Password",show="●",width=300,height=40)
        self.inp_password.place(relx=.12,rely=.6,anchor=NW)

        # inp_password.bind("<Return>",lambda e:connect())

        self.button_connect = CTkButton(master=F_Connect,corner_radius=20,text="Connect",width=300,height=45)
        self.button_connect.place(relx=.12,rely=.8,anchor=NW)

        self.deiconify()

