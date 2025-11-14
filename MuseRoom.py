import requests
import urllib.parse

APIK = "REPLACE_WITH_YOUR_API_KEY"
artist = "Taylor Swift"
safe_artist = urllib.parse.quote(artist)
url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist={safe_artist}&api_key={APIK}&format=json"

response = requests.get(url)
print("Status Code:", response.status_code)
print("Response JSON:")
print(response.json())













