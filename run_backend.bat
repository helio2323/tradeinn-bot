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

:: Instalar Build Tools do Visual Studio (necessário para alguns pacotes)
:: Essa linha é opcional e pode ser removida se o Build Tools já estiver instalado
call python -m pip install setuptools wheel

:: Instalar dependências do projeto
call pip install -r requirements.txt
if errorlevel 1 (
    echo Erro ao instalar pacotes a partir do requirements.txt. Tentando instalar pacotes manualmente...

    :: Pacotes principais
    call pip install altgraph==0.17.4
    call pip install asttokens==2.4.1
    call pip install attrs==24.2.0
    call pip install beautifulsoup4==4.12.3
    call pip install blinker==1.8.2
    call pip install Brotli==1.1.0
    call pip install bs4==0.0.2
    call pip install certifi==2024.7.4
    call pip install cffi==1.17.0
    call pip install chardet==5.2.0
    call pip install charset-normalizer==3.3.2
    call pip install click==8.1.7
    call pip install comm==0.2.2
    call pip install contourpy==1.2.1
    call pip install cssselect2==0.7.0
    call pip install cycler==0.12.1
    call pip install debugpy==1.8.5
    call pip install decorator==5.1.1
    call pip install et-xmlfile==1.1.0
    call pip install executing==2.0.1
    call pip install Flask==3.0.3
    call pip install fonttools==4.53.1
    call pip install h11==0.14.0
    call pip install html5lib==1.1
    call pip install idna==3.7
    call pip install ipykernel==6.29.5
    call pip install ipython==8.26.0
    call pip install itsdangerous==2.2.0
    call pip install jedi==0.19.1
    call pip install Jinja2==3.1.4
    call pip install jupyter_client==8.6.2
    call pip install jupyter_core==5.7.2
    call pip install kiwisolver==1.4.5
    call pip install MarkupSafe==2.1.5
    call pip install matplotlib==3.9.2
    call pip install matplotlib-inline==0.1.7
    call pip install nest-asyncio==1.6.0
    call pip install numpy==2.1.0
    call pip install openpyxl==3.1.5
    call pip install outcome==1.3.0.post0
    call pip install packaging==24.1
    call pip install pandas==2.2.2
    call pip install parso==0.8.4
    call pip install pdfkit==1.0.0
    call pip install pexpect==4.9.0
    call pip install pillow==10.4.0
    call pip install platformdirs==4.2.2
    call pip install prompt_toolkit==3.0.47
    call pip install psutil==6.0.0
    call pip install ptyprocess==0.7.0
    call pip install pure_eval==0.2.3
    call pip install pycparser==2.22
    call pip install pydyf==0.11.0
    call pip install Pygments==2.18.0
    call pip install pyinstaller==6.10.0
    call pip install pyinstaller-hooks-contrib==2024.8
    call pip install pyparsing==3.1.2
    call pip install pyphen==0.16.0
    call pip install PySocks==1.7.1
    call pip install python-dateutil==2.9.0.post0
    call pip install python-dotenv==1.0.1
    call pip install pytz==2024.1
    call pip install pyzmq==26.1.1
    call pip install reportlab==4.2.2
    call pip install requests==2.32.3
    call pip install selenium==4.23.1
    call pip install setuptools==73.0.1
    call pip install six==1.16.0
    call pip install sniffio==1.3.1
    call pip install sortedcontainers==2.4.0
    call pip install soupsieve==2.6
    call pip install stack-data==0.6.3
    call pip install tinycss2==1.3.0
    call pip install tornado==6.4.1
    call pip install tqdm==4.66.5
    call pip install traitlets==5.14.3
    call pip install trio==0.26.2
    call pip install trio-websocket==0.11.1
    call pip install typing_extensions==4.12.2
    call pip install tzdata==2024.1
    call pip install urllib3==2.2.2
    call pip install wcwidth==0.2.13
    call pip install webdriver-manager==4.0.2
    call pip install webencodings==0.5.1
    call pip install websocket-client==1.8.0
    call pip install Werkzeug==3.0.3
    call pip install wsproto==1.2.0
    call pip install zopfli==0.2.3

    :: Verificar novamente se o Selenium foi instalado corretamente
    call pip show selenium
    if errorlevel 1 (
        echo Erro: O pacote "selenium" não pôde ser instalado manualmente.
        pause
        exit /b 1
    )
)

:: Atualizar e reinstalar Pillow para corrigir possíveis problemas de compatibilidade
call pip install --upgrade pillow
call pip uninstall pillow -y
call pip install pillow

:: Verificar se o Flask está instalado (corrige erro de importação)
call pip install flask

:: Verificar se o diretório backend existe
if not exist backend (
    echo Diretório backend não encontrado. Verifique o caminho.
    pause
    exit /b 1
)

:: Mudar para o diretório backend
cd backend

:: Executar o script Python usando o Python do ambiente virtual
call python route.py

:: Manter a janela aberta para depuração
pause
