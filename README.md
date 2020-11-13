# pi_weather_display
playing with weather APIs, units and rasp pi tft/oled displays

for testing:
curl https://api.weather.gov/stations/KCNK/observations/latest > /home/pi/pi_weather_display/latest.json

python -m http.server 8000

for fastapi:

hypercorn testing_app:app --bind 0.0.0.0:8000

## ToDo:
- convert current conditions to class
- fix "null" API returns
- make buttons in display class interupt based and implement them in program (maybe refresh/on off backlight)


### yes, it is really windy!
![](https://raw.githubusercontent.com/ssk8/pi_weather_display/main/2020-11-08-180548.jpeg)
