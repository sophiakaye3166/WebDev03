import streamlit as st
import requests
import urllib.parse

APIK = "YOUR_LASTFM_API_KEY" 

def get_top_albums(artist, apik, limit=5):
    artist_enc = urllib.parse.quote(artist)
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist={artist_enc}&api_key={apik}&format=json"
    r = requests.get(url).json()
    return r.get("topalbums", {}).get("album", [])[:limit]

def get_artist_tags(artist, apik):
    artist_enc = urllib.parse.quote(artist)
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist_enc}&api_key={apik}&format=json"
    r = requests.get(url).json()
    return [tag["name"] for tag in r.get("artist", {}).get("tags", {}).get("tag", [])]

def get_top_track_and_tags(artist, apik):
    artist_enc = urllib.parse.quote(artist)
    track_url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={artist_enc}&api_key={apik}&format=json&limit=1"
    r = requests.get(track_url).json()
    track = r.get("toptracks", {}).get("track", [{}])[0]
    track_name = track.get("name", "")
    
    tag_url = f"http://ws.audioscrobbler.com/2.0/?method=track.getTopTags&artist={artist_enc}&track={urllib.parse.quote(track_name)}&api_key={apik}&format=json"
    tag_r = requests.get(tag_url).json()
    tags = [t["name"] for t in tag_r.get("toptags", {}).get("tag", [])]
    
    return track_name, tags

st.title("Artist Comparison (Last.fm)")
st.write("Compare two artists by top albums, tags, and most played track.")

artist1 = st.text_input("Enter Artist 1", "Ariana Grande")
artist2 = st.text_input("Enter Artist 2", "Taylor Swift")

if artist1 and artist2:
    col1, col2 = st.columns(2)
    
    for col, artist in zip((col1, col2), (artist1, artist2)):
        with col:
            st.header(artist.title())
            
            albums = get_top_albums(artist, APIK)
            if not albums:
                st.error("Could not retrieve album data. Please check spelling or API key.")
                continue
            
            st.subheader("Top Albums:")
            for a in albums:
                st.write(f"- {a['name']}")

            tags = get_artist_tags(artist, APIK)
            if tags:
                st.subheader("Tags:")
                st.write(", ".join(tags[:5]))
            
            top_track, track_tags = get_top_track_and_tags(artist, APIK)
            if top_track:
                st.subheader("Most Played Track:")
                st.write(top_track)
                if track_tags:
                    st.subheader("Track Tags:")
                    st.write(", ".join(track_tags[:5]))














