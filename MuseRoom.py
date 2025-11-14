import streamlit as st
import requests
import urllib.parse

APIK = "7e96bc4d2ecb5f97e26807ee6f2f9048"

def get_top_albums(artist, limit=5):
    artist_enc = urllib.parse.quote(artist)
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist={artist_enc}&api_key={APIK}&format=json"
    res = requests.get(url).json()
    return res.get("topalbums", {}).get("album", [])[:limit]

def get_artist_tags(artist):
    artist_enc = urllib.parse.quote(artist)
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist_enc}&api_key={APIK}&format=json"
    res = requests.get(url).json()
    return [tag["name"] for tag in res.get("artist", {}).get("tags", {}).get("tag", [])]

def get_top_track_and_tags(artist):
    artist_enc = urllib.parse.quote(artist)
    track_url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={artist_enc}&api_key={APIK}&format=json&limit=1"
    res = requests.get(track_url).json()
    top_track = res.get("toptracks", {}).get("track", [{}])[0].get("name", "")

    if top_track:
        tags_url = f"http://ws.audioscrobbler.com/2.0/?method=track.getTopTags&artist={artist_enc}&track={urllib.parse.quote(top_track)}&api_key={APIK}&format=json"
        tag_res = requests.get(tags_url).json()
        track_tags = [tag["name"] for tag in tag_res.get("toptags", {}).get("tag", [])]
        return top_track, track_tags
    return None, None

# Streamlit UI
st.title("🎶 Artist Comparison (Last.fm)")
st.write("Compare two artists' albums, tags, and top tracks using the Last.fm API.")

artist1 = st.text_input("Enter Artist 1", "Taylor Swift")
artist2 = st.text_input("Enter Artist 2", "Ariana Grande")

if artist1 and artist2:
    col1, col2 = st.columns(2)

    for col, artist in zip((col1, col2), (artist1, artist2)):
        with col:
            st.header(artist.title())

            albums = get_top_albums(artist)
            if albums:
                st.subheader("Top Albums:")
                for a in albums:
                    st.write(f"- {a['name']}")
            else:
                st.error("Could not fetch albums.")

            tags = get_artist_tags(artist)
            if tags:
                st.subheader("Tags:")
                st.write(", ".join(tags[:5]))

            track, track_tags = get_top_track_and_tags(artist)
            if track:
                st.subheader("Top Track:")
                st.write(track)
                if track_tags:
                    st.subheader("Track Tags:")
                    st.write(", ".join(track_tags[:5]))













