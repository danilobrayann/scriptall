import subprocess

def executar(cmd):
    subprocess.run(cmd, shell=True)

def windows_update():
    print("\n🔄 Atualizando drivers via Windows Update...\n")
    executar("powershell -Command \"Install-Module PSWindowsUpdate -Force\"")
    executar("powershell -Command \"Import-Module PSWindowsUpdate\"")
    executar("powershell -Command \"Get-WindowsUpdate -Install -AcceptAll -AutoReboot\"")

def winget_update():
    print("\n📦 Atualizando programas (pode incluir drivers)...\n")
    executar("winget upgrade --all")

def abrir_device_manager():
    print("\n🖥️ Abrindo Gerenciador de Dispositivos...")
    executar("devmgmt.msc")

def abrir_windows_update():
    print("\n⚙️ Abrindo Windows Update...")
    executar("start ms-settings:windowsupdate")

while True:
    print("\n=== 🔧 GERENCIADOR DE DRIVERS ===")
    print("""
1 - Atualizar drivers (Windows Update)
2 - Atualizar tudo (winget)
3 - Abrir Gerenciador de Dispositivos
4 - Abrir Windows Update
0 - Sair
""")

    op = input("Escolha: ")

    if op == "1":
        windows_update()

    elif op == "2":
        winget_update()

    elif op == "3":
        abrir_device_manager()

    elif op == "4":
        abrir_windows_update()

    elif op == "0":
        print("Saindo...")
        break

    else:
        print("Opção inválida")