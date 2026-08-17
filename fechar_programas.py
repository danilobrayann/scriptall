import subprocess

PROCESSOS = [
    "chrome.exe",
    "msedge.exe",
    "discord.exe",
    "spotify.exe",
    "steam.exe",
    "notepad.exe"
]

def fechar_processos():
    print("\nFechando programas...\n")

    for processo in PROCESSOS:
        subprocess.run(
            f'taskkill /IM {processo} /F',
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"{processo} finalizado")

    print("\n✔ Limpeza concluída!\n")

while True:
    print("=== GERENCIADOR DE PROCESSOS ===")
    print("""
1 - Fechar programas desnecessários
2 - Ver processos ativos
0 - Sair
""")

    opcao = input("Escolha: ")

    if opcao == "1":
        fechar_processos()

    elif opcao == "2":
        subprocess.run("tasklist", shell=True)

    elif opcao == "0":
        print("Saindo...")
        break

    else:
        print("Opção inválida\n")