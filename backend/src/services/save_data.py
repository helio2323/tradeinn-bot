import sys
import os
import time
from tqdm import tqdm  # Importa a biblioteca tqdm
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.services.bot import get_products_site, login
from openpyxl import Workbook
from openpyxl.drawing.image import Image as ExcelImage
from openpyxl.styles import Alignment
from PIL import Image as PILImage
from src.models.Sqclass import Sqclass

def save_catalog(lst_id):
    bd = Sqclass()

    data = bd.get_products(id_list=lst_id)  # Passe o ID da lista apropriado

    prod_list = bd.get_product_list()
    
    for prod in prod_list:
        if prod[0] == lst_id:
            name_list = prod[1]
            break


    wb = Workbook()
    ws1 = wb.active
    ws1.title = "Sheet1"

    # Adiciona cabeçalhos
    headers = ["ID", "Title", "Photo Src", "Product Site ID", "Image", "Site Option ID", "Size", "Price Web", "Price B2B"]
    ws1.append(headers)

    # Pasta temporária para armazenar imagens
    temp_image_folder = './temp_images'
    os.makedirs(temp_image_folder, exist_ok=True)

    # Adiciona a barra de progresso
    for row in tqdm(data, desc="Processing data", unit="row"):
        product_id, title, photo_src, product_site_id, image_binary, site_option_id, size, price_web, price_b2b = row
        
        # Salva a imagem temporariamente
        image_path = None
        if image_binary:
            image_path = os.path.join(temp_image_folder, f'{product_id}.png')
            with open(image_path, 'wb') as image_file:
                image_file.write(image_binary)

            # Redimensiona a imagem
            with PILImage.open(image_path) as img:
                img = img.resize((150, 150))  # Ajuste o tamanho conforme necessário
                img.save(image_path)

        # Adiciona os dados ao Excel
        excel_row = [product_id, title, photo_src, product_site_id]
        if image_path:
            img = ExcelImage(image_path)
            img.width = 150  # Ajuste a largura da imagem conforme necessário
            img.height = 150  # Ajuste a altura da imagem conforme necessário
            ws1.add_image(img, f'E{ws1.max_row + 1}')  # Adiciona a imagem na coluna E
        else:
            excel_row.append("No Image")

        excel_row.extend([site_option_id, size, price_web, price_b2b])
        ws1.append(excel_row)

        # Ajusta a altura da linha
        ws1.row_dimensions[ws1.max_row].height = 120  # Ajuste a altura da linha conforme necessário
        
        # Ajusta largura de todas colunas
        for col in range(1, ws1.max_column + 1):
            ws1.column_dimensions[ws1.cell(row=1, column=col).column_letter].width = 20

        # Centraliza o conteúdo das células
        for row in range(1, ws1.max_row + 1):
            for col in range(1, ws1.max_column + 1):
                ws1.cell(row=row, column=col).alignment = Alignment(vertical='center', horizontal='center')

    arquive_name = f'./{name_list}-{time.strftime("%Y%m%d-%H%M%S")}.xlsx'

    # Salva o arquivo Excel
    name = arquive_name
    wb.save(filename=name)

    # Remove imagens temporárias
    for file in os.listdir(temp_image_folder):
        os.remove(os.path.join(temp_image_folder, file))
    os.rmdir(temp_image_folder)
