from customtkinter import *
import customtkinter
from pathlib import Path
from CTkMessagebox import *
from CTkMenuBar import *
from PIL import Image
import encode_file
import database
import main

class LoginApp(CTk):
    def __init__(self,title,width,height,color,theme):
        super().__init__()
        self.title(f"{title}")
        screen_x = self.winfo_screenwidth()
        screen_y = self.winfo_screenheight()
        customtkinter.set_appearance_mode(theme)

        x = int((screen_x / 2) - (width/2))
        y = int((screen_y / 2) - (height / 2))
        self.geometry(f"{width}x{height}+{x}+{y-25}")

        self.configure(fg_color=f"{color}")

        self.appdir = Path(__file__).parent
        self.icon = self.appdir / "icon" / "icon.ico"
        self.iconbitmap(self.icon)
            
        self.data = encode_file.EncodeDecode()
        self.load_data = encode_file.EncodeDecode().load_data()
        self.file_server = self.load_data.get("Server_File")
        self.file_account = self.load_data.get("Account_File")

        self.host = self.load_data.get("HOST")
        self.user = self.load_data.get("USER")
        self.pwd = self.load_data.get("PWD")
        self.database = self.load_data.get("DATABASE")
        self.time_zone = self.load_data.get("TIME_ZONE")

        self.username = self.load_data.get("USERNAME")
        self.passwords = self.load_data.get("PASSWORD")
        self.remember_me = self.load_data.get("REMEMBER")
        self.pos = self.load_data.get("POS")

        self.user_str = StringVar(value="")
        self.passwords_str = StringVar(value="")
        self.remember_bol = BooleanVar(value=self.remember_me)

        self.open_main_ui = None
        self.guest_ui = None

        if (self.remember_bol.get() == True):
            self.user_str.set(self.username)
            self.passwords_str.set(self.passwords)
        else:
            self.user_str.set("")
            self.passwords_str.set("")

        self.my_sql = database.Database_Mysql(self.host,self.user,self.pwd,self.database,self.time_zone)
        self.sql , self.sql_err = self.my_sql.connect_db()


        if (self.sql != None and self.sql.is_connected()):
            mes_box = self.text_alert("Connect Success","Successfully Connected.","check",1,"OK")
            
        else:
            mes_box = self.text_alert("Connect Failed","Please connect again.","cancel",1,"OK")
            if (mes_box == "OK"):
                self.top_connect_ui()
        
        self.login_ui()

        self.protocol("WM_DELETE_WINDOW",self.exit_program)
    
    def top_connect_ui(self):
        if self.open_main_ui == None or not self.open_main_ui.winfo_exists():
            self.open_main_ui = main.main_gui(self.my_sql)

        self.open_main_ui.connect_ui("Connection", 480, 360, "#FFFFFF") 
        self.open_main_ui.attributes('-topmost', True)

    def login_ui(self):  

        self.menu = CTkTitleMenu(self)
        self.file_menu = self.menu.add_cascade("Connect",command=self.top_connect_ui)
        self.file_about = self.menu.add_cascade("About",command=lambda:self.text_alert("About","Program : Stock List\n\nVersion : 1.0\n\nDevelop By August_Tas","info",1,"OK"))
        
        self.frameleft = CTkFrame(self, width=400, height=400, fg_color="#3afa80")
        self.frameleft.pack(side=LEFT, fill=BOTH, expand=YES)

        img_icon = self.appdir / "icon" / "icon.png"
        open_img = Image.open(img_icon)

        ctk_img_icon = CTkImage(open_img, size=(160,160))

        label_icon = CTkLabel(self.frameleft, image=ctk_img_icon, text="")
        label_icon.pack(fill=Y, expand=YES)

        frameright = CTkFrame(self, width=340, height=400, fg_color="#FFFFFF")
        frameright.pack(side=RIGHT, fill=BOTH, expand=YES)

        label_title = CTkLabel(frameright, text="Stock List", font=("Bold Arial",45))
        label_title.place(relx=0.15, rely=0.1, anchor="nw")

        self.inp_user = CTkEntry(frameright, width=300, height=40, placeholder_text="Username",fg_color="transparent",border_width=0,font=("Arial",16) , textvariable=self.user_str)
        self.inp_user.place(relx=0.5, rely=0.3, anchor=CENTER)

        line_user = CTkFrame(frameright, width=300, height=2, fg_color="black")
        line_user.place(relx=0.5, rely=0.34, anchor=CENTER)

        self.inp_pwd = CTkEntry(frameright, width=300, height=40, placeholder_text="Password", show="●",fg_color="transparent",border_width=0,font=("Arial",16) , textvariable=self.passwords_str)
        self.inp_pwd.place(relx=0.5, rely=0.45, anchor=CENTER)

        line_pwd = CTkFrame(frameright, width=300, height=2, fg_color="black")
        line_pwd.place(relx=0.5, rely=0.49, anchor=CENTER)

        self.remember = CTkCheckBox(frameright, text="Remember", variable=self.remember_bol)
        self.remember.place(relx=0.15, rely=0.6, anchor="nw")

        self.btn_login = CTkButton(frameright, corner_radius=20 ,width=200, height=40, text="Login",command=self.login)
        self.btn_login.place(relx=0.9, rely=0.58, anchor="ne")

        self.inp_pwd.bind("<Return>",lambda e: self.login())
        
        self.after(500, lambda: self.inp_pwd.focus_force())

    def login(self):
        username = self.inp_user.get()
        passwords = self.inp_pwd.get()
        btn_rem = self.remember.get()

        login_sytem = self.my_sql.Login(username,passwords)
        if (login_sytem):
            self.username = username
            self.passwords = passwords

            account = [
            f"USERNAME={username}",
            f"PASSWORD={passwords}",
            f"REMEMBER={btn_rem}",
            f"POS={self.pos}"
            ]

            self.withdraw()
            
            self.data.edit_data(self.file_account,account)
            if (self.open_main_ui is None or not self.open_main_ui.winfo_exists() or self.guest_ui is None or not self.guest_ui.winfo_exists()):
                self.open_main_ui = main.main_gui(self.my_sql)

            self.open_main_ui.main_ui("Stock List", 1280, 720, "#D4D4D4") 

            self.open_main_ui.protocol("WM_DELETE_WINDOW",self.exit_program)
            self.menu.destroy()

        else:
            mes_box = self.text_alert("Login Failed","Please login again.","cancel",1,"OK")
    
    def exit_program(self):
        try:
            self.my_sql.Log_Out(self.username)
        except:
            pass
        self.quit()


    def text_alert(self,title,message,icon,btn,text_btn1,text_btn2=""):
        if (btn == 1):
            text = CTkMessagebox(title=f"{title}", message=f"{message}", icon=f"{icon}", option_1=f"{text_btn1}")
        elif (btn == 2):
            text = CTkMessagebox(title=f"{title}", message=f"{message}", icon=f"{icon}", option_1=f"{text_btn1}",option_2=f"{text_btn2}")
        return text.get()

if __name__ == "__main__":
    Login = LoginApp("Login",640,480,"#FFFFFF","light")
    Login.resizable(False,False)

    Login.mainloop()