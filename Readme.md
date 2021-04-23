# Strava GPX Data Analysis

## Overview

I started cycling with a foldable bike at end of January 2020 and I felt in love with cycling. I also love working with data so I've recorded all my rides to [Strava](www.strava.com) with [Withings Steel HR](https://www.withings.com/us/en/steel-hr) smart watch. 🚴🏻🚴🏻

At the end of may I upgraded my city bike to a Gravel bike. I had great time with my new bike with outdoor activities until autumn.

![outdoor ride activities](images/outdoor_ride.png)

After practicing outside with nice weather, for cold weather I setup a pain-cave at my home for virtual rides on [Zwift](www.zwift.com) using [Elite Arion AL13 roller](https://www.elite-it.com/en/products/home-trainers/rollers/arion) with [Misuro B+ sensor](https://www.elite-it.com/en/products/home-trainers/sensors/misuro-b). Zwift is a virtual environment where you connect with your 3D avatar to ride with other athletes real-time.

![indoor ride activities](images/indoor_ride.png)

Also my Zwift account is also connected with Strava to collect all my ride data. I’ve completed **“3700km”** so far combining outdoor and indoor activities 🎉🎉

I've decided to analyze my data and after analyzing I've decided to take this to next level with my engineering capabilities.

This repo shows how to analyze your Strava data and visualize it on Jupyter Notebook. There's another aim for this project to predict workout days and distance to find your routine using your own data. You can use this digital personal trainer as a workout companion.

## Highlights

Let's have a look at some highlights I achieved so far, here are some highlights about my data.

1. In 1 year I've completed around **3700 km** including outdoor and indoor workout activities. Around 1 of 3rd is virtual ride on Zwift.

    ![distance per ride type](images/distance_per_ride_types.png)

2. In 2019 I gain some fat, so after my activities and healthy food as a result I lost ~13kgs (~28lbs) during this time.

    ![kg per month](images/kg_per_monh.png)

3. I love this weekly graph showcasing all important life events happened in one year. Started with a passion then lockdown due to pandemic in Turkey, then enjoying riding then new year break challenge #Rapha500, then blessed with a new family member, then trying to find my old routine again, last but not least decided to build a personal trainer.

    ![Weekly total ride distance](images/distance_per_week.png)

4. So far my longest distance in one ride is 62km, and I love this graph to show my performance over time.

    ![Distance per ride](images/distance_per_ride.png)

## Solution

Solution contains data analysis, web API and conversational AI(bot) projects.

Folder Structure:

* `bot` - Bot application to retrieve prediction model
* `data` - Data folder contains Strava output*
* `notebooks`
  * `1 - GPX Analysis.ipynb`
  * `2 - Prepare Data.ipynb`
  * `3 - Total Distance Analysis.ipynb`
  * `4 - GPX Anlaysis Combined.ipynb`
  * `5 - GPX Analysis Visualization.ipynb`
  * `6 - Interactive Dashboard.ipynb`
  * `7 - Predict Workout Model.ipynb`
  * `8 - Predict Workout.ipynb`
  * `9 - Present.ipynb` - Highlight for data analysis and results
  * `app.py` - Flask web app for prediction model*
  * `myconfig.py` - Environmental variables*
  * `utils.py` -  Common utility functions
* `web` - Flask Web API for prediction model

## Run the Project

In this sample, Python 3.8.7 version is used, to run the project.

1. Create virtual environment

    ```bash
    python -m venv .venv
    ```

1. Install dependencies

    ```bash
    pip install -r notebooks/requirements.txt
    ```

1. Export your Strava Data from your profile

    * Visit [Settings > My Account > Download or Delete Your Account](https://www.strava.com/account)
    * Click `Download Request (optional)`
    * Download zip file to export into `Data` folder.

1. Create a `Data` folder and export your Strava Data into this folder.

1. Run `Jupyter Notebook` in your local

    ```bash
    jupyter notebook
    ```

## Flask Web Application for API

Run Flask API for running on your local machine

```bash
cd web
```

```bash
flask run
```

### Test endpoints

* Predict temperature

    [http://127.0.0.1:5000/predictTemp?city=Istanbul&date=2021-04-10&time=14](http://127.0.0.1:5000/predictTemp?city=Istanbul&date=2021-04-10&time=14)

* Predict Ride Type & Distance

    [http://127.0.0.1:5000/predict?city=Istanbul&date=2021-04-10&time=14:00:00](http://127.0.0.1:5000/predict?city=Istanbul&date=2021-04-10&time=14:00:00)

## Publish Web App

Publish python flask web app to Azure Web App service

```bash
cd web

az webapp up --sku B1 --name data-driven-cycling

```

to re-deploy and update existing application:

```bash
az webapp up
```

## Test Bot Application on Local

Prerequisite:

* [.NET Core SDK](https://dotnet.microsoft.com/download) version 3.1

```bash
cd bot
dotnet run
```

Or from Visual Studio

* Launch Visual Studio
* File -> Open -> Project/Solution
* Navigate to `bot` folder
* Select `CyclingPrediction.csproj` file
* Press `F5` to run the project

Your bot service will be available at [https://localhost:3979](https://localhost:3979)

Run your Bot Framework Emulator and connect to [https://localhost:3979](https://localhost:3979) endpoint

![Bot on Emulator for test](images/data_driven_cycling_bot_emulator.png)

After that your bot is ready for interaction.

## Bot on Microsoft Teams

After you publish the bot you can connect with different conversational UI.
I've connected with Microsoft Teams and named as `Data Driven Cycling Bot`.

Once you send first message, it's sending a card to pick `City`, `Date` and `Time` information to predict workout ride type and minimum distance.

![Bot on Microsoft Teams](images/data_driven_cycling_bot.png)
