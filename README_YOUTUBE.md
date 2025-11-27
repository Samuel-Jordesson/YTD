# 🎬 YouTube Video Downloader

Download vídeos do YouTube facilmente com Python!

## 📋 Requisitos

- Python 3.6 ou superior
- Biblioteca `yt-dlp` (instalada automaticamente)
- **FFmpeg** (necessário para vídeos funcionarem corretamente)

### Instalar FFmpeg (Windows)

**Opção 1 - Automática (Recomendado):**
```bash
# Execute o script de instalação
install_ffmpeg.bat
```

**Opção 2 - Manual:**
1. Acesse: https://www.gyan.dev/ffmpeg/builds/
2. Baixe: `ffmpeg-release-essentials.zip`
3. Extraia para `C:\ffmpeg`
4. Adicione `C:\ffmpeg\bin` ao PATH do sistema

**Opção 3 - Chocolatey:**
```bash
choco install ffmpeg
```

**Opção 4 - Winget:**
```bash
winget install Gyan.FFmpeg
```

## 🚀 Como Usar

### Instalação

```bash
# Instalar a biblioteca necessária
pip install yt-dlp
```

### Executar

```bash
python youtube_downloader.py
```

## ✨ Funcionalidades

- ✅ **Download de vídeo** em melhor qualidade disponível
- ✅ **Download de áudio** (MP3) apenas
- ✅ **Barra de progresso** durante o download
- ✅ **Informações do vídeo** (título, duração, views)
- ✅ **Escolha da pasta** de destino
- ✅ **Interface amigável** no terminal

## 📖 Exemplo de Uso

```
🎬 YOUTUBE VIDEO DOWNLOADER 🎬

📋 MENU:
1. Baixar vídeo (melhor qualidade)
2. Baixar apenas áudio (MP3)
3. Sair

Escolha uma opção (1-3): 1

🔗 Cole o link do YouTube: https://www.youtube.com/watch?v=...

📁 Pasta de destino (Enter para 'downloads'): meus_videos

🎬 Baixando vídeo de: https://www.youtube.com/watch?v=...
📁 Salvando em: C:\...\meus_videos

📺 Título: Nome do Vídeo
⏱️  Duração: 5:30
👁️  Views: 1000000

⬇️  Baixando: 100.0% - 50.0MB / 50.0MB
✓ Download finalizado, processando...

✅ Download concluído com sucesso!
📂 Arquivo salvo em: C:\...\meus_videos
```

## 🎯 Opções

### 1. Download de Vídeo
- Baixa o vídeo na melhor qualidade disponível
- Formato: MP4 (geralmente)
- Inclui vídeo e áudio

### 2. Download de Áudio
- Extrai apenas o áudio do vídeo
- Formato: MP3
- Qualidade: 192 kbps

## 📁 Estrutura de Arquivos

```
downloads/           # Pasta padrão para downloads
├── Video1.mp4
├── Video2.mp4
└── Audio1.mp3
```

## ⚠️ Notas Importantes

- Os vídeos são salvos com o título original do YouTube
- A pasta de downloads é criada automaticamente se não existir
- Certifique-se de ter espaço em disco suficiente
- Respeite os direitos autorais dos vídeos

## 🛠️ Tecnologias

- **Python 3**
- **yt-dlp** - Biblioteca para download de vídeos do YouTube
- **FFmpeg** (opcional, para conversão de áudio)

## 💡 Dicas

- Para melhor qualidade de áudio, instale o FFmpeg
- Use links curtos (youtu.be) ou completos (youtube.com)
- Você pode baixar playlists inteiras modificando o código

## 🐛 Solução de Problemas

**Erro ao instalar yt-dlp:**
```bash
pip install --upgrade yt-dlp
```

**Erro de FFmpeg (para áudio MP3):**
```bash
# Windows: Baixe em https://ffmpeg.org/download.html
# Linux: sudo apt install ffmpeg
# Mac: brew install ffmpeg
```

## 📝 Licença

Livre para uso pessoal. Respeite os direitos autorais!
