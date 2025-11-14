import requests

APIK = "your_actual_key_here"
artist = "Taylor Swift"
url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist={artist}&api_key={APIK}&format=json"

response = requests.get(url).json()
print(response)














