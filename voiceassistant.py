import tkinter as tk
from tkinter import ttk
import threading
import smtplib
import requests
import openai
import datetime
from gtts import gTTS
import os
from playsound import playsound
import sounddevice as sd
import numpy as np
import wave
import speech_recognition as sr

# Initialize OpenAI API key (replace with your own key)
openai.api_key = "your-openai-api-key"

def speak(text):
    """Convert text to speech using gTTS."""
    tts = gTTS(text=text, lang='en')
    tts.save("speech.mp3")
    playsound("speech.mp3")
    os.remove("speech.mp3")

def listen():
    """Capture audio using sounddevice and recognize speech using speech_recognition."""
    duration = 5  # seconds
    samplerate = 44100  # Hertz
    print("Listening...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    
    # Save the recorded audio to a temporary file
    temp_filename = "temp_audio.wav"
    with wave.open(temp_filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio.tobytes())
    
    # Debugging: Play back the recorded audio to check clarity
    print("Playing back recorded audio...")
    playsound(temp_filename)
    
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(temp_filename) as source:
            recognizer.adjust_for_ambient_noise(source)
            captured_audio = recognizer.record(source)
            query = recognizer.recognize_google(captured_audio, language='en-US')
            print(f"Recognized: {query}")  # Debugging: print what was recognized
            return query.lower()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
        return "Sorry, I didn't catch that."
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return "Sorry, I didn't catch that."
    finally:
        os.remove(temp_filename)  # Clean up the temporary file

def send_email(to, subject, body):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('your-email@gmail.com', 'your-password')
        email_message = f"Subject: {subject}\n\n{body}"
        server.sendmail('your-email@gmail.com', to, email_message)
        server.close()
        return "Email sent successfully."
    except Exception as e:
        print(f"Error: {e}")
        return "Error sending email."

def get_weather(city):
    api_key = "your-openweathermap-api-key"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    weather_data = response.json()

    if weather_data["cod"] == 200:
        temp = weather_data['main']['temp']
        weather_desc = weather_data['weather'][0]['description']
        return f"The temperature in {city} is {temp}°C with {weather_desc}."
    else:
        return "Error fetching weather data."

def answer_general_question(question):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=100
    )
    return response.choices[0].text.strip()

def perform_task(query):
    print(f"Received command: {query}")  # Debugging: print received command
    if 'email' in query:
        response = send_email("recipient@example.com", "Test Subject", "Test Body")
    elif 'weather' in query:
        response = get_weather("New York")
    elif 'question' in query:
        response = answer_general_question("What is the capital of France?")
    elif 'reminder' in query:
        response = "Reminder set successfully."
    else:
        response = "Command not recognized."
    print(f"Response: {response}")  # Debugging: print response
    return response

# UI/UX Design with tkinter
class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")
        self.root.geometry("500x400")
        self.root.configure(bg='#2c3e50')

        # Title
        self.title_label = tk.Label(root, text="Voice Assistant", font=("Helvetica", 24), bg='#2c3e50', fg='white')
        self.title_label.pack(pady=20)

        # Command Display
        self.command_label = tk.Label(root, text="Your Command:", font=("Helvetica", 14), bg='#2c3e50', fg='white')
        self.command_label.pack(pady=10)
        self.command_text = tk.StringVar()
        self.command_display = tk.Entry(root, textvariable=self.command_text, font=("Helvetica", 14), width=30, state='readonly')
        self.command_display.pack(pady=10)

        # Response Display
        self.response_label = tk.Label(root, text="Assistant's Response:", font=("Helvetica", 14), bg='#2c3e50', fg='white')
        self.response_label.pack(pady=10)
        self.response_text = tk.Text(root, font=("Helvetica", 12), height=4, width=40, wrap='word', state='disabled')
        self.response_text.pack(pady=10)

        # Activate Voice Button
        self.voice_button = ttk.Button(root, text="Activate Voice", command=self.activate_voice)
        self.voice_button.pack(pady=20)

    def activate_voice(self):
        self.command_text.set("Listening...")
        threading.Thread(target=self.process_voice_command).start()

    def process_voice_command(self):
        query = listen()
        self.command_text.set(query)
        response = perform_task(query)
        self.update_response_display(response)

    def update_response_display(self, response):
        self.response_text.config(state='normal')
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(tk.END, response)
        self.response_text.config(state='disabled')
        speak(response)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
