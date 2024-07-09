import subprocess
import getpass

def criar_agendamento_cmd():
    # Obter o nome do usuário atual
    usuario_atual = getpass.getuser()

    # Define o comando PowerShell para criar a tarefa agendada
    comando_powershell = f'''
$action = New-ScheduledTaskAction -Execute 'update_time.exe'
$trigger = New-ScheduledTaskTrigger -AtLogOn
$principal = New-ScheduledTaskPrincipal -UserId "{usuario_atual}" -LogonType Interactive -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "AbrirUpdateTimeComoUsuarioAtual" -Action $action -Trigger $trigger -Principal $principal -Settings $settings
'''

    # Executa o comando PowerShell
    subprocess.run(["powershell", "-Command", comando_powershell], check=True)

# Chama a função para criar o agendamento
if __name__ == "__main__":
    criar_agendamento_cmd()
