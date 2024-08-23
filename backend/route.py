from flask import Flask, render_template, redirect, url_for, request
import sys
import os
import requests
import time

from src.services.bot import get_products_site, update_all_products
from src.models.Sqclass import Sqclass
from src.services.Scraper import Navegador
from src.services.save_data import save_catalog, generate_pdf_from_db

app = Flask(__name__)

bd = Sqclass()

@app.route('/')
def index():
    return render_template('menu.html')

@app.route('/list_products')
def list_products():
    listas = bd.get_product_list()
    if listas:
        listas_text = "\n".join([f'ID: {list_item[0]} | LISTA: {list_item[1]}' for list_item in listas])
    else:
        listas_text = "Nenhuma lista de produtos encontrada."
    return render_template('result.html', result=listas_text)

@app.route('/update_all_products')
def update_all_products_route():
    bot = Navegador()
    update_all_products(bot)
    return render_template('result.html', result="Todos os produtos foram atualizados.")

@app.route('/update_single_list', methods=['GET'])
def update_single_list():
    lista_id = request.args.get('lista_id', type=int)
    if not lista_id:
        return render_template('result.html', result="ID da lista não fornecido.")
    try:
        lista = bd.get_product_list()
        bot = Navegador()
        for list_item in lista:
            if list_item[0] == lista_id:
                url = list_item[2]
                LIST_ID = list_item[0]
                get_products_site(LIST_ID, url, bot)
                bot.click('XPATH', '/html/body/nav/div/div[4]/div[1]')
                time.sleep(5)
                bot.close()
                return render_template('result.html', result=f"Lista de produtos {LIST_ID} atualizada com sucesso.")
    except Exception as e:
        return render_template('result.html', result=f"Erro ao atualizar a lista de produtos: {e}")
    return render_template('result.html', result="ID da lista não encontrado.")

@app.route('/generate_catalog', methods=['GET'])
def generate_catalog():
    lista_id = request.args.get('lista_id', type=int)
    if not lista_id:
        return render_template('result.html', result="ID da lista não fornecido.")
    save_catalog(lista_id)
    prod_list = bd.get_product_list()
    for prod in prod_list:
        if prod[0] == lista_id:
            name_list = prod[1]
            break
    print(name_list)
    generate_pdf_from_db(lista_id, f'./Catalogo/{lista_id}-{name_list}.html', f'./Catalogo/{lista_id}-{name_list}.pdf')
    return render_template('result.html', result=f"Catálogo para a lista {lista_id} gerado com sucesso.")

@app.route('/set_all_list_false')
def set_all_list_false():
    bd.set_all_list_false()
    return render_template('result.html', result="Todas as listas de produtos foram atualizadas como False.")

@app.route('/exit')
def exit_app():
    return render_template('result.html', result="Saindo...")

if __name__ == '__main__':
    app.run(debug=True)
