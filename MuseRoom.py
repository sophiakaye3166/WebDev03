import streamlit as st
import requests

def get_artist_info(artist):
    url = f"https://theaudiodb.com/api/v1/json/2/search.php?s={artist}"
    r = requests.get(url).json()
    return r.get("artists", [None])[0]

st.title("🎶 Artist Comparison (TheAudioDB)")
st.write("Compare two artists using info from TheAudioDB API.")

artist1 = st.text_input("Enter Artist 1", "Adele")
artist2 = st.text_input("Enter Artist 2", "Coldplay")

if artist1 and artist2:
    col1, col2 = st.columns(2)

    for col, artist in zip((col1, col2), (artist1, artist2)):
        with col:
            st.header(artist.title())

            data = get_artist_info(artist)
            if data:
                st.subheader("Genre:")
                st.write(data.get("strGenre", "N/A"))

                st.subheader("Style:")
                st.write(data.get("strStyle", "N/A"))

                st.subheader("Year Formed:")
                st.write(data.get("intFormedYear", "N/A"))

                st.subheader("Album Count (approx.):")
                st.write(data.get("intDiedYear", "N/A") or "Unknown")

                st.subheader("Biography:")
                st.write(data.get("strBiographyEN", "No bio available."))
            else:
                st.error("Artist not found.")












