import os
import shutil
import subprocess
import time

# =========================
# LIMPEZA
# =========================
def limpar_temp():
    print("\n🧹 Limpando TEMP...")
    temp = os.getenv("TEMP")

    for root, dirs, files in os.walk(temp):
        for f in files:
            try:
                os.remove(os.path.join(root, f))
            except:
                pass

def limpar_lixeira():
    print("🗑️ Limpando lixeira...")
    subprocess.run("powershell -Command Clear-RecycleBin -Force", shell=True)

# =========================
# MODO TURBO
# =========================
PROCESSOS = ["chrome.exe", "discord.exe", "spotify.exe", "steam.exe"]

def modo_turbo():
    print("\n⚡ MODO TURBO ATIVADO\n")

    for p in PROCESSOS:
        subprocess.run(f"taskkill /IM {p} /F", shell=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{p} fechado")

    subprocess.run("ipconfig /flushdns", shell=True)
    print("DNS limpo")

# =========================
# LAUNCHER
# =========================
def abrir_programas():
    print("""
1 - Chrome
2 - VS Code
3 - Discord
4 - Spotify
5 - Tudo (modo trabalho)
""")

    op = input("Escolha: ")

    if op == "1":
        subprocess.Popen("start chrome", shell=True)

    elif op == "2":
        subprocess.Popen("code", shell=True)

    elif op == "3":
        subprocess.Popen("start discord", shell=True)

    elif op == "4":
        subprocess.Popen("start spotify", shell=True)

    elif op == "5":
        subprocess.Popen("start chrome", shell=True)
        subprocess.Popen("code", shell=True)
        subprocess.Popen("start discord", shell=True)
        subprocess.Popen("start spotify", shell=True)

# =========================
# ORGANIZADOR
# =========================
def organizar_arquivos():
    print("\n📂 Organizando arquivos...\n")

    pasta = input("Pasta (ENTER = atual): ")
    if pasta == "":
        pasta = os.getcwd()

    tipos = {
        "Imagens": [".jpg", ".png"],
        "Documentos": [".pdf", ".docx", ".xlsx"],
        "Videos": [".mp4", ".mkv"]
    }

    for tipo, extensoes in tipos.items():
        caminho = os.path.join(pasta, tipo)
        os.makedirs(caminho, exist_ok=True)

        for arquivo in os.listdir(pasta):
            for ext in extensoes:
                if arquivo.lower().endswith(ext):
                    try:
                        shutil.move(os.path.join(pasta, arquivo), caminho)
                    except:
                        pass

    print("✔ Arquivos organizados!")

# =========================
# MONITOR
# =========================
def monitorar():
    print("\n📊 Monitorando sistema (CTRL+C pra sair)\n")
    while True:
        os.system("cls")
        subprocess.run("wmic cpu get loadpercentage", shell=True)
        subprocess.run("wmic OS get FreePhysicalMemory", shell=True)
        time.sleep(2)

# =========================
# MENU PRINCIPAL
# =========================
while True:
    print("\n=== 💻 SUPER PC MANAGER ===")
    print("""
1 - Limpar PC
2 - Modo Turbo
3 - Abrir programas
4 - Organizar arquivos
5 - Monitorar sistema
0 - Sair
""")

    escolha = input("Escolha: ")

    if escolha == "1":
        limpar_temp()
        limpar_lixeira()

    elif escolha == "2":
        modo_turbo()

    elif escolha == "3":
        abrir_programas()

    elif escolha == "4":
        organizar_arquivos()

    elif escolha == "5":
        try:
            monitorar()
        except KeyboardInterrupt:
            print("\nSaindo do monitor...")

    elif escolha == "0":
        print("Saindo...")
        break

    else:
        print("Opção inválida")