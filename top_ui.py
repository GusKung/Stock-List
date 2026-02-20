from customtkinter import *
import customtkinter
from pathlib import Path
from CTkMessagebox import *
from CTkMenuBar import *
from CTkScrollableDropdown import CTkScrollableDropdown
from PIL import Image
import encode_file
from tkinter import ttk

class top_gui(CTkToplevel):
    def __init__(self,db=None):
        super().__init__()
        self.withdraw()

        self.data = encode_file.EncodeDecode()
        self.load_data = encode_file.EncodeDecode().load_data()

        self.username = self.load_data.get("USERNAME")
        self.passwords = self.load_data.get("PASSWORD")
        self.pos = self.load_data.get("POS")

        self.user_str = StringVar(value="")
        self.passwords_str = StringVar(value="")

        self.types = StringVar(value="ทั้งหมด")

        self.key_search = StringVar(value="")
        self.on_search = BooleanVar(value=False)
        self.on_reset = BooleanVar(value=False)

        self.appdir = Path(__file__).parent

        self.my_sql = db

        self.obj_list = []
        

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

            img_path = self.appdir / "icon" / "upload.png"
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

            obj["inp_type"] = CTkComboBox(Frame_Center,width=80,values=all_type)
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
                    paths = self.appdir / "products" / f"{barcode}.jpg"

                    rgb_img.save(paths,optimize=True,format='JPEG',quality=10)
                except:
                    img = None

                insert , err = self.my_sql.insert_products(barcode,name,types,cost_price,price,amount)
            
            if (insert == True):
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

    def user_ui(self):
        self.title(f"Add Products")
        screen_x = self.winfo_screenwidth()
        screen_y = self.winfo_screenheight()

        x = int((screen_x / 2) - (1280/2))
        y = int((screen_y / 2) - (720 / 2))
        self.geometry(f"{1280}x{720}+{x}+{y-25}")

        icon = self.appdir / "icon" / "icon.ico"
        
        self.iconbitmap(icon)
        self.after(200, lambda: self.iconbitmap(icon))
        self.deiconify()
        self.resizable(False,False)

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

            table_user.insert("",END,values=(len_id_em,len_id_user,"New","","","","","","",""))
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
                    
                    load_data_user(0)

        def change_page(page):
            page = int(page)
            PAGE.set(page)
            load_data_user(PAGE.get())

        def next_page():
            num = int(PAGE.get())
            if (num < all_row):
                PAGE.set(num+1)
                load_data_user(PAGE.get())
        
        def back_page():
            num = int(PAGE.get())
            if (num <= all_row and num != 0):
                PAGE.set(num-1)
                load_data_user(PAGE.get())

        # //-----------------------Button Edit------------------------------
        def edit():
            if (inp_user.cget("state") == "disabled"):
                inp_user.configure(state="normal",text_color="#000000",border_color="#000000",fg_color="#FFFFFF")
                inp_level.configure(state="normal",border_color="#000000",fg_color="#FFFFFF")
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
                self.my_sql.insert_user(id_user,user , level , password , emp_id , f_name , l_name , contact , address)

            succ = CTkMessagebox(title="Success",message="Apply Changes Successfully!",icon="check",option_1="OK")
            if (succ.get() == "OK"):
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

        amount_page = CTkComboBox(FRight,width=80,variable=PAGE)
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
