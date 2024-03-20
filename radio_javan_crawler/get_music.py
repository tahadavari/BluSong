from radiojavanapi import Client

rj = Client()


def get_music_by_id(music_id):
    return rj.get_song_by_id(music_id)
