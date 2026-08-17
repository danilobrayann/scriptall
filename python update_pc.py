import os
import subprocess

print("=== ATUALIZADOR DE PC ===")

input("Execute como ADMIN (pressione ENTER)")

# Atualizar programas
subprocess.run("winget upgrade --all --include-unknown --accept-package-agreements --accept-source-agreements", shell=True)

# Limpeza mais segura
print("\nLimpando temporários...")
temp = os.getenv('TEMP')

for root, dirs, files in os.walk(temp):
    for name in files:
        try:
            os.remove(os.path.join(root, name))
        except:
            pass

# Só roda sfc se for admin
print("\nVerificando sistema...")
subprocess.run("sfc /scannow", shell=True)

input("\nFinalizado! Pressione ENTER...")