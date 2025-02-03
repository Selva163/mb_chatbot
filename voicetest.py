import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.playback import play

st.title("🎤 Voice-Enabled Chatbot")

recognizer = sr.Recognizer()

def get_voice_input():
    with sr.Microphone() as source:
        st.write("Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError:
            return "Speech service is unavailable."

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    os.system("start response.mp3")  # Windows
    # os.system("afplay response.mp3")  # Mac
    # os.system("mpg321 response.mp3")  # Linux
    return "response.mp3"

if st.button("🎙️ Speak"):
    user_input = get_voice_input()
    st.write("**You said:**", user_input)
    
    # Simulating chatbot response
    chatbot_response = f"Hello! You said: {user_input}"
    st.write("🤖 **Chatbot:**", chatbot_response)
    
    audio_file = speak(chatbot_response)
    st.audio(audio_file, format="audio/mp3")
