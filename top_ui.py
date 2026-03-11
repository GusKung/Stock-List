from customtkinter import *
import customtkinter
from pathlib import Path
from CTkMessagebox import *
from CTkMenuBar import *
from CTkScrollableDropdown import CTkScrollableDropdown
from PIL import Image
import encode_file
from tkinter import ttk
import printer
import main
import threading
from CTkDatePicker import CTkDatePicker
from promptpay import qrcode
from io import BytesIO
import json
import webbrowser
from datetime import datetime

class top_gui(CTkToplevel):
    def __init__(self,db=None):
        super().__init__()
        self.withdraw()

        self.data = encode_file.EncodeDecode()
        self.load_data = encode_file.EncodeDecode().load_data()
        self.account_file = self.load_data.get("Account_File")
        self.setting_file = self.load_data.get("Settings_File")
        self.bill_file = self.load_data.get("Bill File")

        self.printer = [self.load_data.get("PRINTER_NAME"),self.load_data.get("PRINTER_VID"),self.load_data.get("PRINTER_PID"),self.load_data.get("PRINTER_WIDTH")]

        if (self.printer[3] == 384):
            width_printer = "58mm"
        else:
            width_printer = "80mm"

        self.pname = StringVar(value=f"{self.printer[0]}")
        self.vid = StringVar(value=f"{self.printer[1]}")
        self.pid = StringVar(value=f"{self.printer[2]}")
        self.print_width = StringVar(value=f"{width_printer}")

        self.username = self.load_data.get("USERNAME")
        self.passwords = self.load_data.get("PASSWORD")
        self.remember = self.load_data.get("REMEMBER")
        self.pos = self.load_data.get("POS")
        self.shift = self.load_data.get("SHIFT")
        self.prompay = self.load_data.get("PROMPAY")

        self.prom_str = StringVar(value=f"{self.prompay}")

        self.types = StringVar(value="ทั้งหมด")

        self.key_search = StringVar(value="")
        self.on_search = BooleanVar(value=False)
        self.on_reset = BooleanVar(value=False)

        self.date_time = StringVar(value="Day")

        self.appdir = Path(__file__).parent

        self.my_sql = db

        self.obj_list = []
        self.open_printer = None
        self.open_main = None
        default_path = os.path.join(self.appdir, "icon", "upload.png")
        img_raw = Image.open(default_path)
        img_raw.load()
        self.open_pimg_default = CTkImage(img_raw, size=(250, 250))

    def add_products_ui(self):
        self.title(f"Add Products")
        screen_x = self.winfo_screenwidth()
        screen_y = self.winfo_screenheight()

        x = int((screen_x / 2) - (700/2))
        y = int((screen_y / 2) - (400 / 2))
        self.geometry(f"{700}x{400}+{x}+{y-25}")

        icon = os.path.join(self.appdir, "icon","icon.ico")
        
        self.iconbitmap(icon)
        self.after(500, lambda: self.iconbitmap(icon))
        self.deiconify()
        self.resizable(False,False)

        Frame_Scroll = CTkScrollableFrame(self)
        Frame_Scroll.pack(fill=BOTH,expand=True)

        def remove(frame,obj):
            frame.destroy()
            self.obj_list.remove(obj)

        def add_track():
            obj = {}

            def change_img():
                file_path = customtkinter.filedialog.askopenfilename(title="Select Image",filetypes=(("JPG files","*.jpg"),("JPEG files","*.jpeg"),("PNG files","*.png")))

                if (file_path):
                        obj["img_open"] = Image.open(file_path)

                        img = CTkImage(obj["img_open"],size=(200,200))
                        btn_img.configure(image=img)

            Frame_Center = CTkFrame(Frame_Scroll,width=400,height=400,corner_radius=0,fg_color="#FFFFFF")
            Frame_Center.pack(fill=X,pady=(10,0))

            Frame_Center.grid_columnconfigure(1, weight=1)  
            Frame_Center.grid_columnconfigure(2, weight=1)  

            img_path = os.path.join(self.appdir, "icon","upload.png")
            img_open = Image.open(img_path)
            img = CTkImage(light_image=img_open,dark_image=img_open,size=(200,200))

            btn_img = CTkButton(Frame_Center,width=200,height=200,text="",image=img,fg_color="#FFFFFF",hover_color="#F7F7F7",corner_radius=0,command=change_img)
            btn_img.grid(rowspan=3,column=0,padx=(10,20),pady=10)

            obj["inp_barcode"] = CTkEntry(Frame_Center,width=200,height=30,corner_radius=10,placeholder_text="Code",font=("Arial",16))
            obj["inp_barcode"].grid(row=0,column=1,sticky="ew")

            obj["inp_name"] = CTkEntry(Frame_Center,width=200,height=30,corner_radius=10,placeholder_text="Name",font=("Arial",16))
            obj["inp_name"].grid(row=0,column=2,padx=(25,10),sticky="ew")

            obj["inp_cost_price"] = CTkEntry(Frame_Center,width=150,height=30,corner_radius=10,placeholder_text="Cost Price",font=("Arial",16))
            obj["inp_cost_price"].grid(row=1,column=1,sticky="ew")

            obj["inp_price"] = CTkEntry(Frame_Center,width=150,height=30,corner_radius=10,placeholder_text="Price",font=("Arial",16))
            obj["inp_price"].grid(row=1,column=2,padx=(25,10),sticky="ew")

            obj["inp_amount"] = CTkEntry(Frame_Center,width=150,height=30,corner_radius=10,placeholder_text="Amount",font=("Arial",16))
            obj["inp_amount"].grid(row=2,column=1,sticky="ew")

            all_type = self.my_sql.all_type()

            obj["inp_type"] = CTkComboBox(Frame_Center,width=80,values=all_type,state="readonly")
            obj["inp_type"].grid(row=2,column=2,padx=(25,10),sticky="ew")

            btn_remove = CTkButton(Frame_Center,width=60,height=30,corner_radius=0,text="Remove",text_color="white",fg_color="#f33838",hover_color="#f66b6b",command=lambda:remove(Frame_Center,obj))
            btn_remove.grid(row=3,column=1,columnspan=2,padx=(0,0),pady=(0,20),sticky="nesw")

            self.obj_list.append(obj)

        def upload():
            for i in self.obj_list[:]:
                barcode = i["inp_barcode"].get()
                name = i["inp_name"].get()
                types = i["inp_type"].get()
                cost_price  = i["inp_cost_price"].get()
                price = i["inp_price"].get()
                amount = i["inp_amount"].get()
                

                try:
                    img = i["img_open"]
                    rgb_img = img.convert('RGB')
                    paths = os.path.join(self.appdir, "products",f"{barcode}.jpg")

                    rgb_img.save(paths,optimize=True,format='JPEG',quality=10)
                except:
                    img = None

                result, err = self.my_sql.insert_products(barcode,name,types,cost_price,price,amount)
            
            if (result == True):
                boxmes = CTkMessagebox(title="Success",message="Upload Products Success",icon="check",option_1="OK")
                if (boxmes.get() == "OK"):
                    self.destroy()
            else:
                boxmes = CTkMessagebox(title="Failed",message=f"Upload Products Faile: {err}",icon="cancel",option_1="OK")
                if (boxmes.get() == "OK"):
                    self.destroy()

        btn_add = CTkButton(self,font=("Arial",16),width=60,height=30,corner_radius=20,text="Add",text_color="white",fg_color="#38f388",hover_color="#6be59e",command=add_track)
        btn_add.pack(side=LEFT,anchor="sw",padx=10,pady=10)

        btn_upload = CTkButton(self,font=("Arial",16),width=60,height=30,corner_radius=20,text="Upload",text_color="white",fg_color="#38f388",hover_color="#6be59e",command=upload)
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

        icon = os.path.join(self.appdir, "icon","icon.ico")
        
        self.iconbitmap(icon)
        self.after(200, lambda: self.iconbitmap(icon))
        self.deiconify()
        self.resizable(False,False)

        open_bg = Image.open(os.path.join(self.appdir, "icon","sql_connect.png"))  
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

    def account_ui(self):
        self.title("Account")
        screen_x = self.winfo_screenwidth()
        screen_y = self.winfo_screenheight()

        x = int((screen_x / 2) - (1280/2))
        y = int((screen_y / 2) - (720 / 2))
        self.geometry(f"{1280}x{720}+{x}+{y-25}")

        icon = os.path.join(self.appdir, "icon","icon.ico")
        
        self.iconbitmap(icon)
        self.after(200, lambda: self.iconbitmap(icon))
        self.deiconify()

        FLeft = CTkFrame(self,width=400,fg_color="#7cffac", corner_radius=0)
        FLeft.pack(side=LEFT, fill=BOTH)

        FLeft.columnconfigure(0,weight=1)
        FLeft.rowconfigure(2,weight=1)

        FRight = CTkFrame(self,fg_color="#FFFFFF", corner_radius=0)
        FRight.pack(side=RIGHT, fill=BOTH,expand=True)

        FRight.columnconfigure(0,weight=1)
        FRight.rowconfigure(0,weight=1)

        ID = StringVar(value="")
        USER = StringVar(value="Username")
        PASS = StringVar(value="Password")
        LEVEL = StringVar(value="Level")
        PAGE = StringVar(value="0")

        data_user = {}

        inp_user = CTkEntry(FLeft,placeholder_text="Username",text_color="#818181",textvariable=USER,width=200,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16),state="disabled")
        inp_user.grid(row=0,column=0,pady=(40,10),padx=20)

        inp_level = CTkComboBox(FLeft,values=["1","2","3"],variable=LEVEL,state="disabled",width=100,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16))
        inp_level.grid(row=0,column=1,pady=(40,10),padx=20)

        inp_pass = CTkEntry(FLeft,placeholder_text="Password",text_color="#818181",textvariable=PASS,show="●",width=200,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16),state="disabled")
        inp_pass.grid(row=1,column=0,pady=20,padx=20)

        id_user = 8000  
        id_em = 6000

        def add_track():
            nonlocal id_user , id_em
  
            count = self.my_sql.count_user()
            
            len_id_user = len(count) + id_user
            len_id_em = len(count) + id_em

            table_user.insert("",END,values=(len_id_em,len_id_user,"New","1","","","","","",""))
            id_user += 1
            id_em += 1
        
        def del_track():
            sure = CTkMessagebox(title="Delete Account",message="Are you sure to delete this account?",icon="warning",option_1="No",option_2="Yes")
            if (sure.get() == "No"):
                return
            else:
                selected_item = table_user.selection()
                if selected_item:
                    for item in selected_item:
                        values = table_user.item(item, "values")
                    id_user = values[1]  
                    id_emp = values[0]  
                    self.my_sql.del_user(id_user,id_emp)
                    table_user.delete(item)

        def change_page(page):
            page = int(page)
            PAGE.set(page)
            load_data_user(PAGE.get())
            table_user.yview_moveto(0)

        def next_page():
            num = int(PAGE.get())
            if (num < all_row):
                PAGE.set(num+1)
                load_data_user(PAGE.get())
            table_user.yview_moveto(0)
        
        def back_page():
            num = int(PAGE.get())
            if (num <= all_row and num != 0):
                PAGE.set(num-1)
                load_data_user(PAGE.get())
            table_user.yview_moveto(0)

        # //-----------------------Button Edit------------------------------
        def edit():
            if (inp_user.cget("state") == "disabled"):
                inp_user.configure(state="normal",text_color="#000000",border_color="#000000",fg_color="#FFFFFF")
                inp_level.configure(border_color="#000000",fg_color="#FFFFFF",state="readonly")
                inp_pass.configure(state="normal",text_color="#000000",border_color="#000000",fg_color="#FFFFFF")
                data_employee.configure(state="normal",text_color="#000000",border_color="#8D8D8D",fg_color="#FFFFFF")
                btn_edit.configure(text="Save")

                def protect_readonly(event):
                    cursor_pos = data_employee.index("insert")
                    
                    prev_index = data_employee.index(f"{cursor_pos} -1c")
                    
                    if event.keysym in ("BackSpace", "Delete"):
                        if "readonly" in data_employee.tag_names(prev_index):
                            return "break"
                    
                    if event.keysym not in ("BackSpace", "Delete"):
                        if "readonly" in data_employee.tag_names(cursor_pos):
                            
                            insert_after = data_employee.index(f"{prev_index} +1c")
                            data_employee.mark_set("insert", insert_after)


                data_employee.bind("<Key>", protect_readonly)
                data_employee.bind("<BackSpace>", protect_readonly)
                data_employee.bind("<Delete>", protect_readonly)

            else:
                inp_user.configure(state="disabled",text_color="#818181",border_color="#8D8D8D",fg_color="#FCFCFC")
                inp_level.configure(state="disabled",border_color="#8D8D8D",fg_color="#FCFCFC")
                inp_pass.configure(state="disabled",text_color="#818181",border_color="#8D8D8D",fg_color="#FCFCFC")
                data_employee.configure(state="disabled",text_color="#818181",border_color="#A7A7A7",fg_color="#FCFCFC")
                btn_edit.configure(text="Edit")

                em_id = data_employee.get("1.0","3.0").rstrip("\n").replace("Employee ID : ","")

                name = data_employee.get("3.0","5.0").rstrip("\n").replace("Name : ","").split("\n")[0]
                full_name = name.split(" ")
                f_name = full_name[0]
                l_name = full_name[1]

                contact = data_employee.get("5.0","7.0").rstrip("\n").replace("Contact : ","")
                address = data_employee.get("7.0","9.0").rstrip("\n").replace("Address : ","")

                id = ID.get()
                user = USER.get()
                level = LEVEL.get()
                password = PASS.get()

                data_user[id] = (user,level,password,em_id,f_name,l_name,contact,address)
        
        def apply():
            for id_user , values in data_user.items():
                user , level , password , emp_id , f_name , l_name , contact , address = values
                result, err = self.my_sql.insert_user(id_user,user , level , password , emp_id , f_name , l_name , contact , address)
    
            if (result == True):
                succ = CTkMessagebox(title="Success",message="Apply Changes Successfully!",icon="check",option_1="OK")
                if (succ.get() == "OK"):
                    load_data_user(0)
            else:
                boxmes = CTkMessagebox(title=f"Failed {err.errno}",message=f"Apply Changes Faile: {err}",icon="cancel",option_1="OK")
                if (boxmes.get() == "OK"):
                    load_data_user(0)

        btn_add = CTkButton(FLeft,width=100,height=40,text="Add",corner_radius=20,command=add_track)
        btn_add.grid(row=3,column=0,sticky="sw",padx=20,pady=20)

        btn_del = CTkButton(FLeft,width=100,height=40,text="Remove",corner_radius=20,fg_color="#FF3939",hover_color="#DF4949",cursor="hand2",command=del_track)
        btn_del.grid(row=3,column=0,columnspan=2,sticky="s",padx=20,pady=20)

        btn_apply = CTkButton(FLeft,width=100,height=40,text="Apply",corner_radius=20,command=apply)
        btn_apply.grid(row=3,column=1,sticky="se",padx=20,pady=20)

        btn_next = CTkButton(FRight,width=100,height=40,font=("Arial Bold",16),text=">",corner_radius=20,fg_color="#38f388",hover_color="#6be59e",text_color="black",cursor="hand2",command=next_page)
        btn_next.grid(row=2,column=0,sticky="se",padx=(0,20),pady=20)

        btn_back = CTkButton(FRight,width=100,height=40,font=("Arial Bold",16),text="<",corner_radius=20,fg_color="#38f388",hover_color="#6be59e",text_color="black",cursor="hand2",command=back_page)
        btn_back.grid(row=2,column=0,sticky="sw",padx=(20,0),pady=20)

        all_row = self.my_sql.all_row_user()
        rows = [f"{i}" for i in range(0, all_row+1)]

        amount_page = CTkComboBox(FRight,width=80,variable=PAGE,state="readonly")
        amount_page_scroll = CTkScrollableDropdown(amount_page,values=rows,justify="left", button_color="transparent",command=lambda e_num:change_page(e_num))
        amount_page.grid(row=2,column=0,columnspan=2,sticky="S",pady=25)

        btn_edit = CTkButton(FLeft,text="Edit",width=150,corner_radius=14,height=30,font=("Arial", 16),command=edit)
        btn_edit.grid(row=1,column=1,pady=20,padx=20)

        # //-------------------------Table----------------------------
        data_employee = CTkTextbox(FLeft,width=400,height=200,corner_radius=20,font=("Arial", 16),border_width=2,border_color="#A7A7A7",fg_color="#FCFCFC",text_color="#818181")
        data_employee.configure(state="disabled")
        data_employee.grid(row=2,column=0,columnspan=2,pady=10,padx=20,sticky="nsew")

        style = ttk.Style(self)
        style.configure("Treeview", font=("Arial", 12), rowheight=40,borderwidth=0, highlightthickness=0)       
        style.configure("Treeview.Heading", font=("Arial Bold", 12))  

        table_user = ttk.Treeview(FRight,columns=("ID_EM","ID","Username","Level","Employee","First_Name","Last_Name","Password","Address","Contact"),show="headings")

        scrollbar = ttk.Scrollbar(FRight, orient="vertical", command=table_user.yview)
        table_user.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        table_user.heading("ID",text="ID")
        table_user.heading("Username",text="Username")
        table_user.heading("Level",text="Level")
        table_user.heading("Employee",text="Employee")

        table_user.column("ID_EM",width=0,stretch=False)
        table_user.column("ID",width=30,anchor=CENTER)
        table_user.column("Username",width=100,anchor="w")
        table_user.column("Level",width=30,anchor=CENTER)
        table_user.column("Employee",width=100,anchor=CENTER)

        table_user.column("First_Name",width=0,stretch=False)
        table_user.column("Last_Name",width=0,stretch=False)
        table_user.column("Password",width=0,stretch=False)
        table_user.column("Address",width=0,stretch=False)
        table_user.column("Contact",width=0,stretch=False)

        table_user.grid(row=0, column=0, sticky="nsew")

        def load_data_user(num):
            table_user.delete(*table_user.get_children())
            data_user = self.my_sql.load_user(int(num))
            for i in data_user:
                id_employee = i[0] 
                id_user = i[1]
                user = i[7]
                level = i[9]
                employee = i[2]

                f_name = i[2]
                l_name = i[3]
                password = i[8]
                address = i[4]
                contact = i[5]

                table_user.insert("",END,values=(id_employee,id_user,user,level,employee,f_name,l_name,password,address,contact))
            table_user.yview_moveto(0)


        def select_data(event):
            select = table_user.focus()
            values = table_user.item(select,"values")

            id_employee = values[0]
            id_user = values[1]
            user = values[2]
            password = values[7]
            level = values[3]

            employee = values[4]

            f_name = values[5]
            l_name = values[6]
            
            address = values[8]
            contact = values[9]

            ID.set(id_user)
            USER.set(user)
            PASS.set(password)
            LEVEL.set(level)

            data_employee.configure(state="normal")
            data_employee.delete("0.0","end")

            data_employee.insert("1.0","Employee ID : ","readonly")
            data_employee.insert("1.end",f"{id_employee}\n\n")

            data_employee.insert("3.0",f"Name : ","readonly")
            data_employee.insert("3.end",f"{f_name} {l_name}\n\n")

            data_employee.insert("5.0",f"Contact : ","readonly")
            data_employee.insert("5.end",f"{contact}\n\n")

            data_employee.insert("7.0",f"Address : ","readonly")
            data_employee.insert("7.end",f"{address}\n\n")

            data_employee.configure(state="disabled")

        table_user.bind("<Double-1>", select_data)

        load_data_user(0)
    
    def stock_ui(self):
        self.title("Stock")
        screen_x = self.winfo_screenwidth()
        screen_y = self.winfo_screenheight()

        x = int((screen_x / 2) - (1280/2))
        y = int((screen_y / 2) - (720 / 2))
        self.geometry(f"{1280}x{720}+{x}+{y-25}")

        icons = os.path.join(self.appdir, "icon","icon.ico")
        
        self.iconbitmap(icons)
        self.after(200, lambda: self.iconbitmap(icons))
        self.deiconify()

        data_stock= {}

        ID = StringVar(value="Barcode")
        NAME = StringVar(value="Name Product")
        TYPE = StringVar(value="Type")
        COST_PRICE = StringVar(value="Cost Price")
        PRICE = StringVar(value="Price")
        AMOUNT = StringVar(value="Amount")
        num_page = StringVar(value="0")
        on_search = BooleanVar(value=False)
        key_search = StringVar(value="")

        FLeft = CTkFrame(self,width=400,fg_color="#7cffac", corner_radius=0)
        FLeft.pack(side=LEFT, fill=BOTH)

        FLeft.columnconfigure(0,weight=1)
        FLeft.rowconfigure(4,weight=1)

        FRight = CTkFrame(self,fg_color="#FFFFFF", corner_radius=0)
        FRight.pack(side=RIGHT, fill=BOTH,expand=True)

        FRight.columnconfigure(0,weight=1)
        FRight.rowconfigure(1,weight=1)

        all_row_list = self.my_sql.all_row("ทั้งหมด")
        rows = [f"{i}" for i in range(all_row_list+1)]

        all_type_list = self.my_sql.all_type()
        all_type = ["ทั้งหมด"] + all_type_list

        amount_page = CTkComboBox(FRight,width=80,variable=num_page,state="readonly")
        amount_page_scroll = CTkScrollableDropdown(amount_page,values=rows,justify="left", button_color="transparent",command=lambda e_num:change_page(e_num))
        amount_page.grid(row=2,column=0,columnspan=2,sticky="S",pady=25)

        inp_id = CTkEntry(FLeft,placeholder_text="ID",text_color="#818181",textvariable=ID,width=200,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16),state="disabled")
        inp_id.grid(row=0,column=0,pady=(40,10),padx=20)

        inp_name = CTkEntry(FLeft,placeholder_text="NAME",text_color="#818181",textvariable=NAME,width=200,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16),state="disabled")
        inp_name.grid(row=0,column=1,pady=(40,10),padx=20)

        box_type = CTkComboBox(FLeft,values=all_type_list,variable=TYPE,state="disabled",width=200,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16))
        box_type.grid(row=1,column=0,pady=10,padx=20)

        btn_amount = CTkEntry(FLeft,placeholder_text="AMOUNT",text_color="#818181",textvariable=AMOUNT,width=200,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16),state="disabled")
        btn_amount.grid(row=1,column=1,pady=10,padx=20)

        btn_cost_price = CTkEntry(FLeft,placeholder_text="COST PRICE",text_color="#818181",textvariable=COST_PRICE,width=200,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16),state="disabled")
        btn_cost_price.grid(row=2,column=0,pady=10,padx=20)

        btn_price = CTkEntry(FLeft,placeholder_text="PRICE",text_color="#818181",textvariable=PRICE,width=200,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16),state="disabled")
        btn_price.grid(row=2,column=1,pady=10,padx=20)

        # //---------------------------Image Upload----------------------------------------

        img_path = os.path.join(self.appdir, "icon","upload.png")
        img_open = Image.open(img_path)
        img = CTkImage(img_open,size=(200,200))

        images = {}

        def upload_img():

            file_path = customtkinter.filedialog.askopenfilename(title="Select Image",filetypes=(("JPG files","*.jpg"),("JPEG files","*.jpeg"),("PNG files","*.png")))
            if (file_path):
                img_open = Image.open(file_path)

                img = CTkImage(img_open,size=(200,200))
                btn_image.configure(image=img)

                barcode = ID.get()
                images[barcode] = img_open
                

        btn_image = CTkButton(FLeft,state="disabled",command=upload_img,width=200,height=200,text="",image=img,fg_color="#FFFFFF",hover_color="#F7F7F7",corner_radius=0)
        btn_image.grid(row=4,column=0,columnspan=2,sticky="news",pady=10,padx=20)

        # //-----------------------Button Edit------------------------------

        def edit():
            if (inp_name.cget("state") == "disabled"):
                inp_id.configure(state="normal",text_color="#000000",border_color="#000000",fg_color="#FFFFFF")
                inp_name.configure(state="normal",text_color="#000000",border_color="#000000",fg_color="#FFFFFF")
                box_type.configure(border_color="#000000",fg_color="#FFFFFF",state="readonly")
                btn_amount.configure(state="normal",text_color="#000000",border_color="#000000",fg_color="#FFFFFF")
                btn_cost_price.configure(state="normal",text_color="#000000",border_color="#000000",fg_color="#FFFFFF")
                btn_price.configure(state="normal",text_color="#000000",border_color="#000000",fg_color="#FFFFFF")
                btn_image.configure(state="normal")

                btn_edit.configure(text="Save")

            else:
                inp_id.configure(state="disabled",text_color="#818181",border_color="#8D8D8D",fg_color="#FCFCFC")
                inp_name.configure(state="disabled",text_color="#818181",border_color="#8D8D8D",fg_color="#FCFCFC")
                box_type.configure(state="disabled",border_color="#8D8D8D",fg_color="#FCFCFC")
                btn_edit.configure(text="Edit")
                btn_amount.configure(state="disabled",text_color="#818181",border_color="#8D8D8D",fg_color="#FCFCFC")
                btn_cost_price.configure(state="disabled",text_color="#818181",border_color="#8D8D8D",fg_color="#FCFCFC")
                btn_price.configure(state="disabled",text_color="#818181",border_color="#8D8D8D",fg_color="#FCFCFC")
                btn_image.configure(state="disabled")

                barcode = ID.get()
                name_product = NAME.get()
                type_product = TYPE.get()
                cost_price = COST_PRICE.get()
                price = PRICE.get()
                amount = AMOUNT.get()

                data_stock[barcode] = (name_product,type_product,cost_price,price,amount)

        btn_edit = CTkButton(FLeft,text="Edit",command=edit,width=200,corner_radius=14,height=30,font=("Arial", 16))
        btn_edit.grid(row=3,column=0,columnspan=2,sticky="ew",pady=10,padx=20)

        def add_track():
            table_stock.insert("",END,values=("New","New Product","Type",float("0.0"),float("0.0"),int("0"),int("0")))
            table_stock.yview_moveto(1)

        def del_track():
            sure = CTkMessagebox(title="Delete Products",message="Are you sure to delete this products?",icon="warning",option_1="No",option_2="Yes")
            if (sure.get() == "No"):
                return
            else:
                selected_item = table_stock.selection()
                if selected_item:
                    for item in selected_item:
                        values = table_stock.item(item, "values")
                    id_products= values[0]  
                    
                    self.my_sql.del_products(id_products)

                    ID.set("Barcode")
                    NAME.set("Name")
                    TYPE.set("Type")
                    AMOUNT.set("0")
                    COST_PRICE.set("0.0")
                    PRICE.set("0.0")
                    btn_image.configure(image=img)
                    table_stock.delete(item)

        def apply():
            for barcode , values in data_stock.items():

                name_product , type_product , cost_price , price , amount = values

                result , err = self.my_sql.insert_products(barcode,name_product,type_product,cost_price,price,amount)
            
            data_stock.clear()
            
            for barcode, img in images.items():
                try:
                    rgb_img = img.convert('RGB')
                    save_path = os.path.join(self.appdir, "products",f"{barcode}.jpg")
                    
                    rgb_img.save(save_path, optimize=True, format='JPEG', quality=10)
                
                except Exception as e:
                    pass

            images.clear()        

            if (result == True):
                succ = CTkMessagebox(title="Success",message="Apply Changes Successfully!",icon="check",option_1="OK")
                if (succ.get() == "OK"):
                    show_products_table(on_search.get())
            else:
                boxmes = CTkMessagebox(title=f"Failed {err.errno}",message=f"Apply Changes Failed: {err}",icon="cancel",option_1="OK")
                if (boxmes.get() == "OK"):
                    show_products_table(on_search.get())
            
        btn_add = CTkButton(FLeft,width=100,height=40,text="Add",corner_radius=20,cursor="hand2",command=add_track)
        btn_add.grid(row=5,column=0,sticky="sw",padx=20,pady=20)

        btn_del = CTkButton(FLeft,width=100,height=40,text="Remove",corner_radius=20,fg_color="#FF3939",hover_color="#DF4949",cursor="hand2",command=del_track)
        btn_del.grid(row=5,column=0,columnspan=2 ,sticky="s",padx=20,pady=20)

        btn_apply = CTkButton(FLeft,width=100,height=40,text="Apply",corner_radius=20,cursor="hand2",command=apply)
        btn_apply.grid(row=5,column=1,sticky="se",padx=20,pady=20)

        # //----------------------Search-------------------------------
        def search(barcode):
            key_search.set(barcode)
            if (key_search.get() == ""):
                on_search.set(False)
            else:
                on_search.set(True)

            bar_type.set("ทั้งหมด")
            inp_search.delete(0,END)
            show_products_table(on_search.get())
            
    # //----------------------Table-------------------------------
        style = ttk.Style(self)
        style.configure("Treeview", font=("Arial", 12), rowheight=40,borderwidth=0, highlightthickness=0)       
        style.configure("Treeview.Heading", font=("Arial Bold", 12))  

        bar_type = CTkComboBox(FRight,width=200,values=all_type,command=lambda e_num:change_type(e_num),state="readonly") 
        bar_type.grid(row=0,column=0,padx=20,sticky="w")

        inp_search = CTkEntry(FRight,placeholder_text="Search",text_color="black",width=300,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16))
        inp_search.grid(row=0,column=0,pady=10,padx=140,sticky="e")

        appdir = Path(__file__).parent
        icon = appdir / "icon" 

        open_search_icon = Image.open(icon/"search.png")
        search_icon = CTkImage(light_image=open_search_icon,dark_image=open_search_icon,size=(20,20))

        btn_search = CTkButton(FRight,width=100,height=30,text="",corner_radius=20,image=search_icon,fg_color="#38f388",hover_color="#6be59e",cursor="hand2",command=lambda: search(inp_search.get()))
        btn_search.grid(row=0,column=0,pady=10,padx=20,sticky="e") 

        inp_search.bind("<Return>", lambda e: search(inp_search.get()))


        table_stock = ttk.Treeview(FRight,columns=("ID","NAME","TYPE","COST_PRICE","PRICE","AMOUNT","SELL"),show="headings")

        scrollbar = ttk.Scrollbar(FRight, orient="vertical", command=table_stock.yview)
        table_stock.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns")

        table_stock.heading("ID",text="ID")
        table_stock.heading("NAME",text="NAME")
        table_stock.heading("AMOUNT",text="AMOUNT")
        table_stock.heading("COST_PRICE",text="COST PRICE")
        table_stock.heading("PRICE",text="PRICE")
        table_stock.heading("SELL",text="SELL")

        table_stock.column("ID",width=70,anchor=CENTER)
        table_stock.column("NAME",width=200,anchor="w")
        table_stock.column("AMOUNT",width=30,anchor=CENTER)
        table_stock.column("COST_PRICE",width=45,anchor=CENTER)
        table_stock.column("PRICE",width=30,anchor=CENTER)
        table_stock.column("SELL",width=30,anchor=CENTER)

        table_stock.column("TYPE",width=0,stretch=False)

        table_stock.grid(row=1, column=0, sticky="nsew")

        # ------------------------Show Products--------------------------------

        def show_products_table(searchs,types="ทั้งหมด",num=0):
            table_stock.delete(*table_stock.get_children())
            num_page.set(num)
            if (searchs == False):
                result = self.my_sql.show_products(types,num)

                row_list = self.my_sql.all_row(types)
                show_row = [f"{i}" for i in range(row_list+1)]

                amount_page_scroll.configure(values=show_row)

                for i in result:
                    id = i[0]
                    name = i[1]
                    p_type = i[2]
                    cost_price = i[3]
                    price = i[4]
                    amount = i[5]
                    sell = i[6]
                    table_stock.insert("",END,values=(id,name,p_type,cost_price,price,amount,sell))
            else:
                p_id , p_name, p_type, p_price, p_cost_price, p_amount, p_sell ,id_search = self.my_sql.search_products(key_search.get(),num)  

                if (id_search != None):
                    table_stock.delete(*table_stock.get_children())
                    row_search_list = self.my_sql.all_row(types,on_search.get(),key_search.get())
                    row_search = [f"{i}" for i in range(row_search_list+1)]

                    amount_page_scroll.configure(values=row_search)

                    for i in id_search:
                        id = i[0]
                        name = i[1]
                        ty = i[2]
                        cost_price = i[3]
                        price = i[4]
                        amount = i[5]
                        sell = i[6]
                        table_stock.insert("",END,values=(id,name,ty,cost_price,price,amount,sell))
                else:
                    table_stock.delete(*table_stock.get_children())
                    table_stock.insert("",END,values=(p_id,p_name,p_type,p_cost_price,p_price,p_amount,p_sell))
                    amount_page_scroll.configure(values=["0"])
                

        def select_product(event):
            select = table_stock.focus()
            values = table_stock.item(select,"values")

            barcode = values[0]
            name_product = values[1]
            type_product = values[2]
            cost_price = values[3]
            price = values[4]
            amount = values[5]

            ID.set(barcode)
            NAME.set(name_product)
            TYPE.set(type_product)
            COST_PRICE.set(cost_price)
            PRICE.set(price)
            AMOUNT.set(amount)

            img = os.path.join(self.appdir, "products") 
 
            try:
                open_pimg = Image.open(os.path.join(img,f"{barcode}.jpg"))
                pimg = CTkImage(open_pimg,size=(200,250))
            except FileNotFoundError:
                open_pimg = Image.open(os.path.join(img,"Default.jpg")) 
                pimg = CTkImage(open_pimg,size=(200,250))

            btn_image.configure(image=pimg)


        table_stock.bind("<Double-1>", select_product)
    # //-----------------------------Change Type-----------------------------
        def change_type(types):
            if (types == "Type"):
                types = "ทั้งหมด"
            TYPE.set(types)
            show_products_table(on_search.get(),TYPE.get())
            table_stock.yview_moveto(0)

    # //----------------------Button Next Page-------------------------------

        def change_page(page):
            if (TYPE.get() == "Type"):
                TYPE.set("ทั้งหมด")

            num_page.set(page)
            num = int(num_page.get())
            show_products_table(on_search.get(),TYPE.get(),num)

        def next_page():
            if (TYPE.get() == "Type"):
                TYPE.set("ทั้งหมด")

            types = TYPE.get()
            
            if (on_search.get() == False):
                num = int(num_page.get())
                all_row = self.my_sql.all_row(types)

                if (num < all_row):
                    new = num + 1
                    show_products_table(on_search.get(),types,new)
            else:
                num = int(num_page.get())
                all_row = self.my_sql.all_row(types,True,key_search.get())

                if (num < all_row):
                    new = num +1
                    show_products_table(on_search.get(),types,new)
            table_stock.yview_moveto(0)


        def back_page():
            if (TYPE.get() == "Type"):
                TYPE.set("ทั้งหมด")

            types = TYPE.get()
            
            if (on_search.get() == False):
                num = int(num_page.get())
                all_row = self.my_sql.all_row(types)
                if (num <= all_row and num != 0):
                    new = num - 1
                    show_products_table(on_search.get(),types,new)
            else:
                num = int(num_page.get())
                all_row = self.my_sql.all_row(types,True,key_search.get())
                
                if (num <= all_row and num != 0):
                    new = num - 1
                    show_products_table(on_search.get(),types,new)
            table_stock.yview_moveto(0)

        btn_next = CTkButton(FRight,width=100,height=40,font=("Arial Bold",16),text=">",corner_radius=20,fg_color="#38f388",hover_color="#6be59e",text_color="black",cursor="hand2",command=next_page)
        btn_next.grid(row=2,column=0,sticky="se",padx=(0,20),pady=20)

        btn_back = CTkButton(FRight,width=100,height=40,font=("Arial Bold",16),text="<",corner_radius=20,fg_color="#38f388",hover_color="#6be59e",text_color="black",cursor="hand2",command=back_page)
        btn_back.grid(row=2,column=0,sticky="sw",padx=(20,0),pady=20)

        show_products_table(on_search.get())

    def printer_ui(self):
        self.title("Printer")
        screen_x = self.winfo_screenwidth()
        screen_y = self.winfo_screenheight()

        x = int((screen_x / 2) - (520/2))
        y = int((screen_y / 2) - (240 / 2))
        self.geometry(f"{520}x{240}+{x}+{y-25}")
        self.resizable(False,False)

        icon = os.path.join(self.appdir, "icon","icon.ico")
        
        self.iconbitmap(icon)
        self.after(200, lambda: self.iconbitmap(icon))
        self.deiconify()
        self.attributes('-topmost', True)

        self.Frame_main = CTkFrame(self,fg_color="#dfdfdf", corner_radius=0)
        self.Frame_main.pack(fill=BOTH,expand=True)

        Frame = CTkFrame(self.Frame_main,fg_color="#ffffff", corner_radius=20)
        Frame.pack(fill=Y,expand=True,pady=20,padx=20)

        Frame.columnconfigure(3,weight=1)

        name_shop = CTkLabel(Frame,text="Name : ",font=("Arial Bold", 24),text_color="#000000")
        name_shop.grid(row=0,column=0,padx=20,sticky="w")

        inp_name = CTkEntry(Frame,placeholder_text="Name",textvariable=self.pname,text_color="#818181",corner_radius=10,height=25,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 14))
        inp_name.grid(row=0,column=1,columnspan=3,pady=15,padx=(0,40),sticky="news")

        l_vid = CTkLabel(Frame,text="VID:",font=("Arial Bold", 18),text_color="#000000")
        l_vid.grid(row=1,column=0,pady=15,padx=20,sticky="w")

        inp_vid = CTkEntry(Frame,placeholder_text="VID",textvariable=self.vid,text_color="#818181",width=85,corner_radius=10,height=25,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 14))
        inp_vid.grid(row=1,column=1,pady=15,padx=(0,40),sticky="w")

        l_pid = CTkLabel(Frame,text="PID:",font=("Arial Bold", 18),text_color="#000000")
        l_pid.grid(row=1,column=2,pady=15,padx=20,  sticky="w")

        inp_pid = CTkEntry(Frame,placeholder_text="PID",textvariable=self.pid,text_color="#818181",width=85,corner_radius=10,height=25,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 14))
        inp_pid.grid(row=1,column=3,pady=15,padx=(0,40),sticky="w")

        l_size = CTkLabel(Frame,text="Size:",font=("Arial Bold", 18),text_color="#000000")
        l_size.grid(row=2,column=0,pady=15,padx=20,sticky="w")

        box_size = CTkComboBox(Frame,values=["58mm","80mm"],variable=self.print_width,width=85,corner_radius=10,height=25,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 14),state="readonly")
        box_size.grid(row=2,column=1,pady=15,padx=(0,40),sticky="w")

        btn_enter = CTkButton(Frame,text="Enter",height=30,corner_radius=10,font=("Arial", 14),command=lambda: self.connect_printer(inp_name.get(),inp_vid.get(),inp_pid.get(),box_size.get()))
        btn_enter.grid(row=2,column=2,columnspan=3,pady=15,padx=20,sticky="news")
    
    def connect_printer(self,name,vid,pid,size):
        self.pname.set(name)
        self.vid.set(vid)
        self.pid.set(pid)
        if (size == "58mm"):
            self.printer[3] = 384
        else:
            self.printer[3] = 512

        new_setting = {
            "PRINTER_NAME" : self.pname.get(), 
            "PRINTER_VID":self.vid.get(),
            "PRINTER_PID":self.pid.get(),
            "PRINTER_WIDTH":self.printer[3]
            }
        
        self.data.edit_settings(self.setting_file ,new_setting)
        
        if (self.open_printer == None):
            self.open_printer = printer.Printer(self.pname.get(),self.vid.get(),self.pid.get(),self.printer[3])

        err = self.open_printer.connect_print()
        if (err == None):
            mes = CTkMessagebox(title="Printer Connected", message="Printer connected successfully!", icon="check")
            if (mes.get() == "OK"):
                self.destroy()
        else:
            mes =CTkMessagebox(title="Printer Error", message=f"Failed to connect to printer: {err}", icon="cancel")
            if (mes.get() == "OK"):
                self.destroy()
        
    def cash_ui(self,data_order,func,obj):
        self.title("Cash")
        screen_x = self.winfo_screenwidth()
        screen_y = self.winfo_screenheight()

        x = int((screen_x / 2) - (360/2))
        y = int((screen_y / 2) - (240 / 2))
        self.geometry(f"{320}x{240}+{x}+{y-25}")
        self.resizable(False,False)

        icon = os.path.join(self.appdir, "icon","icon.ico")
        
        self.iconbitmap(icon)
        self.after(200, lambda: self.iconbitmap(icon))
        self.deiconify()
        self.attributes('-topmost', True)
        self.register(False,False)
        
        Frame_main = CTkFrame(self,width=400,height=300,fg_color="white")
        Frame_main.pack(fill=BOTH,expand=True)

        inp_cash = CTkEntry(Frame_main,width=200,height=40,placeholder_text="Cash",font=("Arial",18))
        inp_cash.pack(pady=(50,0))

        inp_cash.bind("<Return>",lambda e:pay_cash(float(inp_cash.get())))

        def pay_cash(cash):
            price_cost_total = 0
            price_total = 0
            amount_order = 0
            bill_order = {}
            list_order = []
            on = True

            for id,value in data_order.items():
                name = value["name"]
                amount = value["amount"]
                cost_price = value["cost_price"]
                price = value["price"]
                total = value["total"]

                bill_order[id] = {
                    "name":name,
                    "amount":amount,
                    "cost_price":cost_price,
                    "price":price,
                    "total":total
                }

                list_order.append([id,name,amount,cost_price,price,total])

                price_cost_total += float(cost_price)
                price_total += float(total)
                amount_order += int(amount)
            
            if (self.open_printer == None):
                self.open_printer = printer.Printer(self.pname.get(),self.vid.get(),self.pid.get(),self.printer[3])
            
            self.open_main = main.main_gui(self.my_sql)
            if (cash - price_total >=0 and on == True):
                on = False
                change = cash - price_total

                
                obj.set(f"{amount_order}\n\n{price_total:.2f}\n\n{cash:.2f}\n\n{change:.2f}")

                mes = CTkMessagebox(title="Pay Succeed",message=f"ทอนเงิน : {change}",font=("Arial Bold",16),option_1="OK")
                if (mes.get() == "OK"):
                    func()
                    dates = self.my_sql.date_day_time()
                    count = self.my_sql.count_bill_id()
                    day_time = dates[0].strftime("%d/%m/%Y %H:%M:%S")

                    count_num = count[0]+1
                    bill_id = f"{self.pos} "+dates[0].strftime("%y%m%d") + str(f"{count_num:06d}")
                    

                    self.my_sql.insert_bill(self.pos,bill_id,dates[0],price_cost_total,price_total,int(inp_cash.get()),list_order)

                    html = self.open_printer.html_bill(bill_id,day_time,bill_order,cash)
                    threading.Thread(target=self.open_printer.print_bills,args=(bill_id,html)).start()
            
                    
                    self.destroy()
                else:
                    obj.set(f"{amount_order}\n\n{price_total:.2f}\n\n{0.00}\n\n{0.00}")
                    self.destroy()

        btn_pay = CTkButton(Frame_main,text="Pay",width=200,height=40,command=lambda:pay_cash(float(inp_cash.get())))
        btn_pay.pack(pady=15)

        self.after(500,lambda:inp_cash.focus_force())
    
    def pay_qrcode(self,data_order,func,obj,logo):
        bill_order = {}
        list_order = []
        on = True
        price_cost_total = 0
        price_total = 0
        amount_order = 0

        for id,value in data_order.items():
            name = value["name"]
            amount = value["amount"]
            cost_price = value["cost_price"]
            price = value["price"]
            total = value["total"]

            bill_order[id] = {
                "name":name,
                "amount":amount,
                "cost_price":cost_price,
                "price":price,
                "total":total
            }

            list_order.append([id,name,amount,cost_price,price,total])

            price_cost_total += float(cost_price)
            price_total += float(total)
            amount_order += int(amount)
        
        pay_load = qrcode.generate_payload(self.prompay,price_total)

        byte_io = BytesIO()

        img_qr = qrcode.to_image(pay_load)

        img_qr.save(byte_io,format="PNG")
        byte_io.seek(0)
        

        open_img = Image.open(byte_io)

        logo.configure(light_image=open_img,dark_image=open_img)

        if (self.open_printer == None):
            self.open_printer = printer.Printer(self.pname.get(),self.vid.get(),self.pid.get(),self.printer[3])

        if (on == True):
            on = False
            obj.set(f"{amount_order}\n\n{price_total:.2f}\n\n{price_total:.2f}\n\n{0.0}")

            mes = CTkMessagebox(title="Pay Succeed",message="ลูกค้าชำระเงินเรียบร้อยแล้ว ??",font=("Arial Bold",14),option_1="OK")

            if (mes.get() == "OK"):
                func()
                dates = self.my_sql.date_day_time()
                count = self.my_sql.count_bill_id()
                day_time = dates[0].strftime("%d/%m/%Y %H:%M:%S")

                count_num = count[0]+1
                bill_id = f"{self.pos} "+dates[0].strftime("%y%m%d") + str(f"{count_num:06d}")
                

                self.my_sql.insert_bill(self.pos,bill_id,dates[0],price_cost_total,price_total,int(price_total),list_order)

                html = self.open_printer.html_bill(bill_id,day_time,bill_order,int(price_total))
                threading.Thread(target=self.open_printer.print_bills,args=(bill_id,html)).start()
            
                    
                self.destroy()

            else:
                obj.set(f"{amount_order}\n\n{price_total:.2f}\n\n{0.00}\n\n{0.00}")
                self.destroy()

            open_icon = Image.open(os.path.join(self.appdir, "icon","icon.png"))
            resize = open_icon.resize((410,410))
            logo.configure(light_image=resize,dark_image=resize)


    def audit_ui(self):
        self.title("Audit")
        screen_x = self.winfo_screenwidth()
        screen_y = self.winfo_screenheight()

        x = int((screen_x / 2) - (1280/2))
        y = int((screen_y / 2) - (720 / 2))
        self.geometry(f"{1280}x{720}+{x}+{y-25}")

        icon = os.path.join(self.appdir, "icon","icon.ico")
        
        self.iconbitmap(icon)
        self.after(200, lambda: self.iconbitmap(icon))
        self.deiconify()

        PAGE = IntVar(value="0")
        ALL_ROWS = IntVar(value="0")
        ID_BILL = StringVar(value="")
        TIME = StringVar(value="")
        PAY = IntVar(value="")
        DATE_START = StringVar(value=None)
        DATE_END = StringVar(value=None)

        list_order_bill = []
        order_bill = {}

        frame_main = CTkFrame(self,fg_color="#FFFFFF", corner_radius=0)
        frame_main.pack(fill=BOTH,expand=True)

        FLeft = CTkFrame(frame_main,width=800,fg_color="#dfdfdf", corner_radius=0)
        FLeft.pack(side=LEFT, fill=BOTH)
        FLeft.rowconfigure(5,weight=1)

        FRight = CTkFrame(frame_main,fg_color="#D4D4D4", corner_radius=0)
        FRight.pack(side=RIGHT, fill=BOTH,expand=True)
        FRight.columnconfigure(0,weight=1)

        def change_day(date):
            self.date_time.set(date)
            list_bill()

        def list_bill(search=None):
            data_bills , all_row , b_cost , b_price = self.my_sql.show_bill(self.date_time.get(),PAGE.get(),DATE_START.get(),DATE_END.get(),search)
            table_bill.delete(*table_bill.get_children())

            for i in data_bills:
                id = i[0]
                date = i[1]
                cost_price = i[2]
                price = i[3]
                pay = i[4]
                log = i[5]

                list_product = json.dumps(log,ensure_ascii=False)
                
                table_bill.insert("",END,values=(id,date,cost_price,price,pay,list_product))
            
            self.text_sales.set(f"\n{float(b_price)}\n\n{float(b_price) - float(b_cost)}\n")
            amount_page.set(PAGE.get())
            rows = [f"{i}" for i in range(0, all_row+1)]

            amount_page_scroll.configure(values=rows)
            ALL_ROWS.set(all_row)

        btn_day = CTkButton(FLeft,text="รายวัน",height=50,corner_radius=0,fg_color="white",bg_color="black",hover_color="#dfdfdf",font=("Arial Bold",16),text_color="black",command=lambda:change_day("Day"))
        btn_day.grid(row=0,column=0,sticky="news")

        btn_month = CTkButton(FLeft,text="รายเดือน",height=50,corner_radius=0,fg_color="white",bg_color="black",hover_color="#dfdfdf",font=("Arial Bold",16),text_color="black",command=lambda:change_day("Month"))
        btn_month.grid(row=0,column=1,sticky="news")

        btn_year= CTkButton(FLeft,text="รายปี",height=50,corner_radius=0,fg_color="white",bg_color="black",hover_color="#dfdfdf",font=("Arial Bold",16),text_color="black",command=lambda:change_day("Year"))
        btn_year.grid(row=0,column=2,sticky="news")

        dates = CTkDatePicker(FLeft)
        dates.set_allow_change_month(True)
        dates.set_date_format("%d-%m-%Y")
        dates.set_allow_manual_input(True) 
        dates.grid(row=1,column=0)

        dates_to = CTkDatePicker(FLeft,corner_radius=0)
        dates_to.set_allow_change_month(True)
        dates_to.set_date_format("%d-%m-%Y")
        dates_to.set_allow_manual_input(True) 
        dates_to.grid(row=1,column=1)

        def specify_date():
            self.date_time.set("")
            PAGE.set("0")

            d_start = datetime.strptime(dates.get_date(), "%d-%m-%Y").strftime("%Y-%m-%d")
            d_end = datetime.strptime(dates_to.get_date(), "%d-%m-%Y").strftime("%Y-%m-%d")

            DATE_START.set(d_start)
            DATE_END.set(d_end)

            list_bill()


        btn_dates = CTkButton(FLeft,text="OK",corner_radius=0,command=specify_date)
        btn_dates.grid(row=1,column=2,sticky="news")

        Title_Sales = CTkLabel(FLeft,text="\nยอดขาย : \n\nกำไร : \n",font=("Arial Bold",24),bg_color="white",justify=LEFT)
        Title_Sales.grid(row=2,column=0,sticky="news")

        self.text_sales = StringVar(value=f"\n{0.0}\n\n{0.0}\n")

        Sales = CTkLabel(FLeft,textvariable=self.text_sales,font=("Arial Bold",24),bg_color="white",justify=RIGHT)
        Sales.grid(row=2,column=1,columnspan=2,sticky="news")

        PromPay = CTkLabel(FLeft,text="PromPay :",font=("Arial Bold",24),height=60,bg_color="#264eff",text_color="white",justify=LEFT)
        PromPay.grid(row=3,column=0,sticky="news")

        inp_prom = CTkEntry(FLeft,textvariable=self.prom_str,state="disabled",bg_color="#dfdfdf",font=("Arial Bold",24),text_color="#818181",border_color="#8D8D8D")
        inp_prom.grid(row=3,column=1,columnspan=2,sticky="news")

        def edit_prom():
            if (inp_prom.cget("state") == "disabled"):
                inp_prom.configure(state="normal",text_color="#000000",border_color="#000000")
                btn_edit.configure(text="Save")
            else:
                
                try:
                    new_data = [
                        f"USERNAME={self.username}",
                        f"PASSWORD={self.passwords}",
                        f"REMEMBER={self.remember}",
                        f"POS={self.pos}",
                        f"SHIFT={self.shift}",
                        f"PROMPAY=0{int(inp_prom.get())}"
                    ]
                    inp_prom.configure(state="disabled",text_color="#818181",border_color="#8D8D8D")
                    self.prom_str.set(f"{inp_prom.get()}")
                    self.data.edit_data(self.account_file,new_data)
                    btn_edit.configure(text="Edit")
                except:
                    CTkMessagebox(title="Failed",message="Please Enter a Number.")
                    inp_prom.delete(0,END)
                    inp_prom.configure(state="disabled",text_color="#818181",border_color="#8D8D8D")
                    btn_edit.configure(text="Edit")

        btn_edit = CTkButton(FLeft,text="Edit",font=("Arial Bold",40),corner_radius=0,bg_color="#dfdfdf",height=60,command=edit_prom)
        btn_edit.grid(row=4,column=0,columnspan=3,sticky="news")

        data_bill = CTkTextbox(FLeft,width=400,height=200,corner_radius=0,font=("Arial", 16),border_width=2,border_color="#A7A7A7",fg_color="#FCFCFC",text_color="#818181")
        data_bill.configure(state="disabled")
        data_bill.grid(row=5,column=0,columnspan=3,sticky="news")

        def open_bill():
            order = json.dumps(list_order_bill,ensure_ascii=False)
            order_list = json.loads(order)

          
            file_html = os.path.join(self.bill_file,f"{ID_BILL.get()}.html")

            if (os.path.exists(file_html)):
                webbrowser.open(f"file://{file_html}")

            else:
                for i in order_list:
                    id = i [0]
                    name = i[1]
                    amount = i[2]
                    cost = i[3]
                    price = i[4]
                    total = price * amount

                    order_bill[id] = {
                        "name":name,
                        "amount":amount,
                        "cost_price":cost,
                        "price":price,
                        "total":total
                    }
                
                if (self.open_printer == None):
                    self.open_printer = printer.Printer(self.pname.get(),self.vid.get(),self.pid.get(),self.printer[3])
                
                html = self.open_printer.html_bill(ID_BILL.get(),TIME.get(),order_bill,PAY.get())
                with open(file_html, "w", encoding="utf-8") as f:
                    f.write(html)
                webbrowser.open(f"file://{file_html}")

        btn_open_bill = CTkButton(FLeft,text="Open Bill",height=80,corner_radius=0,command=open_bill)
        btn_open_bill.grid(row=6,column=0,columnspan=3,sticky="news")


        def cancel_bill():
            order = json.dumps(list_order_bill,ensure_ascii=False)
            order_list = json.loads(order)

            mes = CTkMessagebox(title="CanCel Bill",message=f"Are you sure cacnel bill: {ID_BILL.get()}",option_1="CANCEL",option_2="OK")

            if (mes.get() == "OK"):
                for i in order_list:
                    id = i [0]
                    name = i[1]
                    amount = i[2]
                    cost = i[3]
                    price = i[4]
                    total = price * amount

                    order_bill[id] = {
                        "name":name,
                        "amount":amount,
                        "cost_price":cost,
                        "price":price,
                        "total":total
                    }
                
                for id,value in order_bill.items():
                    name = value["name"]
                    amount = value["amount"]
                    cost = value["cost_price"]
                    price = value["price"]
                    total = value["total"]

                    self.my_sql.cancel_bill(ID_BILL.get(),id,amount)
                
                list_bill()

        btn_cancel_bill = CTkButton(FLeft,text="Cancel Bill",height=80,corner_radius=0,fg_color="#f33838",hover_color="#f66b6b",command=cancel_bill)
        btn_cancel_bill.grid(row=7,column=0,columnspan=3,sticky="news")

        bill_search = CTkEntry(FRight,placeholder_text="Search Bill ID",height=30,width=300,font=("Arial Bold",16))
        bill_search.grid(row=0,column=0,sticky="e",padx=(0,100),pady=10)

        open_img = Image.open(os.path.join(self.appdir,"icon","search.png"))
        icon_search = CTkImage(open_img,size=(25,25))

        def search_bill():
            if (bill_search.get() != ""):
                list_bill(bill_search.get())
            else:
                list_bill()

        btn_search = CTkButton(FRight,image=icon_search,width=80,corner_radius=20,text="",fg_color="#38f388",hover_color="#6be59e",command=search_bill)
        btn_search.grid(row=0,column=0,sticky="e",pady=10)

        bill_search.bind("<Return>",lambda e:search_bill())

        # //------------------------------------Table-----------------------------------------------------
        style = ttk.Style(self)
        style.configure("Treeview", font=("Arial", 12), rowheight=40,borderwidth=0, highlightthickness=0)       
        style.configure("Treeview.Heading", font=("Arial Bold", 12))  

        table_bill = ttk.Treeview(FRight,columns=("ID","Time","Cost Price","Price","Pay","Log"),show="headings")

        scrollbar = ttk.Scrollbar(FRight, orient="vertical", command=table_bill.yview)
        table_bill.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns")

        FRight.columnconfigure(0,weight=1)
        FRight.rowconfigure(1,weight=1)

        table_bill.heading("ID",text="ID")
        table_bill.heading("Time",text="Time")
        table_bill.heading("Cost Price",text="Cost Price")
        table_bill.heading("Price",text="Price")
        table_bill.heading("Pay",text="Pay")

        table_bill.column("ID",width=30,anchor=CENTER)
        table_bill.column("Time",width=100,anchor="w")
        table_bill.column("Price",width=30,anchor=CENTER)
        table_bill.column("Pay",width=100,anchor=CENTER)

        table_bill.column("Cost Price",width=0,stretch=False)
        table_bill.column("Log",width=0,stretch=False)

        table_bill.grid(row=1, column=0, sticky="nsew")


        def select_bill(event):
            select = table_bill.focus()
            values = table_bill.item(select,"values")
            row = 1.0

            ID_BILL.set(values[0])
            TIME.set(values[1])
            PAY.set(values[4])

            products = values[5]
            loads_products = json.loads(products)
            list_products = json.loads(loads_products)


            data_bill.configure(state="normal")
            data_bill.delete("0.0","end")

            data_bill.insert("1.0","ID Bill : ","readonly")
            data_bill.insert("1.end",f"{ID_BILL.get()}\n")

            list_order_bill.clear()
            order_bill.clear()


            for i in list_products:
                p_id = i[0]
                name = i[1]
                amount = i[2]
                cost = i[3]
                price = i[4]
                total = i[5]

                row += 1.0
               
                data_bill.insert(f"{row}",f"{p_id:<15} {name[0:20]+" ...":<20} {amount:<12} {price:<10} {total:<10}\n")
                list_order_bill.append([p_id,name[0:20]+" ...",amount,cost,price])

            data_bill.configure(state="disabled")
            
        table_bill.bind("<Double-1>", select_bill)

        data_bills , all_row , cost , price = self.my_sql.show_bill(self.date_time.get(),PAGE.get())
        rows = [f"{i}" for i in range(0, all_row+1)]

        ALL_ROWS.set(all_row)


        def next_page():
            if (PAGE.get() < (ALL_ROWS.get())):
                PAGE.set(PAGE.get()+1)
                list_bill()
        
        def back_page():
            if (PAGE.get() > 0 and PAGE.get() <= (ALL_ROWS.get())):
                PAGE.set(PAGE.get()-1)
                list_bill()

        def change_page(num):
            PAGE.set(num)
            list_bill()


        btn_next = CTkButton(FRight,width=100,height=40,font=("Arial Bold",16),text=">",corner_radius=20,fg_color="#38f388",hover_color="#6be59e",text_color="black",cursor="hand2",command=next_page)
        btn_next.grid(row=2,column=0,sticky="se",padx=(0,20),pady=20)

        btn_back = CTkButton(FRight,width=100,height=40,font=("Arial Bold",16),text="<",corner_radius=20,fg_color="#38f388",hover_color="#6be59e",text_color="black",cursor="hand2",command=back_page)
        btn_back.grid(row=2,column=0,sticky="sw",padx=(20,0),pady=20)

        amount_page = CTkComboBox(FRight,width=80,state="readonly",variable=rows)
        amount_page_scroll = CTkScrollableDropdown(amount_page,values=rows,justify="left", button_color="transparent",command=lambda e_num:change_page(e_num))
        amount_page.grid(row=2,column=0,columnspan=2,sticky="S",pady=25)

        list_bill()

        self.after(200,lambda:dates.focus_force())
