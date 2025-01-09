import tkinter as tk
from .ui.main_window import MainWindow
from .database.db_manager import DatabaseManager

class WarehouseApp:
    def __init__(self, config):
        self.config = config
        self.db = DatabaseManager(config['database']['path'])
        
    def run(self):
        root = tk.Tk()
        app = MainWindow(root, self.db, self.config)
        root.mainloop()