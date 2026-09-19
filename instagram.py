import os
import sys
import yt_dlp


PASTA_DOWNLOADS = "downloads_instagram"


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def baixar_instagram(url):
    os.makedirs(PASTA_DOWNLOADS, exist_ok=True)

    opcoes = {
        "outtmpl": os.path.join(
            PASTA_DOWNLOADS,
            "%(uploader)s_%(id)s.%(ext)s"
        ),

        # Melhor qualidade disponível
        "format": "bestvideo+bestaudio/best",

        # Junta vídeo + áudio quando necessário
        "merge_output_format": "mp4",

        "quiet": False,
        "no_warnings": False,

        # Alguns conteúdos podem exigir cabeçalho de navegador
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/140.0.0.0 Safari/537.36"
            )
        }
    }

    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            print("\nBaixando...\n")
            ydl.download([url])

        print("\n✅ Download concluído!")
        print(f"📁 Pasta: {os.path.abspath(PASTA_DOWNLOADS)}")

    except Exception as erro:
        print("\n❌ Não foi possível baixar.")
        print(f"Erro: {erro}")


def main():
    limpar_tela()

    print("=" * 50)
    print("       INSTAGRAM DOWNLOADER - PYTHON")
    print("=" * 50)

    print("\nCole o link do Instagram.")
    print("Exemplo:")
    print("https://www.instagram.com/reel/XXXXXXXX/")
    print()

    url = input("URL: ").strip()

    if not url:
        print("❌ Você não informou uma URL.")
        input("\nPressione ENTER para sair...")
        return

    if "instagram.com" not in url:
        print("❌ URL não parece ser do Instagram.")
        input("\nPressione ENTER para sair...")
        return

    baixar_instagram(url)

    input("\nPressione ENTER para sair...")


if __name__ == "__main__":
    main()


