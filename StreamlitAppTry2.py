import streamlit as st
import openai
import pyttsx3
import sounddevice as sd
import soundfile as sf
import numpy as np

# Load environment variables
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Global variable to hold the chat history, initialize with system role
conversation = [{"role": "system", "content": "You are an intelligent professor."}]

# Function to transcribe audio using OpenAI's Whisper API
def transcribe_audio(audio_data):
    audio_file = "audio_input.wav"
    sf.write(audio_file, audio_data, 44100, format="wav")
    with open(audio_file, "rb") as file:
        transcript = openai.Audio.transcribe("whisper-1", file)
    os.remove(audio_file)  # Remove the temporary audio file
    return transcript["text"]

# Function to perform chat with OpenAI GPT-3
def chat_with_openai(input_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": input_text}],
    )
    return response["choices"][0]["message"]["content"]

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

    # Audio input section
    st.header("Step 1: Speak to the AI")
    st.write("Click the 'Start Recording' button and speak to the AI.")
    
    if st.button("Start Recording"):
        samplerate = 44100
        duration = 5  # seconds
        st.text("Recording... Please speak.")
        audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype=np.int16)
        sd.wait()
        st.text("Recording finished.")
        
        # Transcribe audio and perform chat
        with st.spinner("Processing..."):
            text = transcribe_audio(audio_data)
            response = chat_with_openai(text)

        # Display the chat history and play response audio
        st.header("Chat History")
        st.write("You: " + text)
        st.write("AI: " + response)

        # Audio output section
        st.header("Step 2: Listen to the AI Response")
        st.audio(text_to_speech(response), format="audio/mp3", start_time=0)

if __name__ == "__main__":
    main()
