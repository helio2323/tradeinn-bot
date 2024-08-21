def get_GPB_to_BRL():
    import requests
    from bs4 import BeautifulSoup

    # Fazer a requisição GET
    url = 'https://www.xe.com/en-gb/currencyconverter/convert/?Amount=1&From=GBP&To=BRL'
    response = requests.get(url)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Analisar o conteúdo da página com BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Localizar o elemento <p> que contém o valor da moeda
        value_element = soup.find('p', class_='sc-e08d6cef-1 fwpLse')
        
        # Extrair o texto do elemento, se encontrado
        if value_element:
            # Extrair o texto principal e o valor adicional dentro do <span>
            main_value = value_element.contents[0].strip()
            faded_digits = value_element.find('span', class_='faded-digits').text.strip()
            
            # Combinar os valores
            currency_value = main_value + faded_digits
            print(f"O valor da conversão é: {currency_value} BRL")
            return currency_value
        else:
            print("Não foi possível encontrar o valor da moeda.")
    else:
        print(f"Erro ao fazer a requisição: {response.status_code}")


def calcular_preco_em_brl(preco_gbp, cotacao_gbp_brl):
    
    preco_gbp = float(preco_gbp)
    cotacao_gbp_brl = float(cotacao_gbp_brl)
    
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
    preco_brl = (preco_gbp + taxa_adicional) * (1 + 0.023 + 0.053) * cotacao_gbp_brl
    # converte 2 casas decimais
    preco_brl = round(preco_brl, 2)

    return preco_brl


