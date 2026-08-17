import subprocess
import os

def abrir(comando, nome):
    try:
        subprocess.Popen(comando, shell=True)
        print(f"Abrindo {nome}...\n")
    except Exception as e:
        print(f"Erro ao abrir {nome}: {e}\n")

def abrir_spotify():
    # Caminho padrão do Spotify (desktop)
    caminho = os.path.expanduser(r"~\AppData\Roaming\Spotify\Spotify.exe")
    
    if os.path.exists(caminho):
        abrir(f'"{caminho}"', "Spotify")
    else:
        # Método alternativo (Microsoft Store)
        abrir(r'start shell:AppsFolder\SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify', "Spotify")

while True:
    print("=== LAUNCHER DE PROGRAMAS ===")

    print("""
1 - Google Chrome
2 - VS Code
3 - Calculadora
4 - Notepad
5 - Discord
6 - Spotify
7 - Steam
8 - Explorador de Arquivos
9 - Terminal (CMD)
10 - Tudo (modo trabalho)
0 - Sair
""")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        abrir("start chrome", "Chrome")

    elif opcao == "2":
        abrir("code", "VS Code")

    elif opcao == "3":
        abrir("calc", "Calculadora")

    elif opcao == "4":
        abrir("notepad", "Notepad")

    elif opcao == "5":
        abrir("start discord", "Discord")

    elif opcao == "6":
        abrir_spotify()

    elif opcao == "7":
        abrir("start steam", "Steam")

    elif opcao == "8":
        abrir("explorer", "Explorador")

    elif opcao == "9":
        abrir("start cmd", "CMD")

    elif opcao == "10":
        print("Abrindo modo trabalho...\n")
        abrir("start chrome", "Chrome")
        abrir("code", "VS Code")
        abrir("start discord", "Discord")
        abrir_spotify()

    elif opcao == "0":
        print("Saindo...")
        break

    else:
        print("Opção inválida\n")