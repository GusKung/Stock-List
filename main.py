
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
import upload_data
import update_data

def main_gui(my_sql,a_user,a_pass):
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

    mydoc = os.path.expanduser('~\\Documents')
    localfile = mydoc + "\\Stock_List"

    file_account = localfile + "\\Account.env"

    appdir = Path(__file__).parent
    icon = appdir / "icon" 

    main = CTKUI("Stock List",1280,720,"#D4D4D4","light")
    
    num_page = IntVar(value=0)
    all_row = IntVar(value=0)
    on_page = BooleanVar(value=False)
    name_search = StringVar(value="")
# //----------------------------------------------------------------------


# //-------------------------------Menu---------------------------------------
    menu = CTkMenuBar(main)
    try:
        func_account = lambda:update_data.gui_account(my_sql)
        account_menu = menu.add_cascade("Account",fg_color="white",command= lambda:check_level(3,func_account))

        func_product = lambda: update_data.gui_stock(my_sql)
        stock_menu = menu.add_cascade("Stock",command= lambda:check_level(2,func_product))
    except Exception as e:
        CTkMessagebox(title="Error", message=f"Something went wrong: {e}", icon="cancel", option_1="OK")
# //----------------------------------------------------------------------


# //----------------------------------------------------------------------
    def next_page(on):
        num =  num_page.get()
        if (num < all_row.get()):
            num_page.set(num+1)
            amount_page.set(num_page.get())
            if (on == False):
                show_products(box_type.get(),num_page.get(),False)
            else:
                search_products_shows(name_search.get(),num_page.get())
    
    def next_last_page(on):
        num_page.set(all_row.get())
        amount_page.set(num_page.get())

        if (on == False):
            show_products(box_type.get(),all_row.get(),False)
        else:
            search_products_shows(name_search.get(),all_row.get())

    def back_page(on):
        num =  num_page.get()
        if (num > 0):
            num_page.set(num-1)
            amount_page.set(num_page.get())
            if (on == False):
                show_products(box_type.get(),num_page.get(),False)
            else:
                search_products_shows(name_search.get(),num_page.get())

    def back_last_page(on):
        num_page.set(0)
        amount_page.set(num_page.get())
        if (on == False):
            show_products(box_type.get(),0,False)
        else:
            search_products_shows(name_search.get(),0)

    sql = my_sql.cursor()

    FLeft= CTkFrame(main,fg_color="#D4D4D4",corner_radius=0,border_color="black",border_width=0)
    FLeft.pack(side=LEFT,fill=BOTH,expand=True)
    FLeft.columnconfigure(1,weight=1)
    FLeft.rowconfigure(1,weight=1)

    FProducts_Scroll = CTkScrollableFrame(FLeft,width=650,height=600,fg_color="#D4D4D4",corner_radius=0)
    FProducts_Scroll.grid(row=1,column=0,columnspan=3,sticky="news")

    btn_next = CTkButton(FLeft,font=("Arial Bold",18),command=lambda:next_page(on_page.get()),text=">",text_color="black",width=65,height=40,corner_radius=12,fg_color="#38f388",hover_color="#6be59e")
    btn_next.grid(row=2,column=1,sticky="SE",pady=20,padx=(0,100))

    btn_last_next = CTkButton(FLeft,font=("Arial Bold",18),command=lambda:next_last_page(on_page.get()),text=">>",text_color="black",width=65,height=40,corner_radius=12,fg_color="#38f388",hover_color="#6be59e")
    btn_last_next.grid(row=2,column=1,sticky="SE",pady=20,padx=(0,20))

    def change_page(page):
        num_page.set(page)
        amount_page.set(num_page.get())
        show_products(box_type.get(),num_page.get(),False)

    value =[f"{i}"for i in range(all_row.get()+1)]

    amount_page = CTkComboBox(FLeft,width=80,values=value)
    amount_page.grid(row=2,column=0,columnspan=2,sticky="S",pady=25)

    amount_page_scroll = CTkScrollableDropdown(amount_page,values=value,justify="left", button_color="transparent",command=change_page)

    btn_back = CTkButton(FLeft,font=("Arial Bold",18),command=lambda:back_last_page(on_page.get()),text="<<",text_color="black",width=65,height=40,corner_radius=12,fg_color="#38f388",hover_color="#6be59e")
    btn_back.grid(row=2,column=0,sticky="SW",pady=20,padx=(20,0))

    btn_last_back = CTkButton(FLeft,font=("Arial Bold",18),command=lambda:back_page(on_page.get()),text="<",text_color="black",width=65,height=40,corner_radius=12,fg_color="#38f388",hover_color="#6be59e")
    btn_last_back.grid(row=2,column=0,sticky="SW",pady=20,padx=(100,0))

    inp_product = CTkEntry(FLeft,font=("Arial Bold",14),width=250,corner_radius=20,border_color="#3B3B3B")

    inp_product.grid(row=0, column=0,padx=(20,10),pady=20,sticky="WE")

    inp_product.focus_set()
    inp_product.bind("<Return>",lambda e:search_product(inp_product.get()))

    open_search_icon = Image.open(icon/"search.png")
    search_icon = CTkImage(light_image=open_search_icon,dark_image=open_search_icon,size=(20,20))

    def search_products_shows(bar_code,num_page):
        sql.execute("SELECT `p_id` , `p_name` , `p_price` FROM `stock_list`.`products` WHERE `p_name` LIKE %s LIMIT 40 offset %s;",(f"%{bar_code}%",num_page*40))  
        products = sql.fetchall()

        sql.execute("SELECT COUNT(*) FROM `stock_list`.`products` WHERE `p_name` LIKE %s;",(f"%{bar_code}%",))
        all_amount = sql.fetchone()[0]

        appdir = Path(__file__).parent
        img_products = appdir / "products" 

        all_row.set(int(all_amount)//40)
        values =[f"{i}"for i in range(all_row.get()+1)]
        amount_page.configure(values=values)
        amount_page_scroll.configure(values=values)

        for widget in FProducts_Scroll.winfo_children():
                widget.destroy()
        for num,value in enumerate(products):
            col = num % 4
            row = num // 4

            id = value[0] 
            name = value[1]
            price = value[2]

            try:
                open_pimg = Image.open(f"{img_products/id}.jpg")
                pimg = CTkImage(light_image=open_pimg,dark_image=open_pimg,size=(150,200))
            except FileNotFoundError:
                open_pimg = Image.open(f"{img_products/"Default.jpg"}")
                pimg = CTkImage(light_image=open_pimg,dark_image=open_pimg,size=(150,200))
    
            pro = CTkFrame(FProducts_Scroll,fg_color="white",width=250,height=250,corner_radius=16)
            pro.grid(column=col,row=row,padx=5,pady=5,sticky="news")

            pro_frame = CTkLabel(pro,image=pimg,text="")
            pro_frame.pack()

            pro_frame.bind("<Button-1>",lambda e,e_id = id:(inp_product.insert(END,e_id),
            search_product(inp_product.get())))
        
            pro_frame.bind("<Enter>",lambda e: hover_enter())
            pro_frame.bind("<Leave>",lambda e: hover_leave())
        
            FProducts_Scroll.grid_columnconfigure(pro,weight=1)

        inp_product.delete(0,END)
        inp_product.focus_set()
        on_page.set(True)

    def search_product(code):
        find_star = code.find("*")
        amount = code[0:find_star]
        bar_code = code[find_star+1:]

        appdir = Path(__file__).parent
        img_products = appdir / "products" 

        if (find_star <= -1):
            sql.execute("SELECT `p_id` , `p_name` , `p_price` FROM `stock_list`.`products` WHERE `p_id` = %s;" , (bar_code,))
            product = sql.fetchone()

            if (product):
                try:
                    id = product[0]
                    
                    try:
                        name_img = product[0]+".jpg"

                        open_image = Image.open(img_products/name_img)
                        image = CTkImage(light_image=open_image,dark_image=open_image,size=(20,20))
                    except FileNotFoundError:
                        name_img = "Default.jpg"
                        open_image = Image.open(img_products/name_img)
                        image = CTkImage(light_image=open_image,dark_image=open_image,size=(20,20))

                    name = product[1]
                    price = product[2]
                    get_values(open_image,id,name,1,price)

                    inp_product.delete(0,END)
                    inp_product.focus_set()

                except TypeError:
                    inp_product.delete(0,END)
                    inp_product.focus_set()
            elif (bar_code != ""):
                name_search.set(bar_code)
                search_products_shows(name_search.get(),0)
            else:
                show_products("ทั้งหมด",0,True)
                name_search.set("")

        elif (find_star >= 0):
            sql.execute("SELECT `p_id` , `p_name` , `p_price` FROM `stock_list`.`products` WHERE `p_id` = %s;" , (bar_code,))
            product = sql.fetchone()

            try:
                id = product[0]

                try:
                    name_img = product[0]+".jpg"

                    open_image = Image.open(img_products/name_img)
                    image = CTkImage(light_image=open_image,dark_image=open_image,size=(20,20))

                except FileNotFoundError:
                    name_img = "Default.jpg"

                    open_image = Image.open(img_products/name_img)
                    image = CTkImage(light_image=open_image,dark_image=open_image,size=(20,20))

                name = product[1]
                price = product[2]
                
                get_values(open_image,id,name,amount,price*int(amount))

                inp_product.delete(0,END)
                inp_product.focus_set()
            except TypeError:
                inp_product.delete(0,END)
                inp_product.focus_set()


    
    button_product = CTkButton(FLeft,font=("Arial Bold",16),width=60,height=30,command=lambda :search_product(inp_product.get()),corner_radius=20,image=search_icon,text="",text_color="white",fg_color="#38f388",hover_color="#6be59e")
    button_product.bind("<Enter>", lambda event: button_product.configure(width=65,height=35)) 
    button_product.bind("<Leave>", lambda event: button_product.configure(width=60,height=30)) 

    button_product.bind("<Enter>",lambda e: hover_enter())
    button_product.bind("<Leave>",lambda e: hover_leave())
    
    button_product.grid(row=0,column=1,padx=5,sticky="W")

    
    open_re_icon = Image.open(icon/"restart.png")
    re_icon = CTkImage(light_image=open_re_icon,dark_image=open_re_icon,size=(20,20))

    def reconnect():
        my_sql.reconnect()
        show_products(box_type.get(),0,False)

    button_re = CTkButton(FLeft,font=("Arial Bold",16),command=reconnect,width=60,height=30,corner_radius=20,text="",image=re_icon,text_color="white",fg_color="#38f388",hover_color="#6be59e")
    button_re.bind("<Enter>", lambda event: button_re.configure(width=65,height=35)) 
    button_re.bind("<Leave>", lambda event: button_re.configure(width=60,height=30)) 
    button_re.grid(row=0,column=1,padx=80,sticky="W")

    button_re.bind("<Enter>",lambda e: hover_enter())
    button_re.bind("<Leave>",lambda e: hover_leave())

    def check_level(lv,func):
        try:
            sql.execute("SELECT IF(`accounts`.`level`>= %s, `accounts`.`level`, `accounts`.`level`) as `status`FROM `stock_list`.`accounts` where `accounts`.`username` = %s;" , (lv,a_user))

            level = sql.fetchone()
            
            if (level[0] >= lv):
                func()
            else:
                level_gui = CTKUI("Stock List",480,360,"#D4D4D4","light")
                level_gui.resizable(False,False)
                level_gui.attributes("-topmost",True)

                appdir = Path(__file__).parent
                photo = appdir / "icon" / "sql_connect.png"
                bg_image = Image.open(photo)
                background_photo= CTkImage(bg_image,size=(500,500))

                background  = CTkLabel(master=level_gui,text="",image=background_photo)
                background.place(x=0,y=0)

                F_Connect = CTkFrame(master=level_gui,fg_color="#FFFFFF",width=420,height=280,corner_radius=0)
                F_Connect.pack(anchor=CENTER,pady=40,expand=NO)

                titel = CTkLabel(F_Connect,text="Login",font=("Arial",24),fg_color="#FFFFFF",bg_color="black")
                titel.place(relx=.45,rely=.05)

                inp_user = CTkEntry(master=F_Connect,border_width=2,corner_radius=8,fg_color="#FBFBFB",border_color="#C1C1C1",placeholder_text="Username",width=300,height=40)
                inp_user.place(relx=.14,rely=.25,anchor=NW)

                inp_password = CTkEntry(master=F_Connect,border_width=2,corner_radius=8,fg_color="#FBFBFB",border_color="#C1C1C1",placeholder_text="Password",show="●",width=300,height=40)
                inp_password.place(relx=.14,rely=.49,anchor=NW)

                def connect_level():
                    username = inp_user.get()
                    passwords = inp_password.get()
                    
                    sql.execute("SELECT * FROM `stock_list`.`accounts` WHERE `username` = %s AND `passwords` = %s AND `level` >= %s;" , (username,passwords,lv))
                    resulte = sql.fetchone()

                    if (resulte):
                        btn_ok = CTkMessagebox(title="Success", message="Login Success", icon="check", option_1="OK")

                        if (btn_ok.get() == "OK"):
                            func()
                            level_gui.destroy()
                    else:
                        CTkMessagebox(title="Error", message="Username or Passwords is incorrect or You don't have permission to access.", icon="cancel", option_1="OK")
                        inp_user.delete(0,END)
                        inp_password.delete(0,END)
                        inp_user.focus_set()

                inp_password.bind("<Return>",lambda e:connect_level())

                button_connect = CTkButton(master=F_Connect,corner_radius=20,command=connect_level,text="Connect",width=300,height=45)
                button_connect.place(relx=.14,rely=.75,anchor=NW)


        except mysql.connector.Error as err:
            CTkMessagebox(title="Error", message=f"Something went wrong: {err}", icon="cancel", option_1="OK")

    func_upload = lambda: upload_data.gui_upload(my_sql)

    button_add = CTkButton(FLeft,font=("Arial Bold",16),command= lambda: check_level(2,func_upload),width=60,height=30,corner_radius=20,text="+",text_color="black",fg_color="#38f388",hover_color="#6be59e")
    button_add.bind("<Enter>", lambda event: button_add.configure(width=65,height=35)) 
    button_add.bind("<Leave>", lambda event: button_add.configure(width=60,height=30)) 

    button_add.bind("<Enter>",lambda e: hover_enter())
    button_add.bind("<Leave>",lambda e: hover_leave())

    button_add.grid(row=0,column=1,padx=(0,20),sticky="E")

    all_type = sql.execute("SELECT DISTINCT p_type FROM stock_list.products;")
    products_type = sql.fetchall()

    type_list = ["ทั้งหมด"]+[t[0] for t in products_type]

    box_type = CTkComboBox(FLeft,width=100,values=type_list,command=lambda value: show_products(value,0,True)) 
    box_type.grid(row=0,column=1,padx=(0,115),sticky="E")

    FRight= CTkFrame(main,corner_radius=0,border_width=0,border_color="black",width=600)
    FRight.pack(side=RIGHT,fill=BOTH)

    Fbill_Scroll = CTkScrollableFrame(FRight,fg_color="#dfdfdf",border_width=0,border_color="black",width=600)
    Fbill_Scroll.pack(fill=BOTH,expand=True)

    FBottom= CTkFrame(FRight,fg_color="#1DF38F",corner_radius=0,border_width=0,border_color="black")
    FBottom.pack(side=BOTTOM,fill=BOTH)

    FBottomPay= CTkFrame(FBottom,fg_color="#1DF38F",corner_radius=0,border_width=0,border_color="black")

    FBottomPay.columnconfigure(0,weight=1)
    FBottomPay.columnconfigure(1,weight=1)

    FBottomPay.pack(side=BOTTOM,fill=BOTH)

    def show_products(type_products,num,reset):
        name_search.set("")

        for widget in FProducts_Scroll.winfo_children():
            widget.destroy()

        if (type_products != "ทั้งหมด"): #// ดึงข้อมูลตามประเภท
            sql.execute("SELECT `p_id` , `p_name` , `p_price` FROM `stock_list`.`products` WHERE `p_type` = %s ORDER BY `p_type`,`p_id`,`p_name` ASC LIMIT 40 offset %s;" , (type_products,(num)*40,))
        else:
            sql.execute("SELECT `p_id` , `p_name` , `p_price` FROM `stock_list`.`products` ORDER BY `p_type`,`p_id`,`p_name` ASC LIMIT 40 offset %s;" , (num*40,))

        products = sql.fetchall()

        if (type_products != "ทั้งหมด"): #// นับจำนวนข้อมูลตามประเภท
            sql.execute("SELECT COUNT(*) FROM `stock_list`.`products` WHERE `p_type` =  %s",(type_products,))
        else:
            sql.execute("SELECT COUNT(*) FROM `stock_list`.`products`")
        
        if (reset == True): #// รีเซ็ตหน้าเมื่อเปลี่ยนประเภท
            num_page.set(0)
            amount_page.set(num_page.get())


        all_amount = sql.fetchone()[0]

        all_row.set(int(all_amount)//40)
        values =[f"{i}"for i in range(all_row.get()+1)]
        amount_page.configure(values=values)
        amount_page_scroll.configure(values=values)
        

        img_products = appdir / "products"

        for num,value in enumerate(products):
            col = num % 4
            row = num // 4

            id = value[0] 
            name = value[1]
            price = value[2]

            try:
                open_pimg = Image.open(f"{img_products/id}.jpg")
                pimg = CTkImage(light_image=open_pimg,dark_image=open_pimg,size=(150,200))
            except FileNotFoundError:
                open_pimg = Image.open(f"{img_products/"Default.jpg"}")
                pimg = CTkImage(light_image=open_pimg,dark_image=open_pimg,size=(150,200))
        
            pro = CTkFrame(FProducts_Scroll,fg_color="white",width=250,height=250,corner_radius=16)
            pro.grid(column=col,row=row,padx=5,pady=5,sticky="news")

            pro_frame = CTkLabel(pro,image=pimg,text="")
            pro_frame.pack()

            pro_frame.bind("<Button-1>",lambda e,e_id = id:(inp_product.insert(END,e_id),
            search_product(inp_product.get())))
        
            pro_frame.bind("<Enter>",lambda e: hover_enter())
            pro_frame.bind("<Leave>",lambda e: hover_leave())
        
            FProducts_Scroll.grid_columnconfigure(pro,weight=1)

        FProducts_Scroll._parent_canvas.yview_moveto(0.0)
        on_page.set(False)
   

    bill_list = []
    def get_values(img,id,name,amount,price):
        frame_product = CTkFrame(Fbill_Scroll,fg_color="white",corner_radius=20)
        frame_product.pack(padx=10,pady=5,anchor="nw")

        bill_list.append(frame_product)

        pimg = CTkImage(light_image=img,dark_image=img,size=(100,100))

        img_products = appdir / "icon"

        open_pimg = Image.open(f"{img_products/"bin.png"}")
        del_img = CTkImage(light_image=open_pimg,dark_image=open_pimg,size=(20,20))

        bproducts = CTkLabel(frame_product,font=("Airal",12),text=f"\t{name[0:20]}\t\tX{amount}\t {price}",image=pimg,compound="left", anchor="w",width=600)
        bproducts.pack()

        btn_del = CTkButton(frame_product,width=20,height=20,text="",corner_radius=5,fg_color="#FF2C2C",hover_color="#F14141",image=del_img,command=lambda:del_product(frame_product,int(amount),price))
        btn_del.place(relx=0.87,y=35)

        p_price.set(price+float(p_price.get()))
        p_amount_list.set(int(amount) + p_amount_list.get())
        vat = float(p_price.get())/100*7

        num_price.configure(text=f"{float(p_price.get())}\n\n{p_amount_list.get()}\n\n{float(p_price.get())}",font=("Arial",24),justify="right")

        btn_del.bind("<Enter>",lambda e: hover_enter())
        btn_del.bind("<Leave>",lambda e: hover_leave())

    def del_product(BillProduct,Amount,Price):
        BillProduct.destroy()
        p_price.set(float(p_price.get())- Price)
        p_amount_list.set(p_amount_list.get() - Amount)
        vat = (float(p_price.get())/100*7)

        bill_list.remove(BillProduct)

        num_price.configure(text=f"{p_price.get()}\n\n{p_amount_list.get()}\n\n{float(p_price.get())}")


    def hover_enter():
        main.config(cursor="hand2")

    def hover_leave():
        main.config(cursor="arrow")


    def offline():
        
        sql.execute("Update `accounts` SET `onlines` = 0 WHERE `username` = %s" , (a_user,))
        my_sql.commit()

        os._exit(0)

    def clear():
        p_price.set(value=0)
        p_amount_list.set(value=0)

        num_price.configure(text=f"{p_price.get()}\n\n{p_amount_list.get()}\n\n{float(p_price.get())}")
        for i in bill_list:
            i.destroy()

    p_price = StringVar(value=0)
    p_amount_list = IntVar(value=0)
    vat = (float(p_price.get())/100*7)

    open_image = Image.open(icon/"clean.png")
    clean_image = CTkImage(light_image=open_image,dark_image=open_image,size=(20,20))

    btn_clear = CTkButton(Fbill_Scroll,text="",image=clean_image,width=20,height=20,fg_color="#FF2C2C",hover_color="#F14141",corner_radius=15,command=clear)
    btn_clear.pack(anchor="ne")

    btn_clear.bind("<Enter>",lambda e: hover_enter())
    btn_clear.bind("<Leave>",lambda e: hover_leave())

    label_price = CTkLabel(FBottom,text="Price :\n\nAmount :\n\nTotal :",font=("Arial",24),justify="left")
    label_price.pack(side=LEFT,anchor="w",padx=20,pady=20)

    num_price = CTkLabel(FBottom,text=f"{float(p_price.get())}\n\n{p_amount_list.get()}\n\n{float(p_price.get())}",font=("Arial",24),justify="right")
    num_price.pack(side=RIGHT,anchor="w",padx=20,pady=20)

    pay_cash = CTkButton(FBottomPay,text="Cash",cursor="hand2",text_color="white",width=200,height=60,corner_radius=0,fg_color="#ffad15",hover_color="#e29e45",font=("Arial Bold",24))
    pay_cash.grid(row=0,column=0,sticky="nsew")

    pay_bank = CTkButton(FBottomPay,text="Bank",cursor="hand2",text_color="white",width=200,height=60,corner_radius=0,fg_color="#264eff",hover_color="#2e5fe6",font=("Arial Bold",24))
    pay_bank.grid(row=0,column=1,sticky="nsew")

    show_products("ทั้งหมด",num_page.get(),True)

    FLeft.bind("<Destroy>",lambda e: offline())
