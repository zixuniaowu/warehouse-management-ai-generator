import os
import json

DEFAULT_CONFIG = {
    "database": {
        "path": "warehouse.db"
    },
    "barcode": {
        "save_path": "barcodes",
        "format": "ean13"
    },
    "ui": {
        "window_size": "800x600",
        "title": "仓库管理系统"
    }
}

def load_config(config_file="config.json"):
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_CONFIG