import requests
import tkinter as tk
from tkinter import messagebox

def get_weather():
    api_key = '30d4741c779ba94c470ca1f63045390a'
    user_input = city_entry.get()
    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}")
    
    if weather_data.json()['cod'] == '404':
        messagebox.showerror("Error", "City Not Found")
    else:
        weather = weather_data.json()['weather'][0]['main']
        temp = round(weather_data.json()['main']['temp'])
        result_label.config(text=f"The weather in {user_input} is: {weather}\nThe temperature in {user_input} is: {temp}ºF")

# Create main window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x300")
root.config(bg="#1e1f29")  # Dark bluish background

# Create widgets
title_label = tk.Label(root, text="Weather App", font=("Helvetica", 16), fg="white", bg="#1e1f29")
title_label.pack(pady=10)

city_label = tk.Label(root, text="Enter City Name:", font=("Helvetica", 12), fg="white", bg="#1e1f29")
city_label.pack(pady=10)

city_entry = tk.Entry(root, font=("Helvetica", 12), width=20)
city_entry.pack(pady=5)

get_weather_button = tk.Button(root, text="Get Weather", font=("Helvetica", 12), command=get_weather)
get_weather_button.pack(pady=20)

result_label = tk.Label(root, font=("Helvetica", 12), fg="white", bg="#1e1f29")
result_label.pack(pady=10)

# Start the main loop
root.mainloop()
