#使用这个录音模块：https://pypi.org/project/audio-recorder-streamlit/
import streamlit as st
import openai
import pyttsx3
import numpy as np

# Load environment variables
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to convert text to speech using pyttsx3
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.setProperty("voice", "english-us")
    engine.save_to_file(text, "response.mp3")
    engine.runAndWait()
    with open("response.mp3", "rb") as file:
        response_audio = file.read()
    os.remove("response.mp3")  # Remove the temporary audio file
    return response_audio

# Main function to run the Streamlit app
def main():
    st.title("Audio to Chat App")
    text = "Click the Record Button below and speak to the AI"
        # Audio output section
        st.header("Step 2: Listen to the AI Response")
        st.audio(text_to_speech(response), format="audio/mp3", start_time=0)

if __name__ == "__main__":
    main()
