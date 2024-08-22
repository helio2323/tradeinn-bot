@echo off
:: Criar ambiente virtual
py -m venv venv

:: Verifique se o ambiente virtual está ativado corretamente
if not exist venv\Scripts\activate (
    echo Ambiente virtual não encontrado. Verifique o caminho.
    pause
    exit /b 1
)

:: Ativar ambiente virtual
call venv\Scripts\activate

:: Instalar dependências
call pip install -r requirements.txt

:: Mudar para o diretório backend
if not exist backend (
    echo Diretório backend não encontrado. Verifique o caminho.
    pause
    exit /b 1
)

cd backend

:: Executar o script Python
py route.py

:: Manter a janela aberta para depuração
pause
