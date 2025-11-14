import streamlit as st
import requests
import urllib.parse

APIK = "7e96bc4d2ecb5f97e26807ee6f2f9048"

def get_artist_topalbums(artist, apik, maxa=5):
    safe_artist = urllib.parse.quote(artist)
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist={safe_artist}&api_key={apik}&format=json"
    r = requests.get(url).json()
    try:
        return r["topalbums"]["album"][:maxa]
    except:
        return None

def get_artist_tags(artist, apik):
    safe_artist = urllib.parse.quote(artist)
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={safe_artist}&api_key={apik}&format=json"
    r = requests.get(url).json()
    tags = r.get("artist", {}).get("tags", {}).get("tag", [])
    return [tag["name"] for tag in tags]

def get_top_track(artist, apik):
    safe_artist = urllib.parse.quote(artist)
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={safe_artist}&api_key={apik}&format=json&limit=1"
    r = requests.get(url).json()
    try:
        track = r["toptracks"]["track"][0]
        track_name = track["name"]
    except:
        return None, None

    # Get tags for that track
    tag_url = f"http://ws.audioscrobbler.com/2.0/?method=track.gettoptags&artist={safe_artist}&track={urllib.parse.quote(track_name)}&api_key={apik}&format=json"
    tag_data = requests.get(tag_url).json()
    tags = tag_data.get("toptags", {}).get("tag", [])
    tag_names = [tag["name"] for tag in tags]
    return track_name, tag_names

# Streamlit UI
st.title("🎵 Artist Comparison (Last.fm)")
st.write("Compare two artists by top albums, tags, and most played track.")

artist1 = st.text_input("Enter Artist 1", "Ariana Grande")
artist2 = st.text_input("Enter Artist 2", "Taylor Swift")

if artist1 and artist2:
    col1, col2 = st.columns(2)

    for i, artist in enumerate([artist1, artist2]):
        with (col1 if i == 0 else col2):
            st.subheader(f"🎤 {artist.title()}")

            # Top albums
            albums = get_artist_topalbums(artist, APIK)
            if albums:
                st.markdown("**Top Albums:**")
                for a in albums:
                    st.write(f"- {a['name']}")
            else:
                st.warning("Could not get albums.")

            # Tags
            tags = get_artist_tags(artist, APIK)
            if tags:
                st.markdown("**Tags:**")
                st.write(", ".join(tags[:5]))

            # Top track
            top_track, track_tags = get_top_track(artist, APIK)
            if top_track:
                st.markdown("**Most Played Track:**")
                st.write(top_track)
                if track_tags:
                    st.markdown("**Track Tags:**")
                    st.write(", ".join(track_tags[:5]))
            else:
                st.warning("No top track found.")












