import streamlit as st
import wave
import pyaudio
import soundfile as sf
import openai
import pyttsx3
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

#   Global variable to hold the chat history, initialise with system role
conversation = [
        {"role": "system", "content": "You are an intelligent professor."}
        ]

#   transcribe function to record the audio input

def transcribe(audio):
    print(audio)

    #   Whisper API

    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    print(transcript)

    #   ChatGPT API

    #   append user's input to conversation
    conversation.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    print(response)

    #   system_message is the response from ChatGPT API
    system_message = response["choices"][0]["message"]["content"]

    #   append ChatGPT response (assistant role) back to conversation
    conversation.append({"role": "assistant", "content": system_message})

    #   Text to speech
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.setProperty("voice", "english-us")
    engine.save_to_file(system_message, "response.mp3")
    engine.runAndWait()

    return "response.mp3"

#   Streamlit output

def main():
    st.title("Audio Transcription and Chat App")

    # Record audio using PyAudio
    st.write("Click the button below to start recording...")
    if st.button("Start Recording"):
        st.session_state.audio_file_path = record_audio()

    # Display audio file path (optional, just for demo)
    if 'audio_file_path' in st.session_state:
        st.write(f"Recorded audio file saved to: {st.session_state.audio_file_path}")

    # Transcribe audio and ChatGPT response
    if 'audio_file_path' in st.session_state:
        st.write("Transcribing and generating ChatGPT response...")
        audio_response = transcribe(st.session_state.audio_file_path)
        st.audio(audio_response, format='audio/mp3')

def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5  # Adjust the recording duration as needed
    WAVE_OUTPUT_FILENAME = "recorded_audio.wav"

#    audio = pyaudio.PyAudio()
    audio = pyaudio.PyAudio(source="microphone")
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    frames = []

    audio_file_path = WAVE_OUTPUT_FILENAME

    st.write("Recording...")
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    st.write("Recording Finished!")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return audio_file_path

if __name__ == "__main__":
    main()
