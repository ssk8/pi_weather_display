from fastapi import FastAPI
import json

# curl https://api.weather.gov/stations/KCNK/observations/latest > /home/pi/weath_api/latest.json
json_file = "/home/pi/weath_api/latest.json"

app = FastAPI()

with open(json_file, "r") as latest:
    weather = latest.read()

@app.get('/')
def index():
    return json.loads(weather)
