import os
import re
import telebot
import requests
from yt_dlp import YoutubeDL
import imageio_ffmpeg
import config  # Імпортуємо наш файл конфігурації

bot = telebot.TeleBot(config.TOKEN)  # Беремо токен з config.py

if not os.path.exists(config.DOWNLOAD_DIR):  # Беремо шлях з config.py
    os.makedirs(config.DOWNLOAD_DIR)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    interkeyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    interkeyboard.add(
        telebot.types.InlineKeyboardButton('🎵 Завантажити Аудіо (MP3) [YouTube / TikTok / Pinterest]', callback_data='download_audio'),
        telebot.types.InlineKeyboardButton('🎬 Завантажити Відео (MP4) [YouTube]', callback_data='download_video'),
        telebot.types.InlineKeyboardButton('📱 Завантажити Відео (MP4) [TikTok]', callback_data='download_tiktok_video'),
        telebot.types.InlineKeyboardButton('📸 Завантажити з Pinterest (Фото / Відео)', callback_data='download_pinterest'),
        telebot.types.InlineKeyboardButton('📸 Завантажити з Instagram (Reels / Фото / Відео)', callback_data='download_instagram')
    )
    bot.send_message(
        message.chat.id, 
        "Привіт! Я універсальний бот для завантаження медіа.\nОберіть, що саме ви хочете завантажити:", 
        reply_markup=interkeyboard
    )

@bot.callback_query_handler(func=lambda call: call.data in [
    'download_audio', 'download_video', 'download_tiktok_video', 'download_pinterest', 'download_instagram'
])
def handle_all_buttons(call):
    bot.answer_callback_query(call.id)
    prompts = {
        'download_audio': "⏩ Відправте посилання (YouTube, TikTok або Pinterest) для витягування audio в MP3:",
        'download_video': "⏩ Відправте посилання на YouTube для завантаження відео в MP4:",
        'download_tiktok_video': "⏩ Відправте посилання на TikTok для завантаження відео:",
        'download_pinterest': "⏩ Відправте посилання на Pinterest (скачаю photo або відео):",
        'download_instagram': "⏩ Відправте посилання на Instagram (Reels або пост):"
    }
    msg = bot.send_message(call.message.chat.id, prompts[call.data])
    bot.register_next_step_handler(msg, process_media_download, call.data)

def process_media_download(message, action):
    url = message.text.strip()
    if not url.startswith(('http://', 'https://')):
        bot.reply_to(message, "❌ Це не схоже на правильне посилання. Спробуйте знову через /start")
        return

    status_msg = bot.reply_to(message, "⏳ Обробляю посилання та починаю завантаження... Зачекайте.")
    
    ydl_opts = {
        'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(),
        'outtmpl': os.path.join(config.DOWNLOAD_DIR, '%(title)s.%(ext)s'),  # Змінено на config
        'nocheckcertificate': True,
        'quiet': True
    }
    
    if action == 'download_audio':
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }]
    elif action == 'download_video':
        ydl_opts['format'] = 'bestext[ext=mp4]/best[ext=mp4]'
    else:
        ydl_opts['format'] = 'best'

    filepath = None

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if action == 'download_audio':
                filepath = os.path.splitext(filename)[0] + '.mp3'
            else:
                filepath = filename

        bot.edit_message_text("🚀 Завантажено! Надсилаю у Телеграм...", chat_id=status_msg.chat.id, message_id=status_msg.message_id)
        
        with open(filepath, 'rb') as f:
            if action == 'download_audio':
                bot.send_audio(message.chat.id, f, title=info.get('title', 'Audio Track'))
            else:
                ext = info.get('ext', '').lower()
                if ext in ['jpg', 'jpeg', 'png', 'webp']:
                    bot.send_photo(message.chat.id, f)
                else:
                    bot.send_video(message.chat.id, f)
                    
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
            
    except Exception as e:
        if filepath and os.path.exists(filepath):
            try: os.remove(filepath)
            except: pass

        if action in ['download_pinterest', 'download_instagram']:
            try:
                bot.edit_message_text("📸 Відео-формат не знайдено. Завантажую як фото...", chat_id=status_msg.chat.id, message_id=status_msg.message_id)
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
                photo_path = os.path.join(config.DOWNLOAD_DIR, 'downloaded_picture.jpg')  # Змінено на config
                success = False

                if action == 'download_instagram':
                    clean_url = url.split('?')[0]
                    if not clean_url.endswith('/'):
                        clean_url += '/'
                    insta_media_url = clean_url + 'media/?size=l'
                    img_res = requests.get(insta_media_url, timeout=12, headers=headers, allow_redirects=True)
                    if img_res.status_code == 200 and 'image' in img_res.headers.get('Content-Type', ''):
                        with open(photo_path, 'wb') as img_f:
                            img_f.write(img_res.content)
                        success = True

                if not success and action == 'download_pinterest':
                    response = requests.get(url, timeout=12, headers=headers)
                    if response.status_code == 200:
                        html_content = response.text
                        img_urls = re.findall(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html_content)
                        if not img_urls:
                            img_urls = re.findall(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', html_content)
                        if img_urls:
                            direct_img_url = img_urls[0].replace('&amp;', '&')
                            img_data = requests.get(direct_img_url, timeout=10, headers=headers).content
                            with open(photo_path, 'wb') as img_f:
                                img_f.write(img_data)
                            success = True

                if success and os.path.exists(photo_path):
                    with open(photo_path, 'rb') as img_f:
                        bot.send_photo(message.chat.id, img_f, caption="✨ Медіа успішно завантажено!")
                    os.remove(photo_path)
                    bot.delete_message(chat_id=status_msg.chat.id, message_id=status_msg.message_id)
                    return
                        
            except Exception as img_err:
                print(f"Error direct downloading photo: {img_err}")

        bot.edit_message_text(f"❌ Не вдалося отримати цей медіафайл.\n\nПеревірте, чи це не приватний профіль, і спробуйте інше посилання.", chat_id=status_msg.chat.id, message_id=status_msg.message_id)

if __name__ == '__main__':
    bot.infinity_polling()