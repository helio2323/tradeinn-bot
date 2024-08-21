import subprocess
import os
import sys
import time

def run_flask_server():
    """Executa o servidor Flask como um subprocesso."""
    flask_process = subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), 'route.py')],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return flask_process

def main():
    # Iniciar o servidor Flask em um subprocesso
    flask_process = run_flask_server()
    print(f"Flask Server PID: {flask_process.pid}")

    # Aguardar um pouco para garantir que o Flask server está totalmente iniciado
    time.sleep(5)

    # Executar o script de terminal principal
    try:
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'main.py')])
    except KeyboardInterrupt:
        print("Interrompido pelo usuário")
        flask_process.terminate()

if __name__ == "__main__":
    main()
