import threading

from radio_javan_crawler.initial_crawling import crawling

# for i in range(13):
#     start = i * 10000
#     end = (i + 1) * 10000
#     t = threading.Thread(target=crawling, args=[start, end])
#     t.start()


crawling(120000,120002)
