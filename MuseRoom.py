import streamlit as st
import requests
import urllib.parse

APIK = "your_real_lastfm_api_key_here"

def get_artist_topalbums(artist, apik, maxa=5):
    safe_artist = urllib.parse.quote(artist)
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist={safe_artist}&api_key={apik}&format=json"
    r = requests.get(url).json()
    print("Album response:", r)
    if "topalbums" not in r or "album" not in r["topalbums"]:
        return None
    return r["topalbums"]["album"][:maxa]

def get_artist_tags(artist, apik):
    safe_artist = urllib.parse.quote(artist)
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={safe_artist}&api_key={apik}&format=json"
    r = requests.get(url).json()
    print("Tags response:", r)
    tags = r.get("artist", {}).get("tags", {}).get("tag", [])
    return [tag["name"] for tag in tags]

def get_top_track(artist, apik):
    safe_artist = urllib.parse.quote(artist)
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={safe_artist}&api_key={apik}&format=json&limit=1"
    r = requests.get(url).json()
    print("Top track response:", r)
    if "toptracks" not in r or "track" not in r["toptracks"]:
        return None, None
    track = r["toptracks"]["track"][0]
    track_name = track["name"]
    track_tags_url = f"http://ws.audioscrobbler.com/2.0/?method=track.gettoptags&artist={safe_artist}&track={urllib.parse.quote(track_name)}&api_key={apik}&format=json"
    tags_r = requests.get(track_tags_url).json()
    print("Track tags response:", tags_r)
    tags = tags_r.get("toptags", {}).get("tag", [])
    tag_names = [tag["name"] for tag in tags]
    return track_name, tag_names

st.title("Artist Comparison (Last.fm)")
st.write("Compare two artists by top albums, tags, and most played track.")

artist1 = st.text_input("Enter Artist 1", "taylor swift")
artist2 = st.text_input("Enter Artist 2", "ariana grande")

if artist1 and artist2:
    col1, col2 = st.columns(2)

    for i, artist in enumerate([artist1, artist2]):
        with col1 if i == 0 else col2:
            st.subheader(f"{artist.title()}")
            albums = get_artist_topalbums(artist, APIK)
            if not albums:
                st.error("Could not retrieve album data. Please check spelling or try another artist.")
                continue

            st.markdown("**Top Albums:**")
            for a in albums:
                st.write(f"- {a['name']}")

            tags = get_artist_tags(artist, APIK)
            if tags:
                st.markdown("**Tags:**")
                st.write(", ".join(tags[:5]))

            top_track, track_tags = get_top_track(artist, APIK)
            if top_track:
                st.markdown("**Most Played Track:**")
                st.write(top_track)
                if track_tags:
                    st.markdown("**Track Tags:**")
                    st.write(", ".join(track_tags[:5]))









