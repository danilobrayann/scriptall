import os
import re

EXTENSOES = [".xlsx", ".xls", ".docx", ".doc", ".pdf"]

def extrair_numero(nome):
    match = re.search(r'\d+', nome)
    return match.group() if match else None

def renomear_arquivos(pasta, nome_base):
    for arquivo in os.listdir(pasta):
        nome, ext = os.path.splitext(arquivo)

        if ext.lower() in EXTENSOES:
            numero = extrair_numero(nome)

            if numero:
                novo_nome = f"{nome_base} {int(numero):02d}{ext}"
            else:
                print(f"⚠️ Sem número: {arquivo}")
                continue

            antigo = os.path.join(pasta, arquivo)
            novo = os.path.join(pasta, novo_nome)

            try:
                os.rename(antigo, novo)
                print(f"{arquivo} -> {novo_nome}")
            except Exception as e:
                print(f"Erro: {arquivo} -> {e}")

def main():
    print("=== RENOMEAR MANTENDO NÚMERO ===")

    pasta = input("Pasta (ENTER = atual): ")
    
    if pasta == "":
        pasta = os.getcwd()

    nome_base = input("Nome base (ex: ph excel): ")

    confirmar = input("Renomear? (s/n): ")

    if confirmar.lower() == "s":
        renomear_arquivos(pasta, nome_base)
        print("\nConcluído!")
    else:
        print("Cancelado.")

if __name__ == "__main__":
    main()