import os
import sys
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# Variáveis globais
caminho_completo = ""
nome_programa = ""
cor = ""

def obter_info_programa():
    global caminho_completo, nome_programa, cor

    # Obter o caminho completo do programa
    caminho_completo = os.path.abspath(sys.argv[0])
    # Obter o nome do programa
    nome_programa = os.path.basename(caminho_completo)
    
    # Verificar se o caminho é C:\Windows\System32
    if caminho_completo.lower().startswith("c:\\windows\\system32"):
        cor = Fore.BLUE
    else:
        cor = Fore.RED

def exibir_info_programa():
    global caminho_completo, nome_programa, cor

    # Exibir resultados
    print(f"Nome do programa: {nome_programa}")
    print(f"{cor}Caminho do programa: {caminho_completo}{Style.RESET_ALL}")

# Chamada das funções
if __name__ == "__main__":
    obter_info_programa()
    exibir_info_programa()
