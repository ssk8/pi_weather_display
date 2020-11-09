import requests
from pint import UnitRegistry
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import busio
from board import SCL, SDA
from datetime import datetime, timedelta

i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
disp.fill(0)
disp.show()
image = Image.new("1", (disp.width, disp.height))
draw = ImageDraw.Draw(image)

ureg = UnitRegistry()
uQ = ureg.Quantity

req = requests.get("https://api.weather.gov/stations/KCNK/observations/latest")
#req = requests.get("http://192.168.1.148:8000/")

w = req.json()["properties"]

w_speed = w['windSpeed']['value']*ureg.kilometers/ureg.hour
temperature = uQ(w['temperature']['value'], ureg.degC)
timestamp = datetime.fromisoformat(w['timestamp']) 

current = [f"{(timestamp-timedelta(hours=5)).strftime('%a, %b-%d %H:%M')}",
        f"{temperature.to('degF'):.1f}",
        f"{w_speed.to(ureg.miles/ureg.hour):.2f} {w['windDirection']['value']}°"]

def display_lines(lines):
    font = ImageFont.load_default()
    draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)
    for n, line in enumerate(lines):
        draw.text((0, n*10), line, font=font, fill=255)
    disp.image(image)
    disp.show()

display_lines(current)