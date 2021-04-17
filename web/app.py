import numpy as np
import pandas as pd
from flask import Flask, request
import pickle
from utils import *
from myconfig import *

app = Flask(__name__)

@app.route('/')
def home():
    return "hello"

# http://127.0.0.1:5000/predict?city=Istanbul&date=2021-04-10&time=14:00:00
@app.route('/predict')
def predict():
    try:
        # get parameters
        city = request.args.get('city')
        workout_date = request.args.get('date')
        workout_time = request.args.get('time')
        workout_temp, workout_wind , workout_weatherdesc, workout_weathericon, result_ridetype, result_distance = predict_workout(api_key,city,workout_date,workout_time)

        # Parse result
        ride_type = "Ride" if result_ridetype[0] == 0 else "Virtual Ride"
        distance = int(result_distance[0])

        return {"temp": workout_temp, "wind": workout_wind , "weather": workout_weatherdesc,"weathericon": workout_weathericon,"ride": ride_type, "distance": distance }
    except Exception as ex:
        return str(ex)

# http://127.0.0.1:5000/predictTemp?city=Istanbul&date=2021-04-10&time=14
@app.route('/predictTemp')
def predict_temp():
    # get parameters
    city = request.args.get('city')
    workout_date = request.args.get('date')
    workout_time = int(request.args.get('time'))
    
    # parse temp
    temp, wind, weather_desc  = get_weather(api_key,city,workout_date,workout_time)

    return (f"Temprature:{temp} C, Wind:{wind}, Description:{weather_desc}")


if __name__ == '__main__':
	app.run(port = 5000, debug=True)