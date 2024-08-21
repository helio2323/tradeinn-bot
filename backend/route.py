from flask import Flask, request, g
import sqlite3
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.services.bot import get_products_site, login, update_all_products
from src.models.Sqclass import Sqclass
from src.services.Scraper import Navegador
from src.services.save_data import save_catalog

import time

bd = Sqclass()

app = Flask(__name__)
def get_db():
    if 'db' not in g:
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/src/database/database.db'))
        g.db = sqlite3.connect(db_path, check_same_thread=False)
        g.db.cursor()  # Initialize cursor
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/update/<name>')
def update_products(name):
    db = get_db()
    cursor = db.cursor()
    
    name = int(name)
    
    cursor.execute("SELECT * FROM product_list")
    lista = cursor.fetchall()
    
    bot = Navegador()
    for list_item in lista:
        if list_item[0] == name:
            url = list_item[2]
            LIST_ID = list_item[0]
            get_products_site(LIST_ID, url, bot)
            print(f"Lista de produtos {LIST_ID} atualizada com sucesso.")
            bot.click('XPATH', '/html/body/nav/div/div[4]/div[1]')
            time.sleep(5)
            bot.close()
            break
    
    return f'Hello, {name}!'

@app.route('/allproducts')
def all_products():
    bot = Navegador()
    update_all_products(bot)
    
    return 'All products updated successfully.'

if __name__ == '__main__':
    app.run(debug=True)
