from html2image import Html2Image
from escpos.printer import Usb
import shutil
import encode_file
import os

class Printer:
    def __init__(self,vid,pid,width):
        self.vid = vid
        self.pid = pid
        self.width = width
        self.load_data = encode_file.EncodeDecode().load_data()
        self.bill_file = self.load_data.get("Bill File")

    def connect(self):
        result = None
        err = None
        try:
            vid = int(self.vid, 16)
            pid = int(self.pid, 16)
            p = Usb(vid, pid)

            p.set(align="center", width=2, height=2)
            if (self.width == 384):
                line = "_" * 32
            else:
                line = "_" * 42

            p.text(f"{line}\n")
            p.text("Printer Connected Successfully!\n")
            p.text("This is a test print to confirm the connection.\n")
            p.text(f"{line}\n")
            p.cut()
            result = True

        except Exception as e:
            err = e
            result = False
        return result, err

    def print_bill(self,html,height):
        edge_path = shutil.which("msedge")

        file_html = os.path.abspath(os.path.join(self.bill_file, "bill.html"))
        save_path = os.path.abspath(os.path.join(self.bill_file, "bill.png"))

        with open(file_html, "w", encoding="utf-8") as f:
            f.write(html)

        if (edge_path):
            hti = Html2Image(browser_executable=edge_path,output_path=self.bill_file)
        else:
            edge_path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
            hti = Html2Image(browser_executable=edge_path,output_path=self.bill_file)

        hti.screenshot(html_str=html, save_as=f"bill.png",size=(self.width,height))
        
        result = None
        err = None
        try:
            vid = int(self.vid, 16)
            pid = int(self.pid, 16)
            p = Usb(vid, pid)
            p.image(f"{save_path}")
            p.cut()
           
            result = True
        except Exception as e:
            result = False
            err = e
        return result, err
    
    def html_bill(self,bill_id,dates,data_products,cash):
        html_order = ""
        total = 0

        calculated_height = (len(data_products) * 40) + 450

        for id,value in data_products.items():
            total += float(value['price'])
            html_order += f"""
            <tr>
                <td>{id}<br>{value['name'][0:30]}...</td>
                <td style="text-align: center; font-size: 16px;">X{value['amount']}</td>
                <td style="text-align: right; font-size: 16px;">{float(value['price']):,.2f}</td>
            </tr>
            """

        change = cash - total
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Tahoma', 
                    sans-serif; 
                    margin: 0; 
                    padding: 0px; 
                    width: {self.width}px;
                    background-color: white;
                }}

                #bill-canvas {{
                    width: 100%;
                    box-sizing: border-box;
                }}

                .bill-container {{ border: 1px solid #eee; 
                    padding: 10px; 
                }}

                .header {{ text-align: center; 
                    margin-bottom: 10px; 
                }}

                table {{ width: 100%; 
                    border-collapse: collapse; 
                    font-size: 16px; 
                }}

                th {{ border-bottom: 1px dashed #000; 
                    padding: 5px 0; 
                    text-align: left; 
                }}

                td {{ padding: 5px 0; 
                    vertical-align: top; 
                }}

                .line {{ border-top: 1px dashed #000; 
                    margin: 10px 0; 
                }}

                .result-row {{ display: flex; 
                    justify-content: space-between; 
                    font-weight: bold; 
                    font-size: 16px;
                }}

                .footer {{ text-align: center; 
                    font-size: 16px; 
                    margin-top: 12px; 
                }}
            </style>
        </head>
        <body>
            <div id="bill-canvas" class="bill-container">
                <div class="header">
                    <h2 style="margin: 0;">STOCK LIST</h2>
                    <p style="font-size: 16px;">วันที่: {dates}</p>
                    <p style="font-size: 16px;">Bill ID: {bill_id}</p>
                </div>

                <table>
                    <thead>
                        <tr>
                            <th>สินค้า</th>
                            <th style="text-align: center; font-size: 16px;">จำนวน</th>
                            <th style="text-align: right; font-size: 16px;">ราคา</th>
                        </tr>
                    </thead>
                    <tbody>
                        {html_order}
                    </tbody>
                </table>

                <div class="line"></div>
                
                <div class="result-row">
                    <span>รวมทั้งสิ้น</span>
                    <span>{total:,.2f} บาท</span>
                </div>
                <div class="result-row" style="font-weight: normal;">
                    <span>รับเงิน</span>
                    <span>{cash:,.2f} บาท</span>
                </div>
                <div class="result-row">
                    <span>เงินทอน</span>
                    <span>{change:,.2f} บาท</span>
                </div>

                <div class="footer">
                    <p>ขอบคุณที่ใช้บริการ</p>
                    <p>*** สินค้าซื้อแล้วไม่รับเปลี่ยนคืน ***</p>
                </div>
            </div>
        </body>
        </html>
        """
        self.print_bill(html,calculated_height)