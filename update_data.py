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
from tkinter import ttk

def gui_account(my_sql):
# //-----------------------------------------------------
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

# //-----------------------------------------------------

    account_gui = CTKUI("Stock List", 1280, 600, "#7cffac", "light")
    account_gui.attributes("-topmost",True)

    FLeft = CTkFrame(account_gui,width=400,fg_color="#7cffac", corner_radius=0)
    FLeft.pack(side=LEFT, fill=BOTH)

    FLeft.columnconfigure(0,weight=1)
    FLeft.rowconfigure(2,weight=1)

    FRight = CTkFrame(account_gui,fg_color="#FFFFFF", corner_radius=0)
    FRight.pack(side=RIGHT, fill=BOTH,expand=True)

    FRight.columnconfigure(0,weight=1)
    FRight.rowconfigure(0,weight=1)

    ID = StringVar(value="")
    USER = StringVar(value="Username")
    PASS = StringVar(value="Password")
    LEVEL = StringVar(value="Level")

    data_account = {}

    inp_user = CTkEntry(FLeft,placeholder_text="Username",text_color="#818181",textvariable=USER,width=200,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16),state="disabled")
    inp_user.grid(row=0,column=0,pady=(40,10),padx=20)

    inp_level = CTkComboBox(FLeft,values=["1","2","3"],variable=LEVEL,state="disabled",width=100,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16))
    inp_level.grid(row=0,column=1,pady=(40,10),padx=20)

    inp_pass = CTkEntry(FLeft,placeholder_text="Password",text_color="#818181",textvariable=PASS,show="●",width=200,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16),state="disabled")
    inp_pass.grid(row=1,column=0,pady=20,padx=20)


    id_ac = 8000  
    id_em = 6000
# //-----------------------------Add Track------------------------------------------
    def add_track():
        nonlocal id_ac , id_em
        sql = my_sql.cursor()
        sql.execute("SELECT id FROM `stock_list`.`accounts`;")
        resulte = sql.fetchall()
        len_id_ac = len(resulte) + id_ac
        len_id_em = len(resulte) + id_em

        table_account.insert("",END,values=(len_id_em,len_id_ac,"New","","","","","","",""))
        id_ac += 1
        id_em += 1
# //-----------------------------Delete Track------------------------------------------
    def del_track():
        sure = CTkMessagebox(title="Delete Account",message="Are you sure to delete this account?",icon="warning",option_1="No",option_2="Yes")
        if (sure.get() == "No"):
            return
        else:
            selected_item = table_account.selection()
            if selected_item:
                for item in selected_item:
                    values = table_account.item(item, "values")
                id_account = values[1]  
                sql = my_sql.cursor()
                sql.execute("DELETE FROM `stock_list`.`accounts` WHERE `id` = %s;", (id_account,))
                my_sql.commit()
                load_data(0)
# //-----------------------------Apply------------------------------------------
    def apply():
        sql = my_sql.cursor()
        for id_account , values in data_account.items():

            user , level , password , emp_id , f_name , l_name , contact , address = values

            sql.execute("SELECT `id` FROM `stock_list`.`accounts` WHERE `id` = %s;", (id_account,))
            resulte = sql.fetchall()
            if (not resulte):
                sql.execute("INSERT INTO `stock_list`.`accounts` (`id`, `username`, `passwords`, `level` , `onlines`) VALUES (%s, %s, %s, %s,%s);", (id_account, user, password, level, 0))

                sql.execute("INSERT INTO `stock_list`.`employee` (`emp_id` ,`account_id`, `first_name`, `last_name` , `address` , `contact`) VALUES (%s,%s, %s, %s, %s, %s);", (emp_id,id_account, f_name, l_name , address , contact))
            else:
                sql.execute("""update `stock_list`.`employee` join `stock_list`.`accounts` on `employee`.`account_id` = `accounts`.`id` set `accounts`.`username` = %s, `accounts`.`passwords` = %s, `accounts`.`level` = %s, `employee`.`emp_id` = %s ,`employee`.`first_name` = %s, `employee`.`last_name` = %s, `employee`.`contact` = %s, `employee`.`address` = %s where `accounts`.`id` = %s;""" , (user,password,level,emp_id,f_name,l_name,contact,address,id_account))
        
        my_sql.commit()
        data_account.clear()
         
        succ = CTkMessagebox(title="Success",message="Apply Changes Successfully!",icon="check",option_1="OK")
        if (succ.get() == "OK"):
            load_data(0)


    btn_add = CTkButton(FLeft,width=100,height=40,text="Add",corner_radius=20,command=add_track)
    btn_add.grid(row=3,column=0,sticky="sw",padx=20,pady=20)

    btn_del = CTkButton(FLeft,width=100,height=40,text="Remove",corner_radius=20,fg_color="#FF3939",hover_color="#DF4949",cursor="hand2",command=del_track)
    btn_del.grid(row=3,column=0,columnspan=2,sticky="s",padx=20,pady=20)

    btn_apply = CTkButton(FLeft,width=100,height=40,text="Apply",corner_radius=20,command=apply)
    btn_apply.grid(row=3,column=1,sticky="se",padx=20,pady=20)

# //-----------------------Button Next Page------------------------------
    num_page = IntVar(value=0)
    def next_page():
        if (num_page.get() < all_row):
            num_page.set(num_page.get()+1)
            amount_page.set(num_page.get())
            load_data(num_page.get())
           

    def back_page():
        if (num_page.get() > 0):
            num_page.set(num_page.get()-1)
            amount_page.set(num_page.get())
            load_data(num_page.get())

    sql = my_sql.cursor()
    sql.execute("SELECT COUNT(*) FROM `stock_list`.`accounts`;")
    all_amount = sql.fetchone()[0]
    all_row = int(all_amount)//50
    value =[f"{i}"for i in range(all_row+1)]

    btn_next = CTkButton(FRight,width=100,height=40,font=("Arial Bold",16),text=">",corner_radius=20,fg_color="#38f388",hover_color="#6be59e",text_color="black",cursor="hand2",command=next_page)
    btn_next.grid(row=2,column=0,sticky="se",padx=(0,20),pady=20)

    btn_back = CTkButton(FRight,width=100,height=40,font=("Arial Bold",16),text="<",corner_radius=20,fg_color="#38f388",hover_color="#6be59e",text_color="black",cursor="hand2",command=back_page)
    btn_back.grid(row=2,column=0,sticky="sw",padx=(20,0),pady=20)

    def change_page(page):
        num_page.set(page)
        amount_page.set(num_page.get())
        load_data(num_page.get())

    amount_page = CTkComboBox(FRight,width=80,values=value)
    amount_page_scroll = CTkScrollableDropdown(amount_page,values=value,justify="left", button_color="transparent",command=change_page)
    amount_page.grid(row=2,column=0,columnspan=2,sticky="S",pady=25)


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

            data_account[id] = (user,level,password,em_id,f_name,l_name,contact,address)
                
    btn_edit = CTkButton(FLeft,text="Edit",width=150,corner_radius=14,height=30,font=("Arial", 16),command=edit)
    btn_edit.grid(row=1,column=1,pady=20,padx=20)


# //-------------------------Table----------------------------
    data_employee = CTkTextbox(FLeft,width=400,height=200,corner_radius=20,font=("Arial", 16),border_width=2,border_color="#A7A7A7",fg_color="#FCFCFC",text_color="#818181")
    data_employee.configure(state="disabled")
    data_employee.grid(row=2,column=0,columnspan=2,pady=10,padx=20,sticky="nsew")

    style = ttk.Style(account_gui)
    style.configure("Treeview", font=("Arial", 12), rowheight=40,borderwidth=0, highlightthickness=0)       
    style.configure("Treeview.Heading", font=("Arial Bold", 12))  

    table_account = ttk.Treeview(FRight,columns=("ID_EM","ID","Username","Level","Employee","First_Name","Last_Name","Password","Address","Contact"),show="headings")

    scrollbar = ttk.Scrollbar(FRight, orient="vertical", command=table_account.yview)
    table_account.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    table_account.heading("ID",text="ID")
    table_account.heading("Username",text="Username")
    table_account.heading("Level",text="Level")
    table_account.heading("Employee",text="Employee")

    table_account.column("ID_EM",width=0,stretch=False)
    table_account.column("ID",width=30,anchor=CENTER)
    table_account.column("Username",width=100,anchor="w")
    table_account.column("Level",width=30,anchor=CENTER)
    table_account.column("Employee",width=100,anchor=CENTER)

    table_account.column("First_Name",width=0,stretch=False)
    table_account.column("Last_Name",width=0,stretch=False)
    table_account.column("Password",width=0,stretch=False)
    table_account.column("Address",width=0,stretch=False)
    table_account.column("Contact",width=0,stretch=False)

    table_account.grid(row=0, column=0, sticky="nsew")

    def select_data(event):
        select = table_account.focus()
        values = table_account.item(select,"values")

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

    table_account.bind("<Double-1>", select_data)

# //-----------------------Load Data------------------------------
    def load_data(num):
        table_account.delete(*table_account.get_children())
        sql = my_sql.cursor()
        sql.execute("SELECT * FROM stock_list.employee join `stock_list`.`accounts` on `employee`.`account_id` = `accounts`.`id` order by `accounts`.`id` asc limit 50 offset %s;" ,(num*50,))
        resulte = sql.fetchall()

        for i in resulte:
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

            table_account.insert("",END,values=(id_employee,id_user,user,level,employee,f_name,l_name,password,address,contact))
        table_account.yview_moveto(0)
    load_data(0)


def gui_stock(my_sql):
# //-----------------------------------------------------
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

# //-----------------------------------------------------


# //----------------------GUI-------------------------------
    stockt_gui = CTKUI("Stock List", 1280, 600, "#7cffac", "light")
    stockt_gui.attributes("-topmost",True)

    FLeft = CTkFrame(stockt_gui,width=400,fg_color="#7cffac", corner_radius=0)
    FLeft.pack(side=LEFT, fill=BOTH)

    FLeft.columnconfigure(0,weight=1)
    FLeft.rowconfigure(4,weight=1)

    FRight = CTkFrame(stockt_gui,fg_color="#FFFFFF", corner_radius=0)
    FRight.pack(side=RIGHT, fill=BOTH,expand=True)

    FRight.columnconfigure(0,weight=1)
    FRight.rowconfigure(1,weight=1)

# //-----------------------------------------------------


# //---------------------Frame-------------------------------

    ID = StringVar(value="Barcode")
    NAME = StringVar(value="Name Product")
    TYPE = StringVar(value="Type")
    COST_PRICE = IntVar(value="Cost Price")
    PRICE = IntVar(value="Price")
    AMOUNT = IntVar(value="Amount")
    num_page = IntVar(value=0)
    all_row = IntVar(value=0)
    on_search = BooleanVar(value=False)

    data_stock= {}

    def change_page(page,on):
        num_page.set(page)
        amount_page.set(num_page.get())
        if (on == False):
            show_products_table(bar_type.get(),num_page.get(),False)
        else:
            search(inp_search.get(),num_page.get())

    sql = my_sql.cursor()
    sql.execute("SELECT COUNT(*) FROM `stock_list`.`products`;")
    all_amount = sql.fetchone()[0]
    all_row = IntVar(value=int(all_amount)//50)
    value =[f"{i}"for i in range(all_row.get()+1)]

    amount_page = CTkComboBox(FRight,width=80,values=value)
    amount_page_scroll = CTkScrollableDropdown(amount_page,values=value,justify="left", button_color="transparent",command=lambda page:change_page(page, on_search.get()))
    amount_page.grid(row=2,column=0,columnspan=2,sticky="S",pady=25)


    all_type = sql.execute("SELECT DISTINCT p_type FROM stock_list.products;")
    products_type = sql.fetchall()

    type_list = [t[0] for t in products_type]

    inp_id = CTkEntry(FLeft,placeholder_text="ID",text_color="#818181",textvariable=ID,width=200,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16),state="disabled")
    inp_id.grid(row=0,column=0,pady=(40,10),padx=20)

    inp_name = CTkEntry(FLeft,placeholder_text="NAME",text_color="#818181",textvariable=NAME,width=200,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16),state="disabled")
    inp_name.grid(row=0,column=1,pady=(40,10),padx=20)

    box_type = CTkComboBox(FLeft,values=type_list,variable=TYPE,state="disabled",width=200,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16))
    box_type.grid(row=1,column=0,pady=10,padx=20)

    btn_amount = CTkEntry(FLeft,placeholder_text="AMOUNT",text_color="#818181",textvariable=AMOUNT,width=200,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16),state="disabled")
    btn_amount.grid(row=1,column=1,pady=10,padx=20)

    btn_cost_price = CTkEntry(FLeft,placeholder_text="COST PRICE",text_color="#818181",textvariable=COST_PRICE,width=200,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16),state="disabled")
    btn_cost_price.grid(row=2,column=0,pady=10,padx=20)

    btn_price = CTkEntry(FLeft,placeholder_text="PRICE",text_color="#818181",textvariable=PRICE,width=200,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16),state="disabled")
    btn_price.grid(row=2,column=1,pady=10,padx=20)

    add_dir = Path(__file__).parent
    img_path = add_dir / "icon" / "upload.png"
    img_open = Image.open(img_path)
    img = CTkImage(light_image=img_open,dark_image=img_open,size=(200,200))

# //---------------------------Image Upload----------------------------------------

    images = {}

    def upload_img():
            stockt_gui.attributes("-topmost",False)

            file_path = customtkinter.filedialog.askopenfilename(title="Select Image",filetypes=(("JPG files","*.jpg"),("JPEG files","*.jpeg"),("PNG files","*.png")))
            if (file_path):
                img_open = Image.open(file_path)

                img = CTkImage(light_image=img_open ,dark_image=img_open,size=(200,200))
                btn_image.configure(image=img)

                barcode = ID.get()
                images[barcode] = img_open
                
            stockt_gui.attributes("-topmost",True)

    btn_image = CTkButton(FLeft,state="disabled",command=upload_img,width=200,height=200,text="",image=img,fg_color="#FFFFFF",hover_color="#F7F7F7",corner_radius=0)
    btn_image.grid(row=4,column=0,columnspan=2,sticky="news",pady=10,padx=20)


# //-----------------------Button Edit------------------------------
    def edit():
        if (inp_name.cget("state") == "disabled"):
            inp_id.configure(state="normal",text_color="#000000",border_color="#000000",fg_color="#FFFFFF")
            inp_name.configure(state="normal",text_color="#000000",border_color="#000000",fg_color="#FFFFFF")
            box_type.configure(state="normal",border_color="#000000",fg_color="#FFFFFF")
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
# //-----------------------------------------------------

# //---------------------------Apply-----------------------------------------
    def apply():
        sql = my_sql.cursor()
        for barcode , values in data_stock.items():

            name_product , type_product , cost_price , price , amount = values

            sql.execute("SELECT `p_id` FROM `stock_list`.`products` WHERE `p_id` = %s;", (barcode,))
            resulte = sql.fetchall()
            if (not resulte):
                sql.execute("INSERT INTO `stock_list`.`products` (`p_id`, `p_name`, `p_type`, `p_cost_price`, `p_price`, `p_amount`, `p_sell`) VALUES (%s, %s, %s, %s, %s, %s, %s);", (barcode, name_product, type_product, cost_price, price, amount, 0))
            else:
                sql.execute("UPDATE `stock_list`.`products` SET `p_name` = %s, `p_type` = %s, `p_cost_price` = %s, `p_price` = %s, `p_amount` = %s WHERE `p_id` = %s;", (name_product, type_product, cost_price, price, amount, barcode))
        
        my_sql.commit()
        data_stock.clear()
         
        for barcode, img in images.items():
            try:
                rgb_img = img.convert('RGB')
                appdir = Path(__file__).parent
                save_path = appdir / "products" / f"{barcode}.jpg"
                
                rgb_img.save(save_path, optimize=True, format='JPEG', quality=10)
            
            except Exception as e:
                pass

        images.clear()        

        succ = CTkMessagebox(title="Success",message="Apply Changes Successfully!",icon="check",option_1="OK")
        if (succ.get() == "OK"):
            show_products_table("ทั้งหมด",num_page.get(),False)

# //---------------------------Add Track-----------------------------------------  
         
    def add_track():
        table_stock.insert("",END,values=("New","New Product","Type",float("0.0"),float("0.0"),int("0"),int("0")))
        table_stock.yview_moveto(1)
# //---------------------------Delete Track-----------------------------------------  
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
                    sql = my_sql.cursor()
                    sql.execute("DELETE FROM `stock_list`.`products` WHERE `p_id` = %s;", (id_products,))
                    my_sql.commit()
                    ID.set("Barcode")
                    NAME.set("Name")
                    TYPE.set("Type")
                    AMOUNT.set("0")
                    COST_PRICE.set("0.0")
                    PRICE.set("0.0")
                    btn_image.configure(image=img)
                    
                    show_products_table(bar_type.get(),num_page.get(),True)

# //----------------------Left Button-------------------------------

    btn_add = CTkButton(FLeft,width=100,height=40,text="Add",corner_radius=20,cursor="hand2",command=add_track)
    btn_add.grid(row=5,column=0,sticky="sw",padx=20,pady=20)

    btn_del = CTkButton(FLeft,width=100,height=40,text="Remove",corner_radius=20,fg_color="#FF3939",hover_color="#DF4949",cursor="hand2",command=del_track)
    btn_del.grid(row=5,column=0,columnspan=2 ,sticky="s",padx=20,pady=20)

    btn_apply = CTkButton(FLeft,width=100,height=40,text="Apply",corner_radius=20,cursor="hand2",command=apply)
    btn_apply.grid(row=5,column=1,sticky="se",padx=20,pady=20)
# //-----------------------------------------------------

# //----------------------Search-------------------------------
    name_products = StringVar(value="")
    def search(bar_code,num):
        inp_search.delete(0,END)
        sql.execute("SELECT * FROM `stock_list`.`products` WHERE `p_id` = %s",(bar_code,))
        products = sql.fetchone()

        on_search.set(True)

        if (bar_code == ""):
            on_search.set(False)
            num_page.set(0)
            num = num_page.get()
            show_products_table("ทั้งหมด",num,True)
            name_products.set("")
        
        elif (products):
            table_stock.delete(*table_stock.get_children())
            id = products[0]
            name = products[1]
            p_type = products[2]
            cost_price = products[3]
            price = products[4]
            amount = products[5]
            sell = products[6]

            table_stock.insert("",END,values=(id,name,p_type,cost_price,price,amount,sell))
            table_stock.yview_moveto(0)

        else:
            sql.execute("SELECT * FROM `stock_list`.`products` WHERE `p_name` LIKE %s ORDER BY `p_name` LIMIT 50 offset %s;" , (f"%{bar_code}%",num*50))
            search_products = sql.fetchall()

            sql.execute("SELECT COUNT(*) FROM `stock_list`.`products` WHERE `p_name` LIKE %s;" , (f"%{bar_code}%",))
            all_amount = sql.fetchone()[0]
            all_row.set(int(all_amount)//50)
            values =[f"{i}"for i in range(all_row.get()+1)]
            amount_page_scroll.configure(values=values)
            name_products.set(bar_code)

            table_stock.delete(*table_stock.get_children())
            for i in search_products:
                id = i[0]
                name = i[1]
                p_type = i[2]
                cost_price = i[3]
                price = i[4]
                amount = i[5]
                sell = i[6]

                table_stock.insert("",END,values=(id,name,p_type,cost_price,price,amount,sell))
            table_stock.yview_moveto(0)

# //----------------------Table-------------------------------
    style = ttk.Style(stockt_gui)
    style.configure("Treeview", font=("Arial", 12), rowheight=40,borderwidth=0, highlightthickness=0)       
    style.configure("Treeview.Heading", font=("Arial Bold", 12))  

    type_list_bar = ["ทั้งหมด"]+[t[0] for t in products_type]

    bar_type = CTkComboBox(FRight,width=200,values=type_list_bar,command=lambda value: show_products_table(value,0,True)) 
    bar_type.grid(row=0,column=0,padx=20,sticky="w")

    inp_search = CTkEntry(FRight,placeholder_text="Search",text_color="black",width=300,corner_radius=20,height=30,border_width=2,border_color="#8D8D8D",fg_color="#FCFCFC",font=("Arial", 16))
    inp_search.grid(row=0,column=0,pady=10,padx=140,sticky="e")

    appdir = Path(__file__).parent
    icon = appdir / "icon" 

    open_search_icon = Image.open(icon/"search.png")
    search_icon = CTkImage(light_image=open_search_icon,dark_image=open_search_icon,size=(20,20))

    btn_search = CTkButton(FRight,width=100,height=30,text="",corner_radius=20,image=search_icon,fg_color="#38f388",hover_color="#6be59e",cursor="hand2",command=lambda: search(inp_search.get(),num_page.get()))
    btn_search.grid(row=0,column=0,pady=10,padx=20,sticky="e") 

    inp_search.bind("<Return>", lambda e: search(inp_search.get(),num_page.get()))


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

        appdir = Path(__file__).parent
        img = appdir / "products"

        try:
            open_pimg = Image.open(f"{img/barcode}.jpg")
            pimg = CTkImage(light_image=open_pimg,dark_image=open_pimg,size=(200,250))
        except FileNotFoundError:
            open_pimg = Image.open(f"{img/"Default.jpg"}")
            pimg = CTkImage(light_image=open_pimg,dark_image=open_pimg,size=(200,250))

        btn_image.configure(image=pimg)

    table_stock.bind("<Double-1>", select_product)
# //-----------------------------------------------------

# //----------------------Show Products-------------------------------
    def show_products_table(type_products,num,reset):
        table_stock.delete(*table_stock.get_children())
        sql = my_sql.cursor()
        on_search.set(False)

        if (type_products != "ทั้งหมด"): #// ดึงข้อมูลตามประเภท
            sql.execute("SELECT * FROM `stock_list`.`products` WHERE `p_type` = %s ORDER BY `p_name` LIMIT 50 offset %s;" , (type_products,(num)*50,))
        else:
            sql.execute("SELECT * FROM `stock_list`.`products` ORDER BY `p_name` LIMIT 50 offset %s;" , (num*50,))

        resulte = sql.fetchall()

        if (type_products != "ทั้งหมด"): #// นับจำนวนข้อมูลตามประเภท
            sql.execute("SELECT COUNT(*) FROM `stock_list`.`products` WHERE `p_type` =  %s",(type_products,))
        else:
            sql.execute("SELECT COUNT(*) FROM `stock_list`.`products`")
        
        if (reset == True): #// รีเซ็ตหน้าเมื่อเปลี่ยนประเภท
            num_page.set(0)
            amount_page.set(num_page.get())


        all_amount = sql.fetchone()[0]

        all_row.set(int(all_amount)//50)
        values =[f"{i}"for i in range(all_row.get()+1)]
        amount_page_scroll.configure(values=values)
        
        for i in resulte:
           id = i[0]
           name = i[1]
           p_type = i[2]
           cost_price = i[3]
           price = i[4]
           amount = i[5]
           sell = i[6]

           table_stock.insert("",END,values=(id,name,p_type,cost_price,price,amount,sell))
        table_stock.yview_moveto(0)
    
# //-----------------------------------------------------

# //----------------------Button Next Page-------------------------------

    def next_page(on):
        if (num_page.get() < all_row.get()):
            num_page.set(num_page.get()+1)
            amount_page.set(num_page.get())
            if (on == False):
                show_products_table(bar_type.get(),num_page.get(),False)
            else:
                search(name_products.get(),num_page.get())

    def back_page(on):
        if (num_page.get() > 0):
            num_page.set(num_page.get()-1)
            amount_page.set(num_page.get())
            if (on == False):
                show_products_table(bar_type.get(),num_page.get(),False)     
            else:
                search(name_products.get(),num_page.get())

    btn_next = CTkButton(FRight,width=100,height=40,font=("Arial Bold",16),text=">",corner_radius=20,fg_color="#38f388",hover_color="#6be59e",text_color="black",cursor="hand2",command=lambda:next_page(on_search.get()))
    btn_next.grid(row=2,column=0,sticky="se",padx=(0,20),pady=20)

    btn_back = CTkButton(FRight,width=100,height=40,font=("Arial Bold",16),text="<",corner_radius=20,fg_color="#38f388",hover_color="#6be59e",text_color="black",cursor="hand2",command=lambda:back_page(on_search.get()))
    btn_back.grid(row=2,column=0,sticky="sw",padx=(20,0),pady=20)



    show_products_table("ทั้งหมด",num_page.get(),True)