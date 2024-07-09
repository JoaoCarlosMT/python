import winreg

def list_startup_programs():
    # Abre a chave de registro do usuário atual
    key = winreg.HKEY_CURRENT_USER
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        key_handle = winreg.OpenKey(key, key_path, 0, winreg.KEY_READ)
        print("Programas configurados para iniciar com o Windows:")
        for i in range(winreg.QueryInfoKey(key_handle)[1]):
            program_name, program_path, _ = winreg.EnumValue(key_handle, i)
            print(f"Nome: {program_name}, Caminho: {program_path}")
        winreg.CloseKey(key_handle)
    except Exception as e:
        print("Erro ao listar programas de inicialização:", e)

if __name__ == "__main__":
    list_startup_programs()
