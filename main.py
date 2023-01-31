import requests
from cons import *
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply('Hello!\nI am a 🌤⛈ Weather Forecast Bot 🌪🌩\n\n Please enter your city:')


@dp.message_handler()
async def get_weather(message: types.Message):
    weather_smile = {
        "Clear": "sunny \U00002600",
        "Clouds": "cloudy \U00002601",
        "Rain": "raining \U00002614",
        "Drizzle": "drizzling \U00002614",
        "Thunderstorm": "thunderstorm \U000026A1",
        "Snow": "snowing \U0001F328",
        "Mist": "misty \U0001F32B",
    }

    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={WEATHER_TOKEN}&units=metric"
        )
        data = response.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in weather_smile:
            wd = weather_smile[weather_description]
        else:
            wd = "Something strange!"

        feels_like = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        await message.reply(f"FORCAST {city}\nIt is {wd} now\nTemp: {cur_weather}°C\n"
                            f"Feels like: {feels_like}°C\n"
                            f"Temp min: {temp_min}°C\nTemp max: {temp_max}°C\n"
                            f"Humidity: {humidity}%\nPressure: {pressure} hPa\nWind speed: {wind} m/s\n"
                            )

    except:
        await message.reply("I can not find this city! Try one more time")


if __name__ == '__main__':
    executor.start_polling(dp)
