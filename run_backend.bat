@echo off
:: Criar ambiente virtual
py -m venv venv

:: Verifique se o ambiente virtual foi criado corretamente
if not exist venv\Scripts\activate (
    echo Ambiente virtual não encontrado. Verifique o caminho.
    pause
    exit /b 1
)

:: Ativar ambiente virtual
call venv\Scripts\activate

:: Atualizar pip para evitar problemas de compatibilidade
call python -m pip install --upgrade pip

:: Instalar dependências do projeto
call pip install -r requirements.txt

:: Atualizar e reinstalar Pillow para corrigir possíveis problemas de compatibilidade
call pip install --upgrade pillow
call pip uninstall pillow -y
call pip install pillow

:: Verificar se o diretório backend existe
if not exist backend (
    echo Diretório backend não encontrado. Verifique o caminho.
    pause
    exit /b 1
)

:: Mudar para o diretório backend
cd backend

:: Executar o script Python
py route.py

:: Manter a janela aberta para depuração
pause
