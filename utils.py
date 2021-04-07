import pandas as pd
from pathlib import Path
from os import listdir
from os.path import isfile, join
from benedict import benedict as bdict
from ipyleaflet import Map, Polyline
from datetime import datetime, timedelta, time
import requests, pickle, gzip , shutil
from sklearn import preprocessing
from matplotlib.axes._axes import _log as matplotlib_axes_logger
matplotlib_axes_logger.setLevel('ERROR')

# Mutual functions across notebooks
filepath = "data/"
fileOutputPath= filepath + "output/"
activityPath = filepath + "activities/"
activityOutputPath = fileOutputPath + "activities/"

def loadData():
    df = pd.read_csv(filepath+ 'activities.csv')
    data = df[df.columns[[0,1,2,3,4,5,6,10,13,14,15,16,17,18,19,20,21,22,23,26,27,31,32,41,44,45,47]]]
    data = data.astype({"Distance": float})
    data[['Date','Time']] = ""

    rideTypes = ['Virtual Ride', 'Ride']
    rideData = data[data['Activity Type'].isin(rideTypes)]    
    return rideData.dropna(subset=['Filename']).reset_index()

def loadCleanData():
    df = pd.read_csv(filepath+ 'activities_clean.csv')
    df['Week'] = pd.to_datetime(df.Week)
    df['Activity Date'] = pd.to_datetime(df['Activity Date']) + timedelta(hours=3)
    return df

def loadCorrelatedData():
    df = pd.read_csv(filepath+ 'activities_correlated.csv')
    df['Week'] = pd.to_datetime(df.Week)
    df['Activity Date'] = pd.to_datetime(df['Activity Date'])
    return df

def saveData(updatedData):
    updatedData.to_csv(filepath+ 'activities_clean.csv', index=False)
    print('Successfully saved!')

def getFilename(fileextension):
    return fileextension[:-3]

def extractAllGPXFiles():
    # Create activity files Path if it's not exists
    Path(activityOutputPath).mkdir(parents=True, exist_ok=True)
    
    # check for all files in activities folder
    activityfiles = [f for f in listdir(filepath+"activities") if isfile(join(filepath+"activities", f))]

    # Extract all files from gz zip files
    for activityzip in activityfiles:
        # Extract activity filename
        filename=getFilename(activityzip)
       
        # Extract GPX File
        with gzip.open(activityPath + activityzip, 'rb') as f_in:
            with open(activityOutputPath + filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    
    print("done!")
        
def getLocations(gpx_output_path,gpx_filename):
    # data-source can be an url, a filepath or data-string (as in this example)
    data_source = gpx_output_path + gpx_filename
    xmldata = bdict.from_xml(data_source)
    trk_list = xmldata['gpx.trk.trkseg.trkpt']
    
    locs = [[float(t['@lat']),float(t['@lon'])] for t in trk_list]
    
    return locs

def getVirtualLocations(gpx_output_path,gpx_filename):
    try:
        data_source = gpx_output_path + gpx_filename
        xmldata = bdict.from_xml(data_source)
        trk_list = xmldata['gpx.trk.trkseg.trkpt']

        locs = [[float(t['@lat']),float(t['@lon']),float(t['ele']),t['extensions']['power'],t['time']] for t in trk_list]
    
        return locs
    except:
        return None

def showOnMap(locations):

    line = Polyline(
        locations=locations,
        color="green" ,
        fill=False
    )

    m = Map(center = (float((min(locations)[0]+max(locations)[0])/2), float(min(locations)[1]+max(locations)[1])/2), zoom =12)
    m.add_layer(line)
    return m

# 1 - Prepare Data & 4 - GPX Analysis Combined
def getTimeInMinute(time):
    result = time/60
    return "{:.1f}".format(result)

def getValue(value):
    return "{:.2f}".format(value)

def getSpeedkmH(speed):
    result = speed * (3600/1000)
    return "{:.2f}".format(result)
    
def getDate(strDateTime):
    date_time_str = strDateTime #'2018-06-29 08:15:27.243860'
    date_time_obj = datetime.strptime(date_time_str, '%b %d, %Y, %H:%M:%S %p')
    return date_time_obj.strftime("%m-%d-%Y")

def getTime(strDateTime):
    timezone_diff = 3
    date_time_str = strDateTime #'2018-06-29 08:15:27.243860'
    date_time_obj = datetime.strptime(date_time_str, '%b %d, %Y, %H:%M:%S %p')
    date_time_obj = date_time_obj + timedelta(hours=timezone_diff)
    return date_time_obj.strftime("%H:%M:%S")

# 4 - GPX Analysis Combined
def printActivityData(row):
    try:
        # print common stats
        print(" -- ", row['Activity Name'], " -- ")
        print("Activity Date:", getDate(row['Activity Date']))
        print(f"Distance: { row['Distance']} km")
        print(f"Elapsed Time: { getTimeInMinute(row['Elapsed Time'])} min")
        print(f"Moving Time: { getTimeInMinute(row['Moving Time'])} min")
        print(f"Max Speed: { getSpeedkmH(row['Max Speed'])} km/h")
        print(f"Average Speed: { getSpeedkmH(row['Average Speed'])} km/h")
        print(f"Elevation Gain: { round(row['Elevation Gain'])}")
        print(f"Elevation High: { round(row['Elevation High'])}")
        
        # print Ride Type specific stats
        if(row['Activity Type']=="Virtual Ride"):
            print(f"Weighted Average Power: { round(row['Weighted Average Power'])}")
            print(f"Power Count: { round(row['Power Count'])}")
            print(f"Max Cadence: { round(row['Max Cadence'])}")
            print(f"Average Cadence: { getValue(row['Average Cadence'])}")
            print(f"Average Watts: { round(row['Average Watts'])}")
            print(f"Calories: { round(row['Calories'])}")

    except Exception as ex:
        print("An Error Occured:", ex)
                  
def showPowerHist(virtualLocList): 
    dfSteps = pd.DataFrame(virtualLocList, columns =['Latitude', 'Longtitude','Elevation','Power','Date']) 
    dfSteps = dfSteps.astype({"Power": int})
    
    return dfSteps['Power'].plot(kind = 'hist')

# def showPowerGraph(virtualLocList): 
#     # Power/Time Distrubition Graph
#     dfSteps = pd.DataFrame(virtualLocList, columns =['Latitude', 'Longtitude','Elevation','Power','Date']) 
#     dfSteps = dfSteps.astype({"Power": int})
#     powerPlot = sns.lineplot(data=dfSteps, x="Date", y="Power")
#     powerPlot.set(xticklabels=[]) 
#     powerPlot.set(xlabel=None)
#     powerPlot.tick_params(bottom=False) 
#     return powerPlot

# 7 - Predict Workout Model
def get_weather(api_key,city,date,hour):
    
    # Use different endpoints if it's an old weather data or future forecast
    if type(date) == str:
        date = datetime.fromisoformat(date)
        
    if date>datetime.now():
        endpoint = f"http://api.worldweatheronline.com/premium/v1/weather.ashx?key={api_key}&q={city}&date={date}&format=json"
    else:
        endpoint = f"http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key={api_key}&q={city}&date={date}&format=json"
    
    response = requests.get(endpoint)
    api_results=response.json()

    ## TODO
    ## Exception handling for API daily limit:
    ## {'data': {'error': [{'msg': 'API key has reached calls per day allowed limit.'}]}}

    # Weather data is splitted into 3hour slices, in below code finding hour slot for weather
    hour_slice = int(hour/3) 

    # Selecting weather hour slice 
    temp = api_results['data']['weather'][0]['hourly'][hour_slice]

    # Return weather details
    temp_c = temp['tempC']
    windspeed_miles = temp['windspeedMiles']
    weather_desc = temp['weatherDesc'][0]['value']

    return int(temp_c), int(windspeed_miles), weather_desc

# 8 - Predict Workout
def predict_workout(api_key,city,wdate,wtime):
    wtime = time.fromisoformat(wtime)
    temp_data = get_weather(api_key,city,wdate,wtime.hour)
    workout_temp, workout_wind , workout_weatherdesc = temp_data
    
    # weather description
    le = preprocessing.LabelEncoder()
    le.fit(['Clear' 'Cloudy' 'Heavy rain' 'Light drizzle' 'Light rain'
            'Light rain shower' 'Moderate rain' 'Moderate rain at times' 'Overcast'
            'Partly cloudy' 'Patchy light rain with thunder' 'Patchy light snow'
            'Patchy rain possible' 'Sunny'])

    try:
        workout_weather = int(le.transform([workout_weatherdesc])[0])
    except:
        workout_weather = 0
    
    wdate = datetime.fromisoformat(wdate)
    workout_hour = wtime.hour
    workout_dayofweek = wdate.isoweekday()
    workout_isweekend = int(workout_dayofweek // 6 == 1)
    
    # Load ride type model from file
    ridetype_model_file = "model/ridetype_model.pkl"
    with open(ridetype_model_file, 'rb') as file:
        ridetype_model = pickle.load(file)
      
    result_ridetype = ridetype_model.predict([[workout_hour,workout_dayofweek,workout_isweekend,workout_temp,workout_wind,workout_weather]])
    print("Result type prediction=%s" % result_ridetype)
    
    # Load distance model from file
    distance_model_file = "model/distance_model.pkl"
    with open(distance_model_file, 'rb') as file:
        distance_model = pickle.load(file)
    
    result = distance_model.predict([[workout_hour,workout_dayofweek,workout_isweekend,workout_temp,workout_wind,workout_weather]])
    return result