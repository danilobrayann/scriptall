import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()



import os
import shutil
import subprocess
import time

def limpar_pasta(caminho):
    if os.path.exists(caminho):
        for item in os.listdir(caminho):
            item_path = os.path.join(caminho, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path, ignore_errors=True)
            except:
                pass  # ignora erros silenciosamente

def executar(comando):
    try:
        subprocess.run(comando, shell=True)
    except:
        pass

def limpar_temp():
    print("🧹 Limpando TEMP...")
    limpar_pasta(os.getenv('TEMP'))
    limpar_pasta("C:\\Windows\\Temp")

def limpar_lixeira():
    print("🗑️ Limpando lixeira...")
    executar("powershell -Command Clear-RecycleBin -Force")

def limpar_dns():
    print("🌐 Limpando DNS...")
    executar("ipconfig /flushdns")

def limpar_prefetch():
    print("⚡ Limpando Prefetch...")
    limpar_pasta("C:\\Windows\\Prefetch")

def limpar_cache_navegadores():
    print("🌍 Limpando cache navegadores...")

    user = os.getenv("USERPROFILE")

    caminhos = [
        f"{user}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache",
        f"{user}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache"
    ]

    for caminho in caminhos:
        limpar_pasta(caminho)

def limpar_logs_windows():
    print("📜 Limpando logs (seguro)...")
    executar('powershell -Command "wevtutil el | ForEach-Object { wevtutil cl $_ }"')

def limpar_arquivos_sistema():
    print("🧼 Limpeza do Windows...")
    executar("cleanmgr /sagerun:1")

def detectar_tipo_disco():
    print("🔍 Verificando tipo de disco...")
    try:
        output = subprocess.check_output("wmic diskdrive get MediaType", shell=True).decode()
        return "SSD" if "SSD" in output.upper() else "HD"
    except:
        return "DESCONHECIDO"

def desfragmentar():
    tipo = detectar_tipo_disco()

    if tipo == "HD":
        print("💽 Desfragmentando HD...")
        executar("defrag C: /O")
    else:
        print("⚠️ SSD detectado — pulando desfragmentação")

def main():
    print("🔥 LIMPEZA AVANÇADA DO SISTEMA 🔥\n")

    input("Execute como ADMIN (ENTER para continuar)")

    limpar_temp()
    limpar_lixeira()
    limpar_dns()
    limpar_prefetch()
    limpar_cache_navegadores()
    limpar_logs_windows()
    limpar_arquivos_sistema()
    desfragmentar()

    print("\n✅ LIMPEZA FINALIZADA!")
    time.sleep(2)

if __name__ == "__main__":
    main()