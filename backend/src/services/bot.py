import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import requests
from io import BytesIO
from PIL import Image as PILImage
from selenium.webdriver.support.ui import Select
from src.models.Sqclass import Sqclass

from src.services.Scraper import Navegador
from src.models.Sqclass import Sqclass

#VARIAVEIS
LOGIN_URL = 'https://b2b.tradeinn.com'
USER_EMAIL = 'vendas@oldfirm.com.br'
USER_PASSWORD = 'Kohlrauschrs18!G'



def login(bot):
        
    bot.get(LOGIN_URL)

    bot.sendkeys('ID', 'email_login', USER_EMAIL)
    bot.sendkeys('ID', 'pass_login', USER_PASSWORD)

    bot.click('XPATH', '/html/body/div[3]/div/div/div[2]/div[1]/form/div[4]/button')

def update_all_products(bot):
    import time

    bd = Sqclass()

    listas = bd.get_product_list()

    elements = bot.get_elements('CLASS_NAME', 'product-listing-wrapper')

    for list in listas:
        
        url = list[2]
        LIST_ID = list[0]
        
        get_products_site(LIST_ID, url)
        
    bot.click('XPATH', '/html/body/nav/div/div[4]/div[1]')
    time.sleep(5)
    bot.close()

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        raise Exception(f"Failed to download image from {url}")

def image_to_binary(image_stream):
    with PILImage.open(image_stream) as img:
        with BytesIO() as output:
            img.save(output, format='PNG')
            return output.getvalue()

def get_products_site(LIST_ID, url, bot):
    
    login(bot)
    
    bd = Sqclass()
    
    try:
        bot.get(url)
        
        elements = bot.get_elements('CLASS_NAME', 'product-listing-wrapper')

        i = 1
        refresh = 0

        start_time = time.time()  # Início da medição de tempo

        total_elements = len(elements)
        
        for i, element in enumerate(elements, start=1):
            # Simulação de barra de progresso
            progress = (i / total_elements) * 100
            elapsed_time = time.time() - start_time
            
            sys.stdout.write(f"\rProgresso: [{'#' * i}{'.' * (total_elements - i)}] {int(progress)}%")
            sys.stdout.write(f"\nTempo decorrido: {elapsed_time:.2f} segundos")
            sys.stdout.flush()

            xpath = f"/html/body/div[3]/div[2]/div[1]/div/main/ul/li[{i}]"
            
            bot.click('XPATH', xpath)
            
            title = bot.element_get_text('ID', 'name_product').text

            photo_src = bot.element_get_text('XPATH', '/html/body/div[3]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/img').get_attribute('src')

            # Baixar e converter a imagem para binário
            try:
                img_stream = download_image(photo_src)
                img_binary = image_to_binary(img_stream)
            except Exception as e:
                print(f"Erro ao baixar ou converter imagem: {e}")
                img_binary = None  # Use None se a imagem não puder ser baixada ou convertida

            product_site_id = bot.element_get_text('XPATH', xpath).get_attribute('data-id_modelo')
            
            # Salvar no BD, incluindo a imagem binária
            new_product = bd.insert_or_update_product(title, photo_src, product_site_id, LIST_ID, img_binary)
            
            # Salvar listas
            drp_element = bot.get_elements('ID', 'tallas_productos')[0]
            select = Select(drp_element)
            num_options = len(select.options)

            for index in range(num_options):
                select.select_by_index(index)
                
                size = select.first_selected_option.text
                option_site_id = select.first_selected_option.get_attribute('value')
                price_web = bot.element_get_text('ID', 'precio_web').text
                price_b2b = bot.element_get_text('ID', 'precio_b2b').text
                
                new_product_info = bd.insert_or_update_products_infos(option_site_id, size, price_web, price_b2b, new_product)

            bot.click('ID', 'js-cerrar-detalle')
            i += 1
            refresh += 1
            
            if refresh == 8:
                refresh = 0
                bot.get(url)

        end_time = time.time()  # Fim da medição de tempo
        execution_time = end_time - start_time  # Cálculo do tempo de execução 

        print(f"\nTempo de execução: {execution_time:.2f} segundos")
        
    except Exception as e:
        print(e)
        bot.click('XPATH', '/html/body/nav/div/div[4]/div[1]')
        time.sleep(5)
        bot.close()