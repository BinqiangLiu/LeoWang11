#pip install openai
#pip install gradio
#pip install pyttsx3
#pip install pydantic
#pip install openai gradio pyttsx3 pydantic
#pip install python-dotenv

import gradio as gr
import openai
import pyttsx3
#import pydantic

from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

#openai.api_key = ""

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

#   append user's inut to conversation
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

#   Gradio output

bot = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="audio")
bot.launch(share=True)

iface.share()