from customtkinter import *
import customtkinter
from pathlib import Path
from CTkMessagebox import *
from CTkMenuBar import *

class LoginApp(CTk):
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
        self.menu = CTkTitleMenu(self)
        self.file_menu = self.menu.add_cascade("File")
        def about():
            CTkMessagebox(title="About", message="\tProgram : Stock List\n\n\tVersion : 1.0\n\n\tDevelop By August_Tas", icon="info", option_1="OK")
        self.file_about = self.menu.add_cascade("About",command=about)

if __name__ == "__main__":
    Login = LoginApp("Login",640,480,"#FFFFFF","light")
    Login.resizable(False,False)
    Login.mainloop()