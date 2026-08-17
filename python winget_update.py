import subprocess

def run_command(command):
    print(f"\n>> {command}\n")
    result = subprocess.run(command, shell=True)
    
    if result.returncode != 0:
        print("Erro ao executar comando.\n")
    else:
        print("Comando executado com sucesso.\n")

def main():
    print("=== WINGET UPDATE SCRIPT ===")

    input("Pressione ENTER para verificar atualizações...")

    # Atualiza a lista de pacotes
    run_command("winget update")

    input("Pressione ENTER para atualizar TODOS os programas...")

    # Atualiza todos os programas
    run_command("winget upgrade --all --include-unknown --accept-package-agreements --accept-source-agreements")

    print("\nTudo atualizado!")

    input("Pressione ENTER para sair...")

if __name__ == "__main__":
    main()