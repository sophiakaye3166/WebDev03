import streamlit as st
import requests
import google.generativeai as genai
import re

LASTFM_API_KEY = "7e96bc4d2ecb5f97e26807ee6f2f9048"
GEMINI_API_KEY = "AIzaSyCOjZ3VAstCobzbh4UI8wmxrkasPPddQbw"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/chat-bison-001")

st.title("Artist Vibe Generator")

artist = st.text_input("Enter an artist name:")
mood = st.selectbox("Choose a mood:", ["Chill", "Hype", "Melancholic", "Romantic", "Energetic"])

if artist and mood:
    api_url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist}&api_key={LASTFM_API_KEY}&format=json"
    response = requests.get(api_url)

    if response.status_code == 200:
        try:
            artist_data = response.json()["artist"]
            raw_bio = artist_data["bio"]["summary"]
            clean_bio = re.sub(r"<.*?>", "", raw_bio)
            short_bio = clean_bio[:500]

            tags = [tag["name"] for tag in artist_data["tags"]["tag"]]
            genres = ", ".join(tags)
            listeners = artist_data["stats"]["listeners"]

            prompt = (
                f"Write a short, creative description of the artist '{artist}'. "
                f"Include the mood '{mood}', genres: {genres}, and listener count: {listeners}. "
                f"Base it on this bio: {short_bio}. Limit to 150 words. Make it casual."
            )

            with st.spinner("Generating description..."):
                result = model.generate_content(prompt)
                st.subheader("Gemini's Output")
                st.write(result.text)

        except Exception as e:
            st.error("Error processing the artist data or generating the response.")
            st.exception(e)
    else:
        st.error("Failed to fetch data from Last.fm.")
