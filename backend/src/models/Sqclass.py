import sqlite3

class Sqclass:
    def __init__(self):
        self.conn = sqlite3.connect('../database/database.db')
        self.cursor = self.conn.cursor()
        self.create_table_lists()
        self.create_table_products()
        self.create_table_products_infos()
        
    def close(self):
        self.conn.close()
    
    def create_table_lists(self):
        self.cursor.execute(""" 
                            CREATE TABLE IF NOT EXISTS product_list (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                url TEXT
                            )
                            """)
        self.conn.commit()
    
    def create_table_products(self):
        self.cursor.execute(""" 
                            CREATE TABLE IF NOT EXISTS products (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT,
                                photo_src TEXT,
                                id_list INTEGER,
                                FOREIGN KEY(id_list) REFERENCES product_list(id)
                            )
                            """)
        self.conn.commit()
    
    def create_table_products_infos(self):
        self.cursor.execute(""" 
                            CREATE TABLE IF NOT EXISTS products_infos (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                size TEXT,
                                price_web REAL,
                                price_b2b REAL,
                                id_product INTEGER,
                                FOREIGN KEY(id_product) REFERENCES products(id)
                            )
                            """)
        self.conn.commit()

    
    def insert_into_product_list(self, name, url):
        self.cursor.execute("""
                            INSERT INTO product_list (name, url)
                            VALUES (?, ?)
                            """, (name, url))
        self.conn.commit()
        return self.cursor.lastrowid  # Retorna o ID do registro inserido
    
    # Método para inserir dados na tabela products
    def insert_into_products(self, title, photo_src, id_list):
        self.cursor.execute("""
                            INSERT INTO products (title, photo_src, id_list)
                            VALUES (?, ?, ?)
                            """, (title, photo_src, id_list))
        self.conn.commit()
        return self.cursor.lastrowid  # Retorna o ID do registro inserido
    
    # Método para inserir dados na tabela products_infos
    def insert_into_products_infos(self, size, price_web, price_b2b, id_product):
        self.cursor.execute("""
                            INSERT INTO products_infos (size, price_web, price_b2b, id_product)
                            VALUES (?, ?, ?, ?)
                            """, (size, price_web, price_b2b, id_product))
        self.conn.commit()
        return self.cursor.lastrowid  # Retorna o ID do registro inserido