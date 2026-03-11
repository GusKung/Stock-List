from customtkinter import *
import customtkinter
from pathlib import Path
from CTkMessagebox import *
from CTkMenuBar import *
from CTkScrollableDropdown import CTkScrollableDropdown
from PIL import Image
import encode_file
import database
import top_ui

class main_gui(CTkToplevel):
    def __init__(self, db=None):
        super().__init__()
        self.withdraw()

        self.data = encode_file.EncodeDecode()
        self.load_data = encode_file.EncodeDecode().load_data()

        self.username = self.load_data.get("USERNAME")
        self.passwords = self.load_data.get("PASSWORD")
        self.remember_me = self.load_data.get("REMEMBER")
        self.pos = self.load_data.get("POS")
        self.prompay = self.load_data.get("PROMPAY")
        self.printer = [self.load_data.get("PRINTER_VID"),self.load_data.get("PRINTER_PID"),self.load_data.get("PRINTER_WIDTH")]

        self.amount = 0
        self.price = 0.0
        self.total = 0.0

        self.amount_page = StringVar(value="0")
        self.types = StringVar(value="ทั้งหมด")
        self.price_order = StringVar(value=f"{self.amount}\n\n{self.price}\n\n{self.total}")
        self.price_order_guest = StringVar(value=f"{self.amount}\n\n{self.total}\n\n0.0\n\n0.0")

        self.key_search = StringVar(value="")
        self.on_search = BooleanVar(value=False)
        self.on_reset = BooleanVar(value=False)

        self.appdir = Path(__file__).parent

        self.my_sql = db
        self.open_top_ui = None
        self.open_top_ui2 = None
        self.image_cache = {}
        self.image_cache_order = {}
        default_path = os.path.join(self.appdir, "products", "Default.jpg")

    
        img_raw = Image.open(default_path)
        img_raw.load()
        self.open_pimg_default = CTkImage(img_raw, size=(150, 200))

        self.open_pimg_default_order = CTkImage(img_raw, size=(100, 100))

        open_remove= Image.open(os.path.join(self.appdir, "icon","bin.png"))  
        self.remove_icon = CTkImage(open_remove,size=(30,30))

        
    
    def connect_ui(self,title,wide,height,color):

        self.title(f"{title}")
        screen_x = self.winfo_screenwidth()
        screen_y = self.winfo_screenheight()
        x = int((screen_x / 2) - (wide/2))
        y = int((screen_y / 2) - (height / 2))
        self.geometry(f"{wide}x{height}+{x}+{y-20}")

        self.config(bg=f"{color}")

        icon = os.path.join(self.appdir, "icon","icon.ico")
        self.iconbitmap(icon)
        self.after(200, lambda: self.iconbitmap(icon))
    
        self.resizable(False,False)
        self.deiconify()

        photo = os.path.join(self.appdir, "icon","sql_connect.png")
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

        my_sql = database.Database_Mysql(host,user,pwd,db,timezone)
        sql , sql_err = my_sql.connect_db()

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

    def main_ui(self,title,wide,height,color):
        self.title(f"{title}")
        screen_x = self.winfo_screenwidth()
        screen_y = self.winfo_screenheight()

        x = int((screen_x / 2) - (wide/2))
        y = int((screen_y / 2) - (height / 2))
        self.geometry(f"{wide}x{height}+{x}+{y-25}")
        
        self.config(bg=f"{color}")
        
        self.iconbitmap(os.path.join(self.appdir, "icon","icon.ico"))
        self.after(200, lambda: self.iconbitmap(os.path.join(self.appdir, "icon","icon.ico")))
        self.deiconify()

        printer_vid =self.printer[0]
        printer_pid = self.printer[1]
        printer_width = self.printer[2]

        if (printer_vid == "" or printer_pid == ""):
            if (self.open_top_ui == None or not self.open_top_ui.winfo_exists()):
                self.open_top_ui = top_ui.top_gui(self.my_sql)

            self.open_top_ui.printer_ui()
        
        if (self.prompay == "" or self.prompay == None):
            if (self.open_top_ui2 == None or not self.open_top_ui2.winfo_exists()):
                self.open_top_ui2 = top_ui.top_gui(self.my_sql)

            self.open_top_ui2.audit_ui()

        self.guest_ui = guest_gui(self.price_order_guest)
        self.guest_ui.guest_ui()

        def open_func(func):
            if (self.open_top_ui == None or not self.open_top_ui.winfo_exists()):
                self.open_top_ui = top_ui.top_gui(self.my_sql)

            func()

        menu = CTkMenuBar(master=self)
        stock_menu = menu.add_cascade("Stock",command=lambda:open_func(lambda:self.open_top_ui.check_level(self.open_top_ui.stock_ui,self.username,self.passwords,2)))
        account_menu = menu.add_cascade("Account",command=lambda:open_func(lambda:self.open_top_ui.check_level(self.open_top_ui.account_ui,self.username,self.passwords,3)))
        audit_menu = menu.add_cascade("Audit",command=lambda:open_func(lambda:self.open_top_ui.check_level(self.open_top_ui.audit_ui,self.username,self.passwords,3)))
        printer_menu = menu.add_cascade("Printer",command=lambda:open_func(lambda:self.open_top_ui.printer_ui()))
        pos_menu = menu.add_cascade("POS",command=lambda:open_func(lambda:self.open_top_ui.check_level(self.open_top_ui.pos_ui,self.username,self.passwords,3)))

        FLeft= CTkFrame(self,fg_color="#D4D4D4",corner_radius=0,border_color="black",border_width=0)
        FLeft.pack(side=LEFT,fill=BOTH,expand=True)
        FLeft.columnconfigure(1,weight=1)
        FLeft.rowconfigure(1,weight=1)

        self.FProducts_Scroll = CTkScrollableFrame(FLeft,width=650,height=600,fg_color="#D4D4D4",corner_radius=0)
        self.FProducts_Scroll.grid(row=1,column=0,columnspan=3,sticky="news")
        
        

        self.obj_products = {}

        self.obj_order = []
        self.products_order = {}
        self.data_products = {}

        def get_value_products(r,c):
            id = self.data_products[r,c]["id"]

            self.inp_product.insert(END,id)
            self.inp_products_order(self.inp_product.get())
            

        for col in range(4):
            self.FProducts_Scroll.grid_columnconfigure(col,weight=1)

        for rows in range(10):
            self.FProducts_Scroll.grid_rowconfigure(rows,weight=1)

            for col in range(4):
                FProducts = CTkFrame(self.FProducts_Scroll,fg_color="white",corner_radius=10)
                FProducts.grid(row=rows,column=col , padx=2, pady=2, sticky="nsew")

                L_img = CTkLabel(FProducts,text="",width=150,height=200)
                L_img.pack(expand=True,fill=BOTH)
            

                L_img.bind("<Enter>", lambda e, f=FProducts: self.hover_enter(f, 0, 0)) 
                L_img.bind("<Leave>", lambda e, f=FProducts: self.hover_leave(f, 0, 0))

                self.obj_products[rows,col] = {
                    "frame":FProducts,
                    "label":L_img
                }
        
                L_img.bind("<Button-1>", lambda e, r=rows,c=col: get_value_products(r,c))


        btn_next = CTkButton(FLeft,font=("Arial Bold",18),text=">",text_color="black",width=65,height=40,corner_radius=12,fg_color="#38f388",hover_color="#6be59e",command=self.next_page)
        btn_next.grid(row=2,column=1,sticky="SE",pady=20,padx=(0,100))

        btn_last_next = CTkButton(FLeft,font=("Arial Bold",18),text=">>",text_color="black",width=65,height=40,corner_radius=12,fg_color="#38f388",hover_color="#6be59e",command=self.next_page_last)
        btn_last_next.grid(row=2,column=1,sticky="SE",pady=20,padx=(0,20))

        btn_last_back = CTkButton(FLeft,font=("Arial Bold",18),text="<<",text_color="black",width=65,height=40,corner_radius=12,fg_color="#38f388",hover_color="#6be59e",command=self.back_page_last)
        btn_last_back.grid(row=2,column=0,sticky="SW",pady=20,padx=(20,0))

        btn_back = CTkButton(FLeft,font=("Arial Bold",18),text="<",text_color="black",width=65,height=40,corner_radius=12,fg_color="#38f388",hover_color="#6be59e",command=self.back_page)
        btn_back.grid(row=2,column=0,sticky="SW",pady=20,padx=(100,0))

        self.inp_product = CTkEntry(FLeft,font=("Arial Bold",14),width=250,corner_radius=20,border_color="#3B3B3B")

        self.inp_product.grid(row=0, column=0,padx=(20,10),pady=20,sticky="WE")

        file_icon = os.path.join(self.appdir, "icon") 

        open_search_icon = Image.open(os.path.join(file_icon, "search.png"))
        search_icon = CTkImage(open_search_icon,size=(20,20))

        open_re_icon = Image.open(os.path.join(file_icon, "restart.png")) 
        re_icon = CTkImage(open_re_icon,size=(20,20))

        btn_product = CTkButton(FLeft,font=("Arial Bold",16),width=60,height=30,corner_radius=20,image=search_icon,text="",text_color="white",fg_color="#38f388",hover_color="#6be59e",command=lambda:self.inp_products_order(self.inp_product.get()))
        btn_product.grid(row=0,column=1,padx=5,sticky="W")

        btn_re = CTkButton(FLeft,font=("Arial Bold",16),width=60,height=30,corner_radius=20,text="",image=re_icon,text_color="white",fg_color="#38f388",hover_color="#6be59e",command=self.re_face)
        btn_re.grid(row=0,column=1,padx=80,sticky="W")

        btn_add = CTkButton(FLeft,font=("Arial Bold",16),width=60,height=30,corner_radius=20,text="+",text_color="black",fg_color="#38f388",hover_color="#6be59e",command=self.add_products)
        btn_add.grid(row=0,column=1,padx=(0,20),sticky="E")

        FRight= CTkFrame(self,corner_radius=0,border_width=0,border_color="black",width=600)
        FRight.pack(side=RIGHT,fill=BOTH)
        FRight.pack_propagate(False)

        self.F_order_Scroll = CTkScrollableFrame(FRight,fg_color="#dfdfdf",border_width=0,border_color="black",width=600)
        self.F_order_Scroll.pack(fill=BOTH,expand=True)

        open_clean_icon = Image.open(os.path.join(file_icon, "clean.png"))  
        clean_image = CTkImage(open_clean_icon,size=(20,20))

        btn_clear = CTkButton(self.F_order_Scroll,text="",image=clean_image,width=25,height=25,fg_color="#FF2C2C",hover_color="#F14141",corner_radius=15,command=self.clear)
        btn_clear.pack(anchor="ne",padx=15,pady=10)

        FBottom= CTkFrame(FRight,fg_color="#1DF38F",corner_radius=0,border_width=0,border_color="black")
        FBottom.pack(side=BOTTOM,fill=BOTH)

        FBottomPay= CTkFrame(FBottom,fg_color="#1DF38F",corner_radius=0,border_width=0,border_color="black")
        FBottomPay.pack(side=BOTTOM,fill=BOTH)

        FBottomPay.columnconfigure(0,weight=1)
        FBottomPay.columnconfigure(1,weight=1)

        FRBLable_name = CTkLabel(FBottom,text="จำนวน :\n\nราคา :\n\nรวม :",font=("Arial",24),justify="left")
        FRBLable_name.pack(side=LEFT,anchor="nw",padx=20,pady=20)

        FRBLable_price = CTkLabel(FBottom,textvariable=self.price_order,font=("Arial",24),justify="right")
        FRBLable_price.pack(side=RIGHT,anchor="nw",padx=20,pady=20)

        pay_cash = CTkButton(FBottomPay,text="Cash",cursor="hand2",text_color="white",width=200,height=60,corner_radius=0,fg_color="#ffad15",hover_color="#e29e45",font=("Arial Bold",24),command=lambda:open_func(lambda:self.open_top_ui.cash_ui(self.products_order,self.clear,self.guest_ui.price_order_guest)))
        pay_cash.grid(row=0,column=0,sticky="nsew")

        pay_prom = CTkButton(FBottomPay,text="Prompay",cursor="hand2",text_color="white",width=200,height=60,corner_radius=0,fg_color="#264eff",hover_color="#2e5fe6",font=("Arial Bold",24),command=lambda:open_func(lambda:self.open_top_ui.pay_qrcode(self.products_order,self.clear,self.guest_ui.price_order_guest,self.guest_ui.icon)))
        pay_prom.grid(row=0,column=1,sticky="nsew")

        all_row = self.my_sql.all_row(self.types.get())
        self.rows = [f"{i}" for i in range(all_row+1)]

        page = CTkComboBox(FLeft,width=80,variable=self.amount_page,state="readonly")
        page.grid(row=2,column=0,columnspan=2,sticky="S",pady=25)

        def change_pag(num):
            num = int(num)
            self.amount_page.set(num)
            if (self.on_search.get() == False):
                self.show_products(self.types.get(),num)
            else:
                self.show_products(self.types.get(),num,False,self.on_search.get())
            
            self.reset_scroll()


        self.page_scroll = CTkScrollableDropdown(page,justify="left", button_color="transparent",values=self.rows,command=lambda e_num:change_pag(e_num))

        all_type_list = self.my_sql.all_type()
        self.all_type = ["ทั้งหมด"] + all_type_list

        def change_type(type_list):
            self.types.set(type_list)

            all_row = self.my_sql.all_row(self.types.get())
            self.rows = [f"{i}" for i in range(all_row+1)]

            self.page_scroll.configure(values=self.rows)

            self.show_products(self.types.get(),0,True)

            self.reset_scroll()

        self.box_type = CTkComboBox(FLeft,width=100,values=self.all_type,command=lambda e:change_type(e),state="readonly") 
        self.box_type.grid(row=0,column=1,padx=(0,115),sticky="E")

        self.show_products(self.types.get())

        self.inp_product.bind("<Return>",lambda e:self.inp_products_order(self.inp_product.get()))

        self.after(500, lambda: self.inp_product.focus_force())
   

    def show_products(self,types,num=0,reset=False,search=False):
        self.data_products.clear()
        
        if (search == True):
            p_id , p_name, p_type, p_price, p_cost_price, p_amount, p_sell ,id_search = self.my_sql.search_products(self.key_search.get(),num)  
            products = id_search
            self.amount_page.set(num)

        else:

            if (reset == False):

                products = self.my_sql.show_products(types,num)
                self.amount_page.set(num)
                
            else:
                products = self.my_sql.show_products(types,0)
                self.amount_page.set(num)

        for i in range(40):
            row = i //4
            col = i % 4
            obj = self.obj_products[row,col]

            if i < len(products):
                p_data = products[i]
                p_id = p_data[0]    
                p_name = p_data[1]  
                p_price = p_data[3]   

                if p_id in self.image_cache:
                    pimg = self.image_cache[p_id]
                
                else:

                    try:
                        path_img = os.path.join(self.appdir, "products", f"{p_id}.jpg")
                        open_pimg = Image.open(path_img)
                        open_pimg.load()
                        
                        pimg = CTkImage(open_pimg,size=(150,200))
                        self.image_cache[p_id] = pimg
                        self.image_cache_order[p_id] = CTkImage(open_pimg,size=(100,100))

                    except FileNotFoundError:
                        pimg = self.open_pimg_default
                
                obj["frame"].grid()
                obj["label"].configure(image=pimg,text="")

                self.data_products[row,col] = {
                    "id":p_id,
                    "name":p_name,
                    "price":p_price
                }
            else:
                obj["frame"].grid_remove()

    def next_page(self):
        types = self.types.get()
        key_search = self.key_search.get()
        
        if (self.on_search.get() == False):
            num = int(self.amount_page.get())
            all_row = self.my_sql.all_row(types)
            if (num < all_row):
                new = num + 1
                self.show_products(types,new)
        else:
            num = int(self.amount_page.get())
            all_row = self.my_sql.all_row(types,True,key_search)
            
            if (num < all_row):
                new = num +1
                self.show_products(types,new,False,self.on_search.get())

        self.reset_scroll()
    
    def next_page_last(self):
        types = self.types.get()
        key_search = self.key_search.get()
    
        if (self.on_search.get() == False):
            all_row = self.my_sql.all_row(types)
        
            self.amount_page.set(all_row)
            num = int(self.amount_page.get())

            self.show_products(types,num)
        else:
            all_row = self.my_sql.all_row(types,True,key_search)
        
            self.amount_page.set(all_row)
            num = int(self.amount_page.get())


            self.show_products(types,num,False,self.on_search.get())

        self.reset_scroll()


    def back_page(self):
        types = self.types.get()
        key_search = self.key_search.get()
        
        if (self.on_search.get() == False):
            num = int(self.amount_page.get())
            all_row = self.my_sql.all_row(types)
            if (num <= all_row and num != 0):
                new = num - 1
                self.show_products(types,new)
        else:
            num = int(self.amount_page.get())
            all_row = self.my_sql.all_row(types,True,key_search)
            
            if (num <= all_row and num != 0):
                new = num - 1
                self.show_products(types,new,False,self.on_search.get())
        
        self.reset_scroll()
    
    def back_page_last(self):
        types = self.types.get()
        key_search = self.key_search.get()
        
        if (self.on_search.get() == False):
            num = int(self.amount_page.get())
            all_row = self.my_sql.all_row(types)

            if (num <= all_row):
                self.show_products(types)
        else:
            num = int(self.amount_page.get())
            all_row = self.my_sql.all_row(types,True,key_search)
            if (num <= all_row):
                self.show_products(types,0,False,self.on_search.get())

        self.reset_scroll()
               

    def hover_enter(self,obj,w,h):
        self.config(cursor="hand2")
        obj.configure(width=w,height=h)

    def hover_leave(self,obj,w,h):
        self.config(cursor="arrow")
        obj.configure(width=w,height=h)

    def reset_scroll(self):
        self.FProducts_Scroll._parent_canvas.yview_moveto(0.0)

    def clear(self):
        all_order = self.obj_order
        all_order_guest = self.guest_ui.obj
        self.amount = 0
        self.price = 0.0
        self.total = 0.0

        for i in all_order:
            i.destroy()
        
        for i in all_order_guest:
            i.destroy()

        self.products_order.clear()
        self.obj_order.clear()
        self.guest_ui.obj.clear()

        self.price_order.set(f"{self.amount}\n\n{self.price}\n\n{self.total}")
        self.price_order_guest.set(f"{self.amount}\n\n{self.total}\n\n0.0\n\n0.0")

        self.after(100,lambda: self.guest_ui.F_order_Scroll._parent_canvas.yview_moveto(0.0)) 
        self.after(100,lambda: self.F_order_Scroll._parent_canvas.yview_moveto(0.0)) 

    def remove(self,obj,obj_guest,id,amount,cost_price,price):
        self.amount -= int(amount)
        self.total -= float(price)

        if (id in self.products_order):
            self.products_order[id]["amount"] = int(self.products_order[id]["amount"]) - int(amount)
            self.products_order[id]["cost_price"] -= float(cost_price)
            self.products_order[id]["total"] -= (float(self.products_order[id]["price"]) * int(amount))

            self.price = float(price)
            
            if (self.products_order[id]["amount"] <= 0):
                del self.products_order[id]

        self.obj_order.remove(obj)
        self.guest_ui.obj.remove(obj_guest)

        self.price_order.set(f"{self.amount}\n\n{self.price}\n\n{self.total}")
        self.price_order_guest.set(f"{self.amount}\n\n{self.total}\n\n0.0\n\n0.0")

        obj.destroy()
        obj_guest.destroy()
        
    
    def re_face(self):
        self.types.set("ทั้งหมด")
        self.box_type.set("ทั้งหมด")
        self.show_products(self.types.get())
        self.key_search.set("")
        self.on_search.set(False)

        all_row = self.my_sql.all_row(self.types.get())
        self.rows = [f"{i}" for i in range(all_row+1)]
        self.page_scroll.configure(values=self.rows)
        self.reset_scroll()

    def inp_products_order(self,id):
        find_star = id.find("*")
        
        if (find_star <= -1):
            amount = 1
            bar_code = id
        else:
            amount = id[0:find_star]
            bar_code = id[find_star+1:]
        
        if (id == "" or id == None):
            self.re_face()
        else:  
            p_id , p_name, p_type, p_price, p_cost_price, p_amount, p_sell ,id_search = self.my_sql.search_products(bar_code)  

            try:
                if (int(amount) <= int(p_amount)):
                    if (id_search == None):
                
                        if (find_star <= -1):
                            self.price = float(p_price)
                            self.amount += int(amount)
                            self.total += float(p_price)    
                            total = float(p_price) * float(amount)           
                        else:
                            self.price = float(p_price)
                            total = float(p_price) * float(amount)
                            
                            self.amount += int(amount)
                            self.total += total
                        
                        if p_id in self.image_cache:
                            pimg = self.image_cache_order[p_id]
                    
                        else:
                            pimg = self.open_pimg_default_order
                    

                        if (bar_code in self.products_order):
                            self.products_order[bar_code]["amount"] += int(amount)
                            self.products_order[bar_code]["cost_price"] += p_cost_price
                            self.products_order[bar_code]["price"] = p_price
                            self.products_order[bar_code]["total"] += total
                        else:
                            self.products_order[bar_code] = {
                                "name":p_name,
                                "amount":int(amount),
                                "cost_price":float(p_cost_price),
                                "price":float(p_price),
                                "total":float(total)
                            }
                        
                        self.create_frame_order(bar_code,pimg,p_name,amount,p_cost_price,total)
                else:
                    CTkMessagebox(title="Error",message=f"สินค้าไม่เพียงพอ จำนวนสินค้าที่มี: {p_amount}",icon="cancel",option_1="OK")
            except:    
                all_row = self.my_sql.all_row(self.types.get(),True,bar_code)
                self.rows = [f"{i}" for i in range(all_row+1)]
                self.page_scroll.configure(values=self.rows)

                self.on_search.set(True)

                self.key_search.set(bar_code)

                self.reset_scroll()

                self.show_products(self.types.get(),0,True,self.on_search.get())
                self.inp_product.delete(0,END)
                
                
    
    def add_products(self):
        if (self.open_top_ui == None or not self.open_top_ui.winfo_exists()):
            self.open_top_ui = top_ui.top_gui(self.my_sql)

        self.open_top_ui.check_level(self.open_top_ui.add_products_ui,self.username,self.passwords,2)
        self.open_top_ui.attributes('-topmost', True)
    
    def create_frame_order(self,bar_code,pimg,p_name,amount,p_cost_price,total):
        frame = CTkFrame(self.F_order_Scroll,fg_color="white")
        frame.pack(side=TOP,fill=X,expand=True,pady=10)

        frame.columnconfigure(1,weight=1)

        l_img = CTkLabel(frame,image=pimg,text="")
        l_img.grid(row=0,column=0,padx=20,sticky="w")

        l_name = CTkLabel(frame,text=f"{p_name[0:20]}...")
        l_name.grid(row=0,column=1,sticky="news")

        l_amount = CTkLabel(frame,text=f"X{amount}",justify=LEFT)
        l_amount.grid(row=0,column=2,sticky="w",padx=100)

    
        guest_frame = CTkFrame(self.guest_ui.F_order_Scroll,fg_color="white")
        
        btn_remove = CTkButton(frame,image=self.remove_icon ,text="",width=30,height=30,fg_color="red",hover_color="#FF6A6A",command=lambda e_amount = amount,e_cost_price=p_cost_price,e_price=total: self.remove(frame,guest_frame,bar_code,e_amount,e_cost_price,e_price))
        btn_remove.grid(row=0,column=3,padx=20,sticky="e")

        self.price_order.set(f"{self.amount}\n\n{self.price}\n\n{self.total}")
        self.obj_order.append(frame)

        self.create_frame_order_guest(guest_frame,pimg,p_name,amount,total)

    def create_frame_order_guest(self,guest_frame,pimg,p_name,amount,total):

        guest_frame.pack(side=TOP,fill=X,expand=True,pady=10)
        guest_frame.columnconfigure(1,weight=1)

        guest_l_img = CTkLabel(guest_frame,image=pimg,text="")
        guest_l_img.grid(row=0,column=0,padx=20,sticky="w")

        guest_l_name = CTkLabel(guest_frame,text=f"{p_name[0:20]}...")
        guest_l_name.grid(row=0,column=1,sticky="news")

        guest_l_amount = CTkLabel(guest_frame,text=f"X{amount}",justify=RIGHT)
        guest_l_amount.grid(row=0,column=2,sticky="w",padx=100)

        guest_l_total = CTkLabel(guest_frame,text=f"{float(total):.2f}",justify=RIGHT,font=("Arial",18))
        guest_l_total.grid(row=0,column=3,sticky="e",padx=60)

        self.guest_ui.price_order_guest.set(f"{self.amount}\n\n{self.total}\n\n0.0\n\n0.0")

        self.guest_ui.obj.append(guest_frame)

        self.inp_product.delete(0,END)

        self.after(100,lambda: self.guest_ui.F_order_Scroll._parent_canvas.yview_moveto(1.0)) 
        self.after(100,lambda: self.F_order_Scroll._parent_canvas.yview_moveto(1.0)) 
        
class guest_gui(CTkToplevel):
    def __init__(self,text_var):
        super().__init__()
        self.withdraw()

        self.amount = 0
        self.price = 0.0
        self.total = 0.0

        self.appdir = Path(__file__).parent

        self.obj = []

        self.price_order_guest = text_var

        open_icon = Image.open(os.path.join(self.appdir, "icon","icon.png"))
        self.icon = CTkImage(open_icon,size=(150,150))

        self.protocol("WM_DELETE_WINDOW",self.quit)


    def guest_ui(self):
        self.title("Stock List")
        screen_x = self.winfo_screenwidth()
        screen_y = self.winfo_screenheight()

        x = int((screen_x / 2) - (1280/2))
        y = int((screen_y / 2) - (720 / 2))
        self.geometry(f"1280x720+{x}+{y-25}")
        
        self.config(bg="#3E3E3E")
        
        self.iconbitmap(os.path.join(self.appdir, "icon","icon.ico"))
        self.after(200, lambda: self.iconbitmap(os.path.join(self.appdir, "icon","icon.ico")))
        self.deiconify()

        FLeft = CTkFrame(self,fg_color="#dfdfdf",width=600,corner_radius=0,border_color="black",border_width=0)
        FLeft.pack(side=LEFT,fill=BOTH,expand=True)
        FLeft.pack_propagate(False)

        self.F_order_Scroll = CTkScrollableFrame(FLeft,fg_color="#dfdfdf",border_width=0,border_color="black",width=600)
        self.F_order_Scroll.pack(fill=BOTH,expand=True)

        FRight = CTkFrame(self,fg_color="#3afa80",corner_radius=0,border_width=0,border_color="black",width=200)
        FRight.pack(side=RIGHT,fill=BOTH,expand=True)
        FRight.pack_propagate(False)

        FPrice = CTkFrame(FRight,fg_color="#ffffff",width=50,height=250,corner_radius=20,border_width=1,border_color="black")
        FPrice.pack(side=TOP,fill=BOTH,padx=60,pady=60)

        l_text = CTkLabel(FPrice,text="จำนวน :\n\nรวม :\n\nรับเงิน :\n\nทอนเงิน :",font=("Arial",24),justify="left")
        l_text.pack(side=LEFT,anchor="nw",padx=20,pady=20)

        l_price = CTkLabel(FPrice,textvariable=self.price_order_guest,font=("Arial",24),justify="right")
        l_price.pack(side=RIGHT,anchor="nw",padx=20,pady=20)

        FBottom = CTkFrame(FRight,fg_color="#3afa80",corner_radius=0,border_width=0,border_color="black")
        FBottom.pack(side=BOTTOM,fill=BOTH)

        

        label_logo = CTkLabel(FBottom,text="",image=self.icon)
        label_logo.pack(pady=100)
