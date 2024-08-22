from cx_Freeze import setup, Executable

setup(
    name="tradeinn",
    version="0.1",
    description="Descrição do seu aplicativo",
    executables=[Executable("route.py")]
)
