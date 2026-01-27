from customtkinter import *
import customtkinter
from pathlib import Path
from CTkMessagebox import *
from CTkMenuBar import *
from PIL import Image
import encode_file
import database
import top_gui
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

        self.db = database.Database_Mysql(self.host,self.user,self.pwd,self.database,self.time_zone)
        self.connect = self.db.connect_db()

        self.top_ui = top_gui

        self.login_ui()

        if (self.connect):
            self.text_alert("Success","Database Connected Successfully","check")
            self.top_ui.connect_ui()

        
        print(self.host,self.user,self.pwd,self.database,self.time_zone)

    def login_ui(self):
        self.user_str = StringVar(value="")
        self.pwd_str = StringVar(value="")
        self.remember_bol = BooleanVar(value=self.remember_me)

        self.menu = CTkTitleMenu(self)
        self.file_menu = self.menu.add_cascade("Connect")
        self.file_about = self.menu.add_cascade("About",command=lambda:self.text_alert("About","Program : Stock List\n\nVersion : 1.0\n\nDevelop By August_Tas","info"))
        
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

        self.inp_pwd = CTkEntry(frameright, width=300, height=40, placeholder_text="Password", show="●",fg_color="transparent",border_width=0,font=("Arial",16) , textvariable=self.pwd_str)
        self.inp_pwd.place(relx=0.5, rely=0.45, anchor=CENTER)

        line_pwd = CTkFrame(frameright, width=300, height=2, fg_color="black")
        line_pwd.place(relx=0.5, rely=0.49, anchor=CENTER)

        self.remember = CTkCheckBox(frameright, text="Remember", variable=self.remember_bol)
        self.remember.place(relx=0.15, rely=0.6, anchor="nw")

        self.btn_login = CTkButton(frameright, width=200, height=40, text="Login",command=self.login)
        self.btn_login.place(relx=0.9, rely=0.59, anchor="ne")

        self.btn_login.bind("<Enter>", lambda event: self.hover_enter())
        self.btn_login.bind("<Leave>", lambda event: self.hover_leave())

        self.inp_pwd.focus()

        if (self.remember == True):
            self.inp_user.insert(0,self.username)
            self.inp_pwd.insert(0,self.passwords)
        else:
            self.inp_user.delete(0,END)
            self.inp_pwd.delete(0,END)

    def login(self):
        username = self.inp_user.get()
        password = self.inp_pwd.get()
        btn_rem = self.remember.get()
        
    def text_alert(self,title,message,icon):
        CTkMessagebox(title=f"{title}", message=f"{message}", icon=f"{icon}", option_1="OK")


    def hover_enter(self):
        self.config(cursor="hand2")

    def hover_leave(self):
        self.config(cursor="arrow")

if __name__ == "__main__":
    Login = LoginApp("Login",640,480,"#FFFFFF","light")
    Login.resizable(False,False)
    Login.mainloop()