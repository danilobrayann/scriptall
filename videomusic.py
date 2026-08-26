import os
import sys
import shutil
import subprocess

try:
    import yt_dlp
except ImportError:
    print("yt-dlp não está instalado.")
    print("Instale com:")
    print("python -m pip install -U yt-dlp")
    input("\nPressione ENTER para sair...")
    sys.exit()


# ==========================================================
# YOUTUBE DOWNLOADER
# ==========================================================

DOWNLOAD_FOLDER = os.path.join(
    os.path.expanduser("~"),
    "Downloads",
    "YouTube"
)


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def verificar_ffmpeg():

    if shutil.which("ffmpeg"):
        return True

    print("\n[ERRO] FFmpeg não encontrado.")
    print("\nO FFmpeg é necessário para:")
    print("- MP3")
    print("- juntar vídeo + áudio")
    print("- conversões de formato")

    print("\nInstale o FFmpeg e adicione ao PATH do Windows.")

    input("\nPressione ENTER para continuar...")
    return False


def progresso(d):

    if d["status"] == "downloading":

        porcentagem = d.get("_percent_str", "0%")
        velocidade = d.get("_speed_str", "N/A")
        eta = d.get("_eta_str", "N/A")

        print(
            f"\rBaixando: {porcentagem} | "
            f"Velocidade: {velocidade} | "
            f"ETA: {eta}",
            end=""
        )

    elif d["status"] == "finished":

        print("\nDownload concluído. Processando...")


def baixar_video():

    limpar_tela()

    print("=" * 60)
    print("                 BAIXAR VÍDEO")
    print("=" * 60)

    url = input("\nCole a URL do YouTube: ").strip()

    if not url:
        return

    print("\nEscolha a qualidade:")
    print("1 - Melhor disponível")
    print("2 - 1080p")
    print("3 - 720p")
    print("4 - 480p")
    print("5 - 360p")

    escolha = input("\nOpção: ").strip()

    formatos = {

        "1": "bestvideo+bestaudio/best",

        "2": (
            "bestvideo[height<=1080]+bestaudio/"
            "best[height<=1080]"
        ),

        "3": (
            "bestvideo[height<=720]+bestaudio/"
            "best[height<=720]"
        ),

        "4": (
            "bestvideo[height<=480]+bestaudio/"
            "best[height<=480]"
        ),

        "5": (
            "bestvideo[height<=360]+bestaudio/"
            "best[height<=360]"
        )
    }

    formato = formatos.get(
        escolha,
        formatos["1"]
    )

    os.makedirs(
        DOWNLOAD_FOLDER,
        exist_ok=True
    )

    opcoes = {

        "format": formato,

        "outtmpl": os.path.join(
            DOWNLOAD_FOLDER,
            "%(title)s.%(ext)s"
        ),

        "merge_output_format": "mp4",

        "progress_hooks": [
            progresso
        ],

        "noplaylist": True,

        "windowsfilenames": True,

        "quiet": True,

        "no_warnings": True
    }

    try:

        print("\nIniciando download...\n")

        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])

        print("\n\nVídeo salvo em:")

        print(DOWNLOAD_FOLDER)

    except Exception as erro:

        print("\n\nERRO:")
        print(erro)

    input("\nPressione ENTER para continuar...")


def baixar_mp3():

    limpar_tela()

    print("=" * 60)
    print("                 BAIXAR MÚSICA")
    print("=" * 60)

    if not verificar_ffmpeg():
        return

    url = input("\nCole a URL do YouTube: ").strip()

    if not url:
        return

    pasta = os.path.join(
        DOWNLOAD_FOLDER,
        "Musicas"
    )

    os.makedirs(
        pasta,
        exist_ok=True
    )

    opcoes = {

        "format": "bestaudio/best",

        "outtmpl": os.path.join(
            pasta,
            "%(title)s.%(ext)s"
        ),

        "noplaylist": True,

        "windowsfilenames": True,

        "quiet": True,

        "no_warnings": True,

        "progress_hooks": [
            progresso
        ],

        "postprocessors": [

            {
                "key": "FFmpegExtractAudio",

                "preferredcodec": "mp3",

                "preferredquality": "320"
            }
        ]
    }

    try:

        print("\nBaixando música...\n")

        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])

        print("\n\nMúsica salva em:")
        print(pasta)

    except Exception as erro:

        print("\n\nERRO:")
        print(erro)

    input("\nPressione ENTER para continuar...")


def baixar_playlist():

    limpar_tela()

    print("=" * 60)
    print("                    PLAYLIST")
    print("=" * 60)

    url = input("\nCole a URL da playlist: ").strip()

    if not url:
        return

    print("\nEscolha:")
    print("1 - Vídeos")
    print("2 - MP3")

    escolha = input("\nOpção: ").strip()

    if escolha == "1":

        pasta = os.path.join(
            DOWNLOAD_FOLDER,
            "%(playlist_title)s",
            "%(playlist_index)03d - %(title)s.%(ext)s"
        )

        formato = "bestvideo+bestaudio/best"

        pos = []

    elif escolha == "2":

        if not verificar_ffmpeg():
            return

        pasta = os.path.join(
            DOWNLOAD_FOLDER,
            "%(playlist_title)s",
            "%(playlist_index)03d - %(title)s.%(ext)s"
        )

        formato = "bestaudio/best"

        pos = [

            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320"
            }

        ]

    else:

        print("\nOpção inválida.")
        input("\nPressione ENTER...")
        return

    opcoes = {

        "format": formato,

        "outtmpl": pasta,

        "merge_output_format": "mp4",

        "windowsfilenames": True,

        "quiet": True,

        "no_warnings": True,

        "progress_hooks": [
            progresso
        ],

        "postprocessors": pos
    }

    try:

        print("\nBaixando playlist...\n")

        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])

        print("\nPlaylist concluída!")

    except Exception as erro:

        print("\n\nERRO:")
        print(erro)

    input("\nPressione ENTER para continuar...")


def informacoes():

    limpar_tela()

    print("=" * 60)
    print("               INFORMAÇÕES DO VÍDEO")
    print("=" * 60)

    url = input("\nCole a URL: ").strip()

    if not url:
        return

    opcoes = {
        "quiet": True,
        "no_warnings": True
    }

    try:

        with yt_dlp.YoutubeDL(opcoes) as ydl:

            info = ydl.extract_info(
                url,
                download=False
            )

            print("\nTítulo:")
            print(info.get("title"))

            print("\nCanal:")
            print(info.get("uploader"))

            print("\nDuração:")
            print(info.get("duration"), "segundos")

            print("\nVisualizações:")
            print(info.get("view_count"))

            print("\nFormato:")
            print(info.get("ext"))

    except Exception as erro:

        print("\nERRO:")
        print(erro)

    input("\nPressione ENTER para continuar...")


def menu():

    while True:

        limpar_tela()

        print("""
╔══════════════════════════════════════════════════════════╗
║                 YOUTUBE DOWNLOADER                      ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  1  - Baixar vídeo                                      ║
║  2  - Baixar música MP3                                 ║
║  3  - Baixar playlist                                   ║
║  4  - Informações do vídeo                              ║
║                                                          ║
║  0  - Sair                                               ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """)

        print(
            f"Pasta de download:\n{DOWNLOAD_FOLDER}"
        )

        escolha = input("\nEscolha uma opção: ").strip()

        if escolha == "1":
            baixar_video()

        elif escolha == "2":
            baixar_mp3()

        elif escolha == "3":
            baixar_playlist()

        elif escolha == "4":
            informacoes()

        elif escolha == "0":

            print("\nAté mais! 👋")
            break

        else:

            print("\nOpção inválida.")
            input("Pressione ENTER...")


if __name__ == "__main__":

    try:
        menu()

    except KeyboardInterrupt:

        print("\n\nPrograma encerrado.")

    except Exception as erro:

        print("\nERRO FATAL:")
        print(erro)

        input(
            "\nPressione ENTER para fechar..."
        )