import yt_dlp

url = input("Cole a URL do YouTube: ")

opcoes = {
    "format": "bestvideo+bestaudio/best",
    "outtmpl": "%(title)s.%(ext)s",
    "merge_output_format": "mp4",
}

try:
    with yt_dlp.YoutubeDL(opcoes) as ydl:
        ydl.download([url])

    print("\nDownload concluído!")

except Exception as e:
    print("\nERRO:")
    print(e)

input("\nPressione ENTER para fechar...")