
import requests       # Biblioteca para trabalhar com requisições 
import json           # Biblioteca para transformar a resposta da requisição em um dicionario Python

def get_GPB_to_BRL(moeda='GBP-BRL'):
    url_api = f'https://economia.awesomeapi.com.br/last/{moeda}'   # URL da API passando o parâmetro
    req = requests.get(url_api)                                    # Realizar o Request
    
    req = json.loads(req.content)
    
    response = req['GBPBRL']['bid']
    # Transformar em dicionario
    print(f"O valor da conversão é: {response} BRL")
    
    return  response   

def calcular_preco_em_brl(preco_gbp, cotacao_gbp_brl):
    
    preco_gbp = float(preco_gbp)
    cotacao_gbp_brl = float(cotacao_gbp_brl)
    
    frete = 6
    
    # Definir as faixas de preço e as taxas adicionais correspondentes
    if 1 <= preco_gbp <= 15:
        taxa_adicional = 5
    elif 15 < preco_gbp <= 30:
        taxa_adicional = 10
    elif 30 < preco_gbp <= 50:
        taxa_adicional = 15
    elif 50 < preco_gbp <= 80:
        taxa_adicional = 20
    elif 80 < preco_gbp <= 120:
        taxa_adicional = 25
    elif 120 < preco_gbp <= 150:
        taxa_adicional = 30
    elif 150 < preco_gbp <= 200:
        taxa_adicional = 35
    elif 200 < preco_gbp <= 300:
        taxa_adicional = 40
    elif 300 < preco_gbp <= 400:
        taxa_adicional = 50
    elif 400 < preco_gbp <= 500:
        taxa_adicional = 60
    else:
        raise ValueError("Faixa de preço fora do escopo definido.")

    # Calcular o preço em BRL
    preco_brl = (preco_gbp + taxa_adicional + frete) * (1 + 0.023 + 0.053) * cotacao_gbp_brl
    # converte 2 casas decimais
    preco_brl = round(preco_brl, 2)

    return preco_brl

                          # Transformar em dicionario
                             # Transformar em dicionario
  