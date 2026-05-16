# Universal Media Downloader Bot

A powerful Telegram bot built with Python and `pyTelegramBotAPI` that allows users to seamlessly download media (audio and video) from various platforms including YouTube, TikTok, Pinterest, and Instagram.

## Features

- **YouTube**: Download videos in MP4 or extract audio tracks directly into high-quality MP3 format.
- **TikTok**: Fast video downloads via `yt-dlp`.
- **Pinterest**: Automatically detects and processes both video links and high-resolution static images.
- **Instagram**: Smart bypass mechanism to download Reels, videos, and photos without login restrictions.
- **Security First**: Configuration settings and sensitive API tokens are decoupled from the core source code.

## Tech Stack

- **Language**: Python 3
- **Core Libraries**: `pyTelegramBotAPI`, `yt-dlp`, `requests`, `imageio-ffmpeg`

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/vova916/gfg.git](https://github.com/vova916/gfg.git)
   cd gfg or vs code ui.

Install dependencies:

Bash
pip install pyTelegramBotAPI yt-dlp requests imageio-ffmpeg
Create a config.py file based on config.example.py and insert your Telegram Bot Token:

Python
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
DOWNLOAD_DIR = 'D:/YouTube_Cache'
Run the application:

Bash
python main.py

