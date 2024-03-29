import requests
import pickle
from sklearn import preprocessing
from datetime import datetime, time


def get_weather(api_key, city, date, hour):
    """
    Predict weather with city name, date and hour of the day
    Weather api is used to retrieve weather conditions
    temperature, wind, weather description and weather icon
    """

    # Use different endpoints if it's an old weather data or future forecast
    if type(date) == str:
        date = datetime.fromisoformat(date)

    # Detect if it's a weather forecast or or old weather data
    if date > datetime.now():
        endpoint = f"http://api.worldweatheronline.com/premium/v1/weather.ashx?key={api_key}&q={city}&date={date}&format=json"
    else:
        endpoint = f"http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key={api_key}&q={city}&date={date}&format=json"

    response = requests.get(endpoint)
    api_results = response.json()

    # TODO
    # Exception handling for API daily limit:
    # {'data':
    #  {'error': [{'msg': 'API key has reached calls per day allowed limit.'}]}
    # }

    # Weather data is splitted into 3hour slices,
    # in below code finding hour slot for weather
    hour_slice = int(hour/3)

    # Selecting weather hour slice
    temp = api_results['data']['weather'][0]['hourly'][hour_slice]

    # Return weather details
    temp_c = temp['tempC']
    windspeed_miles = temp['windspeedMiles']
    weather_desc = temp['weatherDesc'][0]['value']
    weather_icon = temp['weatherIconUrl'][0]['value']

    return int(temp_c), int(windspeed_miles), weather_desc, weather_icon


def predict_workout(api_key, city, wdate, wtime):
    """
    Predict weather with city name, date and time of the day
    returns weather conditions, distance prediction and ride type prediction
    """
    wtime = time.fromisoformat(wtime)
    temp_data = get_weather(api_key, city, wdate, wtime.hour)
    workout_temp, workout_wind, workout_weatherdesc, workout_weathericon = (
        temp_data)

    # numerate weather description
    le = preprocessing.LabelEncoder()
    le.fit(['Clear' 'Cloudy' 'Heavy rain' 'Light drizzle' 'Light rain'
            'Light rain shower' 'Moderate rain' 'Moderate rain at times'
            'Overcast' 'Partly cloudy' 'Patchy light rain with thunder'
            'Patchy light snow' 'Patchy rain possible' 'Sunny'])

    try:
        workout_weather = int(le.transform([workout_weatherdesc])[0])
    except Exception as ex:
        workout_weather = 0

    # set parameters
    wdate = datetime.fromisoformat(wdate)
    workout_hour = wtime.hour
    workout_dayofweek = wdate.isoweekday()
    workout_isweekend = int(workout_dayofweek // 6 == 1)

    # load ride type model from file
    ridetype_model_file = "./model/ridetype_model.pkl"
    with open(ridetype_model_file, 'rb') as file:
        ridetype_model = pickle.load(file)

    # retrieve ride type result from prediction model
    result_ridetype = ridetype_model.predict(
        [[workout_hour, workout_dayofweek, workout_isweekend,
          workout_temp, workout_wind, workout_weather]])

    # Load distance model from file
    distance_model_file = "./model/distance_model.pkl"
    with open(distance_model_file, 'rb') as file:
        distance_model = pickle.load(file)

    # retrieve distance result from prediction model
    result = distance_model.predict(
        [[workout_hour, workout_dayofweek, workout_isweekend,
          workout_temp, workout_wind, workout_weather]])

    # return results
    return (workout_temp, workout_wind, workout_weatherdesc,
            workout_weathericon, result_ridetype, result)
