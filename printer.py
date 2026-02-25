from html2image import Html2Image
from escpos.printer import Usb

class Printer:
    def __init__(self,vid,pid,width):
        self.vid = vid
        self.pid = pid
        self.width = width
        

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

    def print_bill(self,html):
        hti = Html2Image()
        hti.screenshot(html_str=html, save_as="bill.png")
        result = None
        err = None
        try:
            vid = int(self.vid, 16)
            pid = int(self.pid, 16)
            p = Usb(vid, pid)
            p.image("bill.png")
            p.cut()
            result = True
        except Exception as e:
            result = False
            err = e
        return result, err
    
    def html_bill(self,width,date,data_products,cash):
        products_html = ""

        total = sum([product['price'] * product['amount'] for product in data_products])

        cash -= total
        for product in data_products:
            products_html += f"""
                    <div class="item-row">
                        <span>{product['barcode']}</span>
                        <span>{product['name']}</span>
                        <span> X{product['amount']}</span>
                        <span>{product['price']}</span>
                    </div>"""
        html = f"""
        <head>
                <style>
                    body {{
                        font-family: 'Tahoma', sans-serif; 
                        font-size: 14px;
                        width: {width}px; 
                        margin: 0;
                        padding: 10px;
                        background-color: white;
                    }}
                    .header {{
                        text-align: center;
                        font-weight: bold;
                        font-size: 18px;
                        margin-bottom: 5px;
                    }}
                    .info {{
                        text-align: center;
                        font-size: 12px;
                        margin-bottom: 10px;
                    }}
                    .line {{
                        border-top: 1px dashed #000; 
                        margin: 5px 0;
                    }}
                    .item-row {{
                        display: flex;
                        justify-content: space-between; 
                        margin: 3px 0;
                    }}
                    .item-detail {{
                        font-size: 12px;
                        color: #333;
                    }}
                    .total-section {{
                        margin-top: 10px;
                        font-weight: bold;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 20px;
                        font-size: 12px;
                    }}
                </style>
            </head>

            <body>
                <div class="header">STOCK LIST</div>
                <div class="info">เลขที่ใบเสร็จ: #001 | วันที่: {date}</div>
                
                <div class="line"></div>

                <div class="item-row">
                    <span>รหัสสินค้า</span>
                    <span>ชื่อสินค้า</span>
                    <span> จำนวน</span>
                    <span>ราคา</span>
                </div>

       
                {products_html}
                
                <div class="line"></div>

                <div class="item-row total-section">
                    <span>รวมทั้งสิ้น</span>
                    <span>{total} บาท</span>
                </div>
                <div class="item-row">
                    <span>รับเงิน</span>
                    <span>{cash} บาท</span>
                </div>
                <div class="item-row">
                    <span>เงินทอน</span>
                    <span>{cash - total} บาท</span>
                </div>

                <div class="line"></div>

                <div class="footer">
                    ขอบคุณที่ใช้บริการ<br>
                    *** สินค้าซื้อแล้วไม่รับเปลี่ยนคืน ***
                </div>
            </body>
            </html>
        """
        self.print_bill(html)