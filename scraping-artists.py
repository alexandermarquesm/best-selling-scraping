from bs4 import BeautifulSoup
import pandas as pd
import requests

url = 'https://en.wikipedia.org/wiki/List_of_best-selling_music_artists'

response = requests.get(url)
print(response.status_code == 200)
