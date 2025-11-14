import streamlit as st
import requests
import urllib.parse

APIK = "7e96bc4d2ecb5f97e26807ee6f2f9048"

def get_top_albums(artist, limit=5):
    name = urllib.parse.quote(artist.strip())
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist={name}&api_key={APIK}&format=json"
    r = requests.get(url).json()
    
    if "topalbums" not in r:
        st.error(f"API error: {r.get('message', 'No topalbums key found')}")
        return []
    
    albums = r["topalbums"].get("album", [])
    return albums[:limit] if isinstance(albums, list) else []

def get_artist_tags(artist):
    name = urllib.parse.quote(artist.strip())
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={name}&api_key={APIK}&format=json"
    r = requests.get(url).json()
    tags = r.get("artist", {}).get("tags", {}).get("tag", [])
    return [t["name"] for t in tags]

def get_top_track_and_tags(artist):
    name = urllib.parse.quote(artist.strip())
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={name}&api_key={APIK}&format=json&limit=1"
    r = requests.get(url).json()
    
    try:
        top_track = r["toptracks"]["track"][0]["name"]
    except:
        return None, []

    track_name = urllib.parse.quote(top_track)
    tag_url = f"http://ws.audioscrobbler.com/2.0/?method=track.getTopTags&artist={name}&track={track_name}&api_key={APIK}&format=json"
    r2 = requests.get(tag_url).json()
    tags = r2.get("toptags", {}).get("tag", [])
    return top_track, [t["name"] for t in tags]

# Streamlit UI
st.title("🎵 Artist Comparison (Last.fm)")
st.write("Compare two artists by top albums, tags, and most played track.")

artist1 = st.text_input("Enter Artist 1", "Taylor Swift")
artist2 = st.text_input("Enter Artist 2", "Kanye West")

if artist1 and artist2:
    col1, col2 = st.columns(2)

    for col, artist in zip((col1, col2), (artist1, artist2)):
        with col:
            st.header(artist.strip().title())

            albums = get_top_albums(artist)
            if albums:
                st.subheader("Top Albums:")
                for album in albums:
                    st.write(f"- {album['name']}")
            else:
                st.error("❌ Could not retrieve album data. Please check spelling or try a different name.")

            tags = get_artist_tags(artist)
            if tags:
                st.subheader("Artist Tags:")
                st.write(", ".join(tags[:5]))

            track, track_tags = get_top_track_and_tags(artist)
            if track:
                st.subheader("Most Played Track:")
                st.write(track)
                if track_tags:
                    st.subheader("Track Tags:")
                    st.write(", ".join(track_tags[:5]))
