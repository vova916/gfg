# Universal Media Downloader Bot

A powerful Telegram bot built with Python and `telebot` that allows users to seamlessly download media (audio and video) from various platforms including YouTube, TikTok, Pinterest, and Instagram.

## Features

- **YouTube**: Download videos in MP4 or extract audio tracks directly into high-quality MP3 format.
- **TikTok**: Fast video downloads via `yt-dlp`.
- **Pinterest**: Automatically detects and processes both video links and high-resolution static images.
- **Instagram**: Smart bypass mechanism to download Reels, videos, and photos without login restrictions.
- **Security First**: Configuration settings and sensitive API tokens are decoupled from the core source code.

## Tech Stack

- **Language**: Python 3
- **Core Libraries**: `telebot`, `yt-dlp`, `requests`, `imageio-ffmpeg`

## Installation & Setup

Copy and run the following commands in your terminal to set up and start the bot:

```bash
# 1. Clone the repository and navigate to the project folder
git clone [https://github.com/vova916/gfg.git](https://github.com/vova916/gfg.git)
cd gfg

# 2. Install all required dependencies
pip install pyTelegramBotAPI yt-dlp requests imageio-ffmpeg

# 3. Create config.py file with your configuration
echo TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN' > config.py
echo DOWNLOAD_DIR = 'D:/YouTube_Cache' >> config.py

# 4. Run the bot application
python main.py
