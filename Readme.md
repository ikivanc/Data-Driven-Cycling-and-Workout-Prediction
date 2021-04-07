# Strava GPX Data Analysis

I love cycling, I have just started one year ago and recorded all my rides via [Strava](www.strava.com). After practicing outside with nice weather, for cold weather I setup a pain-cave at my home for virtual rides on [Zwift](www.zwift.com).

This repo shows how to analyze your Strava data and visualize it on Jupyter Notebook. There's another aim for this project to predict workout days and distance as a workout companion.

Folder Structure:

* `data` - Data folder contains Strava output*
* `1 - GPX Analysis.ipynb`*
* `2 - Prepare Data.ipynb`*
* `3 - Total Distance Analysis.ipynb`*
* `4 - GPX Anlaysis Combined.ipynb`*
* `5 - GPX Analysis Visualization.ipynb`*
* `6 - Interactive Dashboard.ipynb`*
* `7 - Predict Workout Model.ipynb`*
* `8 - Predict Workout.ipynb`*
* `app.py` - Flask web app for prediction model*
* `myconfig.py` - Environmental variables*
* `utils.py` -  Common utility functions

## Run the Project

In this sample, Python 3.8.7 version is used, to run the project.

1. Create virtual environment

    ```bash
    python -m venv .venv
    ```

1. Install dependencies

    ```bash
    pip install -r requirements.txt
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
