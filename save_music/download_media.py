import csv
import os
import uuid

import requests

# SONG_PATH_SAVE_MEMORY = "/tmp/radiojavan/songs/"
# SONG_THUMBNAIL_PATH_SAVE_MEMORY = "/tmp/radiojavan/thumbnails/"
# SONG_FILE = "/tmp/radiojavan/songs.csv"

SONG_PATH_SAVE_MEMORY = "./songs/"
SONG_THUMBNAIL_PATH_SAVE_MEMORY = "./thumbnails/"
SONG_FILE = "./songs.csv"


def download_music(music):
    link = music.hq_link if music.hq_link else music.link
    ext = link.split('.')[-1]
    response = requests.get(link)
    file_path = SONG_PATH_SAVE_MEMORY + f'{uuid.uuid4()}' + '.' + ext
    with open(file_path, "wb") as file:
        file.write(response.content)
    return file_path


def download_music_thumbnail(music):
    link = music.thumbnail
    ext = link.split('.')[-1]
    response = requests.get(link)
    file_path = SONG_THUMBNAIL_PATH_SAVE_MEMORY + f'{uuid.uuid4()}' + '.' + ext
    with open(file_path, "wb") as file:
        file.write(response.content)
    return file_path


async def create_path():
    if not os.path.exists(SONG_PATH_SAVE_MEMORY):
        os.makedirs(SONG_PATH_SAVE_MEMORY)
    if not os.path.exists(SONG_THUMBNAIL_PATH_SAVE_MEMORY):
        os.makedirs(SONG_THUMBNAIL_PATH_SAVE_MEMORY)


async def add_song_to_file(song_info):
    with open(SONG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(song_info)


async def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
