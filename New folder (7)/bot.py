import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp

# مسیر ذخیره فایل‌های دانلود شده
DOWNLOAD_DIR = "downloads/"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# تابع دانلود ویدیو با yt-dlp
def download_youtube_video(url):
    try:
        ydl_opts = {
            'format': 'best',  # بهترین کیفیت موجود
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)
        return file_path
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

# هندلر شروع ربات
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("سلام! لینک ویدیوی یوتیوب را ارسال کنید تا برای شما دانلود کنم.")

# هندلر پیام‌های کاربران
def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    chat_id = update.message.chat_id

    if "youtube.com" not in url and "youtu.be" not in url:
        update.message.reply_text("لطفاً یک لینک معتبر یوتیوب ارسال کنید.")
        return

    update.message.reply_text("در حال دانلود ویدیو، لطفاً صبر کنید...")

    file_path = download_youtube_video(url)
    if file_path:
        try:
            with open(file_path, 'rb') as video:
                context.bot.send_video(chat_id=chat_id, video=video)
            os.remove(file_path)  # حذف فایل بعد از ارسال
        except Exception as e:
            update.message.reply_text(f"خطا در ارسال ویدیو: {e}")
    else:
        update.message.reply_text("خطا در دانلود ویدیو. لطفاً دوباره تلاش کنید.")

# اجرای ربات
def main():
    TOKEN = "7796148404:AAFTvV0nIwNzHOJqm5FF4A0unJXDpTzeZpI"  # توکن خود را اینجا وارد کنید
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
