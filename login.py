from customtkinter import *
import customtkinter
from pathlib import Path
from CTkMessagebox import *
from CTkMenuBar import *
from PIL import Image
import encode_file

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
        
        self.login_ui()
        self.load_data = encode_file.EncodeDecode().load_data()
        self.data = encode_file.EncodeDecode()

        self.host = self.load_data.get("HOST")
        self.user = self.load_data.get("USER")
        self.pwd = self.load_data.get("PASSWORD")
        self.database = self.load_data.get("DATABASE")
        self.time_zone = self.load_data.get("TIME_ZONE")

        self.username = self.load_data.get("USERNAME")
        self.passwords = self.load_data.get("PASSWORD")
        self.remember_me = self.load_data.get("REMEMBER")
        self.pos = self.load_data.get("POS")

        self.file_server = self.load_data.get("Server_File")
        self.file_account = self.load_data.get("Account_File")

        self.account_data = self.data.edit_data(self.file_account,[
            "USERNAME=admin",
            "PASSWORD=1234",
            "REMEMBER=False",
            "POS=1"
        ])

    def login_ui(self):
        self.user = StringVar(value="")
        self.pwd = StringVar(value="")
        self.remember_var = BooleanVar(value=False)

        self.menu = CTkTitleMenu(self)
        self.file_menu = self.menu.add_cascade("File")
        self.file_about = self.menu.add_cascade("About",command=self.about)
        
        self.frameleft = CTkFrame(self, width=400, height=400, fg_color="#3afa80")
        self.frameleft.pack(side=LEFT, fill=BOTH, expand=YES)

        self.img_icon = self.appdir / "icon" / "icon.png"
        self.open_img = Image.open(self.img_icon)

        self.ctk_img_icon = CTkImage(self.open_img, size=(160,160))

        self.label_icon = CTkLabel(self.frameleft, image=self.ctk_img_icon, text="")
        self.label_icon.pack(fill=Y, expand=YES)

        self.frameright = CTkFrame(self, width=340, height=400, fg_color="#FFFFFF")
        self.frameright.pack(side=RIGHT, fill=BOTH, expand=YES)

        self.label_title = CTkLabel(self.frameright, text="Stock List", font=("Bold Arial",45))
        self.label_title.place(relx=0.15, rely=0.1, anchor="nw")

        self.inp_user = CTkEntry(self.frameright, width=300, height=40, placeholder_text="Username",fg_color="transparent",border_width=0,font=("Arial",16))
        self.inp_user.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.inp_pwd = CTkEntry(self.frameright, width=300, height=40, placeholder_text="Password", show="●",fg_color="transparent",border_width=0,font=("Arial",16))
        self.inp_pwd.place(relx=0.5, rely=0.45, anchor=CENTER)

        self.remember = CTkCheckBox(self.frameright, text="Remember")
        self.remember.place(relx=0.15, rely=0.6, anchor="nw")

        self.btn_login = CTkButton(self.frameright, width=200, height=40, text="Login")
        self.btn_login.place(relx=0.9, rely=0.59, anchor="ne")

        self.btn_login.bind("<Enter>", lambda event: self.hover_enter())
        self.btn_login.bind("<Leave>", lambda event: self.hover_leave())

        self.update()

        self.border_bottom(self.inp_user,self.frameright)
        self.border_bottom(self.inp_pwd,self.frameright)

        self.inp_pwd.focus()

        

    def about(self):
        CTkMessagebox(title="About", message="\tProgram : Stock List\n\n\tVersion : 1.0\n\n\tDevelop By August_Tas", icon="info", option_1="OK")

    def border_bottom(self,obj1,obj2):
        p_x = obj1.winfo_x()
        p_y = obj1.winfo_y() + obj1.winfo_height()

        boder = CTkCanvas(obj2,width=300,height=2,bg="black")
        boder.place(x=p_x,y=p_y,anchor="sw",relwidth=.75)

    def hover_enter(self):
        self.config(cursor="hand2")

    def hover_leave(self):
        self.config(cursor="arrow")

if __name__ == "__main__":
    Login = LoginApp("Login",640,480,"#FFFFFF","light")
    Login.resizable(False,False)
    Login.mainloop()