import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model/distance_model.pkl', 'rb'))

@app.route('/')
def home():
    return "hello"

@app.route('/predict')
def predict():
    result = model.predict([[9,6,1,10,12,3]])
    return str(result)
    
if __name__ == '__main__':
	app.run(port = 5000, debug=True)