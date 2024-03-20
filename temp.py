from radiojavanapi import Client

c = Client()
i = 121000
while i < 200000:
    try:
        print(c.get_song_by_id(i).artist)
        i += 1000
    except:
        i += 1
        continue
