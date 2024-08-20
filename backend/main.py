import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.services.bot import get_products_site, login
from src.models.Sqclass import Sqclass
from src.services.Scraper import Navegador

bd = Sqclass()


while True:
    print('1 - Listas de produtos')
    print('2 - Buscar/Atualizar Todos Produtos')
    print('3 - Buscar/Atualizar uma unica Lista de Produtos')
    print('4 - Gerar catalogo de produtos com base em lista')
    print('5 - Sair')
    
    try:
        op = int(input('Escolha uma opção: '))
    except:
        print('Opção Invalida')
        continue

    if op == 1:
        listas = bd.get_product_list()
        for list in listas:
            print('-------------------------------------------')
            print(f'ID: {list[0]} | LIST: {list[1]}')
            print('-------------------------------------------')

    if op == 3:
        op = int(input('Informe o numero da lista que deseja atualizar: '))

        lista = bd.get_product_list()
        bot = Navegador()
        for list in lista:
            if list[0] == op:
                url = list[2]
                LIST_ID = list[0]
                get_products_site(LIST_ID, url, bot)
        