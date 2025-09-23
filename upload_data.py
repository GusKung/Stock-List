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

def gui_upload(my_sql):
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
                self._fg_color = color
                customtkinter.set_appearance_mode(theme)

                appdir = Path(__file__).parent
                icon = appdir / "icon" / "icon.ico"
                
                self.iconbitmap(icon)
                self.after(200, lambda: self.iconbitmap(icon)) 
                self.attributes("-topmost",True)
# //---------------------------------------------------------------------//

    gui = CTKUI("Stock List",700,400,"#D4D4D4","light")

# //-------------------------------------------------------------------------//

    Frame_Scroll = CTkScrollableFrame(gui)
    Frame_Scroll.pack(fill=BOTH,expand=True) 

    data_list = []
    

# //-------------------------------------------------------------------------//

    def add_track():
        data = {}

        Frame_Center = CTkFrame(Frame_Scroll,width=400,height=400,corner_radius=0,fg_color="#FFFFFF")
        Frame_Center.pack(fill=X,pady=(10,0))

        Frame_Center.grid_columnconfigure(1, weight=1)  
        Frame_Center.grid_columnconfigure(2, weight=1)  

        add_dir = Path(__file__).parent
        img_path = add_dir / "icon" / "upload.png"
        img_open = Image.open(img_path)
        img = CTkImage(light_image=img_open,dark_image=img_open,size=(200,200))

        def upload_img():
            gui.attributes("-topmost",False)

            file_path = customtkinter.filedialog.askopenfilename(title="Select Image",filetypes=(("JPG files","*.jpg"),("JPEG files","*.jpeg"),("PNG files","*.png")))
            if (file_path):
                data["img_open"] = Image.open(file_path)

                img = CTkImage(light_image=data["img_open"] ,dark_image=data["img_open"],size=(200,200))
                btn_img.configure(image=img)
                
            gui.attributes("-topmost",True)

        btn_img = CTkButton(Frame_Center,command=upload_img,width=200,height=200,text="",image=img,fg_color="#FFFFFF",hover_color="#F7F7F7",corner_radius=0)
        btn_img.grid(rowspan=3,column=0,padx=(10,20),pady=10)

        data["inp_barcode"] = CTkEntry(Frame_Center,width=200,height=30,corner_radius=10,placeholder_text="Code",font=("Arial",16))
        data["inp_barcode"].grid(row=0,column=1,sticky="ew")

        data["inp_name"] = CTkEntry(Frame_Center,width=200,height=30,corner_radius=10,placeholder_text="Name",font=("Arial",16))
        data["inp_name"].grid(row=0,column=2,padx=(25,10),sticky="ew")

        data["inp_cost_price"] = CTkEntry(Frame_Center,width=150,height=30,corner_radius=10,placeholder_text="Cost Price",font=("Arial",16))
        data["inp_cost_price"].grid(row=1,column=1,sticky="ew")

        data["inp_price"] = CTkEntry(Frame_Center,width=150,height=30,corner_radius=10,placeholder_text="Price",font=("Arial",16))
        data["inp_price"].grid(row=1,column=2,padx=(25,10),sticky="ew")

        data["inp_amount"] = CTkEntry(Frame_Center,width=150,height=30,corner_radius=10,placeholder_text="Amount",font=("Arial",16))
        data["inp_amount"].grid(row=2,column=1,sticky="ew")

        data["btn_remove"] = CTkButton(Frame_Center,width=60,height=30,corner_radius=20,text="Remove",text_color="white",fg_color="#f33838",hover_color="#f66b6b",command=lambda: remove_track(data,Frame_Center))
        data["btn_remove"].grid(row=2,column=2,padx=(25,10),sticky="ew")

        data_list.append(data)
        

    def remove_track(data,frame):
        frame.destroy()
        data_list.remove(data)

    btn_add = CTkButton(gui,font=("Arial",16),command=add_track,width=60,height=30,corner_radius=20,text="Add",text_color="white",fg_color="#38f388",hover_color="#6be59e")
    btn_add.pack(side=LEFT,anchor="sw",padx=10,pady=10)

    def upload(products):
        
        for i in products:
            barcode = str(i["inp_barcode"].get())
            name = str(i["inp_name"].get())
            cost_price = float(i["inp_cost_price"].get())
            price = float(i["inp_price"].get())
            amount = int(i["inp_amount"].get())
            
            sql = my_sql.cursor()

            try:
                sql.execute("INSERT IGNORE products VALUES ('%s', '%s', %.2f, %.2f, %d , %d) " % (barcode, name, cost_price, price, amount,0))
                my_sql.commit()
            except mysql.connector.Error as err:
                CTkMessagebox(gui, title="Error", message=f"Something went wrong: {err}", icon="cancel", option_1="OK")


            try:
                img = i["img_open"]
                rgb_img = img.convert('RGB')
                appdir = Path(__file__).parent
                paths = appdir / "products" / f"{barcode}.jpg"

                rgb_img.save(paths,optimize=True,format='JPEG',quality=10)
            except:
                pass

        btn_message = CTkMessagebox(gui, title="Success", message="Upload Complete", icon="check", option_1="OK")
        if btn_message.get() == "OK":
            gui.destroy()

            

    btn_upload = CTkButton(gui,font=("Arial",16),command=lambda: upload(data_list[:]),width=60,height=30,corner_radius=20,text="Upload",text_color="white",fg_color="#38f388",hover_color="#6be59e")
    btn_upload.pack(side=RIGHT,anchor="se",padx=10,pady=10)

         