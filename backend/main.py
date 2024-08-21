import sys
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.services.bot import get_products_site, login, update_all_products
from src.models.Sqclass import Sqclass
from src.services.Scraper import Navegador
from src.services.save_data import save_catalog, generate_pdf_from_db

import time

bd = Sqclass()


def show_menu():
    print("\nMenu Principal:")
    print("1 - Listas de produtos")
    print("2 - Buscar/Atualizar Todos Produtos")
    print("3 - Buscar/Atualizar uma Única Lista de Produtos")
    print("4 - Gerar Catálogo de Produtos com Base em Lista")
    print("5 - Atualizar status das listas para False (com isso a busca sera feita em todas as listas)")
    print("6 - Sair")
    
    print()

def get_user_choice():
    try:
        choice = int(input("Escolha uma opção: "))
        if choice not in range(1, 6):
            print("Opção inválida! Por favor, escolha um número entre 1 e 5.")
            return None
        return choice
    except ValueError:
        print("Entrada inválida! Por favor, insira um número.")
        return None

def main():
    while True:
        show_menu()
        choice = get_user_choice()

        if choice is None:
            continue

        if choice == 1:
            listas = bd.get_product_list()
            if listas:
                print("\nListas de Produtos:")
                for list_item in listas:
                    print('-------------------------------------------')
                    print(f'ID: {list_item[0]} | LISTA: {list_item[1]}')
                    print('-------------------------------------------')
            else:
                print("Nenhuma lista de produtos encontrada.")

        elif choice == 2:
            print("Buscando/Atualizando todos os produtos...")
            bot = Navegador()
            update_all_products(bot)
            print("Todos os produtos foram atualizados.")

        elif choice == 3:
            try:
                lista_id = int(input('Informe o número da lista que deseja atualizar: '))
                lista = bd.get_product_list()
                bot = Navegador()
                for list_item in lista:
                    if list_item[0] == lista_id:
                        url = list_item[2]
                        LIST_ID = list_item[0]
                        #requests.get(f'http://127.0.0.1:5000/update/{LIST_ID}')
                        get_products_site(LIST_ID, url, bot)
                        print(f"Lista de produtos {LIST_ID} atualizada com sucesso.")
                        bot.click('XPATH', '/html/body/nav/div/div[4]/div[1]')
                        time.sleep(5)
                        bot.close()
                        break
            except Exception as e:
                print(f"Erro ao atualizar a lista de produtos: {e}")
            else:
                print("ID da lista não encontrado.")

        elif choice == 4:
            lista_id = int(input('Informe o número da lista que deseja gerar o catálogo: '))
            save_catalog(lista_id)
            
            prod_list = bd.get_product_list()
    
            for prod in prod_list:
                if prod[0] == lista_id:
                    name_list = prod[1]
                    break
            
            generate_pdf_from_db(lista_id, f'./backend/Catalogo/{name_list}.html', f'./backend/Catalogo/{name_list}.pdf')
            
            print(f"Catálogo para a lista {lista_id} gerado com sucesso.")
        
        elif choice == 5:
            bd.set_all_list_false()
            print("Todas as listas de produtos foram atualizadas como False.")
        
        elif choice == 6:
            print("Saindo...")
            break

if __name__ == "__main__":
    main()
