from customtkinter import *
import customtkinter
from pathlib import Path
from CTkMessagebox import *
from CTkMenuBar import *
from CTkScrollableDropdown import CTkScrollableDropdown
from PIL import Image
import encode_file
import database

class TOPGUI(CTkToplevel):
    def __init__(self):
        super().__init__()
        self.withdraw()

        self.data = encode_file.EncodeDecode()
        self.load_data = encode_file.EncodeDecode().load_data()

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

        self.appdir = Path(__file__).parent

        self.my_sql = database.Database_Mysql(self.host,self.user,self.pwd,self.database,self.time_zone)

        try:
            self.sql , self.sql_err = self.my_sql.connect_db()
        except:
            self.connect_ui("Connection", 480, 360, "#FFFFFF", "light") 
    
        
    def connect_ui(self,title,wide,height,color,theme):

        self.title(f"{title}")
        screen_x = self.winfo_screenwidth()
        screen_y = self.winfo_screenheight()
        x = int((screen_x / 2) - (wide/2))
        y = int((screen_y / 2) - (height / 2))
        self.geometry(f"{wide}x{height}+{x}+{y-20}")

        self.config(bg=f"{color}")
        customtkinter.set_appearance_mode(theme)

        icon = self.appdir / "icon" / "icon.ico"
        self.iconbitmap(icon)
        self.after(200, lambda: self.iconbitmap(icon))
    
        self.resizable(False,False)
        self.deiconify()

        photo = self.appdir / "icon" / "sql_connect.png"
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

        self.inp_password.bind("<Return>",lambda e:self.connect_server())

        self.button_connect = CTkButton(master=F_Connect,corner_radius=20,text="Connect",width=300,height=45,command=self.connect_server)
        self.button_connect.place(relx=.12,rely=.8,anchor=NW)

        

    def connect_server(self):
        host = self.inp_host.get()
        user = self.inp_user.get()
        pwd = self.inp_password.get()
        db = "stock_list.sql"
        timezone = "+07:00"

        self.data = encode_file.EncodeDecode()
        self.file_server = self.data.load_data().get("Server_File")

        database = database.Database_Mysql(host,user,pwd,db,timezone)
        sql , sql_err = database.connect_db()

        if (sql_err is  None):
            if (sql.is_connected()):
                server = [
                    f"HOST={host}",
                    f"USER={user}",
                    f"PWD={pwd}",
                    f"DATABASE={db}",
                    f"TIME_ZONE={timezone}"
                ]

                self.data.edit_data(self.file_server,server)

                mes = CTkMessagebox(title=f"Connect Success",message=f"Congratulations, you have successfully connected.",icon="check",option_1="OK")

                if (mes.get() == "OK"):
                    self.destroy()
        else:
            CTkMessagebox(title=f"Error {sql_err.errno}",message=f"Error {sql_err}",icon="cancel",option_1="OK")

    def main_ui(self,title,wide,height,color,theme):
        self.title(f"{title}")
        screen_x = self.winfo_screenwidth()
        screen_y = self.winfo_screenheight()

        x = int((screen_x / 2) - (wide/2))
        y = int((screen_y / 2) - (height / 2))
        self.geometry(f"{wide}x{height}+{x}+{y-25}")
        
        self.config(bg=f"{color}")
        customtkinter.set_appearance_mode(theme)

        icon = self.appdir / "icon" / "icon.ico"
        
        self.iconbitmap(icon)
        self.after(200, lambda: self.iconbitmap(icon))
        self.deiconify()

        self.amount = 0.0
        self.total = 0.0

        FLeft= CTkFrame(self,fg_color="#D4D4D4",corner_radius=0,border_color="black",border_width=0)
        FLeft.pack(side=LEFT,fill=BOTH,expand=True)
        FLeft.columnconfigure(1,weight=1)
        FLeft.rowconfigure(1,weight=1)

        FProducts_Scroll = CTkScrollableFrame(FLeft,width=650,height=600,fg_color="#D4D4D4",corner_radius=0)
        FProducts_Scroll.grid(row=1,column=0,columnspan=3,sticky="news")

        self.obj_products = {}
        self.data_products = {}

        def get_value_products(r,c):
            id = self.data_products[r,c]["id"]
            name = self.data_products[r,c]["name"]
            price = self.data_products[r,c]["price"]

            self.inp_product.insert(0,id)
            self.show_order(id,name,price)
            

        for rows in range(10):
            FProducts_Scroll.grid_rowconfigure(rows,weight=1)
            for col in range(4):
                
                FProducts_Scroll.grid_columnconfigure(col,weight=1)

                FProducts = CTkFrame(FProducts_Scroll,fg_color="white",corner_radius=10)
                FProducts.grid(row=rows,column=col , padx=2, pady=2, sticky="nsew")

                L_img = CTkLabel(FProducts,text="",width=150,height=200)
                L_img.pack()
            

                L_img.bind("<Enter>", lambda e: self.hover_enter(FProducts,0,0)) 
                L_img.bind("<Leave>", lambda e: self.hover_leave(FProducts,0,0))

                self.obj_products[rows,col] = {
                    "frame":FProducts,
                    "label":L_img
                }
        
                L_img.bind("<Button-1>", lambda e, r=rows,c=col: get_value_products(r,c))
        
        # self.show_products("ทั้งหมด",0,False)


        btn_next = CTkButton(FLeft,font=("Arial Bold",18),text=">",text_color="black",width=65,height=40,corner_radius=12,fg_color="#38f388",hover_color="#6be59e")
        btn_next.grid(row=2,column=1,sticky="SE",pady=20,padx=(0,100))

        btn_next.bind("<Enter>", lambda e: self.hover_enter(btn_next,70,45)) 
        btn_next.bind("<Leave>", lambda e: self.hover_leave(btn_next,65,40))

        btn_last_next = CTkButton(FLeft,font=("Arial Bold",18),text=">>",text_color="black",width=65,height=40,corner_radius=12,fg_color="#38f388",hover_color="#6be59e")
        btn_last_next.grid(row=2,column=1,sticky="SE",pady=20,padx=(0,20))

        btn_last_next.bind("<Enter>", lambda e: self.hover_enter(btn_last_next,70,45)) 
        btn_last_next.bind("<Leave>", lambda e: self.hover_leave(btn_last_next,65,40))

        btn_back = CTkButton(FLeft,font=("Arial Bold",18),text="<<",text_color="black",width=65,height=40,corner_radius=12,fg_color="#38f388",hover_color="#6be59e")
        btn_back.grid(row=2,column=0,sticky="SW",pady=20,padx=(20,0))

        btn_back.bind("<Enter>", lambda e: self.hover_enter(btn_back,70,45)) 
        btn_back.bind("<Leave>", lambda e: self.hover_leave(btn_back,65,40)) 

        btn_last_back = CTkButton(FLeft,font=("Arial Bold",18),text="<",text_color="black",width=65,height=40,corner_radius=12,fg_color="#38f388",hover_color="#6be59e")
        btn_last_back.grid(row=2,column=0,sticky="SW",pady=20,padx=(100,0))

        btn_last_back.bind("<Enter>", lambda e: self.hover_enter(btn_last_back,70,45)) 
        btn_last_back.bind("<Leave>", lambda e: self.hover_leave(btn_last_back,65,40)) 

        self.inp_product = CTkEntry(FLeft,font=("Arial Bold",14),width=250,corner_radius=20,border_color="#3B3B3B")

        self.inp_product.grid(row=0, column=0,padx=(20,10),pady=20,sticky="WE")

        file_icon = self.appdir / "icon"

        open_search_icon = Image.open(file_icon/"search.png")
        search_icon = CTkImage(light_image=open_search_icon,dark_image=open_search_icon,size=(20,20))

        open_re_icon = Image.open(file_icon/"restart.png")
        re_icon = CTkImage(light_image=open_re_icon,dark_image=open_re_icon,size=(20,20))

        button_product = CTkButton(FLeft,font=("Arial Bold",16),width=60,height=30,corner_radius=20,image=search_icon,text="",text_color="white",fg_color="#38f388",hover_color="#6be59e")
        button_product.grid(row=0,column=1,padx=5,sticky="W")

        button_product.bind("<Enter>", lambda e: self.hover_enter(button_product,65,35)) 
        button_product.bind("<Leave>", lambda e: self.hover_leave(button_product,60,30)) 

        button_re = CTkButton(FLeft,font=("Arial Bold",16),width=60,height=30,corner_radius=20,text="",image=re_icon,text_color="white",fg_color="#38f388",hover_color="#6be59e")
        button_re.grid(row=0,column=1,padx=80,sticky="W")

        button_re.bind("<Enter>", lambda e: self.hover_enter(button_re,65,35)) 
        button_re.bind("<Leave>", lambda e: self.hover_leave(button_re,60,30)) 

        button_add = CTkButton(FLeft,font=("Arial Bold",16),width=60,height=30,corner_radius=20,text="+",text_color="black",fg_color="#38f388",hover_color="#6be59e")
        button_add.grid(row=0,column=1,padx=(0,20),sticky="E")

        button_add.bind("<Enter>", lambda e: self.hover_enter(button_add,65,35)) 
        button_add.bind("<Leave>", lambda e: self.hover_leave(button_add,60,30)) 

        FRight= CTkFrame(self,corner_radius=0,border_width=0,border_color="black",width=600)
        FRight.pack(side=RIGHT,fill=BOTH)
        FRight.pack_propagate(False)

        Fbill_Scroll = CTkScrollableFrame(FRight,fg_color="#dfdfdf",border_width=0,border_color="black",width=600)
        Fbill_Scroll.pack(fill=BOTH,expand=True)

        FBottom= CTkFrame(FRight,fg_color="#1DF38F",corner_radius=0,border_width=0,border_color="black")
        FBottom.pack(side=BOTTOM,fill=BOTH)

        FBottomPay= CTkFrame(FBottom,fg_color="#1DF38F",corner_radius=0,border_width=0,border_color="black")
        FBottomPay.pack(side=BOTTOM,fill=BOTH)

        FBottomPay.columnconfigure(0,weight=1)
        FBottomPay.columnconfigure(1,weight=1)

        FRBLable_name = CTkLabel(FBottom,text="Amount :\n\nTotal :",font=("Arial",24),justify="left")
        FRBLable_name.pack(side=LEFT,anchor="nw",padx=20,pady=20)

        self.FRBLable_price = CTkLabel(FBottom,text=f"{self.amount} \n\n{self.total}",font=("Arial",24),justify="right")
        self.FRBLable_price.pack(side=RIGHT,anchor="nw",padx=20,pady=20)

        pay_cash = CTkButton(FBottomPay,text="Cash",cursor="hand2",text_color="white",width=200,height=60,corner_radius=0,fg_color="#ffad15",hover_color="#e29e45",font=("Arial Bold",24))
        pay_cash.grid(row=0,column=0,sticky="nsew")

        pay_prom = CTkButton(FBottomPay,text="Prompay",cursor="hand2",text_color="white",width=200,height=60,corner_radius=0,fg_color="#264eff",hover_color="#2e5fe6",font=("Arial Bold",24))
        pay_prom.grid(row=0,column=1,sticky="nsew")

        all_row = self.my_sql.all_row("ทั้งหมด")
        self.rows = [f"{i}" for i in range(all_row)]

        amount_page = CTkComboBox(FLeft,width=80,values=self.rows)
        amount_page.grid(row=2,column=0,columnspan=2,sticky="S",pady=25)

        amount_page_scroll = CTkScrollableDropdown(amount_page,justify="left", button_color="transparent",values=self.rows)

        self.all_type = self.my_sql.all_type()

        box_type = CTkComboBox(FLeft,width=100,values=self.all_type) 
        box_type.grid(row=0,column=1,padx=(0,115),sticky="E")

        self.show_products("ทั้งหมด",0,False)

        self.update()

        self.inp_product.focus_set()
        
        # inp_product.bind("<Return>",lambda e:search_product(inp_product.get()))

    def show_products(self,types,num,reset):
        products = self.my_sql.show_products(types,num,reset)

        for i in range(40):
            row = i //4
            col = i % 4
            obj = self.obj_products[row,col]

            if i < len(products):
                p_data = products[i]
                p_id = p_data[0]    
                p_name = p_data[1]  
                p_price = p_data[2] 

                try:
                    open_pimg = Image.open(f"{self.appdir/"products"/p_id}.jpg")
                    pimg = CTkImage(light_image=open_pimg,dark_image=open_pimg,size=(150,200))
                except FileNotFoundError:
                    open_pimg = Image.open(f"{self.appdir/"products"/"Default.jpg"}")
                    pimg = CTkImage(light_image=open_pimg,dark_image=open_pimg,size=(150,200))
                
                obj["label"].configure(image=pimg)

                self.data_products[row,col] = {
                    "id":p_id,
                    "name":p_name,
                    "price":p_price
                }
            else:
                obj["label"].configure(text="",image="") 
                obj["frame"].unbind("<Button-1>")


    def show_order(self,id,name,price):
        self.inp_product.delete(0,END)

        print(id,name,price)          


    def hover_enter(self,obj,w,h):
        self.config(cursor="hand2")
        obj.configure(width=w,height=h)

    def hover_leave(self,obj,w,h):
        self.config(cursor="arrow")
        obj.configure(width=w,height=h)