import sys
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from jinja2 import Template
import pdfkit
from src.models.Sqclass import Sqclass

def generate_html_from_db(id_list, html_file):
    bd = Sqclass()

    # Obtém os dados do banco de dados
    data = bd.get_prod_pdf(id_list)

    # Define o template HTML
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Product Catalog</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            table, th, td {
                border: 1px solid black;
            }
            th, td {
                padding: 8px;
                text-align: left;
            }
            img {
                width: 150px;
                height: 150px;
            }
        </style>
    </head>
    <body>
        <h1>Product Catalog</h1>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Image</th>
                    <th>Price B2B</th>
                </tr>
            </thead>
            <tbody>
                {% for row in data %}
                <tr>
                    <td>{{ row[0] }}</td>
                    <td>{{ row[1] }}</td>
                    <td><img src="{{ row[2] }}" alt="Product Image"></td>
                    <td>{{ row[3] }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """

    # Cria o template Jinja2
    template = Template(html_template)
    
    # Renderiza o HTML com os dados do banco
    html_content = template.render(data=data)
    
    # Salva o HTML em um arquivo
    with open(html_file, 'w') as file:
        file.write(html_content)
    
    

def convert_html_to_pdf(html_file, pdf_file):
    # Configura o caminho para o executável wkhtmltopdf, ajuste conforme necessário
    path_to_wkhtmltopdf = '/usr/bin/wkhtmltopdf'  # Atualize conforme necessário
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    
    # Converte o HTML para PDF
    pdfkit.from_file(html_file, pdf_file, configuration=config)

# Função principal para gerar HTML e PDF
def generate_pdf_from_db(id_list, html_file, pdf_file):
    generate_html_from_db(id_list, html_file)
    convert_html_to_pdf(html_file, pdf_file)


