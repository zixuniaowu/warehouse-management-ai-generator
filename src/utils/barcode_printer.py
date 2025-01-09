import win32print
import win32ui
from PIL import Image, ImageWin
import os

class BarcodePrinter:
    def __init__(self, config):
        self.config = config
        self.printer_name = win32print.GetDefaultPrinter()
        
    def print_barcode(self, barcode_path):
        try:
            # 打开图片
            img = Image.open(barcode_path)
            
            # 获取打印机DC
            hprinter = win32print.OpenPrinter(self.printer_name)
            printer_info = win32print.GetPrinter(hprinter, 2)
            
            # 创建DC
            hdc = win32ui.CreateDC()
            hdc.CreatePrinterDC(self.printer_name)
            
            # 开始打印工作
            hdc.StartDoc('Barcode Print Job')
            hdc.StartPage()
            
            # 获取打印区域尺寸
            width = self.config['barcode']['print']['width']
            height = self.config['barcode']['print']['height']
            margin = self.config['barcode']['print']['margin']
            
            # 打印图片
            dib = ImageWin.Dib(img)
            dib.draw(hdc.GetHandleOutput(), 
                    (margin * 100, 
                     margin * 100, 
                     width * 100, 
                     height * 100))
            
            # 结束打印
            hdc.EndPage()
            hdc.EndDoc()
            
            # 清理资源
            hdc.DeleteDC()
            win32print.ClosePrinter(hprinter)
            
            return True
        except Exception as e:
            print(f"打印错误: {str(e)}")
            return False
            
    def print_multiple_barcodes(self, barcode_paths):
        success = True
        for path in barcode_paths:
            if not self.print_barcode(path):
                success = False
        return success