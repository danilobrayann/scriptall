import os
import threading
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

try:
    import customtkinter as ctk
except ImportError:
    raise SystemExit(
        "CustomTkinter não instalado.\n"
        "Execute: python -m pip install customtkinter yt-dlp"
    )

try:
    import yt_dlp
except ImportError:
    raise SystemExit(
        "yt-dlp não instalado.\n"
        "Execute: python -m pip install -U yt-dlp"
    )


# ============================================================
# IDENTIDADE VISUAL
# ============================================================

BG = "#0b0f14"
SIDEBAR = "#10161f"
CARD = "#151d27"
CARD_2 = "#111820"
ACCENT = "#00c2ff"
ACCENT_HOVER = "#009bd0"
TEXT = "#f4f7fb"
MUTED = "#8b98a8"
SUCCESS = "#24d17e"
DANGER = "#ff5c6c"

# ============================================================
# CONFIGURAÇÃO
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

DOWNLOAD_FOLDER = os.path.join(
    os.path.expanduser("~"),
    "Downloads",
    "YouTube"
)


class YouTubeDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("VideoMusic Pro")
        self.geometry("1180x760")
        self.minsize(980, 680)
        self.configure(fg_color=BG)

        self.url_var = tk.StringVar()
        self.quality_var = tk.StringVar(value="1080p")
        self.status_var = tk.StringVar(value="Pronto para baixar.")
        self.progress_var = tk.DoubleVar(value=0)

        self.criar_interface()

    # ========================================================
    # INTERFACE
    # ========================================================

    def criar_interface(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------- SIDEBAR ----------------
        sidebar = ctk.CTkFrame(
            self,
            width=245,
            corner_radius=0,
            fg_color=SIDEBAR
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        titulo = ctk.CTkLabel(
            sidebar,
            text="▶  YouTube\n    Downloader",
            font=ctk.CTkFont(size=24, weight="bold"),
            justify="left"
        )
        titulo.pack(padx=25, pady=(35, 40), anchor="w")

        self.btn_video = ctk.CTkButton(
            sidebar,
            text="▸  VÍDEO",
            height=45,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            command=lambda: self.selecionar_aba("video")
        )
        self.btn_video.pack(fill="x", padx=20, pady=6)

        self.btn_mp3 = ctk.CTkButton(
            sidebar,
            text="♪  MP3",
            height=45,
            fg_color=CARD,
            hover_color="#202b38",
            command=lambda: self.selecionar_aba("mp3")
        )
        self.btn_mp3.pack(fill="x", padx=20, pady=6)

        self.btn_playlist = ctk.CTkButton(
            sidebar,
            text="≡  PLAYLIST",
            height=45,
            fg_color=CARD,
            hover_color="#202b38",
            command=lambda: self.selecionar_aba("playlist")
        )
        self.btn_playlist.pack(fill="x", padx=20, pady=6)

        self.btn_info = ctk.CTkButton(
            sidebar,
            text="ⓘ  INFORMAÇÕES",
            height=45,
            fg_color=CARD,
            hover_color="#202b38",
            command=lambda: self.selecionar_aba("info")
        )
        self.btn_info.pack(fill="x", padx=20, pady=6)

        ctk.CTkLabel(
            sidebar,
            text="",
        ).pack(expand=True)

        ctk.CTkButton(
            sidebar,
            text="⌂  ABRIR DOWNLOADS",
            height=40,
            fg_color="transparent",
            border_width=1,
            command=self.abrir_pasta
        ).pack(fill="x", padx=20, pady=(10, 20))

        # ---------------- ÁREA PRINCIPAL ----------------
        self.main = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=BG
        )
        self.main.grid(row=0, column=1, sticky="nsew", padx=30, pady=25)
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(2, weight=1)

        self.header = ctk.CTkLabel(
            self.main,
            text="Baixar vídeo",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        self.header.grid(row=0, column=0, sticky="w", pady=(5, 2))

        self.subtitle = ctk.CTkLabel(
            self.main,
            text="Baixe vídeos, músicas e playlists com rapidez.",
            text_color=MUTED,
            font=ctk.CTkFont(size=13)
        )
        self.subtitle.grid(row=0, column=0, sticky="w", pady=(42, 25))

        # URL
        url_frame = ctk.CTkFrame(self.main, fg_color=CARD, corner_radius=14)
        url_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        url_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            url_frame,
            text="URL do YouTube",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(15, 5))

        self.url_entry = ctk.CTkEntry(
            url_frame,
            textvariable=self.url_var,
            height=46,
            corner_radius=10,
            border_width=1,
            border_color="#263342",
            placeholder_text="Cole aqui o link do YouTube..."
        )
        self.url_entry.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=18,
            pady=(0, 18)
        )

        # Conteúdo
        self.content = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )
        self.content.grid(row=2, column=0, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)

        self.criar_aba_video()

        location_label = ctk.CTkLabel(
            self.main,
            text=f"📁  {DOWNLOAD_FOLDER}",
            text_color=MUTED,
            anchor="w",
            font=ctk.CTkFont(size=12)
        )
        location_label.grid(row=3, column=0, sticky="w", pady=(2, 4))

        # Status
        status_frame = ctk.CTkFrame(self.main, height=95, fg_color=CARD, corner_radius=14)
        status_frame.grid(
            row=4,
            column=0,
            sticky="ew",
            pady=(8, 0)
        )
        status_frame.grid_columnconfigure(0, weight=1)

        self.progress = ctk.CTkProgressBar(
            status_frame,
            variable=self.progress_var,
            height=10,
            progress_color=ACCENT
        )
        self.progress.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=18,
            pady=(18, 8)
        )

        self.status_label = ctk.CTkLabel(
            status_frame,
            textvariable=self.status_var,
            anchor="w"
        )
        self.status_label.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=18,
            pady=(0, 15)
        )

    # ========================================================
    # ABAS
    # ========================================================

    def limpar_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def selecionar_aba(self, aba):
        self.limpar_content()

        if aba == "video":
            self.header.configure(text="Baixar vídeo")
            self.criar_aba_video()

        elif aba == "mp3":
            self.header.configure(text="Baixar música MP3")
            self.criar_aba_mp3()

        elif aba == "playlist":
            self.header.configure(text="Baixar playlist")
            self.criar_aba_playlist()

        elif aba == "info":
            self.header.configure(text="Informações do vídeo")
            self.criar_aba_info()

    def criar_aba_video(self):
        frame = ctk.CTkFrame(self.content, fg_color=CARD, corner_radius=14)
        frame.grid(row=0, column=0, sticky="ew", pady=10)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame,
            text="Qualidade",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(18, 8))

        self.quality_menu = ctk.CTkOptionMenu(
            frame,
            values=[
                "Melhor disponível",
                "1080p",
                "720p",
                "480p",
                "360p"
            ],
            variable=self.quality_var,
            height=42
        )
        self.quality_menu.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=18,
            pady=(0, 18)
        )

        ctk.CTkButton(
            self.content,
            text="⬇  BAIXAR VÍDEO",
            height=52,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.iniciar_video
        ).grid(row=1, column=0, sticky="ew", pady=15)

    def criar_aba_mp3(self):
        card = ctk.CTkFrame(self.content, fg_color=CARD, corner_radius=14)
        card.grid(row=0, column=0, sticky="ew", pady=10)

        ctk.CTkLabel(
            card,
            text="🎵 MP3 em alta qualidade",
            font=ctk.CTkFont(size=17, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 8))

        ctk.CTkLabel(
            card,
            text="O áudio será convertido para MP3 320 kbps usando FFmpeg.",
            text_color="gray"
        ).pack(anchor="w", padx=20, pady=(0, 20))

        ctk.CTkButton(
            self.content,
            text="♪  BAIXAR MP3",
            height=52,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.iniciar_mp3
        ).grid(row=1, column=0, sticky="ew", pady=15)

    def criar_aba_playlist(self):
        card = ctk.CTkFrame(self.content, fg_color=CARD, corner_radius=14)
        card.grid(row=0, column=0, sticky="ew", pady=10)

        ctk.CTkLabel(
            card,
            text="Tipo de download",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 8))

        self.playlist_tipo = ctk.CTkOptionMenu(
            card,
            values=["Vídeos", "MP3"],
            height=42
        )
        self.playlist_tipo.pack(fill="x", padx=20, pady=(0, 20))

        ctk.CTkButton(
            self.content,
            text="≡  BAIXAR PLAYLIST",
            height=52,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.iniciar_playlist
        ).grid(row=1, column=0, sticky="ew", pady=15)

    def criar_aba_info(self):
        ctk.CTkButton(
            self.content,
            text="⌕  BUSCAR INFORMAÇÕES",
            height=52,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.iniciar_info
        ).grid(row=0, column=0, sticky="ew", pady=15)

        self.info_box = ctk.CTkTextbox(
            self.content,
            height=260,
            fg_color=CARD_2,
            border_width=1,
            border_color="#263342",
            corner_radius=12
        )
        self.info_box.grid(row=1, column=0, sticky="nsew", pady=10)

    # ========================================================
    # DOWNLOAD
    # ========================================================

    def verificar_ffmpeg(self):
        if shutil.which("ffmpeg"):
            return True

        messagebox.showerror(
            "FFmpeg não encontrado",
            "O FFmpeg é necessário para baixar/converter MP3.\n\n"
            "Instale o FFmpeg e adicione-o ao PATH do Windows."
        )
        return False

    def obter_formato(self):
        formatos = {
            "Melhor disponível": "bestvideo+bestaudio/best",
            "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
            "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
            "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
            "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]"
        }
        return formatos.get(
            self.quality_var.get(),
            formatos["Melhor disponível"]
        )

    def hook_progresso(self, d):
        if d["status"] == "downloading":
            porcentagem = d.get("_percent_str", "0%").strip()
            velocidade = d.get("_speed_str", "N/A")
            eta = d.get("_eta_str", "N/A")

            try:
                valor = float(
                    porcentagem.replace("%", "").replace(",", ".")
                ) / 100
            except Exception:
                valor = 0

            self.after(
                0,
                lambda: self.atualizar_progresso(
                    valor,
                    f"Baixando: {porcentagem}  •  "
                    f"{velocidade}  •  ETA: {eta}"
                )
            )

        elif d["status"] == "finished":
            self.after(
                0,
                lambda: self.atualizar_progresso(
                    1,
                    "Download concluído. Processando..."
                )
            )

    def atualizar_progresso(self, valor, texto):
        self.progress_var.set(valor)
        self.status_var.set(texto)

    def validar_url(self):
        url = self.url_var.get().strip()

        if not url:
            messagebox.showwarning(
                "URL vazia",
                "Cole uma URL do YouTube primeiro."
            )
            return None

        return url

    def iniciar_video(self):
        url = self.validar_url()
        if not url:
            return

        threading.Thread(
            target=self.baixar_video,
            args=(url,),
            daemon=True
        ).start()

    def baixar_video(self, url):
        os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

        self.after(
            0,
            lambda: self.atualizar_progresso(
                0,
                "Iniciando download..."
            )
        )

        opcoes = {
            "format": self.obter_formato(),
            "outtmpl": os.path.join(
                DOWNLOAD_FOLDER,
                "%(title)s.%(ext)s"
            ),
            "merge_output_format": "mp4",
            "progress_hooks": [self.hook_progresso],
            "noplaylist": True,
            "windowsfilenames": True,
            "quiet": True,
            "no_warnings": True
        }

        try:
            with yt_dlp.YoutubeDL(opcoes) as ydl:
                ydl.download([url])

            self.after(
                0,
                lambda: self.download_sucesso(
                    f"Vídeo salvo em:\n{DOWNLOAD_FOLDER}"
                )
            )

        except Exception as erro:
            self.after(
                0,
                lambda: self.erro(str(erro))
            )

    def iniciar_mp3(self):
        url = self.validar_url()
        if not url:
            return

        if not self.verificar_ffmpeg():
            return

        threading.Thread(
            target=self.baixar_mp3,
            args=(url,),
            daemon=True
        ).start()

    def baixar_mp3(self, url):
        pasta = os.path.join(
            DOWNLOAD_FOLDER,
            "Musicas"
        )
        os.makedirs(pasta, exist_ok=True)

        self.after(
            0,
            lambda: self.atualizar_progresso(
                0,
                "Baixando música..."
            )
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
            "progress_hooks": [self.hook_progresso],
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320"
                }
            ]
        }

        try:
            with yt_dlp.YoutubeDL(opcoes) as ydl:
                ydl.download([url])

            self.after(
                0,
                lambda: self.download_sucesso(
                    f"Música salva em:\n{pasta}"
                )
            )

        except Exception as erro:
            self.after(
                0,
                lambda: self.erro(str(erro))
            )

    def iniciar_playlist(self):
        url = self.validar_url()
        if not url:
            return

        tipo = self.playlist_tipo.get()

        if tipo == "MP3" and not self.verificar_ffmpeg():
            return

        threading.Thread(
            target=self.baixar_playlist,
            args=(url, tipo),
            daemon=True
        ).start()

    def baixar_playlist(self, url, tipo):
        if tipo == "Vídeos":
            pasta = os.path.join(
                DOWNLOAD_FOLDER,
                "%(playlist_title)s",
                "%(playlist_index)03d - %(title)s.%(ext)s"
            )
            formato = "bestvideo+bestaudio/best"
            postprocessors = []
        else:
            pasta = os.path.join(
                DOWNLOAD_FOLDER,
                "%(playlist_title)s",
                "%(playlist_index)03d - %(title)s.%(ext)s"
            )
            formato = "bestaudio/best"
            postprocessors = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320"
                }
            ]

        self.after(
            0,
            lambda: self.atualizar_progresso(
                0,
                "Baixando playlist..."
            )
        )

        opcoes = {
            "format": formato,
            "outtmpl": pasta,
            "merge_output_format": "mp4",
            "windowsfilenames": True,
            "quiet": True,
            "no_warnings": True,
            "progress_hooks": [self.hook_progresso],
            "postprocessors": postprocessors
        }

        try:
            with yt_dlp.YoutubeDL(opcoes) as ydl:
                ydl.download([url])

            self.after(
                0,
                lambda: self.download_sucesso(
                    "Playlist concluída com sucesso!"
                )
            )

        except Exception as erro:
            self.after(
                0,
                lambda: self.erro(str(erro))
            )

    # ========================================================
    # INFORMAÇÕES
    # ========================================================

    def iniciar_info(self):
        url = self.validar_url()
        if not url:
            return

        threading.Thread(
            target=self.buscar_info,
            args=(url,),
            daemon=True
        ).start()

    def buscar_info(self, url):
        self.after(
            0,
            lambda: self.status_var.set(
                "Buscando informações..."
            )
        )

        try:
            opcoes = {
                "quiet": True,
                "no_warnings": True
            }

            with yt_dlp.YoutubeDL(opcoes) as ydl:
                info = ydl.extract_info(
                    url,
                    download=False
                )

            duracao = info.get("duration")
            if duracao:
                minutos = duracao // 60
                segundos = duracao % 60
                duracao_texto = f"{minutos}:{segundos:02d}"
            else:
                duracao_texto = "Não informado"

            texto = (
                f"TÍTULO\n"
                f"{info.get('title', 'Não informado')}\n\n"
                f"CANAL\n"
                f"{info.get('uploader', 'Não informado')}\n\n"
                f"DURAÇÃO\n"
                f"{duracao_texto}\n\n"
                f"VISUALIZAÇÕES\n"
                f"{info.get('view_count', 'Não informado')}\n\n"
                f"FORMATO\n"
                f"{info.get('ext', 'Não informado')}\n"
            )

            self.after(
                0,
                lambda: self.mostrar_info(texto)
            )

        except Exception as erro:
            self.after(
                0,
                lambda: self.erro(str(erro))
            )

    def mostrar_info(self, texto):
        if hasattr(self, "info_box"):
            self.info_box.delete("1.0", "end")
            self.info_box.insert("1.0", texto)

        self.status_var.set("Informações carregadas.")

    # ========================================================
    # UTILIDADES
    # ========================================================

    def download_sucesso(self, mensagem):
        self.progress_var.set(1)
        self.status_var.set("✓ Download concluído.")
        messagebox.showinfo(
            "Concluído",
            mensagem
        )

    def erro(self, mensagem):
        self.status_var.set("✕ Ocorreu um erro.")
        messagebox.showerror(
            "Erro",
            mensagem
        )

    def abrir_pasta(self):
        os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

        try:
            os.startfile(DOWNLOAD_FOLDER)
        except Exception:
            messagebox.showinfo(
                "Pasta de downloads",
                DOWNLOAD_FOLDER
            )


if __name__ == "__main__":
    app = YouTubeDownloader()
    app.mainloop()
