import json
from tkinter import *
import requests
import os
import datetime as dt
from io import BytesIO
from PIL import ImageTk, Image
import sys
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"
APP_ID = "2101e506575da15cfd92304fbf56a41e"


def write_into_file(data):
    with open("data.json", "w") as file:
        json.dump(data, file)


def getWeather():
    city = textField.get()
    parameters = {
        "q": city,
        "appid": APP_ID
    }
    response = requests.get(OWM_ENDPOINT, params=parameters)
    weather_data = response.json()
    write_into_file(weather_data)
    try:

        # incons Api
        icons_url = f"http://openweathermap.org/img/wn/{weather_data['weather'][0]['icon']}@2x.png"
        icon_response = requests.get(icons_url)
        icon_data = icon_response.content
        icon_image = ImageTk.PhotoImage(Image.open(BytesIO(icon_data)))

        flag_url = f"https://www.countryflags.io/{weather_data['sys']['country']}/shiny/64.png"
        flag_response = requests.get(flag_url)
        flag_data = flag_response.content
        flag_image = ImageTk.PhotoImage(Image.open(BytesIO(flag_data)))

        condition = weather_data['weather'][0]['main']

        # Changing background Image, Image lai read gareko
        bg_image_data = Image.open('./Picture/' + condition + '.jpg')
        resized_image_data = bg_image_data.resize((800, 800), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(resized_image_data)

        temp = int(weather_data['main']['temp'] - 273)
        temp_min = int(weather_data['main']['temp_min'] - 273)
        temp_max = int(weather_data['main']['temp_max'] - 273)
        pressure = weather_data['main']['pressure']
        humidity = weather_data['main']['humidity']
        wind = weather_data['wind']['speed']
        sunset_unix = weather_data['sys']['sunset']
        sunset_readable = dt.datetime.fromtimestamp(sunset_unix)
        sunrise_unix = weather_data['sys']["sunrise"]
        sunrise_readable = dt.datetime.fromtimestamp(sunrise_unix)
        final_data = f"{condition} \n {temp} c"
        final_info = f"Min Temp: {temp_min} \n Max Temp: {temp_max} \n pressure: {pressure} \n Humidity: {humidity} \n wind:{wind} \n sunrise:{sunrise_readable} \n sunset: {sunset_readable}"
        label1.config(text=final_data)
        label2.config(text=final_info)
        # image lai haleko
        label3.configure(image=bg_image)
        label3.image = (bg_image)

        icons_label.configure(image=icon_image)
        icons_label.image = (icon_image)

        # flag lai haleko
        flag_label.configure(image=flag_image)
        flag_label.image = (flag_image)
    except KeyError:
        label1.config(text=weather_data['message'])
        label2.config(text=weather_data['cod'])

    except FileNotFoundError:
        label1.config(text=f"File Error!!! \n {(sys.stdout)}")


window = Tk()
window.title("Weather App")
window.geometry("800x800")

bg_image_data = Image.open('./Picture/bg.jpg')
resized_image_data = bg_image_data.resize((800, 800), Image.ANTIALIAS)
bg_image = ImageTk.PhotoImage(resized_image_data)
label3 = Label(window, image=bg_image)
label3.place(x=0, y=0)

textField = Entry(window, bg="#fafafa", justify='center', font=("popins", 35, "italic"), width=20)
textField.pack(pady=20)

button = Button(text="Get Weather", highlightthickness=0, command=getWeather)
button.pack(pady=20)

icons_label = Label(window, bg='#afafaf')
icons_label.pack()

label1 = Label(window, bg="#afafaf", font=("popins", 20, "italic"))
label1.pack()

flag_label = Label(window, bg="#afafaf")
flag_label.pack()

label2 = Label(window, bg="#afafaf", font=("popins", 20, "italic"))
label2.pack()
window.mainloop()
