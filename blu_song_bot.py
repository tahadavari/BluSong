import asyncio
import logging
import time

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from radio_javan_crawler.get_music import get_music_by_id
from save_music.download_media import create_path, download_music, download_music_thumbnail, delete_file, \
    add_song_to_file

TOKEN = 'someToken'
CHAT_ID = -1002103799811
TIMEOUT = 1000000

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.INFO)

logger = logging.getLogger(__name__)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hi {update.effective_user.first_name}!"
    )


async def testc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await context.bot.send_message(chat_id=CHAT_ID,

                                   text="testc")
    print(message.message_id)


async def rjs_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await create_path()
    end_message = None
    for music_id in range(120000, 120010):
        try:
            if end_message:
                await context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=end_message.message_id)
            music = get_music_by_id(music_id)
            music_path = download_music(music)
            music_thumbnail_path = download_music_thumbnail(music)
            caption = f"""
                Name: {music.name}

Artist Name: {music.artist}

Enjoy listening with @BluSong
                """
            start_message = await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"music: {music.id} has started"
            )

            # photo_message = await context.bot.send_photo(chat_id=CHAT_ID, caption=caption,
            #                                              photo=open(music_thumbnail_path, "rb"), read_timeout=TIMEOUT,
            #                                              write_timeout=TIMEOUT)
            song_message = await context.bot.send_audio(chat_id=CHAT_ID,
                                                        # reply_to_message_id=photo_message.message_id,
                                                        audio=open(music_path, "rb"),
                                                        filename=f"{music.name} - {music.artist}",
                                                        read_timeout=TIMEOUT,
                                                        caption=caption,
                                                        thumbnail=open(music_thumbnail_path, "rb"),
                                                        write_timeout=TIMEOUT)
            await asyncio.sleep(5)
            await add_song_to_file([music.id, music.name, song_message.message_id])
            await delete_file(music_path)
            await delete_file(music_thumbnail_path)
            end_message = await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"music: {music.id} has finished"
            )
            await context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=start_message.message_id)

        except Exception as e:
            logging.critical(f'Cant download music by id: {music_id}', music_id)
            end_message = await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"music: {music_id} has not download"
            )
            continue


if __name__ == "__main__":
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).read_timeout(TIMEOUT).write_timeout(TIMEOUT).build()
    # Command Handler
    application.add_handler(CommandHandler("start", start_handler))

    application.add_handler(CommandHandler("rjs", rjs_handler))
    application.add_handler(CommandHandler("testc", testc_handler))

    # Run the Bot
    application.run_polling()
