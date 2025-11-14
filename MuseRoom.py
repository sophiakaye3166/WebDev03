import streamlit as st
import requests
import matplotlib.pyplot as plt

API_KEY = "your_lastfm_api_key"

st.title("Artist Comparison (Last.fm)")
st.write("Compare two artists by top albums, tags, and most played track.")

artist1 = st.text_input("Enter Artist 1")
artist2 = st.text_input("Enter Artist 2")

def get_album_data(artist, api_key, maxa=10):
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist={artist}&api_key={api_key}&format=json"
    response = requests.get(url).json()
    if "topalbums" not in response or "album" not in response["topalbums"]:
        return None
    albums = response["topalbums"]["album"][:maxa]
    album_info = []
    for album in albums:
        name = album["name"]
        playcount = int(album.get("playcount", 0))
        album_info.append({"name": name, "playcount": playcount})
    return album_info

def get_artist_tags(artist, api_key):
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist}&api_key={api_key}&format=json"
    response = requests.get(url).json()
    tags = []
    try:
        tag_list = response["artist"]["tags"]["tag"]
        tags = [tag["name"] for tag in tag_list[:5]]
    except:
        pass
    return tags

def get_top_track(artist, api_key):
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={artist}&api_key={api_key}&format=json&limit=1"
    response = requests.get(url).json()
    try:
        track = response["toptracks"]["track"][0]
        name = track["name"]
        playcount = track["playcount"]
        return {"name": name, "playcount": playcount}
    except:
        return None

def get_track_tags(artist, track, api_key):
    url = f"http://ws.audioscrobbler.com/2.0/?method=track.getTopTags&artist={artist}&track={track}&api_key={api_key}&format=json"
    response = requests.get(url).json()
    tags = []
    try:
        tag_list = response["toptags"]["tag"]
        tags = [tag["name"] for tag in tag_list[:5]]
    except:
        pass
    return tags

if artist1 and artist2:
    data1 = get_album_data(artist1, API_KEY)
    data2 = get_album_data(artist2, API_KEY)
    tags1 = get_artist_tags(artist1, API_KEY)
    tags2 = get_artist_tags(artist2, API_KEY)
    track1 = get_top_track(artist1, API_KEY)
    track2 = get_top_track(artist2, API_KEY)
    tags1_track = get_track_tags(artist1, track1["name"], API_KEY) if track1 else []
    tags2_track = get_track_tags(artist2, track2["name"], API_KEY) if track2 else []

    if not data1 or not data2:
        st.error("Could not retrieve album data. Please check spelling.")
    else:
        st.subheader("Number of Top Albums")
        st.write(f"**{artist1}** has {len(data1)} top albums.")
        st.write(f"**{artist2}** has {len(data2)} top albums.")

        st.subheader("Top Album Playcounts")
        fig, ax = plt.subplots(figsize=(10, 5))
        names1 = [a["name"] for a in data1]
        plays1 = [a["playcount"] for a in data1]
        names2 = [a["name"] for a in data2]
        plays2 = [a["playcount"] for a in data2]
        ax.barh(names1, plays1, color="#1db954", label=artist1)
        ax.barh(names2, [-p for p in plays2], color="#ff4b4b", label=artist2)
        ax.set_xlabel("Playcount")
        ax.set_title("Top Albums by Playcount")
        ax.legend()
        st.pyplot(fig)

        top_album1 = max(data1, key=lambda x: x["playcount"])
        top_album2 = max(data2, key=lambda x: x["playcount"])
        st.subheader("Most Popular Albums")
        st.write(f"**{artist1}**: {top_album1['name']} with {top_album1['playcount']} plays")
        st.write(f"**{artist2}**: {top_album2['name']} with {top_album2['playcount']} plays")

        st.subheader("📝 Album Names")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{artist1}'s Albums:**")
            for album in data1:
                st.write(f"- {album['name']}")
        with col2:
            st.markdown(f"**{artist2}'s Albums:**")
            for album in data2:
                st.write(f"- {album['name']}")

        st.subheader("Artist Tags")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{artist1}'s Tags:**")
            for tag in tags1:
                st.write(f"- {tag}")
        with col2:
            st.markdown(f"**{artist2}'s Tags:**")
            for tag in tags2:
                st.write(f"- {tag}")

        st.subheader("Most Played Track")
        st.write(f"**{artist1}**: {track1['name']} with {track1['playcount']} plays") if track1 else st.write("No top track found for artist 1.")
        st.write(f"**{artist2}**: {track2['name']} with {track2['playcount']} plays") if track2 else st.write("No top track found for artist 2.")

        st.subheader("Tags for Most Played Track")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{track1['name']} Tags:**")
            for tag in tags1_track:
                st.write(f"- {tag}")
        with col2:
            st.markdown(f"**{track2['name']} Tags:**")
            for tag in tags2_track:
                st.write(f"- {tag}")
