import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.services.bot import get_products_site, login, update_all_products
from src.models.Sqclass import Sqclass
from src.services.Scraper import Navegador
from src.services.save_data import save_catalog

bd = Sqclass()


def show_menu():
    print("\nMenu Principal:")
    print("1 - Listas de produtos")
    print("2 - Buscar/Atualizar Todos Produtos")
    print("3 - Buscar/Atualizar uma Única Lista de Produtos")
    print("4 - Gerar Catálogo de Produtos com Base em Lista")
    print("5 - Sair")
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
            lista_id = int(input('Informe o número da lista que deseja atualizar: '))
            lista = bd.get_product_list()
            bot = Navegador()
            for list_item in lista:
                if list_item[0] == lista_id:
                    url = list_item[2]
                    LIST_ID = list_item[0]
                    get_products_site(LIST_ID, url, bot)
                    print(f"Lista de produtos {LIST_ID} atualizada com sucesso.")
                    break
            else:
                print("ID da lista não encontrado.")

        elif choice == 4:
            lista_id = int(input('Informe o número da lista que deseja gerar o catálogo: '))
            save_catalog(lista_id)
            print(f"Catálogo para a lista {lista_id} gerado com sucesso.")

        elif choice == 5:
            print("Saindo...")
            break

if __name__ == "__main__":
    main()
