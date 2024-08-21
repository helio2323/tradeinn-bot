import sqlite3
import os

class Sqclass:
    def __init__(self):
        # O caminho do banco de dados
        self.db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../database/database.db'))
        self.create_tables()

    def create_tables(self):
        # Criação das tabelas
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS product_list (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    url TEXT,
                    updated BOOLEAN DEFAULT 0
                )
            """)
            cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    photo_src TEXT,
                    product_site_id TEXT,
                    id_list INTEGER,
                    image BLOB,
                    updated BOOLEAN DEFAULT 0,
                    FOREIGN KEY(id_list) REFERENCES product_list(id)
                )
            """)
            cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS products_infos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    site_option_id TEXT,
                    size TEXT,
                    price_web REAL,
                    price_b2b REAL,
                    id_product INTEGER,
                    FOREIGN KEY(id_product) REFERENCES products(id)
                )
            """)

    def get_db_connection(self):
        """Cria e retorna uma nova conexão com o banco de dados."""
        connection = sqlite3.connect(self.db_path, check_same_thread=False)
        connection.row_factory = sqlite3.Row
        return connection

    def close(self, conn):
        """Fecha a conexão com o banco de dados."""
        conn.close()
    
    def insert_into_product_list(self, name, url):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO product_list (name, url)
                VALUES (?, ?)
            """, (name, url))
            conn.commit()
            return cursor.lastrowid
    
    def get_product_list(self):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM product_list")
            return cursor.fetchall()
    
    def update_status_list(self, id_list):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE product_list SET updated = 1 WHERE id = ?", (id_list,))
            conn.commit()
        
    def set_all_list_false(self):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE product_list SET updated = 0")
            conn.commit()
    
    def get_products(self, id_list):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT products.id, products.title, products.photo_src, products.product_site_id, products.image, products_infos.site_option_id, products_infos.size, products_infos.price_web, products_infos.price_b2b
                FROM products
                INNER JOIN products_infos
                ON products.id = products_infos.id_product
                WHERE products.id_list = ?
            """, (id_list,))
            return cursor.fetchall()
    
    def get_prod_xlsx(self, id_list):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT products.id, products.title, products.image, products_infos.price_b2b
                FROM products
                INNER JOIN products_infos
                ON products.id = products_infos.id_product
                WHERE products.id_list = ?
            """, (id_list,))
            return cursor.fetchall()

    def get_prod_pdf(self, id_list):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT products.id, products.title, products.photo_src, products_infos.price_b2b
                FROM products
                INNER JOIN products_infos
                ON products.id = products_infos.id_product
                WHERE products.id_list = ?
            """, (id_list,))
            return cursor.fetchall()
    
    def insert_or_update_product(self, title, photo_src, product_site_id, id_list, image_binary, updated=0):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM products WHERE product_site_id = ?", (product_site_id,))
            existing_product = cursor.fetchone()
            
            if existing_product:
                product_id = existing_product[0]
                cursor.execute("""
                    UPDATE products
                    SET title = ?, photo_src = ?, id_list = ?, image = ?, updated = ?
                    WHERE product_site_id = ?
                """, (title, photo_src, id_list, image_binary, updated, product_site_id))
            else:
                cursor.execute("""
                    INSERT INTO products (title, photo_src, product_site_id, id_list, image, updated)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (title, photo_src, product_site_id, id_list, image_binary, updated))
                product_id = cursor.lastrowid
            
            conn.commit()
            return product_id

    def insert_or_update_products_infos(self, site_option_id, size, price_web, price_b2b, id_product):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM products_infos WHERE site_option_id = ?", (site_option_id,))
            existing_info = cursor.fetchone()
            
            if existing_info:
                info_id = existing_info[0]
                cursor.execute("""
                    UPDATE products_infos
                    SET size = ?, price_web = ?, price_b2b = ?, id_product = ?
                    WHERE site_option_id = ?
                """, (size, price_web, price_b2b, id_product, site_option_id))
            else:
                cursor.execute("""
                    INSERT INTO products_infos (site_option_id, size, price_web, price_b2b, id_product)
                    VALUES (?, ?, ?, ?, ?)
                """, (site_option_id, size, price_web, price_b2b, id_product))
                info_id = cursor.lastrowid
            
            conn.commit()
            return info_id
