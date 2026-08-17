import subprocess
import os

def executar(comando):
    subprocess.run(comando, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def tema_dark():
    print("\n🌙 Ativando modo DARK...")
    
    executar('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize /v AppsUseLightTheme /t REG_DWORD /d 0 /f')
    executar('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize /v SystemUsesLightTheme /t REG_DWORD /d 0 /f')

    print("✔ Tema escuro ativado!")

def tema_light():
    print("\n☀️ Ativando modo LIGHT...")
    
    executar('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize /v AppsUseLightTheme /t REG_DWORD /d 1 /f')
    executar('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize /v SystemUsesLightTheme /t REG_DWORD /d 1 /f')

    print("✔ Tema claro ativado!")

def reiniciar_explorer():
    print("\n🔄 Atualizando tema...")
    executar("taskkill /f /im explorer.exe")
    executar("start explorer.exe")

while True:
    print("\n=== 🎨 GERENCIADOR DE TEMA ===")
    print("""
1 - Tema Dark 🌙
2 - Tema Light ☀️
3 - Reiniciar Explorer (aplicar tema)
0 - Sair
""")

    op = input("Escolha: ")

    if op == "1":
        tema_dark()

    elif op == "2":
        tema_light()

    elif op == "3":
        reiniciar_explorer()

    elif op == "0":
        print("Saindo...")
        break

    else:
        print("Opção inválida")