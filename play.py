import yt_dlp
import subprocess
import threading
import os
import sys
import time


# Variável global do player
processo_player = None


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def buscar_musica(busca):
    """
    Pesquisa a música no YouTube.
    Retorna informações da primeira música encontrada.
    """

    opcoes = {
        "quiet": True,
        "no_warnings": True,
        "format": "bestaudio/best",
        "default_search": "ytsearch1",
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:

            resultado = ydl.extract_info(
                f"ytsearch1:{busca}",
                download=False
            )

            if not resultado:
                return None

            entries = resultado.get("entries")

            if not entries:
                return None

            video = entries[0]

            return {
                "titulo": video.get("title", "Desconhecido"),
                "url": video.get("url"),
                "duracao": video.get("duration"),
                "canal": video.get("uploader", "Desconhecido"),
            }

    except Exception as erro:
        print(f"\nErro ao buscar música: {erro}")
        return None


def parar_musica():
    global processo_player

    if processo_player is not None:

        try:

            processo_player.terminate()

            try:
                processo_player.wait(timeout=2)

            except subprocess.TimeoutExpired:
                processo_player.kill()

        except Exception:
            pass

        processo_player = None


def tocar_musica(url):
    """
    Reproduz usando FFplay.
    """

    global processo_player

    parar_musica()

    try:

        processo_player = subprocess.Popen(
            [
                "ffplay",
                "-nodisp",
                "-autoexit",
                "-loglevel",
                "error",
                url
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return True

    except FileNotFoundError:

        print("\n❌ FFmpeg não foi encontrado.")
        print("Instale o FFmpeg e coloque no PATH.")

        return False

    except Exception as erro:

        print(f"\n❌ Erro ao iniciar player: {erro}")

        return False


def formatar_duracao(segundos):

    if not segundos:
        return "Desconhecida"

    minutos = segundos // 60
    segundos = segundos % 60

    return f"{minutos}:{segundos:02d}"


def menu():
    print("\n" + "=" * 55)
    print("              🎵 PLAYER YOUTUBE")
    print("=" * 55)
    print("\nDigite o nome de uma música.")
    print("\nComandos especiais:")
    print("sair   - Fechar programa")
    print("parar  - Parar música")
    print("nova   - Buscar outra música")
    print("=" * 55)


def main():

    global processo_player

    print("\nIniciando Player de Música...\n")

    # Verifica se FFplay existe
    try:

        subprocess.run(
            ["ffplay", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    except FileNotFoundError:

        print("❌ FFplay não foi encontrado.")
        print("\nVocê precisa instalar o FFmpeg.")

        input("\nPressione ENTER para sair...")
        return

    try:

        while True:

            menu()

            busca = input("\n🔎 Música: ").strip()

            if not busca:
                print("\nDigite o nome de uma música.")
                time.sleep(1)
                continue

            if busca.lower() == "sair":

                parar_musica()

                print("\n👋 Player encerrado.")
                break

            if busca.lower() == "parar":

                parar_musica()

                print("\n⏹ Música parada.")

                input("\nPressione ENTER...")
                continue

            print("\n🔎 Procurando no YouTube...")

            musica = buscar_musica(busca)

            if musica is None:

                print("\n❌ Nenhuma música encontrada.")

                input("\nPressione ENTER para continuar...")
                continue

            if not musica["url"]:

                print("\n❌ Não foi possível obter o áudio.")

                input("\nPressione ENTER para continuar...")
                continue

            limpar_tela()

            print("\n" + "=" * 55)
            print("🎵 TOCANDO AGORA")
            print("=" * 55)

            print(f"\n🎧 Música: {musica['titulo']}")
            print(f"👤 Canal: {musica['canal']}")
            print(
                f"⏱ Duração: "
                f"{formatar_duracao(musica['duracao'])}"
            )

            print("\n▶ Iniciando áudio...")

            sucesso = tocar_musica(musica["url"])

            if not sucesso:

                input("\nPressione ENTER para continuar...")
                continue

            print("\n" + "-" * 55)
            print("Comandos:")
            print("N = Nova música")
            print("P = Parar música")
            print("S = Sair")
            print("-" * 55)

            while True:

                comando = input("\nComando: ").strip().lower()

                if comando == "n":

                    parar_musica()
                    break

                elif comando == "p":

                    parar_musica()

                    print("\n⏹ Música parada.")

                elif comando == "s":

                    parar_musica()

                    print("\n👋 Encerrando player...")
                    return

                else:

                    print(
                        "\nComando inválido. "
                        "Use N, P ou S."
                    )

    except KeyboardInterrupt:

        parar_musica()

        print("\n\nPlayer encerrado.")

    except Exception as erro:

        parar_musica()

        print("\n❌ Ocorreu um erro inesperado:")
        print(erro)

        input("\nPressione ENTER para fechar...")


if __name__ == "__main__":
    main()