import os
import shutil
import subprocess

def limpar_pasta(caminho):
    print(f"\nLimpando: {caminho}")
    
    if not os.path.exists(caminho):
        print("Pasta não existe.")
        return
    
    for root, dirs, files in os.walk(caminho):
        for name in files:
            try:
                os.remove(os.path.join(root, name))
            except:
                pass
        for name in dirs:
            try:
                shutil.rmtree(os.path.join(root, name), ignore_errors=True)
            except:
                pass

def main():
    print("=== LIMPEZA COMPLETA DO PC ===")

    input("Pressione ENTER para iniciar limpeza...")

    # TEMP do usuário
    limpar_pasta(os.getenv('TEMP'))

    # TEMP do Windows
    limpar_pasta("C:\\Windows\\Temp")

    # Prefetch (cache de inicialização)
    limpar_pasta("C:\\Windows\\Prefetch")

    # Limpeza de disco (automático)
    print("\nExecutando limpeza do Windows...")
    subprocess.run("cleanmgr /sagerun:1", shell=True)

    print("\nLimpeza finalizada!")

    input("Pressione ENTER para sair...")

if __name__ == "__main__":
    main()