import barcode
from barcode.writer import ImageWriter

def generate_barcode(code, save_path):
    EAN13 = barcode.get_barcode_class('ean13')
    ean = EAN13(code, writer=ImageWriter())
    ean.save(save_path)