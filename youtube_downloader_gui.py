#!/usr/bin/env python3
"""
YTD - YouTube Downloader
Interface gráfica moderna para download de vídeos do YouTube
Design baseado em mockups com tema neon green
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp
import os
import sys
import threading
from pathlib import Path
from PIL import Image, ImageTk
import urllib.request
import io

# Configurar tema
ctk.set_appearance_mode("dark")

def resource_path(relative_path):
    """Obter caminho absoluto para recursos (funciona no PyInstaller)"""
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # No modo desenvolvimento, usar o diretório do arquivo atual
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

# Corrigir ícone na barra de tarefas (Windows)
try:
    import ctypes
    myappid = 'ytd.downloader.gui.1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass

class YouTubeDownloaderGUI:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("YTD - YouTube Downloader")
        self.window.geometry("800x750")
        self.window.resizable(False, False)
        
        # Configurar ícone da janela
        try:
            # Tentar carregar .ico primeiro (melhor para Windows)
            icon_path = resource_path("fiveicon.ico")
            if os.path.exists(icon_path):
                self.window.iconbitmap(icon_path)
            else:
                # Fallback para PNG
                icon_path = resource_path("fiveicon.png")
                if os.path.exists(icon_path):
                    icon_image = tk.PhotoImage(file=icon_path)
                    self.window.iconphoto(False, icon_image)
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")
        
        # Variáveis
        self.video_info = None
        self.download_path = str(Path.home() / "Downloads")
        self.is_downloading = False
        self.playlist_videos = []
        
        # Cores do novo design
        self.color_neon = "#C8FF00"  # Verde neon
        self.color_bg = "#212121"     # Fundo principal
        self.color_container = "#121212"  # Containers
        self.color_text = "#FFFFFF"   # Texto branco
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar interface do usuário"""
        
        # Configurar cor de fundo
        self.window.configure(fg_color=self.color_bg)
        
        # Logo Principal "YTD"
        try:
            logo_path = resource_path("YTD.png")
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                # Manter proporção
                ratio = logo_img.width / logo_img.height
                new_height = 30  # Reduzido de 60 para 40
                new_width = int(new_height * ratio)
                
                logo_ctk = ctk.CTkImage(
                    light_image=logo_img,
                    dark_image=logo_img,
                    size=(new_width, new_height)
                )
                title_label = ctk.CTkLabel(
                    self.window,
                    text="",
                    image=logo_ctk
                )
            else:
                title_label = ctk.CTkLabel(
                    self.window,
                    text="YTD",
                    font=("Montserrat Alternates", 48, "bold"),
                    text_color=self.color_text
                )
        except Exception as e:
            print(f"Erro ao carregar logo: {e}")
            title_label = ctk.CTkLabel(
                self.window,
                text="YTD",
                font=("Montserrat Alternates", 48, "bold"),
                text_color=self.color_text
            )
        title_label.pack(pady=(30, 20))
        
        # Campo de entrada URL
        self.url_entry = ctk.CTkEntry(
            self.window,
            height=50,
            font=("Montserrat", 12),
            placeholder_text="Cole seu link",
            placeholder_text_color="#666666",
            border_color=self.color_neon,
            border_width=2,
            corner_radius=0,  # Sem arredondamento
            fg_color=self.color_bg,
            text_color=self.color_text
        )
        self.url_entry.pack(fill="x", padx=50, pady=(0, 15))
        
        # Botão Analisar
        self.analyze_btn = ctk.CTkButton(
            self.window,
            text="Analisar link",
            command=self.analyze_url,
            height=50,
            font=("Montserrat", 14, "bold"),
            fg_color=self.color_neon,
            hover_color="#a0cc00",
            text_color="#000000",
            corner_radius=0
        )
        self.analyze_btn.pack(fill="x", padx=50, pady=(0, 15))
        
        # Frame de pasta (sempre visível no topo)
        folder_frame = ctk.CTkFrame(
            self.window,
            fg_color=self.color_container,
            corner_radius=0,
            height=50
        )
        folder_frame.pack(fill="x", padx=50, pady=(0, 20))
        folder_frame.pack_propagate(False)
        
        self.folder_label = ctk.CTkLabel(
            folder_frame,
            text=f"PASTA: {self.download_path}",
            font=("Montserrat", 10),
            text_color=self.color_neon,
            anchor="w"
        )
        self.folder_label.pack(side="left", fill="both", expand=True, padx=15)
        
        self.folder_btn = ctk.CTkButton(
            folder_frame,
            text="Alterar pasta",
            command=self.choose_folder,
            height=30,
            width=120,
            font=("Montserrat", 10, "bold"),
            fg_color=self.color_neon,
            hover_color="#a0cc00",
            text_color="#000000",
            corner_radius=0
        )
        self.folder_btn.pack(side="right", padx=10, pady=10)
        
        # Frame de informações (container principal)
        self.info_container = ctk.CTkFrame(
            self.window,
            fg_color=self.color_bg,  # Alterado para cor do fundo da janela
            corner_radius=0,
            height=380  # Aumentado de 280 para 320
        )
        self.info_container.pack(fill="x", padx=50, pady=(0, 20))
        self.info_container.pack_propagate(False)  # Manter altura fixa
        
        # Conteúdo do container (horizontal: thumbnail + info)
        self.content_frame = ctk.CTkFrame(self.info_container, fg_color="transparent")
        # self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)  # Removido pack inicial
        
        # Logo inicial
        self.logo_label = ctk.CTkLabel(
            self.info_container,
            text="",
            fg_color="transparent"
        )
        self.logo_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Carregar logo
        self._load_initial_logo()
        
        # Frame esquerdo para thumbnail
        self.thumbnail_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.color_bg,
            corner_radius=0,
            width=300,  # Aumentado de 280
            height=170  # Aumentado de 160
        )
        self.thumbnail_frame.pack(side="left", padx=(0, 20))
        self.thumbnail_frame.pack_propagate(False)
        
        self.thumbnail_label = ctk.CTkLabel(
            self.thumbnail_frame,
            text="",
            width=280,  # Aumentado de 260
            height=150  # Aumentado de 140
        )
        self.thumbnail_label.pack(expand=True)
        
        # Frame direito para informações
        self.text_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.text_frame.pack(side="left", fill="both", expand=True)
        
        self.info_label = ctk.CTkLabel(
            self.text_frame,
            text="",
            font=("Montserrat", 11),
            text_color=self.color_neon,
            justify="left",
            anchor="nw"
        )
        self.info_label.pack(fill="both", expand=True)
        
        # Frame scrollável para lista de vídeos da playlist
        self.playlist_scroll_frame = ctk.CTkScrollableFrame(
            self.info_container,
            fg_color=self.color_bg,
            height=150,  # Alterado para 150
            corner_radius=0
        )
        
        # Frame de botões de controle de playlist
        self.playlist_controls_frame = ctk.CTkFrame(
            self.window,
            fg_color="transparent"
        )
        
        # Botões de seleção
        self.select_all_btn = ctk.CTkButton(
            self.playlist_controls_frame,
            text="Marcar todos",
            command=self.select_all_videos,
            height=40,
            width=140,
            font=("Montserrat", 11, "bold"),
            fg_color=self.color_neon,
            hover_color="#a0cc00",
            text_color="#000000",
            corner_radius=0
        )
        self.select_all_btn.pack(side="left", padx=5)
        
        self.deselect_all_btn = ctk.CTkButton(
            self.playlist_controls_frame,
            text="Desmarcar todoss",
            command=self.deselect_all_videos,
            height=40,
            width=140,
            font=("Montserrat", 11, "bold"),
            fg_color=self.color_neon,
            hover_color="#a0cc00",
            text_color="#000000",
            corner_radius=0
        )
        self.deselect_all_btn.pack(side="left", padx=5)
        
        # Botões MP4/MP3 para playlist
        self.mp4_playlist_btn = ctk.CTkButton(
            self.playlist_controls_frame,
            text="Baixar MP4",
            command=lambda: self.start_download("video"),
            height=40,
            width=140,
            font=("Montserrat", 11, "bold"),
            fg_color=self.color_neon,
            hover_color="#a0cc00",
            text_color="#000000",
            corner_radius=0
        )
        self.mp4_playlist_btn.pack(side="left", padx=5)
        
        self.mp3_playlist_btn = ctk.CTkButton(
            self.playlist_controls_frame,
            text="Baixar MP3",
            command=lambda: self.start_download("audio"),
            height=40,
            width=140,
            font=("Montserrat", 11, "bold"),
            fg_color=self.color_neon,
            hover_color="#a0cc00",
            text_color="#000000",
            corner_radius=0
        )
        self.mp3_playlist_btn.pack(side="left", padx=5)
        
        # Frame de botões de download (vídeo único)
        self.download_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        # self.download_frame.pack(pady=(0, 20))  # Removido pack inicial
        
        self.mp4_btn = ctk.CTkButton(
            self.download_frame,
            text="Baixar MP4",
            command=lambda: self.start_download("video"),
            height=50,
            width=180,
            font=("Montserrat", 13, "bold"),
            fg_color=self.color_neon,
            hover_color="#a0cc00",
            text_color="#000000",
            corner_radius=0,
            state="disabled"
        )
        self.mp4_btn.pack(side="left", padx=10)
        
        self.mp3_btn = ctk.CTkButton(
            self.download_frame,
            text="Baixar MP3",
            command=lambda: self.start_download("audio"),
            height=50,
            width=180,
            font=("Montserrat", 13, "bold"),
            fg_color=self.color_neon,
            hover_color="#a0cc00",
            text_color="#000000",
            corner_radius=0,
            state="disabled"
        )
        self.mp3_btn.pack(side="left", padx=10)
        
        # Barra de progresso
        self.progress_bar = ctk.CTkProgressBar(
            self.window,
            width=700,
            height=20,
            progress_color=self.color_neon,
            fg_color=self.color_container,
            corner_radius=0
        )
        
        # Label de status
        self.status_label = ctk.CTkLabel(
            self.window,
            text="",
            font=("Montserrat", 10),
            text_color=self.color_neon
        )
    
    def select_all_videos(self):
        """Marcar todos os vídeos"""
        for checkbox_var in self.playlist_videos:
            checkbox_var.set(True)
    
    def deselect_all_videos(self):
        """Desmarcar todos os vídeos"""
        for checkbox_var in self.playlist_videos:
            checkbox_var.set(False)
        
    def _load_initial_logo(self):
        """Carregar logo inicial"""
        try:
            image_path = resource_path("Group 3.png")
            if os.path.exists(image_path):
                image = Image.open(image_path)
                # Redimensionar mantendo proporção (altura 200px)
                ratio = image.width / image.height
                new_height = 200
                new_width = int(new_height * ratio)
                
                image = ctk.CTkImage(
                    light_image=image,
                    dark_image=image,
                    size=(new_width, new_height)
                )
                self.logo_label.configure(image=image)
        except Exception as e:
            print(f"Erro ao carregar logo: {e}")

    def choose_folder(self):
        """Escolher pasta de download"""
        folder = filedialog.askdirectory(initialdir=self.download_path)
        if folder:
            self.download_path = folder
            self.folder_label.configure(text=f"PASTA: {self.download_path}")
    
    def analyze_url(self):
        """Analisar URL e obter informações"""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showwarning("Aviso", "Por favor, cole um link do YouTube!")
            return
        
        if 'youtube.com' not in url and 'youtu.be' not in url:
            messagebox.showerror("Erro", "Link inválido! Use um link do YouTube.")
            return
        
        # Desabilitar botão durante análise
        self.analyze_btn.configure(state="disabled", text="Analisando...")
        self.info_label.configure(text="Analisando link, aguarde...")
        
        # Executar em thread separada
        thread = threading.Thread(target=self._analyze_url_thread, args=(url,))
        thread.daemon = True
        thread.start()
    
    def _analyze_url_thread(self, url):
        """Thread para análise de URL"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': 'in_playlist'
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.video_info = ydl.extract_info(url, download=False)
            
            # Se for playlist, pegar thumbnail do primeiro vídeo
            if 'entries' in self.video_info:
                entries = list(self.video_info.get('entries', []))
                if entries and entries[0]:
                    first_video_url = entries[0].get('url') or f"https://www.youtube.com/watch?v={entries[0].get('id')}"
                    try:
                        ydl_opts_single = {'quiet': True, 'no_warnings': True}
                        with yt_dlp.YoutubeDL(ydl_opts_single) as ydl_single:
                            first_video_info = ydl_single.extract_info(first_video_url, download=False)
                            self.video_info['entries'][0]['thumbnail'] = first_video_info.get('thumbnail')
                    except:
                        pass
            
            # Atualizar UI
            self.window.after(0, self._display_info)
            
        except Exception as e:
            self.window.after(0, lambda: self._show_error(str(e)))
    
    def _display_info(self):
        """Exibir informações do vídeo/playlist"""
        self.analyze_btn.configure(state="normal", text="Analisar link")
        
        # Alterar cor do container para destacar
        self.info_container.configure(fg_color=self.color_container)
        
        # Esconder logo e mostrar conteúdo
        self.logo_label.place_forget()
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        if not self.video_info:
            return
        
        is_playlist = 'entries' in self.video_info
        
        # Carregar thumbnail
        thumbnail_url = None
        if is_playlist:
            entries = list(self.video_info.get('entries', []))
            if entries and entries[0]:
                thumbnail_url = entries[0].get('thumbnail')
        else:
            thumbnail_url = self.video_info.get('thumbnail')
        
        # Baixar e exibir thumbnail
        if thumbnail_url:
            try:
                with urllib.request.urlopen(thumbnail_url) as url:
                    image_data = url.read()
                image = Image.open(io.BytesIO(image_data))
                image.thumbnail((320, 180), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.thumbnail_label.configure(image=photo, text="")
                self.thumbnail_label.image = photo
            except:
                self.thumbnail_label.configure(text="Sem thumbnail", image="")
        else:
            self.thumbnail_label.configure(text="Sem thumbnail", image="")
        
        if is_playlist:
            # Informações da playlist
            title = self.video_info.get('title', 'Playlist')
            video_count = len(list(self.video_info.get('entries', [])))
            uploader = self.video_info.get('uploader', 'Desconhecido')
            
            info_text = f"Título da playlist do youtube\n{title}\n\nNome do Canal\n{uploader}\n\nDuração\n-\n\nVisualização\n{video_count} vídeos"
            
            self.info_label.configure(text=info_text)
            
            # Limpar lista anterior
            for widget in self.playlist_scroll_frame.winfo_children():
                widget.destroy()
            self.playlist_videos.clear()
            
            # Criar checkboxes para cada vídeo
            entries = list(self.video_info.get('entries', []))
            for idx, entry in enumerate(entries, 1):
                if entry:
                    video_title = entry.get('title', f'Vídeo {idx}')
                    
                    var = tk.BooleanVar(value=True)
                    self.playlist_videos.append(var)
                    
                    checkbox = ctk.CTkCheckBox(
                        self.playlist_scroll_frame,
                        text=f"{idx}. {video_title}",
                        variable=var,
                        font=("Montserrat", 11),
                        text_color=self.color_text,
                        fg_color=self.color_neon,
                        hover_color="#a0cc00",
                        checkmark_color="#000000",
                        border_color=self.color_neon,
                        corner_radius=0
                    )
                    checkbox.pack(anchor="w", pady=5, padx=10)
            
            # Mostrar lista e controles de playlist
            self.playlist_scroll_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
            self.playlist_controls_frame.pack(pady=(0, 20))
            
            # Esconder botões de vídeo único
            self.download_frame.pack_forget()
            
        else:
            # Informações do vídeo
            title = self.video_info.get('title', 'Sem título')
            duration = self.video_info.get('duration', 0)
            views = self.video_info.get('view_count', 0)
            uploader = self.video_info.get('uploader', 'Desconhecido')
            
            mins = duration // 60
            secs = duration % 60
            duration_str = f"{mins}:{secs:02d}"
            views_str = f"{views:,}".replace(',', '.')
            
            info_text = f"Título do vídeo do youtube\n{title}\n\nNome do Canal\n{uploader}\n\nDuração\n{duration_str}\n\nVisualização\n{views_str}"
            
            self.info_label.configure(text=info_text)
            
            # Esconder elementos de playlist
            self.playlist_scroll_frame.pack_forget()
            self.playlist_controls_frame.pack_forget()
            
            # Mostrar botões de vídeo único
            self.download_frame.pack(pady=(0, 20))
            
            # Habilitar botões
            self.mp4_btn.configure(state="normal")
            self.mp3_btn.configure(state="normal")
    
    def _show_error(self, error_msg):
        """Mostrar erro"""
        self.analyze_btn.configure(state="normal", text="Analisar link")
        self.info_label.configure(text=f"Erro ao analisar: {error_msg}")
        messagebox.showerror("Erro", f"Não foi possível analisar o link:\n{error_msg}")
    
    def start_download(self, download_type):
        """Iniciar download"""
        if self.is_downloading:
            messagebox.showwarning("Aviso", "Já existe um download em andamento!")
            return
        
        if not self.video_info:
            messagebox.showwarning("Aviso", "Analise um link primeiro!")
            return
        
        is_playlist = 'entries' in self.video_info
        selected_indices = []
        
        if is_playlist:
            selected_indices = [i for i, var in enumerate(self.playlist_videos) if var.get()]
            
            if not selected_indices:
                messagebox.showwarning("Aviso", "Selecione pelo menos um vídeo para baixar!")
                return
            
            video_count = len(selected_indices)
            confirm = messagebox.askyesno(
                "Confirmar Download",
                f"Deseja baixar {video_count} vídeo(s) selecionado(s)?"
            )
            if not confirm:
                return
        
        # Esconder botões de download
        if is_playlist:
            self.playlist_controls_frame.pack_forget()
        else:
            self.download_frame.pack_forget()
        
        self.analyze_btn.configure(state="disabled")
        
        # Mostrar barra de progresso no lugar dos botões
        self.progress_bar.pack(pady=(0, 10), padx=50)
        self.progress_bar.set(0)
        self.status_label.pack(pady=(0, 20))
        self.status_label.configure(text="Iniciando download...")
        
        self.is_downloading = True
        
        # Executar download em thread
        url = self.url_entry.get().strip()
        thread = threading.Thread(
            target=self._download_thread,
            args=(url, download_type, is_playlist, selected_indices)
        )
        thread.daemon = True
        thread.start()
    
    def _download_thread(self, url, download_type, is_playlist, selected_indices=None):
        """Thread de download"""
        try:
            # Encontrar FFmpeg (priorizar versão bundled)
            ffmpeg_location = None
            possible_paths = [
                # Bundled com o executável
                resource_path("ffmpeg/ffmpeg.exe"),
                resource_path("ffmpeg.exe"),
                # Instalações do sistema
                os.path.expanduser(r"~\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"),
                r"C:\ffmpeg\bin\ffmpeg.exe",
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    ffmpeg_location = path
                    break
            
            # Se for playlist, criar pasta
            output_path = self.download_path
            if is_playlist and self.video_info:
                playlist_title = self.video_info.get('title', 'Playlist')
                safe_title = "".join(c for c in playlist_title if c.isalnum() or c in (' ', '-', '_')).strip()
                output_path = os.path.join(self.download_path, safe_title)
                
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
            
            # Download com seleção de vídeos
            if is_playlist and selected_indices:
                entries = list(self.video_info.get('entries', []))
                for idx in selected_indices:
                    if idx < len(entries):
                        entry = entries[idx]
                        video_url = entry.get('url') or f"https://www.youtube.com/watch?v={entry.get('id')}"
                        video_title = entry.get('title', f'Video {idx+1}')
                        
                        self.window.after(0, lambda t=video_title: self.status_label.configure(
                            text=f"Baixando: {t[:40]}..."
                        ))
                        
                        if download_type == "video":
                            ydl_opts = {
                                'format': 'best[ext=mp4]/best',
                                'outtmpl': os.path.join(output_path, f'{idx+1} - %(title)s.%(ext)s'),
                                'progress_hooks': [self._progress_hook],
                                'noprogress': False,
                            }
                        else:
                            ydl_opts = {
                                'format': 'bestaudio/best',
                                'outtmpl': os.path.join(output_path, f'{idx+1} - %(title)s.%(ext)s'),
                                'postprocessors': [{
                                    'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3',
                                    'preferredquality': '192',
                                }],
                                'progress_hooks': [self._progress_hook],
                                'noprogress': False,
                            }
                        
                        if ffmpeg_location:
                            ydl_opts['ffmpeg_location'] = ffmpeg_location
                        
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([video_url])
                
            else:
                # Download normal
                if download_type == "video":
                    ydl_opts = {
                        'format': 'best[ext=mp4]/best',
                        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s' if not is_playlist else '%(playlist_index)s - %(title)s.%(ext)s'),
                        'progress_hooks': [self._progress_hook],
                        'noplaylist': not is_playlist,
                        'noprogress': False,
                    }
                else:
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s' if not is_playlist else '%(playlist_index)s - %(title)s.%(ext)s'),
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'progress_hooks': [self._progress_hook],
                        'noplaylist': not is_playlist,
                        'noprogress': False,
                    }
                
                if ffmpeg_location:
                    ydl_opts['ffmpeg_location'] = ffmpeg_location
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            
            # Sucesso
            self.window.after(0, lambda: self._download_complete(output_path))
            
        except Exception as e:
            self.window.after(0, lambda: self._download_error(str(e)))
    
    def _progress_hook(self, d):
        """Hook de progresso"""
        if d['status'] == 'downloading':
            # Tentar obter total de bytes (pode ser total_bytes ou total_bytes_estimate)
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes', 0)
            
            if total_bytes and total_bytes > 0:
                progress = downloaded_bytes / total_bytes
                self.window.after(0, lambda p=progress: self.progress_bar.set(p))
                
                downloaded_mb = downloaded_bytes / 1024 / 1024
                total_mb = total_bytes / 1024 / 1024
                status_text = f"Baixando: {downloaded_mb:.1f}MB / {total_mb:.1f}MB ({progress*100:.1f}%)"
                self.window.after(0, lambda t=status_text: self.status_label.configure(text=t))
            else:
                # Se não tiver total, mostrar apenas o que foi baixado
                downloaded_mb = downloaded_bytes / 1024 / 1024
                status_text = f"Baixando: {downloaded_mb:.1f}MB..."
                self.window.after(0, lambda t=status_text: self.status_label.configure(text=t))
        
        elif d['status'] == 'finished':
            self.window.after(0, lambda: self.progress_bar.set(1.0))
            self.window.after(0, lambda: self.status_label.configure(text="Processando arquivo..."))
    
    def _download_complete(self, output_path=None):
        """Download concluído"""
        self.is_downloading = False
        self.progress_bar.set(1.0)
        self.status_label.configure(text="Download concluído com sucesso!")
        
        # Mostrar botões novamente
        is_playlist = 'entries' in self.video_info if self.video_info else False
        
        if is_playlist:
            self.playlist_controls_frame.pack(pady=(0, 20), padx=50)
        else:
            self.download_frame.pack(pady=(0, 20))
        
        self.analyze_btn.configure(state="normal")
        
        final_path = output_path if output_path else self.download_path
        
        # Criar janela de sucesso customizada
        self._show_success_dialog(final_path)
        
        # Limpar após 3 segundos
        self.window.after(3000, self._reset_progress)
    
    def _show_success_dialog(self, path):
        """Mostrar diálogo de sucesso customizado"""
        dialog = ctk.CTkToplevel(self.window)
        dialog.title("Sucesso")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.configure(fg_color=self.color_bg)
        
        # Centralizar na tela
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"400x200+{x}+{y}")
        
        # Título
        title_label = ctk.CTkLabel(
            dialog,
            text="Download Concluído!",
            font=("Montserrat", 24, "bold"),
            text_color=self.color_neon
        )
        title_label.pack(pady=(30, 10))
        
        # Mensagem
        msg_label = ctk.CTkLabel(
            dialog,
            text=f"Arquivo(s) salvo(s) em:\n{path}",
            font=("Montserrat", 11),
            text_color=self.color_text,
            wraplength=350
        )
        msg_label.pack(pady=(0, 20))
        
        # Botão OK
        ok_btn = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            height=40,
            width=120,
            font=("Montserrat", 13, "bold"),
            fg_color=self.color_neon,
            hover_color="#a0cc00",
            text_color="#000000",
            corner_radius=0
        )
        ok_btn.pack(pady=(0, 20))
        
        # Focar na janela
        dialog.transient(self.window)
        dialog.grab_set()
        dialog.focus()
    
    def _download_error(self, error_msg):
        """Erro no download"""
        self.is_downloading = False
        self.status_label.configure(text=f"Erro: {error_msg}")
        
        # Mostrar botões novamente
        is_playlist = 'entries' in self.video_info if self.video_info else False
        
        if is_playlist:
            self.playlist_controls_frame.pack(pady=(0, 20), padx=50)
        else:
            self.download_frame.pack(pady=(0, 20))
        
        self.analyze_btn.configure(state="normal")
        
        messagebox.showerror("Erro no Download", f"Ocorreu um erro:\n{error_msg}")
    
    def _reset_progress(self):
        """Resetar barra de progresso"""
        self.progress_bar.pack_forget()
        self.status_label.pack_forget()
        self.progress_bar.set(0)
    
    def run(self):
        """Executar aplicação"""
        self.window.mainloop()

def main():
    """Função principal"""
    # Verificar dependências
    try:
        import customtkinter
    except ImportError:
        print("Instalando customtkinter...")
        os.system(f"{sys.executable} -m pip install customtkinter")
    
    try:
        import yt_dlp
    except ImportError:
        print("Instalando yt-dlp...")
        os.system(f"{sys.executable} -m pip install yt-dlp")
    
    # Executar GUI
    app = YouTubeDownloaderGUI()
    app.run()

if __name__ == "__main__":
    main()
