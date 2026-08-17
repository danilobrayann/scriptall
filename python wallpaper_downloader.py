import requests
import os

API_KEY = "SUA_API_KEY_AQUI"
HEADERS = {"Authorization": f"Client-ID {API_KEY}"}
SAVE_FOLDER = os.path.join(os.getcwd(), "Wallpapers")

if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

def buscar_wallpapers(query="nature", per_page=5, resolution="3840x2160"):
    url = f"https://api.unsplash.com/search/photos?query={query}&per_page={per_page}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    wallpapers = []
    for i, foto in enumerate(data['results'], 1):
        img_url = foto['urls']['raw'] + f"&w={resolution.split('x')[0]}&h={resolution.split('x')[1]}"
        wallpapers.append((i, foto['alt_description'], img_url))
        print(f"{i}. {foto['alt_description'] or 'Sem descrição'}")

    return wallpapers

def baixar_wallpaper(url, nome):
    resposta = requests.get(url, stream=True)
    caminho = os.path.join(SAVE_FOLDER, nome + ".jpg")
    with open(caminho, 'wb') as f:
        for chunk in resposta.iter_content(1024):
            f.write(chunk)
    print(f"\n✅ {nome} baixado em {SAVE_FOLDER}\n")

while True:
    print("\n=== WALLPAPER DOWNLOADER 4K/8K ===")

    print("""
1 - Buscar e baixar wallpaper
0 - Sair
""")

    opcao = input("Escolha: ")

    if opcao == "1":
        query = input("Tema (nature, space, carros): ")
        resolucao = input("Resolução (3840x2160 ou 7680x4320): ")

        wallpapers = buscar_wallpapers(query=query, per_page=5, resolution=resolucao)

        try:
            escolha = int(input("\nNúmero para baixar: "))
            _, nome, url = wallpapers[escolha-1]
            baixar_wallpaper(url, f"{query}_{escolha}")
        except:
            print("Erro na escolha!")

    elif opcao == "0":
        print("Saindo...")
        break

    else:
        print("Opção inválida")