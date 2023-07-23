#使用这个录音模块：https://pypi.org/project/audio-recorder-streamlit/
import streamlit as st
import subprocess
import openai
import pyttsx3
import sounddevice as sd
import soundfile as sf
import numpy as np
from audio_recorder_streamlit import audio_recorder
import numpy as np
#运行的时候有报错sh:1: ffmpeg not found
import ffmpeg
import av
from pydub import AudioSegment
# Load environment variables
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Global variable to hold the chat history, initialize with system role
conversation = [{"role": "system", "content": "You are an intelligent professor."}]

st.title("Audio to Chat App")

    # Audio input section
st.header("Step 1: Speak to the AI")
st.write("Click the Record Button below and speak to the AI.")
audio_bytes = audio_recorder(
    text="Yellow Recording///Green Finished",
    recording_color="#e8b62c",
    neutral_color="#6aa36f",
    icon_name="user",
    icon_size="6x",
    sample_rate=41_000,
)

# Save the audio data to a WAV file
#****************更换下面的语音转文字代码，主要是转化录音的格式
    # Convert the audio data to a numpy array with one channel (mono)
audio_data = np.frombuffer(audio_bytes, dtype=np.int16)
audio_file = "justnameit.wav"
sf.write(audio_file, audio_data, 44100, format="wav")

    # Transcribe the audio using OpenAI API
with open(audio_file, "rb") as file:
    transcript = openai.Audio.transcribe("whisper-1", file)
#    return transcript["text"]    
    text = transcript["text"]    
            # Remove the temporary audio file
#    os.remove(audio_file)    
#****************

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

    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")

        # Transcribe audio and perform chat
        #with st.spinner("Processing..."):
        #    text = transcribe_audio(audio_bytes)
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
