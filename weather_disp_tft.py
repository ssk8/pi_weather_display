import requests
from pint import UnitRegistry
from PIL import Image, ImageDraw, ImageFont
import ST7789
from datetime import datetime, timedelta

ureg = UnitRegistry()
uQ = ureg.Quantity

req = requests.get("https://api.weather.gov/stations/KCNK/observations/latest")
#req = requests.get("http://192.168.1.148:8000/")

w = req.json()["properties"]

timestamp = datetime.fromisoformat(w['timestamp']) 
temperature = uQ(w['temperature']['value'], ureg.degC)
dewpoint = uQ(w['dewpoint']['value'], ureg.degC)
windSpeed = w['windSpeed']['value']*ureg.kilometers/ureg.hour
windGust = w['windGust']['value']*ureg.kilometers/ureg.hour
barometricPressure = w['barometricPressure']['value']*ureg.pascal
seaLevelPressure = w['seaLevelPressure']['value']*ureg.pascal
heatIndex = uQ(w['heatIndex']['value'], ureg.degC)


current = [f"{(timestamp-timedelta(hours=5)).strftime('%a, %b-%d %H:%M')}",
        f"station: {w['station'][-4:]}",
        f"temp: {temperature.to('degF').magnitude:.1f}°F",
        f"dewpoint: {dewpoint.to('degF').magnitude:.1f}°F",
        f"wind: {windSpeed.to(ureg.miles/ureg.hour).magnitude:.1f} g {windGust.to(ureg.miles/ureg.hour).magnitude:.1f} miles/hr",
        f"wind direction: {w['windDirection']['value']}°",
        f"press: {barometricPressure.to(ureg.inch_Hg).magnitude:.2f} in Hg",
        f"sealevel press: {seaLevelPressure.to(ureg.inch_Hg).magnitude:.2f} in Hg",
        f"rel. Humidity: {w['relativeHumidity']['value']:.2f}%",
        f"heat index: {heatIndex.to('degF').magnitude:.1f}°F",
        f"{w['textDescription']}",
        f"clouds: {w['cloudLayers'][0]['amount']}", #fix this
        ]


disp = ST7789.ST7789()
disp.Init()
disp.clear()
image = Image.new("RGB", (disp.width, disp.height))
draw = ImageDraw.Draw(image)

def display_lines(lines):
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=(255, 255, 255))
    for n, line in enumerate(lines):
        draw.text((0, n*20), line, font=font, fill="#000000")
    disp.image(image)

display_lines(current)