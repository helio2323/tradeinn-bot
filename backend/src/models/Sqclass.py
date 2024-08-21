import sqlite3
import os

class Sqclass:
    def __init__(self):
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../database/database.db'))
        self.conn = sqlite3.connect(db_path)
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
                                url TEXT,
                                updated BOOLEAN DEFAULT 0
                            )
                            """)
        self.conn.commit()
        
    
    def create_table_products(self):
        self.cursor.execute(""" 
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
        self.conn.commit()
    
    def create_table_products_infos(self):
        self.cursor.execute(""" 
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
        self.conn.commit()

    
    def insert_into_product_list(self, name, url):
        self.cursor.execute("""
                            INSERT INTO product_list (name, url)
                            VALUES (?, ?)
                            """, (name, url))
        self.conn.commit()
        return self.cursor.lastrowid  # Retorna o ID do registro inserido
    
    
    def get_product_list(self):
        self.cursor.execute("SELECT * FROM product_list")
        return self.cursor.fetchall()
    
    def update_status_list(self, id_list):
        self.cursor.execute("UPDATE product_list SET updated = 1 WHERE id = ?", (id_list,))
        self.conn.commit()
        
    def set_all_list_false(self):
        self.cursor.execute("UPDATE product_list SET updated = 0")
        self.conn.commit()
    
    # Pucha os dados da tabela lists e junta com os dados da tabela 'products' + 'products_infos'
    def get_products(self, id_list):
        self.cursor.execute("""
                            SELECT products.id, products.title, products.photo_src, products.product_site_id, products.image, products_infos.site_option_id, products_infos.size, products_infos.price_web, products_infos.price_b2b
                            FROM products
                            INNER JOIN products_infos
                            ON products.id = products_infos.id_product
                            WHERE products.id_list = ?
                            """, (id_list,))
        return self.cursor.fetchall()
    
    def get_prod_xlsx(self, id_list):
        self.cursor.execute("""
                            SELECT products.id, products.title, products.image, products_infos.price_b2b
                            FROM products
                            INNER JOIN products_infos
                            ON products.id = products_infos.id_product
                            WHERE products.id_list = ?
                            """, (id_list,))
        return self.cursor.fetchall()

    def get_prod_pdf(self, id_list):
        self.cursor.execute("""
                            SELECT products.id, products.title, products.photo_src, products_infos.price_b2b
                            FROM products
                            INNER JOIN products_infos
                            ON products.id = products_infos.id_product
                            WHERE products.id_list = ?
                            """, (id_list,))
        return self.cursor.fetchall()


    
    # Método para inserir dados na tabela products verifica se o produto ja existe comparando o product_site_id caso exista faz o update
# Método para inserir ou atualizar dados na tabela 'products'
    def insert_or_update_product(self, title, photo_src, product_site_id, id_list, image_binary, updated=0):
        # Verificar se o produto já existe
        self.cursor.execute("SELECT id FROM products WHERE product_site_id = ?", (product_site_id,))
        existing_product = self.cursor.fetchone()
        
        if existing_product:
            product_id = existing_product[0]
            # Se o produto existir, faça a atualização
            self.cursor.execute("""
                UPDATE products
                SET title = ?, photo_src = ?, id_list = ?, image = ?, updated = ?
                WHERE product_site_id = ?
            """, (title, photo_src, id_list, image_binary, updated, product_site_id))
        else:
            # Se o produto não existir, faça a inserção
            self.cursor.execute("""
                INSERT INTO products (title, photo_src, product_site_id, id_list, image, updated)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (title, photo_src, product_site_id, id_list, image_binary, updated))
            product_id = self.cursor.lastrowid
        
        # Confirma a transação no banco de dados
        self.conn.commit()
        
        # Retorna o ID do produto existente ou recém-inserido
        return product_id



    # Método para inserir dados na tabela products_infos verifica se as informações ja existe comparando o site_option_id caso exista faz o update
    def insert_or_update_products_infos(self, site_option_id, size, price_web, price_b2b, id_product):
        # Verificar se as informações do produto já existem
        self.cursor.execute("SELECT id FROM products_infos WHERE site_option_id = ?", (site_option_id,))
        existing_info = self.cursor.fetchone()
        
        if existing_info:
            info_id = existing_info[0]
            # Se as informações existirem, faça a atualização
            self.cursor.execute("""
                UPDATE products_infos
                SET size = ?, price_web = ?, price_b2b = ?, id_product = ?
                WHERE site_option_id = ?
            """, (size, price_web, price_b2b, id_product, site_option_id))
        else:
            # Se as informações não existirem, faça a inserção
            self.cursor.execute("""
                INSERT INTO products_infos (site_option_id, size, price_web, price_b2b, id_product)
                VALUES (?, ?, ?, ?, ?)
            """, (site_option_id, size, price_web, price_b2b, id_product))
            info_id = self.cursor.lastrowid
        
        # Confirma a transação no banco de dados
        self.conn.commit()
        
        # Retorna o ID do registro existente ou recém-inserido
        return info_id

    
