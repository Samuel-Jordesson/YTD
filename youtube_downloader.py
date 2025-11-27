#!/usr/bin/env python3
"""
YouTube Video Downloader
Download vídeos do YouTube facilmente
"""

import os
import sys

try:
    import yt_dlp
except ImportError:
    print("❌ Biblioteca yt-dlp não encontrada!")
    print("📦 Instalando yt-dlp...")
    os.system(f"{sys.executable} -m pip install yt-dlp")
    import yt_dlp

def download_video(url, output_path="downloads"):
    """
    Baixa um vídeo do YouTube
    
    Args:
        url: Link do vídeo do YouTube
        output_path: Pasta onde salvar o vídeo
    """
    # Criar pasta de downloads se não existir
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Tentar encontrar FFmpeg
    ffmpeg_location = None
    possible_paths = [
        os.path.expanduser(r"~\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"),
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        os.path.expanduser(r"~\scoop\apps\ffmpeg\current\bin\ffmpeg.exe"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            ffmpeg_location = path
            break
    
    # Configurações do download
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'noplaylist': True,
        # Deixar o fixup acontecer - ele cria o .temp.mp4 que funciona
    }
    
    if ffmpeg_location:
        ydl_opts['ffmpeg_location'] = ffmpeg_location
        print(f"✓ FFmpeg disponível")
    else:
        print("⚠️  FFmpeg não encontrado")
    
    try:
        print(f"\n🎬 Baixando vídeo de: {url}")
        print(f"📁 Salvando em: {os.path.abspath(output_path)}\n")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Obter informações do vídeo
            info = ydl.extract_info(url, download=False)
            print(f"📺 Título: {info['title']}")
            print(f"⏱️  Duração: {info['duration'] // 60}:{info['duration'] % 60:02d}")
            print(f"👁️  Views: {info.get('view_count', 'N/A')}")
            print()
            
            # Fazer o download
            ydl.download([url])
            
        print("\n✅ Download concluído com sucesso!")
        print(f"📂 Arquivo salvo em: {os.path.abspath(output_path)}")
        
    except Exception as e:
        print(f"\n❌ Erro ao baixar o vídeo: {str(e)}")
        
        # Tentar limpar arquivos temporários mesmo em caso de erro
        import glob
        temp_files = glob.glob(os.path.join(output_path, "*.temp.mp4")) + \
                     glob.glob(os.path.join(output_path, "*.part")) + \
                     glob.glob(os.path.join(output_path, "*.ytdl"))
        
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception:
                pass
        
        return False
    
    return True

def progress_hook(d):
    """Mostra o progresso do download"""
    if d['status'] == 'downloading':
        # Calcular porcentagem
        if 'total_bytes' in d:
            percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
            print(f"\r⬇️  Baixando: {percent:.1f}% - {d['downloaded_bytes'] / 1024 / 1024:.1f}MB / {d['total_bytes'] / 1024 / 1024:.1f}MB", end='')
        else:
            print(f"\r⬇️  Baixando: {d['downloaded_bytes'] / 1024 / 1024:.1f}MB", end='')
    elif d['status'] == 'finished':
        print(f"\n✓ Download finalizado, processando...")

def download_audio_only(url, output_path="downloads"):
    """
    Baixa apenas o áudio do vídeo (MP3)
    
    Args:
        url: Link do vídeo do YouTube
        output_path: Pasta onde salvar o áudio
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],
        'noplaylist': True,  # Baixar apenas o vídeo, não a playlist inteira
    }
    
    try:
        print(f"\n🎵 Baixando áudio de: {url}")
        print(f"📁 Salvando em: {os.path.abspath(output_path)}\n")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print(f"📺 Título: {info['title']}")
            print()
            ydl.download([url])
            
        print("\n✅ Download de áudio concluído!")
        print(f"📂 Arquivo salvo em: {os.path.abspath(output_path)}")
        
    except Exception as e:
        print(f"\n❌ Erro ao baixar o áudio: {str(e)}")
        return False
    
    return True

def download_playlist(url, output_path="downloads"):
    """
    Baixa uma playlist inteira do YouTube
    
    Args:
        url: Link da playlist do YouTube
        output_path: Pasta onde salvar os vídeos
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Tentar encontrar FFmpeg
    ffmpeg_location = None
    possible_paths = [
        os.path.expanduser(r"~\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"),
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        os.path.expanduser(r"~\scoop\apps\ffmpeg\current\bin\ffmpeg.exe"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            ffmpeg_location = path
            break
    
    # Configurações do download para playlist
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': os.path.join(output_path, '%(playlist_index)s - %(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'noplaylist': False,  # Permitir download de playlist
        'ignoreerrors': True,  # Continuar mesmo se algum vídeo falhar
    }
    
    if ffmpeg_location:
        ydl_opts['ffmpeg_location'] = ffmpeg_location
        print(f"✓ FFmpeg disponível")
    else:
        print("⚠️  FFmpeg não encontrado")
    
    try:
        print(f"\n🎬 Baixando playlist de: {url}")
        print(f"📁 Salvando em: {os.path.abspath(output_path)}\n")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Obter informações da playlist
            info = ydl.extract_info(url, download=False)
            
            if 'entries' in info:
                playlist_title = info.get('title', 'Playlist')
                video_count = len(list(info['entries']))
                print(f"📺 Playlist: {playlist_title}")
                print(f"📊 Total de vídeos: {video_count}")
                print()
                
                # Confirmar download
                confirm = input(f"Deseja baixar {video_count} vídeos? (s/n): ").strip().lower()
                if confirm != 's':
                    print("❌ Download cancelado.")
                    return False
                
                # Fazer o download
                ydl.download([url])
            else:
                print("⚠️  Não foi possível detectar a playlist. Verifique o link.")
                return False
            
        print("\n✅ Download da playlist concluído!")
        print(f"📂 Arquivos salvos em: {os.path.abspath(output_path)}")
        
    except Exception as e:
        print(f"\n❌ Erro ao baixar a playlist: {str(e)}")
        return False
    
    return True

def cleanup_temp_files(output_path="downloads"):
    """Limpa arquivos temporários e renomeia .temp.mp4 para .mp4"""
    import glob
    import time
    
    print("\n🧹 Organizando arquivos...")
    time.sleep(1)  # Pequena pausa
    
    # Procurar arquivos .temp.mp4 (esses funcionam)
    temp_files = glob.glob(os.path.join(output_path, "*.temp.mp4"))
    
    if temp_files:
        for temp_file in temp_files:
            try:
                # Nome final sem .temp
                final_name = temp_file.replace('.temp.mp4', '.mp4')
                
                # Remover o arquivo .mp4 quebrado se existir
                if os.path.exists(final_name):
                    try:
                        os.remove(final_name)
                        print(f"🗑️  Removido arquivo quebrado: {os.path.basename(final_name)}")
                    except Exception as e:
                        print(f"⚠️  Não foi possível remover: {os.path.basename(final_name)}")
                        print(f"   Delete manualmente e renomeie {os.path.basename(temp_file)} para .mp4")
                        continue
                
                # Renomear o .temp.mp4 (que funciona) para .mp4
                try:
                    os.rename(temp_file, final_name)
                    print(f"✓ Arquivo organizado: {os.path.basename(final_name)}")
                except Exception as e:
                    print(f"⚠️  Use o arquivo: {os.path.basename(temp_file)}")
            except Exception as e:
                print(f"⚠️  Erro ao processar: {str(e)}")
    
    # Limpar outros temporários
    other_temp = glob.glob(os.path.join(output_path, "*.part")) + \
                 glob.glob(os.path.join(output_path, "*.ytdl"))
    
    for temp_file in other_temp:
        try:
            os.remove(temp_file)
        except:
            pass

def main():
    """Função principal - interface do usuário"""
    print("=" * 60)
    print("🎬 YOUTUBE VIDEO DOWNLOADER 🎬".center(60))
    print("=" * 60)
    print()
    
    while True:
        print("\n📋 MENU:")
        print("1. Baixar vídeo (melhor qualidade)")
        print("2. Baixar apenas áudio (MP3)")
        print("3. Baixar playlist inteira")
        print("4. Sair")
        print()
        
        choice = input("Escolha uma opção (1-4): ").strip()
        
        if choice == '4':
            cleanup_temp_files()  # Limpar antes de sair
            print("\n👋 Até logo!")
            break
        
        if choice not in ['1', '2', '3']:
            print("❌ Opção inválida! Tente novamente.")
            continue
        
        url = input("\n🔗 Cole o link do YouTube: ").strip()
        
        if not url:
            print("❌ Link vazio! Tente novamente.")
            continue
        
        # Validação básica do link
        if 'youtube.com' not in url and 'youtu.be' not in url:
            print("❌ Link inválido! Use um link do YouTube.")
            continue
        
        output_path = input("📁 Pasta de destino (Enter para 'downloads'): ").strip()
        if not output_path:
            output_path = "downloads"
        
        if choice == '1':
            download_video(url, output_path)
        elif choice == '2':
            download_audio_only(url, output_path)
        elif choice == '3':
            download_playlist(url, output_path)
        
        continuar = input("\n🔄 Baixar outro vídeo? (s/n): ").strip().lower()
        
        # Limpar arquivos temporários após a resposta do usuário
        cleanup_temp_files(output_path)
        
        if continuar != 's':
            print("\n👋 Até logo!")
            break

if __name__ == "__main__":
    main()
