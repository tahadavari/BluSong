import telegram

TOKEN = "someToken"
CHAT_ID = -1002103799811
BOT = telegram.Bot(token=TOKEN)


async def send_music_to_channel(music, music_path, music_thumbnail_path):
    caption = f"""
    Name: {music.name}
    
    Artist Name: {music.artist}
    
    @song_blue
    """
    await BOT.send_photo(chat_id=CHAT_ID, photo=open(music_thumbnail_path, "rb"), caption=caption)
    await BOT.send_audio(chat_id=CHAT_ID, audio=open(music_path, "rb"))
