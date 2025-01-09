import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    barcode VARCHAR(50) UNIQUE NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    quantity INTEGER DEFAULT 0,
                    unit_price DECIMAL(10,2),
                    category VARCHAR(50),
                    location VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inventory_transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER,
                    transaction_type VARCHAR(20),
                    quantity INTEGER,
                    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    note TEXT,
                    operator VARCHAR(50),
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            """)
            conn.commit()
    
    def add_product(self, product_data):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO products (barcode, name, quantity, unit_price, description, category, location)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                product_data['barcode'],
                product_data['name'],
                product_data['quantity'],
                product_data['unit_price'],
                product_data.get('description', ''),
                product_data.get('category', ''),
                product_data.get('location', '')
            ))
            conn.commit()
            return cursor.lastrowid

    def get_all_products(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            return cursor.fetchall()