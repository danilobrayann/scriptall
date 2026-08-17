import subprocess

def run_command(command):
    print(f"\n>> {command}\n")
    result = subprocess.run(command, shell=True)
    return result.returncode

print("=== WINGET UPDATE SCRIPT ===")

input("Pressione ENTER para verificar atualizações...")

code = run_command("winget upgrade")

if code != 0:
    print("Nenhuma atualização disponível.")

input("\nPressione ENTER para atualizar tudo...")

run_command("winget upgrade --all --include-unknown --accept-package-agreements --accept-source-agreements")

print("\nSistema já está atualizado ou foi atualizado agora!")

input("Pressione ENTER para sair...")