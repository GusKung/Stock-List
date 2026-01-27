from cryptography.fernet import Fernet
from dotenv import load_dotenv, dotenv_values 
import io
import os
from pathlib import Path

class EncodeDecode:
    def __init__(self):
        self.appdir = Path(__file__).parent
        self.doc = self.check_doc()
        self.stocklist_dir = self.doc / "Stock List"
        self.account_file = self.stocklist_dir / "account.env"
        self.server_file = self.stocklist_dir / "server.env"
        self.key = self.appdir / "mykey.key"

        self.data_server = {}
        self.data_account = {}

        self.server = [
            "HOST=localhost",
            "USER=root",
            "PASSWORD=",
            "DATABASE=stock_list",
            "TIME_ZONE=+07:00"
        ]
        self.account = [
            "USERNAME=admin",
            "PASSWORD=1234",
            "REMEMBER=False",
            "POS=1"
        ]

    def load_data(self):
    
        if (not self.stocklist_dir.exists()):
            os.makedirs(self.stocklist_dir)

        if (not self.server_file.exists()):
            with open(self.server_file, "wb") as ds:
                ds.write("\n".join(self.server).encode("utf-8"))
            self.encode(self.server_file)
            server = self.decode(self.server_file)
            self.data_server.update(server)
        else:
            server = self.decode(self.server_file)
            self.data_server.update(server)

        if (not self.account_file.exists()):
            with open(self.account_file, "wb") as da:
                da.write("\n".join(self.account).encode("utf-8"))
            self.encode(self.account_file)
            account = self.decode(self.account_file)
            self.data_account.update(account)
        else:
            account = self.decode(self.account_file)
            self.data_account.update(account)

        return {**self.data_server, **self.data_account,"Server_File":self.server_file,"Account_File":self.account_file}
           
    
    def encode(self, filepath):
        fernet = Fernet(open(self.key, "rb").read())

        with open(filepath, "rb") as file:
            original = file.read()

        encrypted = fernet.encrypt(original)

        with open(filepath, "wb") as encrypted_file:
            encrypted_file.write(encrypted)

    def decode(self, filepath):
        fernet =Fernet(open(self.key, "rb").read())

        with open (filepath, "rb") as enc_file:
            encrypted = enc_file.read()

        decrypted = fernet.decrypt(encrypted).decode("utf-8")

        data = io.StringIO(decrypted)

        config = dotenv_values(stream=data)

        return config

    def edit_data(self, filepath, new_data):
        fernet =Fernet(open(self.key, "rb").read())

        with open (filepath, "rb") as enc_file:
            encrypted = enc_file.read()

        decrypted = fernet.decrypt(encrypted).decode("utf-8")

        data = io.StringIO(decrypted)

        config = dotenv_values(stream=data)

        config.update({item.split("=")[0]: item.split("=")[1] for item in new_data})

        updated_content = "\n".join([f"{key}={value}" for key, value in config.items()])
        
        with open(filepath, "wb") as file:
            file.write(updated_content.encode("utf-8"))

        if (filepath == self.server_file):
            self.data_server.update(config)

        elif (filepath == self.account_file):
            self.data_account.update(config)

        self.encode(filepath)


    def check_doc(self):
        user_home = Path.home()
        self.doc_folder = user_home / "Documents"

        if (not self.doc_folder.exists()):
            
            self.doc_folder = user_home / "OneDrive" / "Documents"

        return self.doc_folder