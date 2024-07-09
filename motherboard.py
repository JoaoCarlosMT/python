import subprocess
from prettytable import PrettyTable

def executar_comando(comando):
    resultado = subprocess.run(comando, capture_output=True, text=True, shell=True)
    return resultado.stdout.strip()

def listar_informacoes_hardware_windows():
    # Inicializando as tabelas
    tabela_placa_mae = PrettyTable(["Placa-mãe"])
    tabela_memoria = PrettyTable(["Memória"])
    tabela_processador = PrettyTable(["Processador"])
    tabela_pci = PrettyTable(["Slots PCI"])

    # Placa-mãe
    comando = "wmic baseboard get Manufacturer,Product,Version,SerialNumber /format:list"
    placa_mae_info = executar_comando(comando).split('\n')
    placa_mae = {item.split('=')[0]: item.split('=')[1] for item in placa_mae_info if '=' in item}
    placa_mae_str = f"{placa_mae.get('Manufacturer', 'Desconhecido')} {placa_mae.get('Product', 'Desconhecido')} - Versão: {placa_mae.get('Version', 'Desconhecido')} - Serial: {placa_mae.get('SerialNumber', 'Desconhecido')}"
    tabela_placa_mae.add_row([placa_mae_str])

    # Memória
    comando = "wmic memorychip get Capacity,Speed,MemoryType /format:list"
    memoria_info = executar_comando(comando).split('\n\n')
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
        memoria_detalhes.append(f"{int(capacidade)}GB {frequencia}MHz {tipo_memoria}")
    memoria_detalhes_str = ", ".join(memoria_detalhes)
    tabela_memoria.add_row([memoria_detalhes_str])
    
    # Processador e Socket
    comando = "wmic cpu get Name,SocketDesignation /format:list"
    cpu_info = executar_comando(comando).split('\n')
    processador = {item.split('=')[0]: item.split('=')[1] for item in cpu_info if '=' in item}
    processador_str = f"{processador.get('Name', 'Desconhecido')} - Socket: {processador.get('SocketDesignation', 'Desconhecido')}"
    tabela_processador.add_row([processador_str])
    
    # Slots PCI
    comando = "wmic path Win32_PnPEntity where \"PNPDeviceID like 'PCI%'\" get Name,DeviceID /format:list"
    pci_info = executar_comando(comando).split('\n\n')
    pci_detalhes = []
    for info in pci_info:
        detalhes = dict(item.split('=') for item in info.split('\n') if '=' in item)
        pci_detalhes.append(f"{detalhes.get('Name', 'Desconhecido')} - ID: {detalhes.get('DeviceID', 'Desconhecido')}")
    pci_detalhes_str = "\n".join(pci_detalhes)
    tabela_pci.add_row([pci_detalhes_str])

    # Imprimindo as tabelas
    print(tabela_placa_mae)
    print(tabela_processador)
    print(tabela_memoria)
    print(tabela_pci)

if __name__ == "__main__":
    listar_informacoes_hardware_windows()
