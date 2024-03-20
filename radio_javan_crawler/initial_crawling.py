import logging

from radio_javan_crawler.get_music import get_music_by_id
from save_music.download_media import download_music, download_music_thumbnail, delete_file, create_path
from send_to_channel.telegram_channel import send_music_to_channel


async def crawling(start_id, end_id):
    create_path()
    for music_id in range(start_id, end_id):
        try:
            music = get_music_by_id(music_id)
            music_path = download_music(music)
            music_thumbnail_path = download_music_thumbnail(music)
            await send_music_to_channel(music, music_path, music_thumbnail_path)
            delete_file(music_path)
            delete_file(music_thumbnail_path)
        except Exception as e:
            logging.error(f'Cant download music by id: {music_id}', music_id)
            logging.error(e)
            continue
