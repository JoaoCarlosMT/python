import sys
import os

def get_current_exe_path():
    # Obtém o caminho completo do executável atual
    if getattr(sys, 'frozen', False):
        # Se estiver congelado (exemplo: executável gerado pelo PyInstaller)
        return sys.executable
    else:
        # Se estiver rodando como script Python
        return os.path.abspath(__file__)

if __name__ == "__main__":
    current_exe_path = get_current_exe_path()
    print(current_exe_path)
