import subprocess

def listar_informacoes_hardware_windows():
    # Placa-mãe
    comando = "wmic baseboard get Product /format:list"
    resultado = subprocess.run(comando, capture_output=True, text=True, shell=True)
    placa_mae = resultado.stdout.strip().split('=')[1]
    
    comando = "wmic baseboard get Name /format:list"
    resultado = subprocess.run(comando, capture_output=True, text=True, shell=True)
    nome_placa_mae = resultado.stdout.strip().split('=')[1]

    print(f"Placa-mãe: {nome_placa_mae} ({placa_mae})")
    
    # Processador
    comando = "wmic cpu get Name /format:list"
    resultado = subprocess.run(comando, capture_output=True, text=True, shell=True)
    processador = resultado.stdout.strip().split('=')[1]
    print(f"Processador: {processador}")
    
    # Memória
    comando = "wmic memorychip get Capacity,Speed,MemoryType /format:list"
    resultado = subprocess.run(comando, capture_output=True, text=True, shell=True)
    memoria_info = resultado.stdout.strip().split('\n\n')
    
    memoria_total = 0
    memoria_detalhes = []
    
    for info in memoria_info:
        detalhes = dict(item.split('=') for item in info.split('\n') if '=' in item)
        capacidade = int(detalhes.get('Capacity', 0)) / (1024**3)  # Convertendo bytes para gigabytes
        frequencia = detalhes.get('Speed', 'Desconhecido')
        tipo_memoria = detalhes.get('MemoryType', 'Desconhecido')
        
        if tipo_memoria == '20':
            tipo_memoria = 'DDR'
        elif tipo_memoria == '21':
            tipo_memoria = 'DDR2'
        elif tipo_memoria == '24':
            tipo_memoria = 'DDR3'
        elif tipo_memoria == '26':
            tipo_memoria = 'DDR4'
        
        memoria_total += capacidade
        memoria_detalhes.append(f"{int(capacidade)}GB {frequencia}MHz {tipo_memoria}")
    
    memoria_total_gb = f"{memoria_total:.0f}GB"
    memoria_detalhes_str = ", ".join(memoria_detalhes)
    print(f"Memória: {memoria_total_gb} ({memoria_detalhes_str})")
    
    # HD ou SSD
    comando = "wmic diskdrive get Model,Size /format:list"
    resultado = subprocess.run(comando, capture_output=True, text=True, shell=True)
    discos_info = resultado.stdout.strip().split('\n\n')
    
    discos_detalhes = []
    for info in discos_info:
        detalhes = dict(item.split('=') for item in info.split('\n') if '=' in item)
        modelo = detalhes.get('Model', 'Desconhecido')
        tamanho = int(detalhes.get('Size', 0)) / (1024**3)  # Convertendo bytes para gigabytes
        discos_detalhes.append(f"{modelo} ({tamanho:.0f}GB)")
    
    discos_detalhes_str = ", ".join(discos_detalhes)
    print(f"Discos (HD/SSD): {discos_detalhes_str}")
    
    # Placa de vídeo
    comando = "wmic path win32_videocontroller get Name /format:list"
    resultado = subprocess.run(comando, capture_output=True, text=True, shell=True)
    placa_video = resultado.stdout.strip().split('=')[1]
    print(f"Placa de Vídeo: {placa_video}")
    
    # Outros dispositivos (Bluetooth, Wireless)
    comando = "wmic path Win32_PnPEntity where \"PNPClass='Bluetooth' or PNPClass='Net'\" get Name,Manufacturer /format:list"
    resultado = subprocess.run(comando, capture_output=True, text=True, shell=True)
    dispositivos_info = resultado.stdout.strip().split('\n\n')
    
    dispositivos_detalhes = []
    for info in dispositivos_info:
        detalhes = dict(item.split('=') for item in info.split('\n') if '=' in item)
        nome = detalhes.get('Name', 'Desconhecido')
        fabricante = detalhes.get('Manufacturer', 'Desconhecido')
        dispositivos_detalhes.append(f"{nome} ({fabricante})")
    
    dispositivos_detalhes_str = ", ".join(dispositivos_detalhes)
    print(f"Outros dispositivos (Bluetooth, Wireless): {dispositivos_detalhes_str}")

if __name__ == "__main__":
    listar_informacoes_hardware_windows()
