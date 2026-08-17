while True:
    try:
        print("\n=== 🤖 JARVIS PC MANAGER ===")
        print("""
1 - Limpar PC
2 - Modo Turbo
3 - Abrir Programas
4 - Organizar Arquivos
5 - Monitor Sistema
6 - Modo Gamer
7 - Downloader
8 - Wallpaper automático
9 - Bloquear sites
10 - Assistente IA
0 - Sair
""")

        op = input("Escolha: ").strip()

        print(f"DEBUG -> Você digitou: {op}")  # 👈 ajuda a ver erro

        if op == "1":
            print("Executando limpar_pc...")
            limpar_pc()

        elif op == "2":
            print("Executando modo_turbo...")
            modo_turbo()

        elif op == "3":
            print("Executando abrir_programas...")
            abrir_programas()

        elif op == "4":
            print("Executando organizar...")
            organizar()

        elif op == "5":
            try:
                monitor()
            except KeyboardInterrupt:
                print("Saindo monitor")

        elif op == "6":
            modo_gamer()

        elif op == "7":
            baixar()

        elif op == "8":
            wallpaper()

        elif op == "9":
            bloquear()

        elif op == "10":
            assistente()

        elif op == "0":
            print("Saindo...")
            break

        else:
            print("❌ Opção inválida")

    except Exception as e:
        print(f"Erro: {e}")
        input("ENTER...")