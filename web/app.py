import os
from utils import *
from dotenv import load_dotenv

# Fast API libraries
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get('/')
def home():
    return "Cycling Prediction API"


# http://127.0.0.1:8000/predict?city=Istanbul&date=2021-04-19&time=14:00
@app.get("/predict")
def predict(city: str, date: str, time: str):
    """
    This function uses city name, date of the ride and time as parameters
    returns prediction of ride type, ride distance and weather conditions
    these values will be presented to user
    """
    try:
        # load and get api key from environment variables
        load_dotenv()
        api_key = os.getenv("WEATHER_API_KEY")

        # get parameters
        (workout_temp,
         workout_wind,
         workout_weatherdesc,
         workout_weathericon,
         result_ridetype,
         result_distance) = predict_workout(api_key, city, date, time)

        # parse results
        ridetype = "Outdoor Ride" if result_ridetype[0] == 0 else "Indoor Ride"
        distance = int(result_distance[0])

        # return results
        return {"temp": workout_temp,
                "wind": workout_wind,
                "weather": workout_weatherdesc,
                "weathericon": workout_weathericon,
                "ride": ridetype,
                "distance": distance}
    except Exception as ex:
        return str(ex)


if __name__ == '__main__':
    print("main started")
    uvicorn.run("app:app", port=8000)
