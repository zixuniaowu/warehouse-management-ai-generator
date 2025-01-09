import os
import sys
from src.app import WarehouseApp
from src.config import load_config

def main():
    config = load_config()
    app = WarehouseApp(config)
    app.run()

if __name__ == "__main__":
    main()