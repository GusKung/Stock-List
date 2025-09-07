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

def gui_upload():
# //---------------------------------------------------------------------//
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
                self.attributes('-topmost',True)
# //---------------------------------------------------------------------//

    gui = CTKUI("Stock List",700,400,"#D4D4D4","light")
    