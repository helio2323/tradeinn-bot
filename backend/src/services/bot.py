import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.services.Scraper import Navegador
from src.models.Sqclass import Sqclass

#VARIAVEIS
LOGIN_URL = 'https://b2b.tradeinn.com'
USER_EMAIL = 'vendas@oldfirm.com.br'
USER_PASSWORD = 'Kohlrauschrs18'

bot = Navegador()
bd = Sqclass()

bot.get(LOGIN_URL)

bot.sendkeys('ID', 'email_login', USER_EMAIL)
bot.sendkeys('ID', 'pass_login', USER_PASSWORD)

bot.click('XPATH', '/html/body/div[3]/div/div/div[2]/div[1]/form/div[4]/button')

time.sleep(5)
