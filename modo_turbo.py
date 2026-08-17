import subprocess
import os

PROCESSOS = [
    "chrome.exe",
    "msedge.exe",
    "discord.exe",
    "spotify.exe",
    "steam.exe"
]

def fechar_processos():
    print("\n🔥 Liberando RAM...\n")
    for p in PROCESSOS:
        subprocess.run(
            f"taskkill /IM {p} /F",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"{p} fechado")

def limpar_temp():
    print("\n🧹 Limpando TEMP...")
    temp = os.getenv("TEMP")

    for root, dirs, files in os.walk(temp):
        for f in files:
            try:
                os.remove(os.path.join(root, f))
            except:
                pass

def limpar_dns():
    print("\n🌐 Limpando DNS...")
    subprocess.run("ipconfig /flushdns", shell=True)

def otimizar_disco():
    print("\n💽 Otimizando disco...")
    subprocess.run("defrag C: /O", shell=True)

def verificar_sistema():
    print("\n🔍 Verificando sistema...")
    subprocess.run("sfc /scannow", shell=True)

while True:
    print("\n=== ⚡ MODO TURBO PC ===")
    print("""
1 - Liberar RAM (fechar apps)
2 - Limpar arquivos temporários
3 - Limpar DNS
4 - Otimizar disco
5 - Verificar sistema
6 - Executar TUDO (modo turbo completo)
0 - Sair
""")

    opcao = input("Escolha: ")

    if opcao == "1":
        fechar_processos()

    elif opcao == "2":
        limpar_temp()

    elif opcao == "3":
        limpar_dns()

    elif opcao == "4":
        otimizar_disco()

    elif opcao == "5":
        verificar_sistema()

    elif opcao == "6":
        print("\n🚀 Executando modo turbo completo...\n")
        fechar_processos()
        limpar_temp()
        limpar_dns()
        otimizar_disco()
        verificar_sistema()
        print("\n✅ Finalizado!")

    elif opcao == "0":
        print("Saindo...")
        break

    else:
        print("Opção inválida")