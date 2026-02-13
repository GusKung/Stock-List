from customtkinter import *
import customtkinter
from pathlib import Path
from CTkMessagebox import *
from CTkMenuBar import *
from CTkScrollableDropdown import CTkScrollableDropdown
from PIL import Image
import encode_file

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

    def add_products_ui(self):
        self.title(f"Add Products")
        screen_x = self.winfo_screenwidth()
        screen_y = self.winfo_screenheight()

        x = int((screen_x / 2) - (700/2))
        y = int((screen_y / 2) - (400 / 2))
        self.geometry(f"{700}x{400}+{x}+{y-25}")

        icon = self.appdir / "icon" / "icon.ico"
        
        self.iconbitmap(icon)
        self.after(200, lambda: self.iconbitmap(icon))
        self.deiconify()
        self.resizable(False,False)

        Frame_Scroll = CTkScrollableFrame(self)
        Frame_Scroll.pack(fill=BOTH,expand=True) 

        self.upload_products = {}

        Frame_Center = CTkFrame(Frame_Scroll,width=400,height=400,corner_radius=0,fg_color="#FFFFFF")
        Frame_Center.pack(fill=X,pady=(10,0))

        Frame_Center.grid_columnconfigure(1, weight=1)  
        Frame_Center.grid_columnconfigure(2, weight=1)  

        add_dir = Path(__file__).parent
        img_path = add_dir / "icon" / "upload.png"
        img_open = Image.open(img_path)
        img = CTkImage(light_image=img_open,dark_image=img_open,size=(200,200))

        btn_img = CTkButton(Frame_Center,width=200,height=200,text="",image=img,fg_color="#FFFFFF",hover_color="#F7F7F7",corner_radius=0)
        btn_img.grid(rowspan=3,column=0,padx=(10,20),pady=10)

        inp_barcode = CTkEntry(Frame_Center,width=200,height=30,corner_radius=10,placeholder_text="Code",font=("Arial",16))
        inp_barcode.grid(row=0,column=1,sticky="ew")

        inp_name = CTkEntry(Frame_Center,width=200,height=30,corner_radius=10,placeholder_text="Name",font=("Arial",16))
        inp_name.grid(row=0,column=2,padx=(25,10),sticky="ew")

        inp_cost_price = CTkEntry(Frame_Center,width=150,height=30,corner_radius=10,placeholder_text="Cost Price",font=("Arial",16))
        inp_cost_price.grid(row=1,column=1,sticky="ew")

        inp_price = CTkEntry(Frame_Center,width=150,height=30,corner_radius=10,placeholder_text="Price",font=("Arial",16))
        inp_price.grid(row=1,column=2,padx=(25,10),sticky="ew")

        inp_amount = CTkEntry(Frame_Center,width=150,height=30,corner_radius=10,placeholder_text="Amount",font=("Arial",16))
        inp_amount.grid(row=2,column=1,sticky="ew")

        all_type = self.my_sql.all_type()

        inp_type = CTkComboBox(Frame_Center,width=80,values=all_type)
        inp_type.grid(row=2,column=2,padx=(25,10),sticky="ew")

        self.upload_products[Frame_Center] = {
            "img":btn_img,
            "barcode":inp_barcode.get(),
            "name":inp_name.get(),
            "cost_price":inp_cost_price.get(),
            "price":inp_price.get(),
            "amount":inp_amount.get(),
            "type":inp_type.get()
        }

        btn_remove = CTkButton(Frame_Center,width=60,height=30,corner_radius=0,text="Remove",text_color="white",fg_color="#f33838",hover_color="#f66b6b",command=lambda e_obj=Frame_Center:remove(e_obj))
        btn_remove.grid(row=3,column=1,columnspan=2,padx=(0,0),pady=(0,20),sticky="nesw")

        def remove(frame):
            frame.destroy()
            if frame in self.upload_products:
                del self.upload_products[frame]

        def add_track():
            Frame_Center = CTkFrame(Frame_Scroll,width=400,height=400,corner_radius=0,fg_color="#FFFFFF")
            Frame_Center.pack(fill=X,pady=(10,0))

            Frame_Center.grid_columnconfigure(1, weight=1)  
            Frame_Center.grid_columnconfigure(2, weight=1)  

            add_dir = Path(__file__).parent
            img_path = add_dir / "icon" / "upload.png"
            img_open = Image.open(img_path)
            img = CTkImage(light_image=img_open,dark_image=img_open,size=(200,200))

            btn_img = CTkButton(Frame_Center,width=200,height=200,text="",image=img,fg_color="#FFFFFF",hover_color="#F7F7F7",corner_radius=0)
            btn_img.grid(rowspan=3,column=0,padx=(10,20),pady=10)

            inp_barcode = CTkEntry(Frame_Center,width=200,height=30,corner_radius=10,placeholder_text="Code",font=("Arial",16))
            inp_barcode.grid(row=0,column=1,sticky="ew")

            inp_name = CTkEntry(Frame_Center,width=200,height=30,corner_radius=10,placeholder_text="Name",font=("Arial",16))
            inp_name.grid(row=0,column=2,padx=(25,10),sticky="ew")

            inp_cost_price = CTkEntry(Frame_Center,width=150,height=30,corner_radius=10,placeholder_text="Cost Price",font=("Arial",16))
            inp_cost_price.grid(row=1,column=1,sticky="ew")

            inp_price = CTkEntry(Frame_Center,width=150,height=30,corner_radius=10,placeholder_text="Price",font=("Arial",16))
            inp_price.grid(row=1,column=2,padx=(25,10),sticky="ew")

            inp_amount = CTkEntry(Frame_Center,width=150,height=30,corner_radius=10,placeholder_text="Amount",font=("Arial",16))
            inp_amount.grid(row=2,column=1,sticky="ew")

            all_type = self.my_sql.all_type()

            inp_type = CTkComboBox(Frame_Center,width=80,values=all_type)
            inp_type.grid(row=2,column=2,padx=(25,10),sticky="ew")

            self.upload_products[Frame_Center] = {
                "img":btn_img,
                "barcode":inp_barcode.get(),
                "name":inp_name.get(),
                "cost_price":inp_cost_price.get(),
                "price":inp_price.get(),
                "amount":inp_amount.get(),
                "type":inp_type.get()
            }
            btn_remove = CTkButton(Frame_Center,width=60,height=30,corner_radius=0,text="Remove",text_color="white",fg_color="#f33838",hover_color="#f66b6b",command=lambda e_obj=Frame_Center:remove(e_obj))
            btn_remove.grid(row=3,column=1,columnspan=2,padx=(0,0),pady=(0,20),sticky="nesw")

        btn_add = CTkButton(self,font=("Arial",16),width=60,height=30,corner_radius=20,text="Add",text_color="white",fg_color="#38f388",hover_color="#6be59e",command=add_track)
        btn_add.pack(side=LEFT,anchor="sw",padx=10,pady=10)

        btn_upload = CTkButton(self,font=("Arial",16),width=60,height=30,corner_radius=20,text="Upload",text_color="white",fg_color="#38f388",hover_color="#6be59e")
        btn_upload.pack(side=RIGHT,anchor="se",padx=10,pady=10)

    def check_level(self,func,username,passwords,level=2):
        check = self.my_sql.check_level(username,passwords,level)
        if (check == None):
            self.level_ui(func,level)
        else:
            for widget in self.winfo_children():
                widget.destroy()
            func()
            
    
    def level_ui(self,func,level):
        self.title(f"Login")
        screen_x = self.winfo_screenwidth()
        screen_y = self.winfo_screenheight()

        x = int((screen_x / 2) - (480/2))
        y = int((screen_y / 2) - (360 / 2))
        self.geometry(f"{480}x{360}+{x}+{y-25}")

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
        F_Connect.place(relx=0.5, rely=0.5, anchor="center")

        titel = CTkLabel(F_Connect,text="Login",font=("Arial",24),fg_color="#FFFFFF",bg_color="black")
        titel.place(relx=.45,rely=.05)

        inp_user = CTkEntry(master=F_Connect,border_width=2,corner_radius=8,fg_color="#FBFBFB",border_color="#C1C1C1",placeholder_text="Username",width=300,height=40)
        inp_user.place(relx=.14,rely=.25,anchor=NW)

        inp_password = CTkEntry(master=F_Connect,border_width=2,corner_radius=8,fg_color="#FBFBFB",border_color="#C1C1C1",placeholder_text="Password",show="●",width=300,height=40)
        inp_password.place(relx=.14,rely=.49,anchor=NW)

        button_connect = CTkButton(master=F_Connect,corner_radius=20,text="Connect",width=300,height=45,command=lambda:self.check_level(func,inp_user.get(),inp_password.get(),level))
        button_connect.place(relx=.14,rely=.75,anchor=NW)

        inp_password.bind("<Return>",lambda e:self.check_level(func,inp_user.get(),inp_password.get(),level))
