import streamlit as st
import requests
import urllib.parse

APIK = "7e96bc4d2ecb5f97e26807ee6f2f9048"  # Your real Last.fm API key

def get_top_albums(artist, limit=5):
    name = urllib.parse.quote(artist)
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist={name}&api_key={APIK}&format=json"
    res = requests.get(url).json()
    return res.get("topalbums", {}).get("album", [])[:limit]

def get_artist_tags(artist):
    name = urllib.parse.quote(artist)
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={name}&api_key={APIK}&format=json"
    res = requests.get(url).json()
    return [tag["name"] for tag in res.get("artist", {}).get("tags", {}).get("tag", [])]

def get_top_track_and_tags(artist):
    name = urllib.parse.quote(artist)
    track_url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={name}&api_key={APIK}&format=json&limit=1"
    res = requests.get(track_url).json()
    try:
        track_name = res["toptracks"]["track"][0]["name"]
    except:
        return None, []

    tag_url = f"http://ws.audioscrobbler.com/2.0/?method=track.getTopTags&artist={name}&track={urllib.parse.quote(track_name)}&api_key={APIK}&format=json"
    tag_res = requests.get(tag_url).json()
    tags = [tag["name"] for tag in tag_res.get("toptags", {}).get("tag", [])]
    return track_name, tags

# Streamlit Interface
st.title("🎶 Artist Comparison (using Last.fm API)")
st.write("Compare two artists based on albums, tags, and top tracks.")

artist1 = st.text_input("Enter Artist 1", "Ariana Grande")
artist2 = st.text_input("Enter Artist 2", "Taylor Swift")

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
                st.warning("No album data found.")

            tags = get_artist_tags(artist)
            if tags:
                st.subheader("Artist Tags:")
                st.write(", ".join(tags[:5]))
            else:
                st.warning("No tags found.")

            track, track_tags = get_top_track_and_tags(artist)
            if track:
                st.subheader("Most Played Track:")
                st.write(track)
                if track_tags:
                    st.subheader("Track Tags:")
                    st.write(", ".join(track_tags[:5]))
                else:
                    st.warning("No track tags found.")
            else:
                st.warning("No top track found.")













