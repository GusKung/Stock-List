from escpos.printer import Usb
from escpos.capabilities import Profile
from pathlib import Path
import encode_file
import os
import imgkit
from io import BytesIO
from PIL import Image

class Printer:
    def __init__(self,vid,pid,width):
        self.vid = vid
        self.pid = pid
        self.width = width
        self.load_data = encode_file.EncodeDecode().load_data()
        self.bill_file = self.load_data.get("Bill File")


        vid = int(self.vid, 16)
        pid = int(self.pid, 16)
        self.p = Usb(vid, pid)
        self.p.set(align="center", width=2, height=2)

        self.appdir = Path(__file__).parent

    def connect(self):
        result = None
        err = None

        try:
            if (self.width == 384):
                line = "_" * 32
            else:
                line = "_" * 42

            self.p.text(f"{line}\n")
            self.p.text("Printer Connected Successfully!\n")
            self.p.text("This is a test print to confirm the connection.\n")
            self.p.text(f"{line}\n")
            self.p.cut()
            result = True

        except Exception as e:
            err = e
            result = False
        return result, err

    def create_bill(self,bill_id,html,height):

        file_html = os.path.abspath(os.path.join(self.bill_file, f"{bill_id}.html"))

        options = {
            'quiet': '',
            'width': self.width,
            'disable-smart-width': '',
            'encoding': "UTF-8",
            'enable-local-file-access': ''
        }

        config = imgkit.config(wkhtmltoimage=os.path.join(self.appdir, "wkhtmltoimage.exe"))
        img_bytes = imgkit.from_string(html, False, config=config, options=options)

        img_buffer = BytesIO(img_bytes)
        img = Image.open(img_buffer).convert("L")

        self.print_bills(img)

        with open(file_html, "w", encoding="utf-8") as f:
            f.write(html)


        
    
    def html_bill(self, bill_id, dates, data_products, cash):
        html_order = ""
        total = 0

        calculated_height = (len(data_products) * 50) + 500

        for p_id, value in data_products.items():
            p_total = float(value['total'])
            total += p_total

            html_order += f"""
            <tr>
                <td style="word-break: break-all; width: 45%;">{p_id}<br>{value['name'][0:25]} . . .</td>
                <td style="text-align: center; width: 15%;">X{value['amount']}</td>
                <td style="text-align: right; width: 20%;">{float(value['price']):.2f}</td>
                <td style="text-align: right; width: 20%;">{p_total:.2f}</td>
            </tr>
            """

        change = cash - total
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: 'Tahoma', sans-serif; 
                    width: {self.width}px;
                    background-color: white;
                    color: black;
                    padding: 5px;
                }}

                .header {{ text-align: center; margin-bottom: 10px; }}
                
                table {{ 
                    width: 100%; 
                    border-collapse: collapse; 
                    font-size: 16px; 
                }}

                th {{ 
                    border-bottom: 1px dashed #000; 
                    padding: 5px 0; 
                    text-align: left; 
                }}

                td {{ padding: 4px 0; vertical-align: top; }}

                .line {{ border-top: 1px dashed #000; margin: 8px 0; }}

                .summary-table {{ width: 100%; font-size: 16px; font-weight: bold; }}
                .summary-table td {{ padding: 2px 0; }}
                .text-right {{ text-align: right; }}

                .footer {{ 
                    text-align: center; 
                    font-size: 16px; 
                    margin-top: 15px; 
                    line-height: 1.4;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2 style="margin: 0;">STOCK LIST</h2> <br>
                <p>วันที่: {dates}</p>
                <p>Bill ID: {bill_id}</p>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>สินค้า</th>
                        <th style="text-align: center;">จำนวน</th>
                        <th style="text-align: right;">ราคา</th>
                        <th style="text-align: right;">รวม</th>
                    </tr>
                </thead>
                <tbody>
                    {html_order}
                </tbody>
            </table>

            <div class="line"></div>
            
            <table class="summary-table">
                <tr>
                    <td>รวมทั้งสิ้น</td>
                    <td class="text-right">{total:.2f} บาท</td>
                </tr>
                <tr style="font-weight: normal;">
                    <td>รับเงิน</td>
                    <td class="text-right">{cash:.2f} บาท</td>
                </tr>
                <tr>
                    <td>เงินทอน</td>
                    <td class="text-right">{change:.2f} บาท</td>
                </tr>
            </table>

            <div class="footer">
                <p>ขอบคุณที่ใช้บริการ</p>
                <p>*** สินค้าซื้อแล้วไม่รับเปลี่ยนคืน ***</p>
            </div> <br> <br> <br> <br>
        </body>
        </html>
        """
        return html, calculated_height


    def print_bills(self,content):
        result = None
        err = None
        try:
            self.p.image(content,center=False)
            self.p.cut()
           
            result = True
        except Exception as e:
            result = False
            err = e
        return result, err