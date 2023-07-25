from flask import Flask, jsonify
import os.path
import gspread
import json
from google.oauth2.service_account import Credentials
import pandas as pd
from neuralprophet import NeuralProphet
import pickle


@app.route('/forecast', methods=['GET'])
def get_forecast():
    .

    # Add this at the end of your function
    return jsonify({
        'pressure_trend': pressure_trend,
        'pressure_forecast': pressure_forecast,
        'zambretti_forecast': zambretti_forecast
    })

