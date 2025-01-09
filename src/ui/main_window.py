import tkinter as tk
from tkinter import ttk, messagebox
import os
from ..utils.barcode_generator import generate_barcode
from ..utils.barcode_printer import BarcodePrinter
from ..utils.translations import TRANSLATIONS

class MainWindow:
    def __init__(self, root, db, config):
        self.root = root
        self.db = db
        self.config = config
        self.printer = BarcodePrinter(config)
        
        # 加载语言配置
        self.lang = config['ui'].get('language', 'en')
        self.texts = TRANSLATIONS[self.lang]
        
        self.root.title(self.texts['title'])
        self.root.geometry(config['ui']['window_size'])
        
        self.setup_ui()
        
    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.create_product_frame()
        self.create_product_list_frame()
        self.create_print_frame()
        
    def create_product_frame(self):
        product_frame = ttk.LabelFrame(self.main_frame, text=self.texts['product_info'], padding="5")
        product_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # 条形码
        ttk.Label(product_frame, text=self.texts['barcode']).grid(row=0, column=0, sticky=tk.W)
        self.barcode_entry = ttk.Entry(product_frame)
        self.barcode_entry.grid(row=0, column=1, padx=5, pady=2)
        
        # 产品名称
        ttk.Label(product_frame, text=self.texts['product_name']).grid(row=1, column=0, sticky=tk.W)
        self.name_entry = ttk.Entry(product_frame)
        self.name_entry.grid(row=1, column=1, padx=5, pady=2)
        
        # 数量
        ttk.Label(product_frame, text=self.texts['quantity']).grid(row=2, column=0, sticky=tk.W)
        self.quantity_entry = ttk.Entry(product_frame)
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=2)
        
        # 单价
        ttk.Label(product_frame, text=self.texts['unit_price']).grid(row=3, column=0, sticky=tk.W)
        self.price_entry = ttk.Entry(product_frame)
        self.price_entry.grid(row=3, column=1, padx=5, pady=2)
        
        ttk.Button(product_frame, text=self.texts['add_product'], 
                  command=self.add_product).grid(row=4, column=0, columnspan=2, pady=10)
        
    def create_product_list_frame(self):
        list_frame = ttk.LabelFrame(self.main_frame, text=self.texts['product_list'], padding="5")
        list_frame.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        columns = ("barcode", "name", "quantity", "price")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        self.tree.heading("barcode", text=self.texts['barcode'])
        self.tree.heading("name", text=self.texts['product_name'])
        self.tree.heading("quantity", text=self.texts['quantity'])
        self.tree.heading("price", text=self.texts['unit_price'])
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.refresh_product_list()

    def create_print_frame(self):
        print_frame = ttk.Frame(self.main_frame)
        print_frame.grid(row=2, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Button(print_frame, text=self.texts['print_selected'],
                  command=self.print_selected_barcode).pack(side=tk.LEFT, padx=5)
        ttk.Button(print_frame, text=self.texts['print_all'],
                  command=self.print_all_barcodes).pack(side=tk.LEFT, padx=5)
    
    def print_selected_barcode(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(self.texts['error'], self.texts['select_product'])
            return
            
        item = self.tree.item(selection[0])
        barcode = item['values'][0]
        barcode_path = os.path.join(
            self.config['barcode']['save_path'],
            f"barcode_{barcode}.png"
        )
        
        if self.printer.print_barcode(barcode_path):
            messagebox.showinfo(self.texts['success'], self.texts['print_success'])
        else:
            messagebox.showerror(self.texts['error'], self.texts['print_error'])
    
    def print_all_barcodes(self):
        barcodes = []
        for item in self.tree.get_children():
            barcode = self.tree.item(item)['values'][0]
            barcode_path = os.path.join(
                self.config['barcode']['save_path'],
                f"barcode_{barcode}.png"
            )
            barcodes.append(barcode_path)
        
        if self.printer.print_multiple_barcodes(barcodes):
            messagebox.showinfo(self.texts['success'], self.texts['print_success'])
        else:
            messagebox.showerror(self.texts['error'], self.texts['print_error'])
    
    def add_product(self):
        try:
            product_data = {
                'barcode': self.barcode_entry.get(),
                'name': self.name_entry.get(),
                'quantity': int(self.quantity_entry.get()),
                'unit_price': float(self.price_entry.get())
            }
            
            if not all([product_data['barcode'], product_data['name']]):
                messagebox.showerror(self.texts['error'], self.texts['fill_required'])
                return
            
            # 生成条形码图片
            barcode_path = os.path.join(
                self.config['barcode']['save_path'],
                f"barcode_{product_data['barcode']}.png"
            )
            generate_barcode(product_data['barcode'], barcode_path)
            
            # 保存到数据库
            self.db.add_product(product_data)
            self.refresh_product_list()
            self.clear_entries()
            messagebox.showinfo(self.texts['success'], self.texts['product_added'])
            
        except Exception as e:
            messagebox.showerror(self.texts['error'], str(e))
    
    def refresh_product_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        products = self.db.get_all_products()
        for product in products:
            self.tree.insert("", tk.END, values=(product[1], product[2], product[4], product[5]))
    
    def clear_entries(self):
        for entry in [self.barcode_entry, self.name_entry, self.quantity_entry, self.price_entry]:
            entry.delete(0, tk.END)